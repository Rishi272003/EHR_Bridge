from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    PatientQuerySerializer,
    PatientSearchSerializer,
    AppointmentByDateSerializer,
    AppointmentByIdSerializer,
    CancelAppointmentSerializer,
    RescheduleAppointmentSerializer,
    VisitQuerySerializer,
    ProviderByIdSerializer,
    CreateProviderSerializer,
)
from drf_spectacular.utils import extend_schema
from core.models import EHRConnection
from .utils import *
from django.forms.models import model_to_dict
from .ehr.athena.categories.Appointment import Appointment
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer,OpenApiParameter
import base64
import urllib
import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.models import EHRConnection
from services.ehr.value_sets import *
from rest_framework import serializers,status
class PatientQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    summary="Clinical Summary Patient Query",
    description="Return List of Patient Clinical Data",
    request=inline_serializer(
        name="Clinical-Summary-Patient-Query",
        fields={
            "Source_json": serializers.CharField(),
        },
    ),
    examples=[
        OpenApiExample(
            name="Clinical-Summary-Patient-Query",
            value=clinical_summary_value_sets.get("patient_query"),
        )
    ],
    )
    def post(self, request):
        source_data = request.data
        try:
            connection_id = source_data.get("Meta",{}).get("Source",{}).get("ID")
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            transformer_response = get_query_transformer(connection_obj,source_data)
        except Exception as e:
            return Response({"detail":f"Somthing went wrong {str(e)}"})
        return Response({"data":transformer_response},status=status.HTTP_200_OK)

class PatientSearch(APIView):
    permission_class = [IsAuthenticated]
    @extend_schema(
    summary="Patient Search Query",
    description="Return List of Patients",
    request=inline_serializer(
        name="Patient-Search-Query",
        fields={
            "Source_json": serializers.CharField(),
        },
    ),
    examples=[
        OpenApiExample(
            name="Patient-Search-Query",
            value=patient_search_value_sets,
        )
    ],
    )

    def post(self,request):
        source_data = request.data
        try:
            connection_id = source_data.get("Meta",{}).get("Source",{}).get("ID")
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            transformer_response = get_search_transformer(connection_obj,source_data)
        except Exception as e:
            return Response({"detail":f"Somthing went wrong {str(e)}"})
        return Response({"data":transformer_response},status=status.HTTP_200_OK)


class AppointmentByDateAPIView(APIView):
    serializer_class = AppointmentByDateSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AppointmentByDateSerializer,
        description="Get appointments by date range"
    )
    def post(self, request):
        """
        Get appointments by date range.
        POST /api/appointments/by-date/
        """
        serializer = AppointmentByDateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
            if not connection_obj:
                return Response(
                    {"detail": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointment = Appointment(connection_obj)
            appointment.authenticate()

            appointments_response, status_code = appointment.get_appointments_by_dates(
                startdate=data["startdate"],
                enddate=data["enddate"],
                departmentid=data["departmentid"]
            )

            if status_code == 200:
                return Response(
                    {"detail": "Appointments retrieved successfully", "data": appointments_response},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Failed to retrieve appointments", "error": appointments_response},
                    status=status_code
                )
        except Exception as e:
            return Response(
                {"detail": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentByIdSerializer
    @extend_schema(
        request=AppointmentByIdSerializer,
        description="Get appointment by ID"
    )
    def post(self, request):
        """
        Get appointment by ID.
        POST /api/appointments/by-id/
        """
        serializer = AppointmentByIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
            if not connection_obj:
                return Response(
                    {"detail": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointment = Appointment(connection_obj)
            appointment.authenticate()

            appointment_response, status_code = appointment.get_appointment_by_id(
                data["appointment_id"]
            )

            if status_code == 200:
                return Response(
                    {"detail": "Appointment retrieved successfully", "data": appointment_response},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Failed to retrieve appointment", "error": appointment_response},
                    status=status_code
                )
        except Exception as e:
            return Response(
                {"detail": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CancelAppointmentSerializer
    @extend_schema(
        request=CancelAppointmentSerializer,
        description="Cancel an appointment"
    )
    def put(self, request):
        """
        Cancel an appointment.
        PUT /api/appointments/cancel/
        """
        serializer = CancelAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
            if not connection_obj:
                return Response(
                    {"detail": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointment = Appointment(connection_obj)
            appointment.authenticate()

            cancel_response, status_code = appointment.cancel_appointment(
                data["appointment_id"],
                cancellationreason=data["cancellationreason"],
                patientid=data["patientid"],
                ignoreschedulablepermission=str(data.get("ignoreschedulablepermission", False)).lower(),
                nopatientcase=str(data.get("nopatientcase", False)).lower(),
            )

            if status_code in [200, 201, 204]:
                return Response(
                    {"detail": "Appointment cancelled successfully", "data": cancel_response},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Failed to cancel appointment", "error": cancel_response},
                    status=status_code
                )
        except Exception as e:
            return Response(
                {"detail": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentRescheduleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RescheduleAppointmentSerializer
    @extend_schema(
        request=RescheduleAppointmentSerializer,
        description="Reschedule an appointment"
    )
    def put(self, request):
        """
        Reschedule an appointment.
        PUT /api/appointments/reschedule/
        """
        serializer = RescheduleAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
            if not connection_obj:
                return Response(
                    {"detail": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            appointment = Appointment(connection_obj)
            appointment.authenticate()

            reschedule_response, status_code = appointment.reschedule_appointment(
                data["appointment_id"],
                newappointmentid=data["newappointmentid"],
                patientid=data["patientid"],
                cancellationreason=data.get("cancellationreason", ""),
                ignoreschedulablepermission=str(data.get("ignoreschedulablepermission", False)).lower(),
                nopatientcase=str(data.get("nopatientcase", False)).lower(),
            )

            if status_code in [200, 201, 204]:
                return Response(
                    {"detail": "Appointment rescheduled successfully", "data": reschedule_response},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Failed to reschedule appointment", "error": reschedule_response},
                    status=status_code
                )
        except Exception as e:
            return Response(
                {"detail": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VisitQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VisitQuerySerializer
    @extend_schema(
    summary="Clinical Summary Visit Query",
    description="Return List of Visits for a Patient",
    request=inline_serializer(
        name="Clinical-Summary-Visit-Query",
        fields={
            "Source_json": serializers.CharField(),
        },
    ),
    examples=[
        OpenApiExample(
            name="Clinical-Summary-Visit-Query",
            value=clinical_summary_value_sets.get("visit_query"),
        )
    ],
)
    def post(self, request):
        source_data = request.data
        try:
            connection_id = source_data.get("Meta",{}).get("Source",{}).get("ID")
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            transformer_response = get_visit_transformer(connection_obj,source_data)

            return Response(
                transformer_response,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AllProvidersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get all providers",
        parameters=[
            OpenApiParameter(
                name="connection_id",
                description="Connection ID",
                required=True,
                type=str
            )
        ]
    )
    def get(self,request):
        connection_id = request.query_params.get("connection_id")
        try:
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"all"}
            transformer = get_providers_transformer(connection_obj,connection_data,source_data)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"detail": "Providers retrieved successfully", "data": transformer}, status=status.HTTP_200_OK)

class ProviderByIdAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProviderByIdSerializer
    @extend_schema(
        request=ProviderByIdSerializer,
        description="Get provider by ID"
    )
    def post(self,request):
        serializer = ProviderByIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"single","provider_id":data["provider_id"]}
            transformer = get_providers_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Provider retrieved successfully", "data": transformer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateProviderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProviderSerializer
    @extend_schema(
        request=CreateProviderSerializer,
        description="Create a new provider"
    )
    def post(self,request):
        serializer = CreateProviderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # try:
        connection_obj = EHRConnection.objects.filter(uuid=data["connection_id"]).first()
        if not connection_obj:
            return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
        connection_data = model_to_dict(connection_obj)
        source_data = {"type":"create","provider_data":serializer.validated_data}
        transformer = get_providers_transformer(connection_obj,connection_data,source_data)
        return Response({"detail": "Provider created successfully", "data": transformer}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewPatientAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Patient",
        description="Create New Patient",
        request=inline_serializer(
            name="Patient-Admin-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Patient-Admin-New",
                value=patient_admin_value_sets.get("new_patient"),
            )
        ],
    )

    def post(self,request):
        try:
            request_body = request.data
            connection_obj = EHRConnection.objects.filter(uuid=request_body["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"new_patient","patient_data":request_body}
            transformer = get_patient_admin_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Patient created successfully", "data": transformer}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicationNewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Medication",
        description="Create New Medication",
        request=inline_serializer(
            name="Medication-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Medication-New",
                value=medications_value_sets.get("new_medication"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_obj = EHRConnection.objects.filter(uuid=request_body["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"new_medication","medication_data":request_body}
            transformer = get_medication_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Medication created successfully", "data": transformer}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateMediaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Media",
        description="Create New Media",
        request=inline_serializer(
            name="Media-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Media-New",
                value=medias_value_sets.get("new_media"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_obj = EHRConnection.objects.filter(uuid=request_body["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"new_media","media_data":request_body}
            transformer_response = get_media_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Media created successfully", "data": transformer_response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetMediaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Get Media",
        description="Get Media",
        request=inline_serializer(
            name="Media-Get",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Media-Get",
                value=medias_value_sets.get("get_media"),
            )
        ],
    )
    def get(self,request):
        try:
            request_body = request.data
            connection_obj = EHRConnection.objects.filter(uuid=request_body["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            connection_data = model_to_dict(connection_obj)
            source_data = {"type":"get_media","media_data":request_body}
            transformer_response = get_media_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Media retrieved successfully", "data": transformer_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PushClinicalSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Push Clinical Summary",
        description="Push Clinical Summary",
        request=inline_serializer(
            name="Clinical-Summary-Push",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Clinical-Summary-Push",
                value=clinical_summary_value_sets.get("push_clinical_summary"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_obj = EHRConnection.objects.filter(uuid=request_body["connection_id"]).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = clinicals_push_transformer(connection_obj,request_body)
            return Response({"detail": "Clinical summary pushed successfully", "data": transformer_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["GET"])
def ecw_callback(request):
    """
    ECW OAuth callback handler.
    Receives authorization code from ECW and exchanges it for access token.
    """
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    if not state:
        return JsonResponse({"error": "State parameter not provided"}, status=400)

    try:
        state_parts = state.split(",")

        if len(state_parts) >= 3:
            connection_uuid = state_parts[0]
            ehr_name = state_parts[1]  # eclinicalworks
            app_type = state_parts[2]  # provider or patient
        else:
            # Fallback: try to get connection by UUID only
            connection_uuid = state_parts[0]
            ehr_name = "eclinicalworks"
            app_type = "provider"  # default

        # Get ECW connection directly by UUID
        try:
            ecw_connection = EHRConnection.objects.get(
                uuid=connection_uuid, ehr_name=ehr_name
            )
        except EHRConnection.DoesNotExist:
            return JsonResponse({"error": "ECW connection not found"}, status=404)

        # Prepare headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Prepare Basic Auth header (client_id:client_secret)
        client_id = ecw_connection.client_id
        client_secret = ecw_connection.client_secret or ""

        # Create Basic Auth credentials
        auth_credentials = base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()
        headers["Authorization"] = f"Basic {auth_credentials}"

        # Prepare payload
        # Use redirect_uri from connection to ensure it matches the authorization request
        redirect_uri = ecw_connection.redirect_uri or request.build_absolute_uri(
            "/callback-uri"
        )
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # Add code_verifier if available (PKCE flow)
        if ecw_connection.code_verifier:
            payload["code_verifier"] = ecw_connection.code_verifier

        # Exchange code for token
        try:
            print("token_url>>>",ecw_connection.token_url)
            print("headers>>>",headers)
            print("payload>>>",payload)
            response = requests.post(
                ecw_connection.token_url,
                headers=headers,
                data=payload,
            )
            print("response>>>",response.json())
            response.raise_for_status()
            try:
                token_data = response.json()
            except ValueError:
                # If response is not JSON, return error
                return JsonResponse(
                    {
                        "error": "Invalid response from token endpoint",
                        "response": response.text[:500],  # Limit response length
                    },
                    status=500,
                )
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (4xx, 5xx)
            error_response = None
            if hasattr(e.response, "text"):
                try:
                    error_response = e.response.json()
                except ValueError:
                    error_response = {"error": e.response.text[:500]}
            return JsonResponse(
                {
                    "error": "Failed to exchange code for token",
                    "status_code": (
                        e.response.status_code if hasattr(e, "response") else None
                    ),
                    "details": error_response or str(e),
                },
                status=e.response.status_code if hasattr(e, "response") else 500,
            )
        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {
                    "error": "Failed to exchange code for token",
                    "details": str(e),
                },
                status=500,
            )

        # Save tokens to connection
        ecw_connection.access_token = token_data.get("access_token")
        ecw_connection.refresh_token = token_data.get("refresh_token")
        ecw_connection.access_token_generated_at = timezone.now()
        ecw_connection.save()


        # Redirect to org_redirect_uri if set, otherwise return JSON
        if ecw_connection.org_redirect_uri:
            redirect_url = (
                ecw_connection.org_redirect_uri
                + "?"
                + urllib.parse.urlencode(
                    {
                        "status": "success",
                        "access_token": token_data.get("access_token"),
                    }
                )
            )
            return redirect(redirect_url)

        # Return JSON response with token data
        return JsonResponse(
            {
                "status": "success",
                "access_token": token_data.get("access_token"),
                "token_type": token_data.get("token_type"),
                "expires_in": token_data.get("expires_in"),
                "refresh_token": token_data.get("refresh_token"),
                "scope": token_data.get("scope"),
            },
            status=200,
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Internal server error", "details": str(e)}, status=500
        )
