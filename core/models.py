from django.db import models
import uuid, random, string
from .constants import EHR_CHOICES,APP_TYPES,ENVIRONMENT_CHOICE,CONNECTION_STATUS
import json
from django.conf import settings
from django.core.validators import URLValidator
from .utils import generate_code_verifier, generate_code_challenge
# Create your models here.

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=False,editable=False,default=uuid.uuid4,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class EHRConnection(BaseModel):
    title = models.CharField(max_length=250)
    ehr_name = models.CharField(choices=EHR_CHOICES, max_length=120)
    app_type = models.CharField(choices=APP_TYPES, max_length=50)
    grant_type = models.CharField(
        max_length=25, editable=False, default="client_credentials"
    )
    client_id = models.CharField(max_length=250, blank=True, null=True)
    client_secret = models.CharField(max_length=250, blank=True, null=True)
    redirect_uri = models.CharField(max_length=255, blank=True, null=True)
    auth_code_uri = models.CharField(max_length=255,blank=True,null=True)
    auth_code = models.CharField(max_length=255,blank=True,null=True)
    scope = models.TextField(blank=True, null=True)
    audiance = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    base_url = models.CharField(max_length=250, blank=True, null=True)
    token_url = models.CharField(max_length=250, blank=True, null=True)
    authorize_url = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    access_token_generated_at = models.DateTimeField(blank=True, null=True)
    refresh_token_generated_at = models.DateTimeField(null=True,blank=True)
    practice_id = models.CharField(max_length=100, blank=True, null=True)
    enterprise_id = models.CharField(max_length=100, blank=True, null=True)
    site_id = models.CharField(max_length=255, blank=True, null=True)
    session_id = models.TextField(blank=True, null=True, editable=False)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)

    client_assertion = models.CharField(max_length=2084,blank=True,null=True)
    ehr_environment = models.CharField(
        choices=ENVIRONMENT_CHOICE, max_length=50, null=True, blank=True
    )
    connection_status = models.CharField(
        choices=CONNECTION_STATUS, max_length=50, blank=True, default="active"
    )
    office_key = models.CharField(max_length=8, blank=True, null=True)
    status_url = models.CharField(max_length=100, blank=True, null=True)
    export_url = models.CharField(max_length=100, blank=True, null=True)
    jobId = models.CharField(max_length=6, blank=True, null=True)
    department_id = models.CharField(max_length=5,blank=True,null=True)
    customer_auth_url = models.TextField(blank=True,null=True,validators=[URLValidator()])
    code_verifier = models.CharField(
        max_length=255, blank=True, null=True, editable=False
    )
    code_challenge = models.CharField(
        max_length=255, blank=True, null=True, editable=False
    )
    org_redirect_uri = models.URLField(max_length=255, blank=True, null=True)
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # Generate code_verifier and code_challenge on creation
        # If they're missing on updates (shouldn't happen, but safety check), regenerate them
        if self._state.adding:
            if not self.code_verifier:
                self.code_verifier = generate_code_verifier()
            if not self.code_challenge and self.code_verifier:
                self.code_challenge = generate_code_challenge(self.code_verifier)
        else:
            # On updates, preserve existing values but regenerate if somehow missing
            if not self.code_verifier:
                self.code_verifier = generate_code_verifier()
            if not self.code_challenge and self.code_verifier:
                self.code_challenge = generate_code_challenge(self.code_verifier)

        data = json.loads(settings.EHR_URLS)
        selected_ehr_object = data[self.ehr_name.upper()]
        self.redirect_uri = selected_ehr_object.get("redirect_uri")
        self.organization_redirect_uri = selected_ehr_object.get(
            "organization_redirect_uri"
        )
        if self.ehr_name=="athena":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"].format(practiceId=self.practice_id)
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
            else:
                self.base_url = selected_ehr_object["base_url_prod"].format(practiceId=self.practice_id)
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
        elif self.ehr_name=="PracticeFusion":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"]
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
            else:
                self.base_url = selected_ehr_object["base_url_prod"]
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
        elif self.ehr_name=="eclinicalworks":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"].format(practiceid=self.practice_id)
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
                self.audiance = self.base_url
                self.state = (
                    f"{self.uuid},{self.ehr_name.lower()},{self.app_type.lower()}"
                )
                self.redirect_uri = selected_ehr_object.get("redirect_uri")
                self.customer_auth_url = (
                    "{}?response_type=code&client_id={}&redirect_uri={}"
                    "&scope={}&code_challenge={}&code_challenge_method=S256&aud={}&state={}".format(
                        self.authorize_url,
                        self.client_id,
                        self.redirect_uri,
                        self.scope,
                        self.code_challenge,
                        self.audiance,
                        self.state,
                    )
                )
            else:
                self.base_url = selected_ehr_object["base_url_prod"].format(practiceid=self.practice_id)
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
                self.audiance = self.base_url
                self.state = (
                    f"{self.uuid},{self.ehr_name.lower()},{self.app_type.lower()}"
                )
                self.redirect_uri = selected_ehr_object.get("redirect_uri")
                self.customer_auth_url = (
                    "{}?response_type=code&client_id={}&redirect_uri={}"
                    "&scope={}&code_challenge={}&code_challenge_method=S256&aud={}&state={}".format(
                        self.authorize_url,
                        self.client_id,
                        self.redirect_uri,
                        self.scope,
                        self.code_challenge,
                        self.audiance,
                        self.state,
                    )
                )
        elif self.ehr_name=="epic":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"]
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
            else:
                self.base_url = selected_ehr_object["base_url_prod"]
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
        elif self.ehr_name=="NextGen":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"]
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
            else:
                self.base_url = selected_ehr_object["base_url_prod"]
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
        elif self.ehr_name=="advance_md":
            if self.ehr_environment == "sandbox":
                self.base_url = selected_ehr_object["base_url_test"]
                self.token_url = selected_ehr_object["auth_url_test"]
                self.authorize_url = selected_ehr_object["auth_code_test"]
            else:
                self.base_url = selected_ehr_object["base_url_prod"]
                self.token_url = selected_ehr_object["auth_url_prod"]
                self.authorize_url = selected_ehr_object["auth_code_prod"]
        if self.app_type == "provider":
            self.grant_type = "authorization_code"
        else:
            self.grant_type = "client_credentials"

        super().save(*args, **kwargs)

class WebHook(BaseModel):

    def code_generate():
        while 1:
            prom_code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(25))

            return prom_code

    name = models.CharField(max_length=120)
    webhook_url = models.CharField(max_length=150, blank=True, null=True)
    connection = models.ForeignKey(EHRConnection, on_delete=models.CASCADE)
    token = models.CharField(max_length=250, blank=True, null=True, default = code_generate)
    is_verified = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=False, null=False)
    method = models.CharField(max_length=5, choices=(("get", "GET"), ("post", "POST")), blank=True, null=True)

    class Meta:
        db_table = 'ehr_webhook'

    def __str__(self) -> str:
        return f'{self.name}:- {self.uuid}'
