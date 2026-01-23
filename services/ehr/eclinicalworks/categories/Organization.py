from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS


class Organization(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_organization(self, organization_id=None, name=None, org_type=None, address=None):
        """
        Fetch organization(s) from eClinicalWorks FHIR API.

        Args:
            organization_id: Organization ID to filter by
            name: Organization name to filter by
            org_type: Organization type to filter by
            address: Address to filter by
        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            ECW_URLS["Organization"]["get_organization"]["path"],
        )
        params = {}

        if organization_id:
            params["_id"] = organization_id
        if name:
            params["name"] = name
        if org_type:
            params["type"] = org_type
        if address:
            params["address"] = address

        return self.get(url, content_type="application/json+fhir", params=params)
