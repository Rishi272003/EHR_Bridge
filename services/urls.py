from django.urls import path
from .views import *

urlpatterns = [
    # Patients
    path("patient/patient-query/", PatientQueryAPIView.as_view(), name="Patient_query"),
    path("patient/patient-search/", PatientSearch.as_view(), name="patient_search"),
    path("patient/new-patient/",NewPatientAPIView.as_view(), name="new_patient"),
    # Clinical Summary
    path("clinical-summary/create-allergy/", CreateAllergyAPIView.as_view(), name="create_allergy"),
    path("clinical-summary/create-patient-diagnosis/", CreateDiagnosisAPIView.as_view(), name="create_medication"),
    # Appointments
    path("appointments/by-date/", AppointmentByDateAPIView.as_view(), name="appointments_by_date"), # Not in use
    path("appointments/by-id/", AppointmentByIdAPIView.as_view(), name="appointments_by_id"),
    path("appointments/cancel/", CancelAppointmentAPIView.as_view(), name="appointments_cancel"),
    path("appointments/reschedule/", AppointmentRescheduleAPIView.as_view(), name="appointments_reschedule"),
    # Providers
    path("provider/query/",ProviderQueryAPIView.as_view(), name="provider_query"),
    path("provider/create/",CreateProviderAPIView.as_view(), name="create_provider"),
    # Medications
    path("medication/medication-new/",MedicationNewAPIView.as_view(), name="medication_new"),
    # Media
    path("media/create-media/",CreateMediaAPIView.as_view(), name="create_media"),
    path("media/get-media/",GetMediaAPIView.as_view(), name="get_media"),
    # Visit Query
    path("visit/visit-query/", VisitQueryAPIView.as_view(), name="visit_query"),
    # Organizations
    path("organization/organization-query/", OrganizationQueryAPIView.as_view(), name="organization_query"),
    path("organization/create-organization/", CreateOrganizationAPIView.as_view(), name="create_organization"),
    # Document References
    path("document-reference/query/", DocumentReferenceQueryAPIView.as_view(), name="document_reference_query"),
]
