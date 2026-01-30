from services.ehr.practice_fusion.client import PracticeFusionClient
from services.ehr.practice_fusion.urls import PRACTICE_FUSION_URLS


class Patient(PracticeFusionClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def search_patients(self, **kwargs):
        """
        Search for patients that meet supplied query parameters.

        Args:
            **kwargs: Search parameters (e.g., name, birthdate, identifier)

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Patient"]["search_patients"]["path"]
        )
        return self.get(url, params=kwargs)

    def get_patient(self, patient_id):
        """
        Get specific patient by ID.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Patient"]["get_patient"]["path"],
            patient_id=patient_id
        )
        return self.get(url)

    def create_patient(self, **kwargs):
        """
        Create a new patient.

        Args:
            **kwargs: Patient data

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Patient"]["create_patient"]["path"]
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def update_patient(self, patient_id, **kwargs):
        """
        Update an existing patient.

        Args:
            patient_id: Patient ID
            **kwargs: Patient data to update

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Patient"]["update_patient"]["path"],
            patient_id=patient_id
        )
        payload = self.build_payload(**kwargs)
        return self.put(url, data=payload)
