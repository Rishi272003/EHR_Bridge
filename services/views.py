from urllib import request
from core import serializers
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
from .ehr.athena.transformers.clinical_summary import PatientQueryTransformer
from .utils import (
    get_query_transformer,
    get_search_transformer,
    get_visit_transformer,
    get_providers_transformer
)
from django.forms.models import model_to_dict
from .ehr.athena.categories.Appointment import Appointment
from drf_spectacular.utils import OpenApiParameter

class PatientQueryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=PatientQuerySerializer
    )
    def post(self, request):
        serializer = PatientQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        meta = data["Meta"]
        patient = data["Patient"]
        identifiers = patient["Identifiers"]
        events = data["Events"]
        # Example: extract MRN
        mrn = None
        ehr_id = None

        for ident in identifiers:
            if ident["IDType"] == "MR":
                mrn = ident["ID"]
            elif ident["IDType"] == "EHRID":
                patient_id = ident["ID"]
        try:
            connection_obj = EHRConnection.objects.filter(uuid=meta["ConnectionID"]).first()
            transformer = get_query_transformer(connection_obj,patient_id,events,serializer.validated_data)
        except Exception as e:
            return Response({"detail":f"Somthing went wrong {str(e)}"})
        return Response(
            {
                "detail": "Patient query received",
                "mrn": mrn,
                "ehr_id": ehr_id,
                "connection_id": meta["ConnectionID"],
                "events":events,
                "data":transformer
            },
            status=status.HTTP_200_OK,
        )

class PatientSearch(APIView):
    permission_class = [IsAuthenticated]
    @extend_schema(
        request=PatientSearchSerializer
    )
    def post(self,request):
        serializer = PatientSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        source_data = serializer.validated_data
        try:
            connection_obj = EHRConnection.objects.filter(uuid=source_data.get("connection_id")).first()
            connection_data = model_to_dict(connection_obj)
            transformer = get_search_transformer(connection_obj,source_data,connection_data)
        except Exception as e:
            return Response({"detail":f"Somthing went wrong {str(e)}"})
        return Response({"detial":serializer.validated_data,"data":transformer})


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
        request=VisitQuerySerializer,
        description="Get visit/appointment query response"
    )
    def post(self, request):
        """
        Visit Query API.
        Accepts either VisitNumber (appointment ID) OR StartDateTime/EndDateTime/departmentid.
        POST /api/visit-query/
        """
        serializer = VisitQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        meta = data["Meta"]
        patient = data["Patient"]
        visit = data.get("Visit", {})
        location = data.get("Location", {})
        # Extract patient identifier
        identifiers = patient["Identifiers"]
        patient_identifier = None
        for ident in identifiers:
            if ident["IDType"] in ["EHRID", "NIST", "MR"]:
                patient_identifier = ident["ID"]
                break

        # Build visit_data - either VisitNumber or date range
        visit_data = {}
        if visit and visit.get("VisitNumber"):
            # Use appointment ID
            visit_data["VisitNumber"] = visit["VisitNumber"]
        elif visit and (visit.get("StartDateTime") or visit.get("EndDateTime")):
            # Use date range - need to extract departmentid from Location or connection
            visit_data["StartDateTime"] = visit.get("StartDateTime")
            visit_data["EndDateTime"] = visit.get("EndDateTime")
            # departmentid will be extracted from connection_data

        try:
            connection_obj = EHRConnection.objects.filter(uuid=meta["ConnectionID"]).first()
            if not connection_obj:
                return Response(
                    {"detail": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            connection_data = model_to_dict(connection_obj)
            # If using date range and no departmentid in visit_data, use from connection
            if not visit_data.get("VisitNumber") and not location.get("Department"):
                return Response({"detail": "Department not found"}, status=status.HTTP_400_BAD_REQUEST)
            if not visit_data.get("VisitNumber") and location.get("Department"):
                visit_data["departmentid"] = location.get("Department")
            transformer = get_visit_transformer(
                connection_obj,
                visit_data,
                connection_data,
                meta
            )

            return Response(
                transformer,
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
