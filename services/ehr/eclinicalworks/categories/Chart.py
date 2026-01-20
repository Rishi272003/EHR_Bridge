from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS


class Chart(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_patient_demographics(self, patientid):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_demographics"]["path"],
        )
        return self.get(url, params={"_id": patientid})

    def get_patient_allergy(self, patientid):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_allergy"]["path"],
        )
        return self.get(
            url,
            params={"patient": patientid},
        )

    def get_patient_medication(self, patientid):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_medication"]["path"],
        )
        return self.get(
            url,
            params={
                "patient": patientid,
                # "intent": "order",
                # "date": [
                #     "ge" + kwargs.get("start_date"),
                #     "le" + kwargs.get("end_date"),
                # ],
            },
        )

    def get_patient_diagnoses(self, patientid):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_problem"]["path"],
        )
        return self.get(
            url,
            params={
                "patient": patientid,
                "category": "problem-list-item",
            },
        )

    def get_patient_encounter(self, patientid=None, visit_number=None, start_date=None, end_date=None):
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_encounter"]["path"],
        )
        params = {}

        # Add visit number if provided
        if visit_number:
            params["_id"] = visit_number
        # Add patient ID if provided
        if patientid:
            params["patient"] = patientid
        # Add date filters if provided
        if start_date:
            params["date"] = f"ge{start_date}"
        if end_date:
            # If date already exists, append end date
            if "date" in params:
                params["date"] = f"{params['date']}&date=le{end_date}"
            else:
                params["date"] = f"le{end_date}"

        return self.get(url, params=params)

    def get_patient_vitals(self, patientid):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_vitals"]["path"],
        )
        return self.get(
            url,
            params={
                "patient": patientid,
                "category": "vital-signs",
                # "date": [
                #     "ge" + kwargs.get("start_date"),
                #     "le" + kwargs.get("end_date"),
                # ],
            },
        )

    def get_patient_lab_result(self, practiceid=None, **kwargs):
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_lab_result"]["path"],
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "laboratory",
            },
        )

    def get_patient_insurance(self, practiceid=None, **kwargs):
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_insurance"]["path"],
        )
        return self.get(
            url,
            params={"patient": kwargs.get("patientid")},
        )
