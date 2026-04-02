from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS


class Task(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def create_task(self, bundle_data):
        url = self.build_url(
            ECW_URLS["Task"]["create_task"]["path"]
        )
        return self.post(url, content_type="application/fhir+json", data=bundle_data)
