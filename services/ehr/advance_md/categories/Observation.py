from ecaremd.ehr_integrations.ehr_services.advance_md.client import AdvanceMDFhirClient
from ecaremd.ehr_integrations.ehr_services.advance_md.urls import ADVANCEMD_URLS


class Observation(AdvanceMDFhirClient):
    def __init__(self, customer_id, tenant_name=None, source_json=None):
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_observations(self, **kwargs):
        url = self.build_url(
            ADVANCEMD_URLS["Observation"]["search_patient_vitals"]["path"]
        )
        params = {
            "patient": f"Patient/{kwargs.get('patient')}",
            "category": kwargs.get("category"),
        }

        return self.get(url=url, params=params)
