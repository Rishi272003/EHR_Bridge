from services.ehr.practice_fusion.client import PracticeFusionClient
from services.ehr.practice_fusion.urls import PRACTICE_FUSION_URLS


class Practitioner(PracticeFusionClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_practitioner_by_id(self, practitioner_id):
        """
        Get Practitioner by specific ID.
        GET [base]/Practitioner/{practitioner_id}

        Args:
            practitioner_id: Practitioner ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Practitioner"]["get_practitioner_by_id"]["path"],
            practitioner_id=practitioner_id
        )
        return self.get(url)

    def search_practitioners(self, identifier=None, given=None, name=None):
        """
        Search for Practitioners that meet supplied query parameters.
        GET [base]/Practitioner?identifier=[id]&given=[firstname]&name=[name]

        Args:
            identifier: Practitioner identifier (can be NPI, internal ID, etc.)
            given: First name (given name)
            name: Full name

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            PRACTICE_FUSION_URLS["Practitioner"]["get_practitioner"]["path"]
        )
        params = {}

        if identifier:
            params["identifier"] = identifier
        if given:
            params["given"] = given
        if name:
            params["name"] = name

        return self.get(url, params=params)
