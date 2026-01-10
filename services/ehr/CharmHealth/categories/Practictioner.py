from ecaremd.ehr_integrations.ehr_services.CharmHealth.client import CHFHIRClient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.urls import CH_URLS


class Practitioner(CHFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_practitioner(self, practiceid, **kwargs):
        url = self.build_url(
            CH_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"name": kwargs.get("name")})
