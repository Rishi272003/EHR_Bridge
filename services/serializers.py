from random import choice
from rest_framework import serializers
class PatientIdentifierSerializer(serializers.Serializer):
    ID = serializers.CharField()
    IDType = serializers.CharField(default="EHRID")

class PatientSerializer(serializers.Serializer):
    Identifiers = PatientIdentifierSerializer(many=True)

class MetaSerializer(serializers.Serializer):
    DateModel = serializers.CharField(default="Clinical Summary")
    EventType = serializers.CharField(default="PatientQuery")
    EventDateTime = serializers.DateTimeField()
    Test = serializers.BooleanField(required=False,default=True)
    ConnectionID = serializers.UUIDField()

class LocationSerializer(serializers.Serializer):
    Department = serializers.CharField(allow_null=True, required=False)


class PatientQuerySerializer(serializers.Serializer):
    Meta = MetaSerializer()
    Patient = PatientSerializer()
    Location = LocationSerializer()
    Events = serializers.ListField(
        default =  ["patients","allergies", "medication", "conditions", "vitals"],
        help_text="List of EHR event types to sync"
    )

class PatientSearchSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    ehr_id = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    fname = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    lname = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    dob = serializers.DateField(required=False,allow_null=True)
    gender = serializers.CharField(required=False,allow_null=True,allow_blank=True,default=["m","f"])
    department_id = serializers.CharField(required=False,allow_null=True,allow_blank=True)

# Appointment Serializers
class AppointmentByDateSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    startdate = serializers.CharField(required=True, help_text="Date in MM/DD/YYYY format")
    enddate = serializers.CharField(required=True, help_text="Date in MM/DD/YYYY format")
    departmentid = serializers.CharField(required=True)

class AppointmentByIdSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    appointment_id = serializers.IntegerField(required=True)

class CancelAppointmentSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    appointment_id = serializers.IntegerField(required=True)
    cancellationreason = serializers.CharField(required=True)
    patientid = serializers.IntegerField(required=True)
    ignoreschedulablepermission = serializers.BooleanField(required=False, default=False)
    nopatientcase = serializers.BooleanField(required=False, default=False)

class RescheduleAppointmentSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    appointment_id = serializers.IntegerField(required=True)
    newappointmentid = serializers.IntegerField(required=True)
    patientid = serializers.IntegerField(required=True)
    cancellationreason = serializers.CharField(required=False, allow_blank=True)
    ignoreschedulablepermission = serializers.BooleanField(required=False, default=False)
    nopatientcase = serializers.BooleanField(required=False, default=False)

# VisitQuery Serializers

class VisitLogSerializer(serializers.Serializer):
    ID = serializers.UUIDField()
    AttemptID = serializers.UUIDField()

class VisitMetaSerializer(serializers.Serializer):
    DataModel = serializers.CharField(default="Clinical Summary")
    EventType = serializers.CharField(default="VisitQuery")
    EventDateTime = serializers.DateTimeField()
    Test = serializers.BooleanField(required=False, default=True)
    ConnectionID = serializers.UUIDField(required=False, allow_null=True)
    Logs = VisitLogSerializer(many=True, required=False)
    FacilityCode = serializers.CharField(allow_null=True, required=False)

class VisitSerializer(serializers.Serializer):
    VisitNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    StartDateTime = serializers.DateTimeField(required=False, allow_null=True)
    EndDateTime = serializers.DateTimeField(required=False, allow_null=True)

class VisitQuerySerializer(serializers.Serializer):
    Meta = VisitMetaSerializer()
    Patient = PatientSerializer()
    Visit = VisitSerializer(required=False, allow_null=True)
    Location = LocationSerializer()

    def validate(self, data):
        """
        Validate that either VisitNumber is provided OR startdate/enddate/departmentid are provided.
        For now, we'll handle this in the view since VisitNumber might be in Visit.VisitNumber
        """
        return data

class ProviderByIdSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    provider_id = serializers.IntegerField(required=True)

class CreateProviderSerializer(serializers.Serializer):
    connection_id = serializers.UUIDField()
    billable = serializers.BooleanField(required=True)
    entitytypeid = serializers.IntegerField(required=True)
    medicalgroupid = serializers.IntegerField(required=True)
    schedulingname = serializers.CharField(required=True)
    signatureonfileflag = serializers.BooleanField(required=True)
    sex = serializers.CharField(required=True)
    ssn = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    namesuffix = serializers.CharField(required=True)
    providergroupid = serializers.IntegerField(required=True)
    billednamecase = serializers.CharField(required=True)
    specialtyid = serializers.IntegerField(required=True)
    providertype = serializers.CharField(required=True)
    ansicode = serializers.CharField(required=True)
