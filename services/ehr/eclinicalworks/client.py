import logging
from datetime import timedelta

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth
from services.ehr.client import SuperClient

logger = logging.getLogger(__name__)

# Default timeout for all HTTP requests (connect timeout, read timeout)
REQUEST_TIMEOUT = (10, 30)


class ECWClient(SuperClient):
    """
    A client to call API's for GET, POST, PUT, PATCH, DELETE methods for given URL & Payload.
    """

    def __init__(self, connection_obj):
        super().__init__()
        self.ehr = connection_obj
        self.base_url = self.ehr.base_url
        self.auth_url = self.ehr.token_url
        self.auth_token = None
        self.scope = self.ehr.scope
        self.headers = {}
        self.payload = {}
        self.ecw_client_id = self.ehr.client_id
        self.ecw_client_secret_key = self.ehr.client_secret
        self.ecw_grant_type = self.ehr.grant_type
        self.ecw_api_scope = self.ehr.scope

    def authenticate(self):
        """
        Get Auth Token from eClinicalWorks API.
        Returns 200 on success, None on failure.
        """
        token = self.read_token()
        if token:
            self.auth_token = token
            self.headers["Authorization"] = "Bearer " + self.auth_token
            return 200
        logger.warning("Failed to obtain auth token for connection %s", self.ehr.uuid)
        return None

    def persist_token(self):
        """
        Persist token to database.
        """
        self.ehr.access_token = self.auth_token
        self.ehr.access_token_generated_at = timezone.now()
        self.ehr.save(update_fields=['access_token', 'access_token_generated_at'])

    def read_token(self):
        """
        Read stored token from database, refreshing if expired.
        Returns the valid token or None if unavailable.
        """
        if not self.ehr.access_token:
            return None

        # Check if token is about to expire (4.8 minute threshold for 5-min tokens)
        if self.ehr.access_token_generated_at:
            expiry_threshold = timezone.now() - timedelta(minutes=4.8)
            if self.ehr.access_token_generated_at <= expiry_threshold:
                # Token expired or about to expire - refresh it
                if not self._refresh_token():
                    logger.error("Token refresh failed for connection %s", self.ehr.uuid)
                    return None

        return self.ehr.access_token

    def _refresh_token(self):
        """
        Refresh the access token.
        Returns True on success, False on failure.
        """
        if not self.ehr.refresh_token:
            logger.warning("No refresh token available for connection %s", self.ehr.uuid)
            return False

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.ehr.refresh_token,
            "scope": self.ehr.scope,
        }
        try:
            response = requests.post(
                url=self.auth_url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=payload,
                auth=HTTPBasicAuth(self.ecw_client_id, self.ecw_client_secret_key),
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                token_data = response.json()
                self.ehr.access_token = token_data.get("access_token")
                self.ehr.refresh_token = token_data.get("refresh_token")
                self.ehr.access_token_generated_at = timezone.now()
                self.ehr.save(update_fields=['access_token', 'refresh_token', 'access_token_generated_at'])
                logger.debug("Token refreshed successfully for connection %s", self.ehr.uuid)
                return True
            else:
                logger.error(
                    "Token refresh failed with status %s for connection %s",
                    response.status_code, self.ehr.uuid
                )
                return False
        except requests.exceptions.Timeout:
            logger.error("Token refresh timed out for connection %s", self.ehr.uuid)
            return False
        except requests.exceptions.RequestException as e:
            logger.exception("Token refresh request failed for connection %s: %s", self.ehr.uuid, e)
            return False
        except ValueError as e:
            logger.exception("Token refresh JSON decode failed for connection %s: %s", self.ehr.uuid, e)
            return False

    def build_url(self, rawurl: str, **kwargs) -> str:
        url = self.base_url + rawurl.format(**kwargs)
        return url

    def build_payload(self, **kwargs) -> dict:
        payload = kwargs
        return payload

    def get_ehr_data(self, ehr_element):
        """
        Stub method for logging/storing EHR API interactions.
        Can be implemented later if needed for logging or audit purposes.
        """
        # Log API calls at debug level for troubleshooting
        logger.debug(
            "EHR API Call: %s %s -> %s",
            ehr_element.get("ehr_method"),
            ehr_element.get("ehr_api"),
            ehr_element.get("ehr_status_code")
        )

    def _safe_json_response(self, response):
        """
        Safely parse JSON response, returning error dict if parsing fails.
        """
        try:
            return response.json()
        except ValueError:
            return {"detail": response.text or "Empty response", "raw_status": response.status_code}

    def get(
        self, url: str = "", content_type: str = "application/json", params: dict = None
    ) -> tuple:
        """
        Get data from eClinicalWorks API.
        Returns tuple of (response_data, status_code).
        """
        if params is None:
            params = {}

        self.headers["Content-Type"] = content_type

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout:
            logger.error("GET request timed out: %s", url)
            return {"detail": "Request timed out"}, 504
        except requests.exceptions.RequestException as e:
            logger.exception("GET request failed: %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

        response_data = self._safe_json_response(response)

        ehr_element = {
            "ehr_api": url,
            "ehr_body": params,
            "ehr_response": response_data,
            "ehr_method": "GET",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)

        return response_data, response.status_code

    def post(
        self, url: str = "", content_type: str = "application/json", data: dict = None
    ) -> tuple:
        """
        Post data to eClinicalWorks API.
        Returns tuple of (response_data, status_code).
        """
        self.headers["Content-Type"] = content_type

        try:
            # Use json parameter for JSON content type, data for form-encoded
            if content_type == "application/json" and data:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=REQUEST_TIMEOUT
                )
            else:
                response = requests.post(
                    url,
                    headers=self.headers,
                    data=data,
                    timeout=REQUEST_TIMEOUT
                )
        except requests.exceptions.Timeout:
            logger.error("POST request timed out: %s", url)
            return {"detail": "Request timed out"}, 504
        except requests.exceptions.RequestException as e:
            logger.exception("POST request failed: %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

        response_data = self._safe_json_response(response)

        ehr_element = {
            "ehr_api": url,
            "ehr_body": data,
            "ehr_response": response_data,
            "ehr_method": "POST",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)

        return response_data, response.status_code

    def put(
        self, url: str = "", content_type: str = "application/json", data: dict = None
    ) -> tuple:
        """
        Put data to eClinicalWorks API.
        Returns tuple of (response_data, status_code).
        """
        self.headers["Content-Type"] = content_type

        try:
            response = requests.put(
                url,
                headers=self.headers,
                data=data,
                timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout:
            logger.error("PUT request timed out: %s", url)
            return {"detail": "Request timed out"}, 504
        except requests.exceptions.RequestException as e:
            logger.exception("PUT request failed: %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

        response_data = self._safe_json_response(response)

        ehr_element = {
            "ehr_api": url,
            "ehr_body": data,
            "ehr_response": response_data,
            "ehr_method": "PUT",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)

        return response_data, response.status_code

    def delete(
        self, url: str = "", content_type: str = "application/json", params: dict = None
    ) -> tuple:
        """
        Delete data from eClinicalWorks API.
        Returns tuple of (response_data, status_code).
        """
        self.headers["Content-Type"] = content_type

        try:
            response = requests.delete(
                url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout:
            logger.error("DELETE request timed out: %s", url)
            return {"detail": "Request timed out"}, 504
        except requests.exceptions.RequestException as e:
            logger.exception("DELETE request failed: %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

        response_data = self._safe_json_response(response)

        ehr_element = {
            "ehr_api": url,
            "ehr_body": params,
            "ehr_response": response_data,
            "ehr_method": "DELETE",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)

        return response_data, response.status_code
