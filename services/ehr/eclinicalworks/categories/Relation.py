from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class Relation(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name, source_json) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_relation(self, practiceid, organizationid):
        url = self.build_url(
            ECW_URLS["Charts"]["get_patient_relation"]["path"],
            practiceid=practiceid,
        )

        return self.get(url, params={"_id": organizationid})
