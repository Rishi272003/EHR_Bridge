from ecaremd.ehr_integrations.ehr_services.CharmHealth.client import CHFHIRClient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.urls import CH_URLS


class Patient(CHFHIRClient):
    def __init__(self, customer_id, tenant_name=None, source_json=None) -> None:
        super().__init__(customer_id, tenant_name, source_json)

    def get_patient_by_name(self, **kwargs):
        url = self.build_url(CH_URLS["Patient"]["get_specific_patient"]["path"])
        return self.get(
            url,
            params={
                "first_name": kwargs.get("firstname"),
                "last_name": kwargs.get("lastname"),
                "dob": kwargs.get("dob"),
                "gender": kwargs.get("gender"),
            },
        )

    def get_patient_by_id(self, **kwargs):
        url = self.build_url(CH_URLS["Patient"]["get_specific_patient"]["path"])
        return self.get(
            url,
            params={
                "_id": kwargs.get("patientid"),
            },
        )

    def get_patient_demographics(self, **kwargs):
        url = self.build_url(
            CH_URLS["Patient"]["get_patient_demographics"]["path"],
            patientid=kwargs.get("patientid"),
        )
        return self.get(url)
