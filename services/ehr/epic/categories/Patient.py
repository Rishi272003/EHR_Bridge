from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Patient(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_patient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["create_new_patient"]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def search_patient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["search_patient"]["path"],
        )
        return self.get(
            url,
            params={
                "given": kwargs.get("firstname"),
                "family": kwargs.get("lastname"),
                "birthdate": kwargs.get("dob"),
            },
        )

    def get_specific_patient(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["get_specific_patient"]["path"],
            ID=ID,
        )

        return self.get(url)
