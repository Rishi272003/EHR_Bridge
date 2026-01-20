from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS

class Patient(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)
    def get_search_criteria(self, **kwargs):
        print("kwargs",kwargs)
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

    def create_new_patient(self, **kwargs):
        url = self.build_url(
            ECW_URLS["Patient"]["create_new_patient"]["path"],
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def get_specific_patient(self, patientid):
        url = self.build_url(
            ECW_URLS["Patient"]["specific_patient"]["path"], patientid=patientid
        )
        return self.get(url)
