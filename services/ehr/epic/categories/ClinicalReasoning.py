from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class CDSHooksServiceRequest(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name) -> None:
        super().__init__(customer_id, tenant_name)

    def get_unsigned_order(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["ClinicalReasoning"]["CDS Hooks ServiceRequest"][
                "get_unsigned_order"
            ]["path"],
            ID=ID,
        )

        return self.get(url)


class CDSHooksMedicationRequest(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_unsigned_order(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["ClinicalReasoning"]["CDS Hooks MedicationRequest"][
                "get_unsigned_order"
            ]["path"],
            ID=ID,
        )

        return self.get(url)
