import logging
from datetime import timedelta

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth
from services.ehr.client import SuperClient

logger = logging.getLogger(__name__)

# Default timeout for all HTTP requests (connect timeout, read timeout)
REQUEST_TIMEOUT = (10, 30)


class PracticeFusionClient(SuperClient):
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
        self.client_id = self.ehr.client_id
        self.client_secret = self.ehr.client_secret
        self.grant_type = self.ehr.grant_type
        self.api_scope = self.ehr.scope

    def authenticate(self):
        """
        Get Auth Token from Practice Fusion API.
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
        if self.auth_token:
            self.ehr.access_token = self.auth_token
            self.ehr.token_expires_at = timezone.now() + timedelta(seconds=3600)
            self.ehr.save(update_fields=["access_token", "token_expires_at"])

    def read_token(self):
        """
        Read token from database.
        """
        if self.ehr.access_token and self.ehr.token_expires_at:
            if timezone.now() < self.ehr.token_expires_at:
                return self.ehr.access_token
        return None

    def refresh_token(self):
        """
        Refresh auth token.
        """
        # Implement token refresh logic here
        pass

    def build_url(self, path, **kwargs):
        """
        Build full URL from base URL and path.
        """
        # Remove leading slash from path if present
        path = path.lstrip("/")
        # Format path with any provided kwargs
        formatted_path = path.format(**kwargs)
        # Combine base_url and formatted_path
        return f"{self.base_url}/{formatted_path}"

    def build_headers(self):
        """
        Build headers for request.
        """
        if self.auth_token:
            self.headers["Authorization"] = "Bearer " + self.auth_token
        return self.headers

    def build_payload(self, **kwargs):
        """
        Build payload for request.
        """
        return kwargs

    def get(self, url, content_type="application/json", params=None):
        """
        Make GET request.
        Returns tuple (response_json, status_code).
        """
        self.build_headers()
        self.headers["Content-Type"] = content_type
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                try:
                    error_data = response.json()
                except (ValueError, AttributeError):
                    error_data = {"detail": "Something went wrong", "error": response.text}
                return error_data, response.status_code
            return response.json(), response.status_code
        except Exception as e:
            logger.exception("GET request failed for URL %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

    def post(self, url, data=None, content_type="application/json"):
        """
        Make POST request.
        Returns tuple (response_json, status_code).
        """
        self.build_headers()
        self.headers["Content-Type"] = content_type
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code not in [200, 201]:
                try:
                    error_data = response.json()
                except (ValueError, AttributeError):
                    error_data = {"detail": "Something went wrong", "error": response.text}
                return error_data, response.status_code
            return response.json(), response.status_code
        except Exception as e:
            logger.exception("POST request failed for URL %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

    def put(self, url, data=None, content_type="application/json"):
        """
        Make PUT request.
        Returns tuple (response_json, status_code).
        """
        self.build_headers()
        self.headers["Content-Type"] = content_type
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code not in [200, 201, 204]:
                try:
                    error_data = response.json()
                except (ValueError, AttributeError):
                    error_data = {"detail": "Something went wrong", "error": response.text}
                return error_data, response.status_code
            try:
                return response.json(), response.status_code
            except (ValueError, AttributeError):
                return {"detail": "Success"}, response.status_code
        except Exception as e:
            logger.exception("PUT request failed for URL %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

    def patch(self, url, data=None, content_type="application/json"):
        """
        Make PATCH request.
        Returns tuple (response_json, status_code).
        """
        self.build_headers()
        self.headers["Content-Type"] = content_type
        try:
            response = requests.patch(
                url,
                headers=self.headers,
                json=data,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code not in [200, 201, 204]:
                try:
                    error_data = response.json()
                except (ValueError, AttributeError):
                    error_data = {"detail": "Something went wrong", "error": response.text}
                return error_data, response.status_code
            try:
                return response.json(), response.status_code
            except (ValueError, AttributeError):
                return {"detail": "Success"}, response.status_code
        except Exception as e:
            logger.exception("PATCH request failed for URL %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500

    def delete(self, url, content_type="application/json"):
        """
        Make DELETE request.
        Returns tuple (response_json, status_code).
        """
        self.build_headers()
        self.headers["Content-Type"] = content_type
        try:
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code not in [200, 201, 204]:
                try:
                    error_data = response.json()
                except (ValueError, AttributeError):
                    error_data = {"detail": "Something went wrong", "error": response.text}
                return error_data, response.status_code
            try:
                return response.json(), response.status_code
            except (ValueError, AttributeError):
                return {"detail": "Success"}, response.status_code
        except Exception as e:
            logger.exception("DELETE request failed for URL %s", url)
            return {"detail": f"Request failed: {str(e)}"}, 500
