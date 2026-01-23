from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS


class Practitioner(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_practitioners(self, practitioner_id=None, name=None, identifier=None):
        """
        Fetch practitioner(s) from eClinicalWorks FHIR API.

        Search parameters:
        - id: GET [base]/Practitioner?_id=[id] - Returns specific practitioner
        - name: GET [base]/Practitioner?name=[string] - Search by name
        - identifier: GET [base]/Practitioner?identifier={system|}[code] - Search by identifier (NPI, DEA, etc.)
        - no params: GET [base]/Practitioner - Returns all practitioners

        Args:
            practitioner_id: Practitioner ID to filter by
            name: Practitioner name to search (matches start of any part of name)
            identifier: Identifier string (e.g., "http://hl7.org/fhir/sid/us-npi|1234567890")

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(ECW_URLS["Practitioner"]["get_practitioner"]["path"])
        params = {}

        if practitioner_id:
            params["_id"] = practitioner_id
        if name:
            params["name"] = name
        if identifier:
            params["identifier"] = identifier

        return self.get(url, content_type="application/json+fhir", params=params)

    def get_practitioner_by_id(self, practitioner_id):
        """
        Fetch a specific practitioner by ID using direct resource URL.

        GET [base]/Practitioner/[id]

        Args:
            practitioner_id: The FHIR resource ID

        Returns:
            tuple: (response_json, status_code)
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["get_practitioner_by_id"]["path"],
            practitioner_id=practitioner_id
        )
        return self.get(url, content_type="application/json+fhir", params={})
