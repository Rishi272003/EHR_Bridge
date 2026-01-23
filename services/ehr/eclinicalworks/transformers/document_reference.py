from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.DocumentReference import DocumentReference


class DocumentReferenceQueryTransformer(Transformer):
    """
    Transformer for eClinicalWorks DocumentReference queries.
    Transforms FHIR DocumentReference/Binary responses to standardized format.

    Supported search parameters:
    - _id: Get document by specific ID
    - patient: Get documents for a specific patient
    - patient + category: Get documents by patient and category (e.g., clinical-note)
    - patient + category + date: Get documents with date range filter
    - patient + type: Get documents by patient and type code (e.g., 34133-9)
    - patient + encounter: Get visit summary for specific encounter
    """

    def __init__(self, connection_obj, source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "DocumentReference",
                "EventType": "Query",
                "Source": {"ID": str(self.connection.uuid), "Name": "connectionid"},
                "Raw": [],
            },
            "Documents": [],
            "Paging": None,
        }

    def transform(self):
        """
        Transform document reference query request and fetch data from eClinicalWorks.
        """
        try:
            # Initialize DocumentReference category and authenticate
            doc_ref_client = DocumentReference(self.connection)
            auth_status = doc_ref_client.authenticate()

            if auth_status != 200:
                self.destination_response["detail"] = "Authentication failed"
                self.destination_response["statuscode"] = 401
                return self.destination_response

            # Extract search parameters from source_json
            doc_data = self.source_json.get("Document", {})
            patient_data = self.source_json.get("Patient", {})

            # Extract document ID if provided
            document_id = None
            doc_identifiers = doc_data.get("Identifiers", [])
            if doc_identifiers:
                if isinstance(doc_identifiers, list) and len(doc_identifiers) > 0:
                    document_id = doc_identifiers[0].get("ID")
                elif isinstance(doc_identifiers, dict):
                    document_id = doc_identifiers.get("ID")

            # Extract patient ID
            patient_id = None
            patient_identifiers = patient_data.get("Identifiers", [])
            if patient_identifiers:
                if isinstance(patient_identifiers, list) and len(patient_identifiers) > 0:
                    patient_id = patient_identifiers[0].get("ID")
                elif isinstance(patient_identifiers, dict):
                    patient_id = patient_identifiers.get("ID")

            # Extract category
            category = doc_data.get("Category")

            # Extract type code
            type_code = None
            type_data = doc_data.get("Type", {})
            if type_data:
                type_code = type_data.get("Code")

            # Extract date parameters
            date_params = None
            date_data = doc_data.get("Date", {})
            if date_data:
                date_params = {}
                if date_data.get("Start"):
                    date_params["ge"] = date_data.get("Start")
                if date_data.get("End"):
                    date_params["le"] = date_data.get("End")

            # Extract encounter ID
            encounter_id = doc_data.get("EncounterID") or doc_data.get("Encounter")

            # Determine which search method to use and fetch data
            # Note: ECW client methods return tuple (data, status_code)
            doc_response = None
            status_code = None

            if document_id:
                # Search by document ID
                doc_response, status_code = doc_ref_client.get_document_by_id(document_id)
            elif patient_id and encounter_id:
                # Search by patient and encounter
                doc_response, status_code = doc_ref_client.search_by_patient_and_encounter(
                    patient_id, encounter_id
                )
            elif patient_id and category and date_params:
                # Search by patient, category, and date range
                doc_response, status_code = doc_ref_client.search_by_patient_category_and_date(
                    patient_id, category, date_params
                )
            elif patient_id and category:
                # Search by patient and category
                doc_response, status_code = doc_ref_client.search_by_patient_and_category(
                    patient_id, category
                )
            elif patient_id and type_code:
                # Search by patient and type
                doc_response, status_code = doc_ref_client.search_by_patient_and_type(
                    patient_id, type_code
                )
            elif patient_id:
                # Search by patient only
                doc_response, status_code = doc_ref_client.search_by_patient(patient_id)
            else:
                # Generic search with all available parameters
                search_params = {}
                if document_id:
                    search_params["_id"] = document_id
                if patient_id:
                    search_params["patient"] = patient_id
                if category:
                    search_params["category"] = category
                if type_code:
                    search_params["type"] = type_code
                if date_params:
                    search_params["date"] = date_params
                if encounter_id:
                    search_params["encounter"] = encounter_id

                doc_response, status_code = doc_ref_client.search_patient_documents(**search_params)

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(doc_response)

            if status_code == 200:
                self._transform_fhir_response(doc_response)
            else:
                self.destination_response["detail"] = "Failed to fetch document data"
                self.destination_response["statuscode"] = status_code
                self.destination_response["error"] = doc_response

            return self.destination_response

        except Exception as e:
            self.destination_response["detail"] = f"Error processing document reference query: {str(e)}"
            self.destination_response["statuscode"] = 500
            return self.destination_response

    def _transform_fhir_response(self, fhir_response):
        """
        Transform FHIR Bundle response to standardized document reference format.
        Handles both DocumentReference and Binary resources.
        """
        documents = []
        binary_resources = {}  # Store Binary resources for reference

        # Handle FHIR Bundle response
        if fhir_response.get("resourceType") == "Bundle":
            total = fhir_response.get("total", 0)
            entries = fhir_response.get("entry", [])

            # First pass: collect Binary resources
            for entry in entries:
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "Binary":
                    binary_id = resource.get("id")
                    if binary_id:
                        binary_resources[binary_id] = self._transform_binary_resource(
                            resource, entry.get("fullUrl")
                        )

            # Second pass: process DocumentReference resources and standalone Binary
            for entry in entries:
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "DocumentReference":
                    doc_obj = self._transform_document_reference_resource(
                        resource, entry.get("fullUrl"), binary_resources
                    )
                    documents.append(doc_obj)
                elif resource.get("resourceType") == "Binary":
                    # Add standalone Binary resources as documents if no DocumentReference
                    binary_id = resource.get("id")
                    if binary_id and binary_id in binary_resources:
                        documents.append(binary_resources[binary_id])

            # Handle pagination
            self._extract_paging(fhir_response)

        # Handle single DocumentReference resource
        elif fhir_response.get("resourceType") == "DocumentReference":
            doc_obj = self._transform_document_reference_resource(fhir_response, None, {})
            documents.append(doc_obj)
        # Handle single Binary resource
        elif fhir_response.get("resourceType") == "Binary":
            doc_obj = self._transform_binary_resource(fhir_response, None)
            documents.append(doc_obj)

        self.destination_response["Documents"] = documents

    def _transform_binary_resource(self, resource, full_url=None):
        """
        Transform a FHIR Binary resource to standardized format.
        """
        return {
            "ID": resource.get("id"),
            "ResourceType": "Binary",
            "ContentType": resource.get("contentType"),
            "Data": resource.get("data"),  # Base64 encoded content
            "FullUrl": full_url,
            "Profile": self._extract_profile(resource.get("meta", {})),
        }

    def _transform_document_reference_resource(self, resource, full_url=None, binary_resources=None):
        """
        Transform a FHIR DocumentReference resource to standardized format.
        """
        binary_resources = binary_resources or {}

        doc_obj = {
            "ID": resource.get("id"),
            "ResourceType": "DocumentReference",
            "FullUrl": full_url,
            "Identifiers": [],
            "Status": resource.get("status"),
            "DocStatus": resource.get("docStatus"),
            "Type": None,
            "Category": [],
            "Subject": None,
            "Date": resource.get("date"),
            "Authors": [],
            "Custodian": None,
            "Description": resource.get("description"),
            "SecurityLabels": [],
            "Content": [],
            "Context": None,
            "Profile": self._extract_profile(resource.get("meta", {})),
        }

        # Transform identifiers
        identifiers = resource.get("identifier", [])
        for identifier in identifiers:
            id_value = identifier.get("value")
            if id_value:
                id_type = self._get_identifier_type(identifier)
                doc_obj["Identifiers"].append({
                    "ID": id_value,
                    "IDType": id_type,
                    "System": identifier.get("system")
                })

        # Add FHIR resource ID as identifier
        if resource.get("id"):
            doc_obj["Identifiers"].append({
                "ID": resource.get("id"),
                "IDType": "FHIR_ID"
            })

        # Transform type (CodeableConcept)
        type_data = resource.get("type")
        if type_data:
            doc_obj["Type"] = self._transform_codeable_concept(type_data)

        # Transform category (list of CodeableConcept)
        categories = resource.get("category", [])
        for cat in categories:
            doc_obj["Category"].append(self._transform_codeable_concept(cat))

        # Transform subject (Reference to Patient)
        subject = resource.get("subject")
        if subject:
            doc_obj["Subject"] = {
                "Reference": subject.get("reference"),
                "Display": subject.get("display"),
                "Type": subject.get("type"),
            }

        # Transform authors (list of References)
        authors = resource.get("author", [])
        for author in authors:
            doc_obj["Authors"].append({
                "Reference": author.get("reference"),
                "Display": author.get("display"),
                "Type": author.get("type"),
            })

        # Transform custodian (Reference to Organization)
        custodian = resource.get("custodian")
        if custodian:
            doc_obj["Custodian"] = {
                "Reference": custodian.get("reference"),
                "Display": custodian.get("display"),
            }

        # Transform security labels (list of CodeableConcept)
        security_labels = resource.get("securityLabel", [])
        for label in security_labels:
            doc_obj["SecurityLabels"].append(self._transform_codeable_concept(label))

        # Transform content (list of attachment info)
        contents = resource.get("content", [])
        for content in contents:
            attachment = content.get("attachment", {})
            format_data = content.get("format")

            content_obj = {
                "Attachment": {
                    "ContentType": attachment.get("contentType"),
                    "Language": attachment.get("language"),
                    "Data": attachment.get("data"),  # Base64 encoded inline data
                    "Url": attachment.get("url"),  # Reference to Binary resource
                    "Size": attachment.get("size"),
                    "Hash": attachment.get("hash"),
                    "Title": attachment.get("title"),
                    "Creation": attachment.get("creation"),
                },
                "Format": self._transform_coding(format_data) if format_data else None,
            }

            # If URL references a Binary resource, include the binary data
            url = attachment.get("url")
            if url:
                # Extract Binary ID from URL (e.g., "Binary/abc123" or full URL)
                binary_id = url.split("/")[-1] if "/" in url else url
                if binary_id in binary_resources:
                    content_obj["BinaryData"] = binary_resources[binary_id].get("Data")

            doc_obj["Content"].append(content_obj)

        # Transform context
        context = resource.get("context")
        if context:
            doc_obj["Context"] = {
                "Encounter": [],
                "Events": [],
                "Period": None,
                "FacilityType": None,
                "PracticeSetting": None,
                "SourcePatientInfo": None,
                "Related": [],
            }

            # Transform encounter references
            encounters = context.get("encounter", [])
            for enc in encounters:
                doc_obj["Context"]["Encounter"].append({
                    "Reference": enc.get("reference"),
                    "Display": enc.get("display"),
                })

            # Transform event codes
            events = context.get("event", [])
            for event in events:
                doc_obj["Context"]["Events"].append(self._transform_codeable_concept(event))

            # Transform period
            period = context.get("period")
            if period:
                doc_obj["Context"]["Period"] = {
                    "Start": period.get("start"),
                    "End": period.get("end"),
                }

            # Transform facility type
            facility_type = context.get("facilityType")
            if facility_type:
                doc_obj["Context"]["FacilityType"] = self._transform_codeable_concept(facility_type)

            # Transform practice setting
            practice_setting = context.get("practiceSetting")
            if practice_setting:
                doc_obj["Context"]["PracticeSetting"] = self._transform_codeable_concept(practice_setting)

            # Transform source patient info
            source_patient = context.get("sourcePatientInfo")
            if source_patient:
                doc_obj["Context"]["SourcePatientInfo"] = {
                    "Reference": source_patient.get("reference"),
                    "Display": source_patient.get("display"),
                }

            # Transform related references
            related = context.get("related", [])
            for rel in related:
                doc_obj["Context"]["Related"].append({
                    "Reference": rel.get("reference"),
                    "Display": rel.get("display"),
                })

        return doc_obj

    def _transform_codeable_concept(self, codeable_concept):
        """
        Transform a FHIR CodeableConcept to standardized format.
        """
        if not codeable_concept:
            return None

        result = {
            "Coding": [],
            "Text": codeable_concept.get("text"),
        }

        codings = codeable_concept.get("coding", [])
        for coding in codings:
            result["Coding"].append(self._transform_coding(coding))

        return result

    def _transform_coding(self, coding):
        """
        Transform a FHIR Coding to standardized format.
        """
        if not coding:
            return None

        return {
            "System": coding.get("system"),
            "Version": coding.get("version"),
            "Code": coding.get("code"),
            "Display": coding.get("display"),
            "UserSelected": coding.get("userSelected"),
        }

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

    def _extract_profile(self, meta):
        """
        Extract profile information from meta.
        """
        profiles = meta.get("profile", [])
        if isinstance(profiles, list):
            return profiles
        elif profiles:
            return [profiles]
        return []

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
