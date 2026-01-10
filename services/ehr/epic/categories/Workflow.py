from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Task(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_community_resource(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["Task"]["get_community_resource"]["path"], ID=ID
        )

        return self.get(url)

    def search_community_resource(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["Task"]["search_community_resource"]["path"],
            **kwargs
        )

        return self.get(url)

    def update_community_resource(self, ID, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["Task"]["update_community_resource"]["path"], ID=ID
        )
        payload = self.build_payload(10087, **kwargs)
        return self.put(url, data=payload)


class NutritionOrder(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_nutrition_order(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["NutritionOrder"]["get_nutrition_order"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_nutrition_order(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["NutritionOrder"]["search_nutrition_order"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class DeviceRequest(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_device_request(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceRequest"]["get_specific_device_request"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_device_request(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceRequest"]["search_device_request"]["path"],
            **kwargs
        )

        return self.get(url)


class DeviceUseStatement(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_external_devices(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceUseStatement"]["get_external_devices"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_implants(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceUseStatement"]["get_specific_implants"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_external_devices(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceUseStatement"]["search_external_devices"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_implants(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["DeviceUseStatement"]["search_implants"]["path"],
            **kwargs
        )

        return self.get(url)


class Provenance(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_provenance(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Workflow"]["Provenance"]["get_specific_provenance"]["path"],
            ID=ID,
        )

        return self.get(url)
