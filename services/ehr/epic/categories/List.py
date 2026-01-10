from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class List(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_medications(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_medications"]["path"],
            patient=kwargs.get("patientid"),
            code="medications",
        )
        return self.get(url)
