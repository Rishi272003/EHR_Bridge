from django.urls import path
from .views import (
    PatientQueryAPIView,
    PatientSearch,
    AppointmentByDateAPIView,
    AppointmentByIdAPIView,
    CancelAppointmentAPIView,
    AppointmentRescheduleAPIView,
    VisitQueryAPIView,
    AllProvidersAPIView,
    ProviderByIdAPIView,
    CreateProviderAPIView,
)

urlpatterns = [
    path("patient-query/", PatientQueryAPIView.as_view(), name="Patient_query"),
    path("patient-search/", PatientSearch.as_view(), name="patient_search"),
    # Appointment endpoints
    path("appointments/by-date/", AppointmentByDateAPIView.as_view(), name="appointments_by_date"),
    path("appointments/by-id/", AppointmentByIdAPIView.as_view(), name="appointments_by_id"),
    path("appointments/cancel/", CancelAppointmentAPIView.as_view(), name="appointments_cancel"),
    path("appointments/reschedule/", AppointmentRescheduleAPIView.as_view(), name="appointments_reschedule"),
    # Visit Query endpoint
    path("visit-query/", VisitQueryAPIView.as_view(), name="visit_query"),
    path("providers/",AllProvidersAPIView.as_view(), name="all_providers"),
    path("providers/by-id/",ProviderByIdAPIView.as_view(), name="provider_by_id"),
    path("providers/create/",CreateProviderAPIView.as_view(), name="create_provider"),
]
