from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class Organization(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_organization(self, practiceid, organizationid):
        url = self.build_url(
            ECW_URLS["Organization"]["get_organization"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"_id": organizationid})
