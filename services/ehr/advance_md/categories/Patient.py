from ecaremd.ehr_integrations.ehr_services.advance_md.client import AdvanceMDFhirClient
from ecaremd.ehr_integrations.ehr_services.advance_md.urls import ADVANCEMD_URLS


class Patient(AdvanceMDFhirClient):
    def __init__(self, customer_id, tenant_name, source_json):
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_demographics_by_id(self, **kwargs):
        url = self.build_url(
            ADVANCEMD_URLS["Patient"]["get_patient_demographics"]["path"]
        )
        payload = {
            "_id": kwargs.get("patientid"),
        }
        return self.get(url, params=payload)

    def get_patient_demographics_by_name(self, data: dict):
        url = self.build_url(
            ADVANCEMD_URLS["Patient"]["get_patient_demographics"]["path"]
        )
        payload = {
            f"{data.get('param')}": data.get("value"),
        }
        return self.get(url, params=payload)
