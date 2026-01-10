# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import EHRConnection
# from django.http import JsonResponse
# from .utils import athena_backend
# from django.utils import timezone
# headers = {"Content-Type": "application/x-www-form-urlencoded",}
# @receiver(pre_save,sender=EHRConnection)
# def ehr_connection_saved(sender,instance,**kwargs):
#     if instance.ehr_name=="athena":
#         if instance.app_type=="provider":
#             pass
#         elif instance.app_type=="system":
#             payload = {
#                 "grant_type": "client_credentials",
#                 "scope": instance.scope,
#             }
#             response, status_code = athena_backend(
#                 payload, headers, instance.token_url, instance.client_id, instance.client_secret
#             )
#             if status_code != 200:
#                 return JsonResponse(
#                     {"Detail": response.json().get("error")},
#                     status=response.status_code,
#                 )
#             elif status_code==200:
#                 instance.access_token=response.json().get("access_token")
#                 instance.refresh_token=response.json().get("refres_token")
#                 instance.access_token_generated_at=timezone.now()
#                 instance.refresh_token_generated_at=timezone.now()
#     else:
#         print(f"EHR connection updated>>>>>{instance.ehr_name}")
