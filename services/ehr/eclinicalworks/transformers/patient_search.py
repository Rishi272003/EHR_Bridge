from rest_framework.response import Response

from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.Chart import Chart
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.Patient import (
    Patient,
)
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer
from ecaremd.provider_group.models import EHRConnection


class QueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_response["potentialmatches"] = []

    def transform(self):
        firstname = self.source_json.get("firstname")
        lastname = self.source_json.get("lastname")
        self.destination_json["dob"] = self.source_json.get("dateofbirth")

        if firstname and lastname:
            self.destination_json["name"] = f"{lastname} {firstname}"

        elif firstname or lastname:
            self.destination_json["name"] = firstname if firstname else lastname
        if self.source_json.get("patientid"):
            patient_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
            patient_chart.authenticate()
            conn = EHRConnection.objects.filter(
                provider_group_id=self.source_json["pg_id"],
                ehr_name__icontains=self.source_json["ehr_name"],
            ).first()
            if conn:
                practiceid = conn.practice_id
            else:
                practiceid = None
            patient_list = [pid for pid in self.source_json.get("patientid").split(",")]
            if len(patient_list) > 0:
                for single_patient in patient_list:
                    self.destination_json["patientid"] = single_patient
                    try:
                        PatientModel.objects.get(
                            ehr_id=self.destination_json["patientid"]
                        )
                        return Response(
                            {"detail": "Patient already imported"}, status=400
                        )

                    except PatientModel.DoesNotExist:
                        (
                            patient_response,
                            status_code,
                        ) = patient_chart.get_patient_demographics(
                            practiceid, **self.destination_json
                        )
                        if status_code == 404:
                            self.destination_response["potentialmatches"] = []
                        elif status_code == 200:
                            for patient in patient_response.get("entry"):
                                emailadress = None
                                if patient.get("resource").get("telecom"):
                                    for contacts in patient.get("resource").get(
                                        "telecom"
                                    ):
                                        if contacts.get("system") == "email":
                                            emailadress = contacts.get("value")

                                self.destination_response["potentialmatches"].append(
                                    {
                                        "id": patient.get("resource").get("id"),
                                        "firstname": (
                                            patient.get("resource")
                                            .get("name")[0]
                                            .get("given")[0]
                                            if patient.get("resource")
                                            .get("name")[0]
                                            .get("given")
                                            else None
                                        ),
                                        "lastname": (
                                            patient.get("resource")
                                            .get("name")[0]
                                            .get("family")
                                            if patient.get("resource")
                                            .get("name")[0]
                                            .get("family")
                                            else None
                                        ),
                                        "middlename": (
                                            patient.get("resource")
                                            .get("name")[0]
                                            .get("given")[1]
                                            if len(
                                                patient.get("resource")
                                                .get("name")[0]
                                                .get("given")
                                            )
                                            > 1
                                            else None
                                        ),
                                        "dateofbirth": (
                                            patient.get("resource").get("birthDate")
                                            if patient.get("resource").get("birthDate")
                                            else None
                                        ),
                                        "sex": (
                                            patient.get("resource")
                                            .get("gender")
                                            .title()
                                            if patient.get("resource").get("gender")
                                            else None
                                        ),
                                        "mrn": patient.get("resource", {"resource": {}})
                                        .get("identifier", [])[1]
                                        .get("value", None),
                                        "ssn": None,  # eCW does not return this value
                                        "status": patient.get("active"),
                                        "emailaddress": emailadress,
                                    }
                                )

                        else:
                            del self.destination_response["potentialmatches"]
                            self.destination_response.update(
                                {
                                    "errormessage": patient_response,
                                    "statuscode": status_code,
                                }
                            )

        else:
            patient = Patient(self.customer_id, self.tenant_name, self.source_json)
            patient.authenticate()
            conn = EHRConnection.objects.filter(
                provider_group_id=self.source_json["pg_id"],
                ehr_name=self.source_json["ehr_name"],
            ).first()
            if conn:
                practiceid = conn.practice_id
            else:
                practiceid = None

            patient_response, status_code = patient.get_search_criteria(
                practiceid, **self.destination_json
            )
            print("patient_response", patient_response)
            print("status_code", status_code)
            if status_code == 400:
                del self.destination_response["potentialmatches"]
                self.destination_response.update(
                    {"detail": "Not data found in EHR", "statuscode": status_code}
                )
            elif status_code == 200:
                if patient_response.get("total") == 0:
                    self.destination_response["potentialmatches"] = []
                else:
                    for patient in patient_response.get("entry"):
                        try:
                            PatientModel.objects.get(
                                ehr_id=patient.get("resource").get("id")
                            )
                        except PatientModel.DoesNotExist:
                            emailadress = None
                            if patient.get("resource").get("telecom"):
                                for contacts in patient.get("resource").get("telecom"):
                                    if contacts.get("system") == "email":
                                        emailadress = contacts.get("value")

                            self.destination_response["potentialmatches"].append(
                                {
                                    "id": patient.get("resource").get("id"),
                                    "firstname": (
                                        patient.get("resource")
                                        .get("name")[0]
                                        .get("given")[0]
                                        if patient.get("resource")
                                        .get("name")[0]
                                        .get("given")
                                        else None
                                    ),
                                    "lastname": (
                                        patient.get("resource")
                                        .get("name")[0]
                                        .get("family")
                                        if patient.get("resource")
                                        .get("name")[0]
                                        .get("family")
                                        else None
                                    ),
                                    "middlename": (
                                        patient.get("resource")
                                        .get("name")[0]
                                        .get("given")[1]
                                        if len(
                                            patient.get("resource")
                                            .get("name")[0]
                                            .get("given")
                                        )
                                        > 1
                                        else None
                                    ),
                                    "dateofbirth": (
                                        patient.get("resource").get("birthDate")
                                        if patient.get("resource").get("birthDate")
                                        else None
                                    ),
                                    "sex": (
                                        patient.get("resource").get("gender").title()
                                        if patient.get("resource").get("gender")
                                        else None
                                    ),
                                    "mrn": patient.get("resource", {"resource": {}})
                                    .get("identifier", [])[1]
                                    .get("value", None),
                                    "ssn": None,  # eCW does not return this value
                                    "status": patient.get("active"),
                                    "emailaddress": emailadress,
                                }
                            )

            else:
                del self.destination_response["potentialmatches"]
                self.destination_response.update(
                    {"errormessage": patient_response, "statuscode": status_code}
                )

        return self.destination_response
