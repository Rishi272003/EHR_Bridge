from services.ehr.athena.client import AthenaHealthClient
from services.ehr.athena.urls import ATHENA_URLS


class Patient(AthenaHealthClient):
    def __init__(self,connection_obj) -> None:
        super().__init__(connection_obj)
    def get_patient_by_id(self,patient_id):
        url = self.build_url(ATHENA_URLS["Patient"]["get_by_id"]["path"],id=patient_id)
        return self.get(url)
    def get_patient_by_name(self,searchterm):
        url = self.build_url(ATHENA_URLS["Patient"]["get_by_name"]["path"])
        params = {
            "searchterm":searchterm
        }
        return self.get(url,payload=params)
