from services.ehr.practice_fusion.client import PracticeFusionClient
from services.ehr.practice_fusion.urls import PRACTICE_FUSION_URLS


class Chart(PracticeFusionClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_patient_demographics(self, patient_id):
        """
        Get patient's demographics.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_demographics"]["path"]
        )
        return self.get(url, params={"_id": patient_id})

    def get_patient_allergy(self, patient_id):
        """
        Get patient's allergies.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_allergy"]["path"]
        )
        return self.get(url, params={"patient": patient_id})

    def get_patient_medication(self, patient_id):
        """
        Get patient's medications.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_medication"]["path"]
        )
        return self.get(
            url,
            params={"patient": patient_id}
        )

    def get_patient_diagnoses(self, patient_id):
        """
        Get patient's diagnoses.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_problem"]["path"]
        )
        return self.get(
            url,
            params={
                "patient": patient_id,
                "category": "problem-list-item",
            },
        )

    def get_patient_encounter(self, patient_id=None, visit_number=None, start_date=None, end_date=None):
        """
        Get patient's encounters.

        Args:
            patient_id: Patient ID
            visit_number: Visit/Encounter number
            start_date: Start date filter
            end_date: End date filter

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_encounter"]["path"]
        )
        params = {}

        if visit_number:
            params["_id"] = visit_number
        if patient_id:
            params["patient"] = patient_id
        if start_date:
            params["date"] = f"ge{start_date}"
        if end_date:
            if "date" in params:
                params["date"] = f"{params['date']}&date=le{end_date}"
            else:
                params["date"] = f"le{end_date}"

        return self.get(url, params=params)

    def get_patient_vitals(self, patient_id):
        """
        Get patient's vitals.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_vitals"]["path"]
        )
        return self.get(
            url,
            params={
                "patient": patient_id,
                "category": "vital-signs",
            },
        )

    def get_patient_lab_result(self, patient_id):
        """
        Get patient's lab results.

        Args:
            patient_id: Patient ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_lab_result"]["path"]
        )
        return self.get(
            url,
            params={
                "patient": patient_id,
                "category": "laboratory",
            },
        )

    def get_patient_insurance(self, patient_id=None, **kwargs):
        """
        Get patient's insurance details.

        Args:
            patient_id: Patient ID
            **kwargs: Additional parameters

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Chart"]["get_patient_insurance"]["path"]
        )
        return self.get(
            url,
            params={"patient": kwargs.get("patientid") or patient_id},
        )
