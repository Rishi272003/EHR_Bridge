from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS

class Patient(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)
    def get_search_criteria(self, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["search_criteria"]["path"]
        )
        return self.get(
            url,
            params={
                "birthdate": kwargs.get("dob"),
                "name": kwargs.get("name"),
            },
        )

    def get_patient_ccda(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["search_criteria"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "ccda",
            },
        )

    def create_new_patient(self, patient_resource):
        # Bundle transactions go to the FHIR base URL (no resource path)
        url = self.base_url
        bundle = {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {
                    "resource": patient_resource,
                    "request": {
                        "method": "POST",
                        "url": "Patient",
                    },
                }
            ],
        }
        return self.post(url, content_type="application/fhir+json", data=bundle)

    def get_specific_patient(self, patientid):
        url = self.build_url(
            ECW_URLS["Patient"]["specific_patient"]["path"], patientid=patientid
        )
        return self.get(url)
