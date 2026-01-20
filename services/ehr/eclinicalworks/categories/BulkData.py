from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class BulkData(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name, source_json) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_job_id(self, group_id, practiceid, category):
        url = self.build_url(
            ECW_URLS["BulkData"]["get_job_id"]["path"],
            practiceid=practiceid,
            group_id=group_id,
        )

        return self.bulk_get(
            url,
            params={"_type": category},
        )
