import time
import uuid
from datetime import timedelta

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth
from services.ehr.client import SuperClient
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
        """
        if self.read_token():
            self.auth_token = self.read_token()
            self.headers["Authorization"] = "Bearer " + self.auth_token
            return 200

    def persist_token(self):
        """
        Persist token to database.
        """
        self.ehr.access_token = self.auth_token
        self.ehr.access_token_generated_at = timezone.now()
        self.ehr.save()

    def read_token(self):
        """
        Read stored token from database.
        """
        time_difference = timezone.now() - timedelta(minutes=4.8)
        token = self.ehr.access_token
        if token:
            if self.ehr.access_token_generated_at <= time_difference:
                payload = {
                    "grant_type": "refresh_token",
                    "refresh_token": self.ehr.refresh_token,
                    "scope": self.ehr.scope,
                }
                renew_token = requests.request(
                    "POST",
                    url=self.auth_url,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data=payload,
                    auth=HTTPBasicAuth(self.ecw_client_id, self.ecw_client_secret_key),
                )
                if renew_token.status_code == 200:
                    self.ehr.access_token = renew_token.json().get("access_token")
                    self.ehr.refresh_token = renew_token.json().get("refresh_token")

                    self.ehr.access_token_generated_at = timezone.now()
                    self.ehr.save()
            return token if token else False

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
        # TODO: Implement EHR data logging if needed
        pass

    def get(
        self, url: str = "", content_type: str = "application/json", params: dict = {}
    ) -> str:
        """
        Get data from Athena Health API.
        """
        self.headers["Content-Type"] = content_type
        print("url", url)
        print("headers", self.headers)
        print("params", params)
        response = requests.request("GET", url, headers=self.headers, params=params)
        print("response", response.json())
        ehr_element = {
            "ehr_api": url,
            "ehr_body": params,
            "ehr_response": response.json(),
            "ehr_method": "GET",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)
        return response.json(), response.status_code

    def post(
        self, url: str = "", content_type: str = "application/json", data: dict = None
    ):

        self.headers["Content-Type"] = content_type

        # Use json parameter for JSON content type, data for form-encoded
        if content_type == "application/json" and data:
            response = requests.request("POST", url, headers=self.headers, json=data)
        else:
            response = requests.request("POST", url, headers=self.headers, data=data)

        ehr_element = {
            "ehr_api": url,
            "ehr_body": data,
            "ehr_response": response.json() if response.content else {},
            "ehr_method": "POST",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)

        try:
            return response.json(), response.status_code
        except ValueError:
            return {"detail": response.text}, response.status_code

    def put(
        self, url: str = "", content_type: str = "application/json", data: dict = None
    ):

        self.headers["Content-Type"] = content_type
        response = requests.request("PUT", url, headers=self.headers, data=data)
        ehr_element = {
            "ehr_api": url,
            "ehr_body": data,
            "ehr_response": response.json(),
            "ehr_method": "PUT",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)
        return response.json(), response.status_code

    def delete(
        self, url: str = "", content_type: str = "application/json", params: list = None
    ):

        self.headers["Content-Type"] = content_type
        response = requests.request("DELETE", url, headers=self.headers, params=params)
        ehr_element = {
            "ehr_api": url,
            "ehr_body": params,
            "ehr_response": response.json(),
            "ehr_method": "DELETE",
            "ehr_status_code": response.status_code,
        }
        self.get_ehr_data(ehr_element)
        return response.json(), response.status_code
