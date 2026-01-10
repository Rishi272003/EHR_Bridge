import json
from datetime import timedelta

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth

from ecaremd.ehr_integrations.ehr_services.client import ClientBase


class EpicFHIRClient(ClientBase):
    """
    A client to call API's for GET, POST, PUT, PATCH, DELETE methods for given URL & Payload.
    """

    def __init__(self, customer_id, tenant_name=None, source_json=None):
        super().__init__()

        self.customer, self.ehr = super().get_customer_obj(
            customer_id, tenant_name, source_json
        )

        # try:
        #     self.customer = Practice.objects.get(uuid=customer_id)
        # except Practice.DoesNotExist:
        #     if self.ehr.app_type == "provider":
        #         self.customer = Provider.objects.get(uuid=customer_id)

        self.base_url = self.ehr.base_url
        self.auth_url = self.ehr.token_url
        self.auth_token = None
        self.auth_token_type = None
        self.auth_token_expires_in = None
        self.is_token_expired = False
        self.scope = None
        self.app_type = self.ehr.app_type
        self.headers = {}
        self.payload = {}
        self.epic_client_id = self.ehr.client_id
        self.epic_client_secret_key = self.ehr.client_secret
        self.epic_grant_type = self.ehr.grant_type
        self.epic_api_scope = self.ehr.scope
        self.redirect_url = self.ehr.redirect_uri

    def authenticate(self):
        """
        Get Auth Token from EPIC EHR API.
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

    def build_payload(self, **kwargs) -> dict:
        payload = kwargs
        return json.dumps(payload)

    def read_token(self):
        """
        Read stored token from database.
        """
        if self.ehr.app_type in ("provider", "patient"):
            ehr_provider = (
                self.customer.ehr_provider
                if not self.customer.ehr_provider.multi_connection
                else self.customer.ehr_provider.creds.filter(
                    provider_group_id=self.ehr.provider_group,
                    ehr_name=self.ehr.ehr_name,
                ).first()
            )

            token = ehr_provider.access_token
            if token:
                time_difference = timezone.now() - timedelta(minutes=55)
                payload = {
                    "grant_type": "refresh_token",
                    "refresh_token": ehr_provider.refresh_token,
                }
                if ehr_provider.access_token_generated_at <= time_difference:
                    renew_token = requests.request(
                        "POST",
                        url=self.auth_url,
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        data=payload,
                        auth=HTTPBasicAuth(
                            self.epic_client_id, self.epic_client_secret_key
                        ),
                    )
                    if renew_token.status_code == 200:
                        ehr_provider.access_token = renew_token.json().get(
                            "access_token"
                        )
                        ehr_provider.access_token_generated_at = timezone.now()
                        ehr_provider.save()
            return token if token else False

    def build_url(self, rawurl: str, **kwargs) -> str:
        url = self.base_url + rawurl.format(**kwargs)
        return url

    def get(self, url: str = "", params: list = None) -> str:
        """
        Get data from EPIC Health API.
        """
        self.headers["Accept"] = "application/json"
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        response = requests.request("GET", url, headers=self.headers, params=params)
        return response.json(), response.status_code

    def post(
        self, url: str = "", content_type: str = "application/json", data: dict = None
    ):
        self.headers["Content-Type"] = content_type
        self.headers["Accept"] = "application/json"
        response = requests.request("POST", url, headers=self.headers, data=data)

        if response.status_code != 201:
            return response.json(), response.status_code
        return {
            "status": True,
            "Location": response.headers.get("Location"),
        }, response.status_code
