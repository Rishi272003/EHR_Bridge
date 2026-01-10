from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Medication(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_medications(self, patientid, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Medication"]["Medication"]["search_medications"]["path"],
            _id=patientid,
        )

        return self.get(url)
