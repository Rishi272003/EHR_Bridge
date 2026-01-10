from ecaremd.ehr_integrations.ehr_services.advance_md.client import AdvanceMDFhirClient
from ecaremd.ehr_integrations.ehr_services.advance_md.urls import ADVANCEMD_URLS


class Device(AdvanceMDFhirClient):
    def __init__(self, customer_id, tenant_name=None, source_json=None):
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_devices(self, patient_id):
        url = self.build_url(ADVANCEMD_URLS["Device"]["get_patient_devices"]["path"])
        params = self.build_payload({"patient": patient_id})
        return self.get(url, params)
