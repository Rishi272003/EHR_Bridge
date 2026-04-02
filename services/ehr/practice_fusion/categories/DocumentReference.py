from services.ehr.practice_fusion.client import PracticeFusionClient
from services.ehr.practice_fusion.urls import PRACTICE_FUSION_URLS


class DocumentReference(PracticeFusionClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_document_by_id(self, document_id):
        """
        Get Document Reference by specific ID.
        GET [base]/DocumentReference/{document_id}

        Args:
            document_id: Document Reference ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["DocumentReference"]["get_document_by_id"]["path"],
            document_id=document_id
        )
        return self.get(url)

    def search_patient_documents(self, patient_id=None, category=None, type_code=None, date_params=None, encounter_id=None, document_id=None):
        """
        Search for Document References that meet supplied query parameters.
        GET [base]/DocumentReference?patient=[id]&category=[category]&type=[type]&date=[date]

        Args:
            patient_id: Patient ID
            category: Category code (e.g., 'clinical-note')
            type_code: Document type LOINC code (e.g., '34133-9')
            date_params: Dictionary with date search parameters. Can include:
                - 'ge': greater than or equal to date
                - 'le': less than or equal to date
            encounter_id: Encounter ID
            document_id: Document ID (for _id parameter)

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["DocumentReference"]["search_patient_documents"]["path"]
        )
        params = {}

        if document_id:
            params["_id"] = document_id
        if patient_id:
            params["patient"] = patient_id
        if category:
            params["category"] = category
        if type_code:
            params["type"] = type_code
        if encounter_id:
            params["encounter"] = encounter_id
        if date_params:
            # Build date parameter string
            date_str_parts = []
            if date_params.get("ge"):
                date_str_parts.append(f"ge{date_params['ge']}")
            if date_params.get("le"):
                date_str_parts.append(f"le{date_params['le']}")
            if date_str_parts:
                params["date"] = ",".join(date_str_parts)

        return self.get(url, params=params)
