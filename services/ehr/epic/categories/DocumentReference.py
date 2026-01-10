from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class DocumentReference(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_external_CCDA_document(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "search_external_CCDA_document"
            ]["path"],
        )

        return self.get(url, params=kwargs)

    def search_clinical_notes(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_clinical_notes"][
                "path"
            ],
        )
        return self.get(url, params={"patient": kwargs.get("patientid")})

    def create_clinical_note(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "create_new_clinical_notes"
            ]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)
