from medarch_engine.ehrbridge.ecw.client import ECWClient
from medarch_engine.ehrbridge.ecw.urls import ECW_URLS


class Organization(ECWClient):
    def __init__(self, customer_id, connection_id, source_json=None) -> None:
        super().__init__(customer_id, connection_id, source_json)

    def get_organization_by_id(self, organization_id):
        """
        Search for Organization by specific ID.
        GET [base]/Organization?_id=[id]

        Args:
            organization_id: Organization ID

        Returns:
            Organization resource for the specific id
        """
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Organization"]["get_organization"]["path"],
        )
        return self.get(url, params={"_id": organization_id})

    def get_organization_by_name(self, name):
        """
        Search for Organization by name.
        GET [base]/Organization?name=[name]

        Args:
            name: Organization name

        Returns:
            Organization resources matching the name
        """
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Organization"]["get_organization"]["path"],
        )
        return self.get(url, params={"name": name})

    def get_all_organizations(self):
        """
        Get all organizations.
        GET [base]/Organization

        Returns:
            All Organization resources
        """
        # Path doesn't include {practiceid}, it's already in base_url
        url = self.build_url(
            ECW_URLS["Organization"]["get_organization"]["path"],
        )
        return self.get(url)
