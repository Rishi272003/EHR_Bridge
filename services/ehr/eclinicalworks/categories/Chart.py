from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class Chart(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name, source_json) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_demographics(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_demographics"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"_id": kwargs.get("patientid")})

    def get_patient_allergy(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_allergy"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={"patient": kwargs.get("patientid")},
        )

    def get_patient_medication(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_medication"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                # "intent": "order",
                # "date": [
                #     "ge" + kwargs.get("start_date"),
                #     "le" + kwargs.get("end_date"),
                # ],
            },
        )

    def get_patient_diagnoses(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_problem"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": kwargs.get("category"),
            },
        )

    def get_patient_encounter(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_encounter"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "date": "ge" + kwargs.get("start_date"),
            },
        )

    def get_patient_vitals(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_vitals"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "vital-signs",
                # "date": [
                #     "ge" + kwargs.get("start_date"),
                #     "le" + kwargs.get("end_date"),
                # ],
            },
        )

    def get_patient_lab_result(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_lab_result"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "laboratory",
            },
        )

    def get_patient_insurance(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Chart"]["get_patient_insurance"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={"patient": kwargs.get("patientid")},
        )
