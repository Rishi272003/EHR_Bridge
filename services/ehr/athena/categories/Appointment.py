from services.ehr.athena.client import AthenaHealthClient
from services.ehr.athena.urls import ATHENA_URLS


class Appointment(AthenaHealthClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_appointments_by_dates(self, **kwargs):
        """
        Get appointments by date range.
        Required: startdate, enddate, departmentid
        """
        url = self.build_url(ATHENA_URLS["Appointment"]["get_appointments_by_dates"]["path"])
        params = {
            "startdate": kwargs.get("startdate"),
            "enddate": kwargs.get("enddate"),
            "departmentid": kwargs.get("departmentid"),
        }
        return self.get(url, payload=params)

    def get_appointment_by_id(self, appointment_id, **kwargs):
        """
        Get appointment by ID.
        """
        url = self.build_url(
            ATHENA_URLS["Appointment"]["get_appointments_by_id"]["path"],
            appointmentId=appointment_id
        )
        return self.get(url)

    def cancel_appointment(self, appointment_id, **kwargs):
        """
        Cancel an appointment.
        Required: cancellationreason, patientid
        Optional: ignoreschedulablepermission, nopatientcase
        """
        url = self.build_url(
            ATHENA_URLS["Appointment"]["cancel_appointment"]["path"],
            appointmentId=appointment_id
        )
        payload = self.build_payload(
            cancellationreason=kwargs.get("cancellationreason"),
            ignoreschedulablepermission=kwargs.get("ignoreschedulablepermission", "false"),
            nopatientcase=kwargs.get("nopatientcase", "false"),
            patientid=kwargs.get("patientid"),
        )
        return self.put(url, content_type="application/x-www-form-urlencoded", data=payload)

    def reschedule_appointment(self, appointment_id, **kwargs):
        """
        Reschedule an appointment.
        Required: newappointmentid, patientid
        Optional: cancellationreason, ignoreschedulablepermission, nopatientcase
        """
        url = self.build_url(
            ATHENA_URLS["Appointment"]["reschedule_appointment"]["path"],
            appointmentId=appointment_id
        )
        payload = self.build_payload(
            newappointmentid=kwargs.get("newappointmentid"),
            cancellationreason=kwargs.get("cancellationreason"),
            ignoreschedulablepermission=kwargs.get("ignoreschedulablepermission", "false"),
            nopatientcase=kwargs.get("nopatientcase", "false"),
            patientid=kwargs.get("patientid"),
        )
        return self.put(url, content_type="application/x-www-form-urlencoded", data=payload)
