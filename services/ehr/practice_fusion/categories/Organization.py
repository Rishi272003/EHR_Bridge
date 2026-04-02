from services.ehr.practice_fusion.client import PracticeFusionClient
from services.ehr.practice_fusion.urls import PRACTICE_FUSION_URLS


class Organization(PracticeFusionClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_organization(self, organization_id=None, name=None, org_type=None, identifier=None):
        """
        Fetch organization(s) from Practice Fusion FHIR API.

        Args:
            organization_id: Organization ID to filter by
            name: Organization name to filter by
            org_type: Organization type to filter by
            identifier: Organization identifier to filter by
        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Organization"]["get_organization"]["path"],
        )
        params = {}

        if organization_id:
            params["_id"] = organization_id
        if name:
            params["name"] = name
        if org_type:
            params["type"] = org_type
        if identifier:
            params["identifier"] = identifier

        return self.get(url, params=params)
