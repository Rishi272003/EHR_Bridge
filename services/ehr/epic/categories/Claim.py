from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Claim(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_explanation_of_benefit(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Financial"]["ExplanationOfBenefit"][
                "search_explanation_of_benefit"
            ]["path"],
            **kwargs
        )
        return self.get(url)
