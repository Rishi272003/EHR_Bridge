from services.ehr.transformer import Transformer
from services.ehr.practice_fusion.categories.Practitioner import Practitioner


class PractitionerQueryTransformer(Transformer):
    """
    Transformer for Practice Fusion Practitioner queries.
    Transforms FHIR Practitioner responses to standardized format.

    Supported search parameters:
    - identifier: Search by identifier (NPI, internal ID, etc.)
    - given: Search by first name
    - name: Search by full name
    - If no parameters: Returns all practitioners in the practice
    """

    def __init__(self, connection_obj, source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Provider",
                "EventType": "ProviderQuery",
                "Source": {"ID": str(self.connection.uuid), "Name": "connectionid"},
                "Raw": [],
            },
            "Providers": [],
            "Paging": None,
        }

    def transform(self):
        """
        Transform practitioner query request and fetch data from Practice Fusion.
        """
        try:
            # Extract filter parameters from source_json
            provider_data = self.source_json.get("Provider", {})
            demographics = self.source_json.get("Demographics", {})

            practitioner_id = None
            identifier = None
            given = None
            name = None

            # Extract practitioner ID if provided
            identifiers = provider_data.get("Identifiers", [])
            if identifiers:
                for ident in identifiers:
                    id_type = ident.get("IDType", "").upper()
                    id_value = ident.get("ID")

                    if id_type == "EHRID" or id_type == "FHIR_ID":
                        practitioner_id = id_value
                    elif id_type == "NPI":
                        # For Practice Fusion, NPI identifier format
                        identifier = id_value
                    else:
                        # Use as generic identifier
                        identifier = id_value

            # Extract name from Demographics if provided
            first_name = demographics.get("FirstName")
            last_name = demographics.get("LastName")
            if first_name:
                given = first_name
            if first_name and last_name:
                name = f"{first_name} {last_name}"
            elif last_name:
                name = last_name

            # Initialize Practitioner category and authenticate
            practitioner_client = Practitioner(self.connection)
            auth_status = practitioner_client.authenticate()

            if auth_status != 200:
                self.destination_response["detail"] = "Authentication failed"
                self.destination_response["statuscode"] = 401
                return self.destination_response

            # Fetch practitioner data from Practice Fusion
            if practitioner_id:
                # Get specific practitioner by ID
                practitioner_response, status_code = practitioner_client.get_practitioner_by_id(practitioner_id)
            else:
                # Search practitioners with filters
                practitioner_response, status_code = practitioner_client.search_practitioners(
                    identifier=identifier,
                    given=given,
                    name=name
                )

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(practitioner_response)

            if status_code == 200:
                self._transform_fhir_response(practitioner_response)
            else:
                self.destination_response["detail"] = "Failed to fetch practitioner data"
                self.destination_response["statuscode"] = status_code
                self.destination_response["error"] = practitioner_response

            return self.destination_response

        except Exception as e:
            self.destination_response["detail"] = f"Error processing practitioner query: {str(e)}"
            self.destination_response["statuscode"] = 500
            return self.destination_response

    def _transform_fhir_response(self, fhir_response):
        """
        Transform FHIR Bundle response to standardized provider format.
        """
        providers = []

        # Handle FHIR Bundle response
        if fhir_response.get("resourceType") == "Bundle":
            entries = fhir_response.get("entry", [])

            if entries:
                for entry in entries:
                    resource = entry.get("resource", {})
                    if resource.get("resourceType") == "Practitioner":
                        provider_obj = self._transform_practitioner_resource(resource)
                        providers.append(provider_obj)

                # Handle pagination
                self._extract_paging(fhir_response)

        # Handle single Practitioner resource (direct ID lookup)
        elif fhir_response.get("resourceType") == "Practitioner":
            provider_obj = self._transform_practitioner_resource(fhir_response)
            providers.append(provider_obj)

        self.destination_response["Providers"] = providers

    def _transform_practitioner_resource(self, resource):
        """
        Transform a single FHIR Practitioner resource to standardized Provider format.
        """
        provider_obj = {
            "Identifiers": [],
            "Demographics": {
                "FirstName": None,
                "MiddleName": None,
                "LastName": None,
                "Credentials": [],
                "Sex": None,
            },
            "Billable": None,
            "Role": [],
            "IsActive": resource.get("active", True),
        }

        # Transform identifiers
        identifiers = resource.get("identifier", [])
        for identifier in identifiers:
            # Handle NPI with data-absent-reason extension
            if identifier.get("_value"):
                # Skip identifiers with data-absent-reason (unknown NPI)
                continue

            id_value = identifier.get("value")
            if id_value:
                id_type = self._get_identifier_type(identifier)
                provider_obj["Identifiers"].append({
                    "ID": id_value,
                    "IDType": id_type
                })

        # Add FHIR resource ID as identifier
        if resource.get("id"):
            provider_obj["Identifiers"].append({
                "ID": resource.get("id"),
                "IDType": "FHIR_ID"
            })

        # Transform name
        names = resource.get("name", [])
        if names:
            name = names[0]  # Use first name entry
            given_names = name.get("given", [])

            provider_obj["Demographics"]["FirstName"] = given_names[0] if len(given_names) > 0 else None
            provider_obj["Demographics"]["MiddleName"] = given_names[1] if len(given_names) > 1 else None
            provider_obj["Demographics"]["LastName"] = name.get("family")

            # Extract credentials from suffix
            suffixes = name.get("suffix", [])
            if suffixes:
                provider_obj["Demographics"]["Credentials"] = suffixes

            # Extract prefix (titles like Dr, Mr, Ms)
            prefixes = name.get("prefix", [])
            if prefixes:
                provider_obj["Demographics"]["Prefix"] = prefixes

        # Transform gender
        gender = resource.get("gender", "").lower()
        if gender == "male":
            provider_obj["Demographics"]["Sex"] = "Male"
        elif gender == "female":
            provider_obj["Demographics"]["Sex"] = "Female"
        elif gender == "unknown":
            provider_obj["Demographics"]["Sex"] = "Unknown"
        else:
            provider_obj["Demographics"]["Sex"] = None

        # Transform telecom (contact info)
        telecoms = resource.get("telecom", [])
        if telecoms:
            phone_numbers = {}
            email_addresses = []

            for telecom in telecoms:
                system = telecom.get("system")
                value = telecom.get("value")
                use = telecom.get("use", "work")

                if system == "phone":
                    if use == "home":
                        phone_numbers["Home"] = value
                    elif use == "mobile":
                        phone_numbers["Mobile"] = value
                    else:
                        phone_numbers["Office"] = value
                elif system == "email":
                    email_addresses.append(value)

            if phone_numbers:
                provider_obj["Demographics"]["PhoneNumber"] = phone_numbers
            if email_addresses:
                provider_obj["Demographics"]["EmailAddresses"] = email_addresses

        # Transform address
        addresses = resource.get("address", [])
        if addresses:
            provider_addresses = []
            for addr in addresses:
                address_obj = {
                    "Use": addr.get("use", "work").capitalize(),
                    "StreetAddress": ", ".join(addr.get("line", [])) if isinstance(addr.get("line"), list) else addr.get("line", ""),
                    "City": addr.get("city"),
                    "State": addr.get("state"),
                    "ZIP": addr.get("postalCode"),
                    "Country": addr.get("country"),
                    "County": addr.get("district"),
                }
                provider_addresses.append(address_obj)
            provider_obj["Demographics"]["Addresses"] = provider_addresses

        # Transform extensions (practitioner-role)
        extensions = resource.get("extension", [])
        for ext in extensions:
            url = ext.get("url", "")
            if "practitioner-role" in url.lower():
                value_ref = ext.get("valueReference", {})
                if value_ref.get("reference"):
                    # Extract organization reference
                    org_ref = value_ref.get("reference", "")
                    if "Organization/" in org_ref:
                        org_id = org_ref.split("Organization/")[-1]
                        provider_obj["Role"].append({
                            "Organization": {
                                "ID": org_id,
                                "IDType": "OrganizationID"
                            }
                        })

        # Transform qualifications
        qualifications = resource.get("qualification", [])
        if qualifications:
            qual_list = []
            for qual in qualifications:
                qual_obj = {
                    "Identifiers": [],
                    "Code": None,
                    "Codeset": None,
                    "Description": None,
                    "StartDate": None,
                    "EndDate": None,
                }

                # Get qualification identifiers
                qual_identifiers = qual.get("identifier", [])
                for qi in qual_identifiers:
                    qual_obj["Identifiers"].append({
                        "ID": qi.get("value"),
                        "IDType": qi.get("system")
                    })

                # Get qualification code
                code = qual.get("code", {})
                codings = code.get("coding", [])
                if codings:
                    coding = codings[0]
                    qual_obj["Code"] = coding.get("code")
                    qual_obj["Codeset"] = coding.get("system")
                    qual_obj["Description"] = coding.get("display")
                elif code.get("text"):
                    qual_obj["Description"] = code.get("text")

                # Get period
                period = qual.get("period", {})
                qual_obj["StartDate"] = period.get("start")
                qual_obj["EndDate"] = period.get("end")

                qual_list.append(qual_obj)

            provider_obj["Qualifications"] = qual_list

        return provider_obj

    def _get_identifier_type(self, identifier):
        """
        Determine identifier type from FHIR identifier object.
        """
        system = identifier.get("system", "")

        if "us-npi" in system or "npi" in system.lower():
            return "NPI"
        elif "2.16.840.1.113883.3.3388" in system:
            # Practice Fusion internal ID system
            return "INTERNAL_ID"
        elif identifier.get("type"):
            type_coding = identifier.get("type", {}).get("coding", [])
            if type_coding:
                return type_coding[0].get("code", "Unknown")

        return "Unknown"

    def _extract_paging(self, fhir_response):
        """
        Extract pagination information from FHIR Bundle.
        """
        links = fhir_response.get("link", [])
        paging = {}

        for link in links:
            relation = link.get("relation")
            url = link.get("url")
            if relation and url:
                paging[relation] = url

        if paging:
            self.destination_response["Paging"] = {
                "Total": fhir_response.get("total"),
                "Self": paging.get("self"),
                "Next": paging.get("next"),
                "Previous": paging.get("previous"),
                "First": paging.get("first"),
                "Last": paging.get("last"),
            }
