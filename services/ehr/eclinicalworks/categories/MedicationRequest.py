from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class MedicationRequest(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name, source_json) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_orders(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["MedicationRequest"]["get_patient_orders"]["path"],
            practiceid=practiceid,
        )

        return self.get(
            url,
            params={"patient": kwargs.get("patientid"), "intent": kwargs.get("intent")},
        )
