from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS


class DocumentReference(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_document_by_id(self, document_id):
        """
        Search for Document Reference by specific id.
        GET [base]/DocumentReference/[id] or GET [base]/DocumentReference?_id=[id]

        Args:
            document_id: Document Reference ID

        Returns:
            DocumentReference resource for the specific id
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        return self.get(
            url,
            params={"_id": document_id},
        )

    def search_by_patient(self, patient_reference):
        """
        Search for Document Reference by patient.
        GET [base]/DocumentReference?patient=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])

        Returns:
            DocumentReference resources associated with the specific patient
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={"patient": patient_reference},
        )

    def search_by_patient_and_category(self, patient_reference, category):
        """
        Search for Document Reference by patient and category.
        GET [base]/DocumentReference?patient=[reference]&category=clinical-note

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            category: Category code (e.g., 'clinical-note')

        Returns:
            DocumentReference resources associated with the specific patient and category
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "category": category,
            },
        )

    def search_by_patient_category_and_date(
        self, patient_reference, category, date_params=None
    ):
        """
        Search for Document Reference by patient, category and date range.
        GET [base]/DocumentReference?patient=[reference]&category=clinical-note&date=ge2019

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            category: Category code (e.g., 'clinical-note')
            date_params: Dictionary with date search parameters. Can include:
                - 'ge': greater than or equal to date
                - 'gt': greater than date
                - 'le': less than or equal to date
                - 'lt': less than date
                - 'eq': equal to date
                Example: {'ge': '2019-01-01', 'le': '2019-12-31'}

        Returns:
            DocumentReference resources associated with the specific patient, category and date range
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        params = {
            "patient": patient_reference,
            "category": category,
        }

        # Add date parameters
        if date_params:
            date_values = []
            for operator, date_value in date_params.items():
                if operator in ["ge", "gt", "le", "lt", "eq"]:
                    date_values.append(f"{operator}{date_value}")

            if date_values:
                # FHIR allows multiple date parameters
                params["date"] = date_values

        return self.get(url, params=params)

    def search_by_patient_and_type(self, patient_reference, type_code):
        """
        Search for Document Reference by patient and type.
        GET [base]/DocumentReference?patient=[reference]&type=[code]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            type_code: Document type code (e.g., '34133-9' for Summary of Episode Note)

        Returns:
            DocumentReference resources associated with the specific patient and type
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "type": type_code,
            },
        )

    def search_by_patient_and_encounter(self, patient_reference, encounter_id):
        """
        Search for Document Reference by patient and encounter.
        GET [base]/DocumentReference?encounter={ID}&patient=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            encounter_id: Encounter ID

        Returns:
            Visit summary type C-CDA document associated with the specific encounter
        """
        # base_url already includes practice_id, path has no {practiceid} placeholder
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        # Remove 'Encounter/' prefix if present
        if encounter_id and encounter_id.startswith("Encounter/"):
            encounter_id = encounter_id.replace("Encounter/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "encounter": encounter_id,
            },
        )

    def search_patient_documents(self, **kwargs):
        """
        Generic search method that supports all search parameters.
        This method can handle any combination of search parameters.

        Args:
            **kwargs: Search parameters including:
                - patient: Patient reference
                - category: Category code
                - type: Document type code
                - encounter: Encounter ID
                - date: Date search parameter (can be string like 'ge2019' or dict with operators)
                - _id: Document ID

        Returns:
            DocumentReference resources matching the search criteria
        """
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
        )

        params = {}

        # Handle patient parameter
        if kwargs.get("patient") or kwargs.get("patientid"):
            patient_ref = kwargs.get("patient") or kwargs.get("patientid")
            if patient_ref.startswith("Patient/"):
                patient_ref = patient_ref.replace("Patient/", "")
            params["patient"] = patient_ref

        # Handle category parameter
        if kwargs.get("category"):
            params["category"] = kwargs.get("category")

        # Handle type parameter
        if kwargs.get("type"):
            params["type"] = kwargs.get("type")

        # Handle encounter parameter
        if kwargs.get("encounter"):
            encounter_ref = kwargs.get("encounter")
            if encounter_ref.startswith("Encounter/"):
                encounter_ref = encounter_ref.replace("Encounter/", "")
            params["encounter"] = encounter_ref

        # Handle date parameter
        if kwargs.get("date"):
            date_param = kwargs.get("date")
            if isinstance(date_param, dict):
                # Multiple date operators
                date_values = []
                for operator, date_value in date_param.items():
                    if operator in ["ge", "gt", "le", "lt", "eq"]:
                        date_values.append(f"{operator}{date_value}")
                if date_values:
                    params["date"] = date_values
            elif isinstance(date_param, str):
                # Single date parameter (e.g., 'ge2019')
                params["date"] = date_param

        # Handle _id parameter
        if kwargs.get("_id") or kwargs.get("id"):
            params["_id"] = kwargs.get("_id") or kwargs.get("id")

        return self.get(url, params=params)

    def get_patient_ccda(self, practiceid, binaryid, **kwargs):
        """
        Get Patient CCDA document.

        Args:
            practiceid: Practice ID
            binaryid: Binary resource ID (document ID)

        Returns:
            Binary resource containing the CCDA document
        """
        url = self.build_url(
            ECW_URLS["Binary"]["get_patient_ccda"]["path"],
            practiceid=practiceid,
            binaryid=binaryid,
        )
        return self.get(url)

    def new_clinical_note(self, **kwargs):
        """
        Create a new clinical note (DocumentReference).

        Args:
            **kwargs: DocumentReference resource data

        Returns:
            Created DocumentReference resource
        """
        url = self.build_url(
            ECW_URLS["DocumentReference"]["new_clinical_note"]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)
