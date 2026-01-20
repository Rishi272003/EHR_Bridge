from django.urls import path
from .views import *

urlpatterns = [
    path("clinical-summary/patient-query/", PatientQueryAPIView.as_view(), name="Patient_query"),    path("patient/patient-search/", PatientSearch.as_view(), name="patient_search"),
    path("clinical-summary/push-clinical-summary/", PushClinicalSummaryAPIView.as_view(), name="push_clinical_summary"),
    # Appointment endpoints
    path("appointments/by-date/", AppointmentByDateAPIView.as_view(), name="appointments_by_date"),
    path("appointments/by-id/", AppointmentByIdAPIView.as_view(), name="appointments_by_id"),
    path("appointments/cancel/", CancelAppointmentAPIView.as_view(), name="appointments_cancel"),
    path("appointments/reschedule/", AppointmentRescheduleAPIView.as_view(), name="appointments_reschedule"),
    # Provider endpoints
    path("provider/providers/",AllProvidersAPIView.as_view(), name="all_providers"),
    path("provider/by-id/",ProviderByIdAPIView.as_view(), name="provider_by_id"),
    path("provider/create/",CreateProviderAPIView.as_view(), name="create_provider"),
    path("patient/new-patient/",NewPatientAPIView.as_view(), name="new_patient"),
    # Medication endpoints
    path("medication/medication-new/",MedicationNewAPIView.as_view(), name="medication_new"),
    # Media endpoints
    path("media/create-media/",CreateMediaAPIView.as_view(), name="create_media"),
    path("media/get-media/",GetMediaAPIView.as_view(), name="get_media"),
    # Visit Query endpoint
    path("visit/visit-query/", VisitQueryAPIView.as_view(), name="visit_query"),
]
