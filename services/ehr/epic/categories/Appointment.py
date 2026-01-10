from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Appointment(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_appointment(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Appointment"]["new_appointment"]["path"]
        )
        payload = self.build_payload(
            resourceType=kwargs.get("resourceType"), parameter=kwargs.get("parameter")
        )
        return self.post(url, data=payload)

    def get_specific_appointment(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Appointment"]["get_appointment"]["path"],
            ID=kwargs.get("appointmentid"),
        )
        return self.get(url)

    def search_encounter(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Encounter"]["search_encounter"]["path"]
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "date": [
                    "ge" + kwargs.get("start_date"),
                    "le" + kwargs.get("end_date"),
                ],
            },
        )

    def search_appointment(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Appointment"]["get_appointment"]["path"],
            ID=kwargs.get("appointmentid"),
        )
        return self.get(url)

    def get_open_appointment(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Appointment"]["get_open_appointment"][
                "path"
            ],
        )

        payload = self.build_payload(
            resourceType=kwargs.get("resourceType"), parameter=kwargs.get("parameter")
        )

        return self.post(url, data=payload)
