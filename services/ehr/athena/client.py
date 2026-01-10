from typing_extensions import runtime
import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.utils import timezone
from services.ehr.client  import SuperClient
from rest_framework.response import Response
from rest_framework import status

class AthenaHealthClient(SuperClient):
    def __init__(self,connection_obj):
        self.connection_obj = connection_obj
        self.base_url = self.connection_obj.base_url
        self.practice_id = self.connection_obj.practice_id
        self.headers = {"Content-type":"application/x-www-form-urlencoded"}

    def get(self,url:str="",content_type: str = "application/json",payload:dict={}):
        self.headers["Content-Type"]=content_type
        response = requests.request("GET",params=payload,url=url,headers=self.headers)
        print("url till here>>>",url)
        print("payload till here>>>",payload)
        print("headers till here>>>",self.headers)
        print("response status code till here>>>",response.json())

        # Always return a tuple (data, status_code) for consistency
        if response.status_code != 200:
            try:
                error_data = response.json()
            except (ValueError, AttributeError):
                error_data = {"detail": "Something went wrong", "error": response.text}
            return error_data, response.status_code
        try:
            return response.json(), response.status_code
        except (ValueError, AttributeError):
            # If response is not JSON, return text
            return {"detail": response.text}, response.status_code
    def build_url(self,url,**kwargs):
        full_url = self.base_url+"/"+url.format(**kwargs)
        return full_url

    def authenticate(self):
        if self.get_token():
            self.headers["Authorization"]="Bearer "+self.connection_obj.access_token

    def get_token(self):
        if hasattr(self.connection_obj,"app_type") and self.connection_obj.app_type=="system":
            payload = {
                "grant_type": "client_credentials",
                "scope": self.connection_obj.scope,
            }
            response, status_code = self.athena_backend(
                payload,self.headers, self.connection_obj.token_url, self.connection_obj.client_id, self.connection_obj.client_secret
            )
            print("payload till here>>>",payload)
            print("headers till here>>>",self.headers)
            print("url till here>>>",self.connection_obj.token_url)
            print("client_id till here>>>",self.connection_obj.client_id)
            print("client_secret till here>>>",self.connection_obj.client_secret)
            print("response till here>>>",response)
            print("status_code till here>>>",status_code)
            if status_code != 200:
                return False
            else:
                self.connection_obj.access_token=response.json().get("access_token")
                self.connection_obj.refresh_token=response.json().get("refres_token")
                self.connection_obj.access_token_generated_at=timezone.now()
                self.connection_obj.refresh_token_generated_at=timezone.now()
                self.connection_obj.save()
        return True

    def athena_backend(self,payload,headers,url,client_id,client_secret):
        response = requests.request("POST",data=payload,url=url,headers=headers,auth=HTTPBasicAuth(client_id,client_secret))
        if response.status_code==200:
            return response,response.status_code
        else:
            return None,None

    def put(self, url: str = "", content_type: str = "application/x-www-form-urlencoded", data: dict = {}):
        """
        PUT method to update data at given URL.
        Returns tuple (data, status_code) for consistency.
        """
        self.headers["Content-Type"] = content_type
        response = requests.request("PUT", url=url, headers=self.headers, data=data)

        # Always return a tuple (data, status_code) for consistency
        if response.status_code not in [200, 201, 204]:
            try:
                error_data = response.json()
            except (ValueError, AttributeError):
                error_data = {"detail": "Something went wrong", "error": response.text}
            return error_data, response.status_code

        try:
            # Some PUT requests return empty body (204 No Content)
            if response.status_code == 204:
                return {"detail": "Success"}, response.status_code
            return response.json(), response.status_code
        except (ValueError, AttributeError):
            return {"detail": response.text}, response.status_code

    def build_payload(self,**kwargs):
        payload = kwargs
        return payload

    def post(self, url: str = "", content_type: str = "application/x-www-form-urlencoded", data: dict = {}):
        self.headers["Content-Type"] = content_type
        response = requests.request("POST", url=url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return None, None
