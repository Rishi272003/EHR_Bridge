from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class DocumentReference(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def search_patient_documents(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["DocumentReference"]["search_patient_documents"]["path"],
            practiceid=practiceid,
        )

        return self.get(
            url,
            params={
                "category": kwargs.get("category"),
                "patient": kwargs.get("patientid"),
            },
        )

    def get_patient_ccda(self, practiceid, binaryid, **kwargs):
        url = self.build_url(
            ECW_URLS["Binary"]["get_patient_ccda"]["path"],
            practiceid=practiceid,
            binaryid=binaryid,
        )
        return self.get(url)

    def new_clinical_note(self, **kwargs):
        url = self.build_url(
            ECW_URLS["DocumentReference"]["new_clinical_note"]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)
