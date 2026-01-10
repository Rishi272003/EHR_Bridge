from services.ehr.athena.client import AthenaHealthClient
from services.ehr.athena.urls import ATHENA_URLS

class Providers(AthenaHealthClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_all_providers(self):
        url = self.build_url(
            ATHENA_URLS["Providers"]["get_all_providers"]["path"],
        )
        return self.get(url)

    def get_provider_by_id(self, provider_id):
        url = self.build_url(
            ATHENA_URLS["Providers"]["get_provider_by_id"]["path"],
            providerid=provider_id,
        )
        return self.get(url)
    def create_provider(self, provider_data):
        url = self.build_url(
            ATHENA_URLS["Providers"]["create_provider"]["path"],
        )
        return self.post(url, provider_data)
