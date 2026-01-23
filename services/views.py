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
            connection_id = data.get("Meta",{}).get("Source",{}).get("ID")
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
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

class ProviderQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Query Providers/Practitioners",
        description="Query Providers/Practitioners from EHR",
        request=inline_serializer(
            name="Provider-Query",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Provider-Query",
                value=provider_value_sets.get("provider_query"),
            )
        ],
    )
    def post(self, request):
        source_data = request.data
        try:
            connection_id = source_data.get("Meta", {}).get("Source", {}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = get_providers_transformer(connection_obj, source_data)
            return Response(transformer_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                value=patient_clinicals.get("push_medications"),
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
                value=media.get("Document_new"),
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
            return Response(transformer_response, status=status.HTTP_201_CREATED)
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
                value=medias_value_sets.get("media_query"),
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
            source_data = {"type":"get_media","media_data":request_body}
            transformer_response = get_media_transformer(connection_obj,connection_data,source_data)
            return Response({"detail": "Media retrieved successfully", "data": transformer_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateAllergyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Allergy",
        description="Create New Allergy",
        request=inline_serializer(
            name="Allergy-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Allergy-New",
                value=patient_clinicals.get("push_allergies"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_id = request_body.get("Meta",{}).get("Source",{}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = clinicals_push_transformer(connection_obj,request_body,"allergies")
            return Response(transformer_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateDiagnosisAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Diagnosis",
        description="Create New Diagnosis",
        request=inline_serializer(
            name="Diagnosis-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Diagnosis-New",
                value=patient_clinicals.get("push_conditions"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_id = request_body.get("Meta",{}).get("Source",{}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = clinicals_push_transformer(connection_obj,request_body,"diagnoses")
            return Response(transformer_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganizationQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Query Organizations",
        description="Query Organizations",
        request=inline_serializer(
            name="Organization-Query",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Organization-Query",
                value=organization_query_value_sets.get("organization"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_id = request_body.get("Meta",{}).get("Source",{}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = get_organization_transformer(connection_obj,request_body)
            return Response(transformer_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Create New Organization",
        description="Create New Organization",
        request=inline_serializer(
            name="Organization-New",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="Organization-New",
                value=organization_query_value_sets.get("organization"),
            )
        ],
    )
    def post(self,request):
        try:
            request_body = request.data
            connection_id = request_body.get("Meta",{}).get("Source",{}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = create_organization_transformer(connection_obj,request_body)
            return Response(transformer_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentReferenceQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Query Document References",
        description="""Query Document References from EHR.

        Supported search parameters:
        - Document.Identifiers[0].ID: Get document by specific ID
        - Patient.Identifiers[0].ID: Get documents for a specific patient
        - Document.Category: Category code (e.g., 'clinical-note')
        - Document.Type.Code: Document type LOINC code (e.g., '34133-9')
        - Document.Date.Start/End: Date range filter
        - Document.EncounterID: Get visit summary for specific encounter
        """,
        request=inline_serializer(
            name="DocumentReference-Query",
            fields={
                "Source_json": serializers.CharField(),
            },
        ),
        examples=[
            OpenApiExample(
                name="DocumentReference-Query-ByPatient",
                value={
                    "Meta": {
                        "DataModel": "DocumentReference",
                        "EventType": "Query",
                        "Test": True,
                        "Source": {
                            "ID": "connection-uuid-here",
                            "Name": "connectionid"
                        }
                    },
                    "Patient": {
                        "Identifiers": [{"ID": "patient-id-here"}]
                    },
                    "Document": {
                        "Category": "clinical-note",
                        "Type": {"Code": "34133-9"},
                        "Date": {
                            "Start": "2024-01-01",
                            "End": "2024-12-31"
                        }
                    }
                }
            )
        ],
    )
    def post(self, request):
        try:
            request_body = request.data
            connection_id = request_body.get("Meta", {}).get("Source", {}).get("ID")
            if not connection_id:
                return Response({"detail": "Connection ID not found"}, status=status.HTTP_400_BAD_REQUEST)
            connection_obj = EHRConnection.objects.filter(uuid=connection_id).first()
            if not connection_obj:
                return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
            transformer_response = get_document_reference_transformer(connection_obj, request_body)
            return Response(transformer_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
