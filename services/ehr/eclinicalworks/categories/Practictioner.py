from medarch_engine.ehrbridge.ecw.client import ECWClient
from medarch_engine.ehrbridge.ecw.urls import ECW_URLS


class Practitioner(ECWClient):
    def __init__(self, customer_id, connection_id, source_json=None) -> None:
        super().__init__(customer_id, connection_id, source_json)
        # Extract practice_id from base_url or connection
        self._practice_id = self.ehr.practice_id
        if not self._practice_id:
            # Extract from base_url if practice_id is not set
            base_url = self.base_url
            if base_url and "/fhir/r4/" in base_url:
                parts = base_url.split("/fhir/r4/")
                if len(parts) > 1:
                    self._practice_id = (
                        parts[1].split("/")[0] if "/" in parts[1] else parts[1]
                    )

    def get_practitioner_by_id(self, practitioner_id):
        """
        Search for Practitioner by specific ID.
        GET [base]/{practiceid}/Practitioner?_id=[id]

        Args:
            practitioner_id: Practitioner ID

        Returns:
            Practitioner resource for the specific id
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["get_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        return self.get(url, params={"_id": practitioner_id})

    def search_practitioner_by_name(self, name):
        """
        Search for Practitioner by name.
        GET [base]/{practiceid}/Practitioner?name=[name]

        Args:
            name: Practitioner name

        Returns:
            Practitioner resources matching the name
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        return self.get(url, params={"name": name})

    def search_practitioner_by_identifier(self, identifier_value, identifier_type=None):
        """
        Search for Practitioner by identifier.
        GET [base]/{practiceid}/Practitioner?identifier=[system|code]

        Args:
            identifier_value: Identifier value
            identifier_type: Identifier type/system (optional)

        Returns:
            Practitioner resources matching the identifier
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        params = {}
        if identifier_type:
            params["identifier"] = f"{identifier_type}|{identifier_value}"
        else:
            params["identifier"] = identifier_value
        return self.get(url, params=params)

    def search_practitioner_by_gender(self, gender):
        """
        Search for Practitioner by gender.
        GET [base]/{practiceid}/Practitioner?gender=[gender]

        Args:
            gender: Gender code (male, female, other, unknown)

        Returns:
            Practitioner resources matching the gender
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        return self.get(url, params={"gender": gender})

    def search_practitioner_by_organization(self, organization_id):
        """
        Search for Practitioner by organization.
        GET [base]/{practiceid}/Practitioner?organization=[reference]

        Args:
            organization_id: Organization ID

        Returns:
            Practitioner resources associated with the organization
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        # Remove 'Organization/' prefix if present
        if organization_id and organization_id.startswith("Organization/"):
            organization_id = organization_id.replace("Organization/", "")
        return self.get(url, params={"organization": organization_id})

    def search_practitioner_by_location(self, location_id):
        """
        Search for Practitioner by location.
        GET [base]/{practiceid}/Practitioner?location=[reference]

        Args:
            location_id: Location ID

        Returns:
            Practitioner resources associated with the location
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        # Remove 'Location/' prefix if present
        if location_id and location_id.startswith("Location/"):
            location_id = location_id.replace("Location/", "")
        return self.get(url, params={"location": location_id})

    def search_practitioners(self, **kwargs):
        """
        Generic search method that supports all search parameters.
        This method can handle any combination of search parameters.

        Args:
            **kwargs: Search parameters including:
                - _id: Practitioner ID
                - name: Practitioner name
                - identifier: Identifier value or system|value
                - gender: Gender code
                - organization: Organization ID
                - location: Location ID

        Returns:
            Practitioner resources matching the search criteria
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )

        params = {}

        # Handle _id parameter
        if kwargs.get("_id"):
            params["_id"] = kwargs.get("_id")

        # Handle name parameter
        if kwargs.get("name"):
            params["name"] = kwargs.get("name")

        # Handle identifier parameter
        if kwargs.get("identifier"):
            params["identifier"] = kwargs.get("identifier")

        # Handle gender parameter
        if kwargs.get("gender"):
            params["gender"] = kwargs.get("gender")

        # Handle organization parameter
        if kwargs.get("organization"):
            org_id = kwargs.get("organization")
            if org_id and org_id.startswith("Organization/"):
                org_id = org_id.replace("Organization/", "")
            params["organization"] = org_id

        # Handle location parameter
        if kwargs.get("location"):
            loc_id = kwargs.get("location")
            if loc_id and loc_id.startswith("Location/"):
                loc_id = loc_id.replace("Location/", "")
            params["location"] = loc_id

        return self.get(url, params=params)

    def get_all_providers(self):
        """
        Get all practitioners/providers.
        GET [base]/{practiceid}/Practitioner

        Returns:
            All Practitioner resources
        """
        url = self.build_url(
            ECW_URLS["Practitioner"]["search_practitioner"]["path"],
            practiceid=self._practice_id,
        )
        return self.get(url)
