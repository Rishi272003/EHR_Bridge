from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class MedicationRequest(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_orders(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Medication"]["MedicationRequest"]["search_orders"]["path"],
        )

        return self.get(url, params={"patient": kwargs.get("patientid")})

    def get_orders(self,med_id):
        url = self.build_url(
            EPIC_R4_URLS["Medication"]["MedicationRequest"]["get_orders"]["path"],ID=med_id)
        return self.get(url)
