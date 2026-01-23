from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Organization import Organization


class OrganizationQueryTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Organization",
                "EventType": "Query",
                "Source": {"ID": str(self.connection.uuid), "Name": "connectionid"},
                "Raw": [],
            },
            "Organizations": [],
            "Paging": None,
        }

    def transform(self):
        """
        Transform organization query request and fetch data from eClinicalWorks.
        """
        try:
            # Extract filter parameters from source_json
            org_data = self.source_json.get("Organization", {})

            organization_id = None
            name = None
            org_type = None
            address = None

            # Extract organization ID if provided
            identifiers = org_data.get("Identifiers", {})
            if identifiers:
                organization_id = identifiers.get("ID")

            # Extract name if provided
            name = org_data.get("Name")

            # Extract type if provided
            type_data = org_data.get("Type", {})
            if type_data:
                org_type = type_data.get("Code") or type_data.get("Name")

            # Extract address if provided
            address_data = org_data.get("Address", {})
            if address_data:
                # Build address string from components
                address_parts = [
                    address_data.get("StreetAddress"),
                    address_data.get("City"),
                    address_data.get("State"),
                    address_data.get("ZIP"),
                ]
                address = " ".join(filter(None, address_parts)) or None

            # Initialize Organization category and authenticate
            organization_client = Organization(self.connection)
            auth_status = organization_client.authenticate()

            if auth_status != 200:
                self.destination_response["detail"] = "Authentication failed"
                self.destination_response["statuscode"] = 401
                return self.destination_response

            # Fetch organization data from eClinicalWorks
            org_response, status_code = organization_client.get_organization(
                organization_id=organization_id,
                name=name,
                org_type=org_type,
                address=address
            )

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(org_response)

            if status_code == 200:
                self._transform_fhir_response(org_response)
            else:
                self.destination_response["detail"] = "Failed to fetch organization data"
                self.destination_response["statuscode"] = status_code
                self.destination_response["error"] = org_response

            return self.destination_response

        except Exception as e:
            self.destination_response["detail"] = f"Error processing organization query: {str(e)}"
            self.destination_response["statuscode"] = 500
            return self.destination_response

    def _transform_fhir_response(self, fhir_response):
        """
        Transform FHIR Bundle response to standardized organization format.
        """
        organizations = []

        # Handle FHIR Bundle response
        if fhir_response.get("resourceType") == "Bundle":
            total = fhir_response.get("total", 0)
            entries = fhir_response.get("entry", [])

            if total >= 1 and entries:
                for entry in entries:
                    resource = entry.get("resource", {})
                    if resource.get("resourceType") == "Organization":
                        org_obj = self._transform_organization_resource(resource)
                        organizations.append(org_obj)

                # Handle pagination
                self._extract_paging(fhir_response)

        # Handle single Organization resource
        elif fhir_response.get("resourceType") == "Organization":
            org_obj = self._transform_organization_resource(fhir_response)
            organizations.append(org_obj)

        self.destination_response["Organizations"] = organizations

    def _transform_organization_resource(self, resource):
        """
        Transform a single FHIR Organization resource to standardized format.
        """
        org_obj = {
            "Active": resource.get("active", False),
            "Name": resource.get("name"),
            "Aliases": resource.get("alias", []),
            "Address": [],
            "Contacts": [],
            "PartOf": None,
            "Type": None,
            "Identifiers": [],
        }

        # Transform identifiers
        identifiers = resource.get("identifier", [])
        for identifier in identifiers:
            id_value = identifier.get("value")
            if id_value:
                id_type = self._get_identifier_type(identifier)
                org_obj["Identifiers"].append({
                    "ID": id_value,
                    "IDType": id_type
                })
            # Handle data-absent-reason extension
            elif identifier.get("_value"):
                extensions = identifier.get("_value", {}).get("extension", [])
                for ext in extensions:
                    if ext.get("url") == "http://hl7.org/fhir/StructureDefinition/data-absent-reason":
                        org_obj["Identifiers"].append({
                            "ID": None,
                            "IDType": self._get_identifier_type(identifier),
                            "AbsentReason": ext.get("valueCode")
                        })

        # Add FHIR resource ID as identifier
        if resource.get("id"):
            org_obj["Identifiers"].append({
                "ID": resource.get("id"),
                "IDType": "FHIR_ID"
            })

        # Transform addresses
        addresses = resource.get("address", [])
        for addr in addresses:
            address_obj = {
                "Use": addr.get("use"),
                "StreetAddress": ", ".join(addr.get("line", [])),
                "City": addr.get("city"),
                "State": addr.get("state"),
                "ZIP": addr.get("postalCode"),
                "Country": addr.get("country"),
                "County": addr.get("district"),
            }
            org_obj["Address"].append(address_obj)

        # Transform telecom (contacts)
        telecoms = resource.get("telecom", [])
        for telecom in telecoms:
            contact_obj = {
                "System": telecom.get("system"),
                "Value": telecom.get("value"),
                "Use": telecom.get("use"),
            }
            org_obj["Contacts"].append(contact_obj)

        # Transform type
        types = resource.get("type", [])
        if types:
            type_obj = types[0]
            codings = type_obj.get("coding", [])
            if codings:
                coding = codings[0]
                org_obj["Type"] = {
                    "Code": coding.get("code"),
                    "CodeSystem": coding.get("system"),
                    "Name": coding.get("display"),
                }
            elif type_obj.get("text"):
                org_obj["Type"] = {
                    "Code": None,
                    "CodeSystem": None,
                    "Name": type_obj.get("text"),
                }

        # Transform partOf reference
        part_of = resource.get("partOf")
        if part_of:
            org_obj["PartOf"] = {
                "Reference": part_of.get("reference"),
                "Display": part_of.get("display"),
            }

        return org_obj

    def _get_identifier_type(self, identifier):
        """
        Determine identifier type from FHIR identifier object.
        """
        system = identifier.get("system", "")

        if "us-npi" in system or "npi" in system.lower():
            return "NPI"
        elif "2.16.840.1.113883.4.391" in system:
            return "OID"
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
            }


class OrganizationCreateTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Organization",
                "EventType": "Create",
                "Source": {"ID": str(self.connection.uuid), "Name": "connectionid"},
                "Raw": [],
            },
        }

    def transform(self):
        self.destination_response["detail"] = "Not implemented"
        self.destination_response["statuscode"] = 501
        return self.destination_response
