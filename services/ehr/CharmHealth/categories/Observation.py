from ecaremd.ehr_integrations.ehr_services.CharmHealth.client import CHFHIRClient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.urls import CH_URLS


class Observation(CHFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_patient_vitals(self, **kwargs):
        url = self.build_url(
            CH_URLS["Observation"]["get_patient_vitals"]["path"],
        )

        return self.get(
            url,
            params={
                "patient": kwargs.get("patient"),
            },
        )
