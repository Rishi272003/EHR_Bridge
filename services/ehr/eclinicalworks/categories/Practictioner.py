from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class Practitioner(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_provider(self, practiceid, practitionerid):
        url = self.build_url(
            ECW_URLS["Practitioner"]["get_practitioner"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"_id": practitionerid})

    def search_practitioner(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"name": kwargs.get("name")})

    def get_provider_by_id(self, practiceid, practitionerid):
        url = self.build_url(
            ECW_URLS["Practitioner"]["get_practitioner_by_id"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"_id": practitionerid})
