from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class Patient(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name=None, source_json=None) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_search_criteria(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["search_criteria"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "birthdate": kwargs.get("dob"),
                "name": kwargs.get("name"),
            },
        )

    def get_patient_ccda(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["search_criteria"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "ccda",
            },
        )

    def create_new_patient(self, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["create_new_patient"]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)
