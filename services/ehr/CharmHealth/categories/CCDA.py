from ecaremd.ehr_integrations.ehr_services.CharmHealth.client import CHFHIRClient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.urls import CH_URLS


class CCDA(CHFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_patient_ccda(self, **kwargs):
        url = self.build_url(
            CH_URLS["CCDA"]["get_patients_ccda"]["path"],
        )

        return self.get(
            url,
            params={
                "patient": kwargs.get("patient"),
            },
        )
