from ecaremd.ehr_integrations.ehr_services.CharmHealth.client import CHFHIRClient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.urls import CH_URLS


class DocumentReference(CHFHIRClient):
    def __init__(self, customer_id, tenant_name, source_json) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def search_patient_documents(self, **kwargs):
        url = self.build_url(
            CH_URLS["DocumentReference"]["search_patient_documents"]["path"],
            patient_id=kwargs.get("patient"),
        )

        return self.get(
            url,
            params={
                "category": kwargs.get("category"),
                "patient": kwargs.get("patientid"),
            },
        )
