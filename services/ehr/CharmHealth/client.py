import json
from datetime import timedelta

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth

from ecaremd.ehr_integrations.ehr_services.client import ClientBase


class CHFHIRClient(ClientBase):
    """
    A client to call API's for GET, POST, PUT, PATCH, DELETE methods for given URL & Payload.
    """

    def __init__(self, customer_id, tenant_name=None, source_json=None):
        super().__init__()

        self.customer, self.ehr = super().get_customer_obj(
            customer_id, tenant_name, source_json
        )
        self.base_url = self.ehr.base_url
        self.auth_url = self.ehr.token_url
        self.auth_token = None
        self.auth_token_type = None
        self.auth_token_expires_in = None
        self.is_token_expired = False
        self.scope = self.ehr.scope
        self.headers = {}
        self.payload = {}
        self.app_type = self.ehr.app_type
        self.client_id = self.ehr.client_id
        self.client_secret_key = self.ehr.client_secret
        self.grant_type = self.ehr.grant_type
        self.redirect_url = self.ehr.redirect_uri
        self.practice_id = self.ehr.practice_id
        self.redirect_url = self.ehr.redirect_uri

    def authenticate(self):
        """
        Get Auth Token from CharmHealth API.
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
        time_difference = timezone.now() - timedelta(minutes=55)
        if self.ehr.app_type == "provider":
            ehr_provider = (
                self.customer.ehr_provider
                if not self.customer.ehr_provider.multi_connection
                else self.customer.ehr_provider.creds.filter(
                    provider_group=self.ehr.provider_group, ehr_name=self.ehr.ehr_name
                ).first()
            )

            token = ehr_provider.access_token
            if token:
                if ehr_provider.access_token_generated_at <= time_difference:
                    payload = {
                        "grant_type": "refresh_token",
                        "refresh_token": ehr_provider.refresh_token,
                        "client_secret": self.client_secret_key,
                        "client_id": self.client_id,
                        "redirect_uri": self.redirect_url,
                    }
                    renew_token = requests.request(
                        "POST",
                        url=self.auth_url,
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        data=payload,
                        auth=HTTPBasicAuth(self.client_id, self.client_secret_key),
                    )
                    if renew_token.status_code == 200:
                        ehr_provider.access_token = renew_token.json().get(
                            "access_token"
                        )
                        ehr_provider.refresh_token = self.refresh_token

                        ehr_provider.access_token_generated_at = timezone.now()
                        ehr_provider.save()
            return token if token else False

    def build_url(self, rawurl: str, **kwargs) -> str:
        url = self.base_url + rawurl.format(**kwargs)
        return url

    def build_payload(self, **kwargs) -> dict:
        payload = kwargs
        return payload

    def bulk_get(
        self, url: str = "", content_type: str = "application/json", params: dict = {}
    ) -> str:
        """
        Get data from CharmHealth API.
        """
        self.headers["Content-Type"] = content_type
        self.headers["Prefer"] = "respond-async"
        self.headers["Accept"] = "application/fhir+json"

        response = requests.request("GET", url, headers=self.headers, params=params)
        if response.status_code == 202:
            response_data = response.headers
        else:
            response_data = response.json()

        return response_data, response.status_code

    def get(
        self, url: str = "", content_type: str = "application/json", params: dict = {}
    ) -> str:
        """
        Get data from CharmHealth API.
        """
        self.headers["Content-Type"] = content_type
        self.headers["api_key"] = self.practice_id
        response = requests.request("GET", url, headers=self.headers, params=params)
        if response.status_code == 200:
            if response.headers.get("Content-Type") == "application/xml":
                return response.content, response.status_code
            return response.json(), response.status_code
        return response, response.status_code

    def post(
        self,
        url: str = "",
        content_type: str = "application/fhir+json",
        data: dict = None,
    ):
        self.headers["Content-Type"] = content_type
        response = requests.request(
            "POST", url, headers=self.headers, data=json.dumps(data)
        )

        return response.json(), response.status_code
