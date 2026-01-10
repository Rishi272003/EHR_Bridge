from rest_framework import status
from rest_framework.response import Response

from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.ehr_integrations.ehr_services.epic.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class QueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_response["potentialmatches"] = []

    def transform(self):

        try:
            patient = Patient(self.customer_id, self.tenant_name,self.source_json)
            patient.authenticate()
            if self.source_json.get("patientid"):

                patient_list = [
                    pid for pid in self.source_json.get("patientid").split(",") if pid
                ]
                if len(patient_list) > 0:
                    for single_patient in patient_list:
                        self.destination_json["patientid"] = single_patient
                        try:
                            PatientModel.objects.get(
                                ehr_id=self.destination_json["patientid"]
                            )
                        except PatientModel.DoesNotExist:
                            (
                                patient_response,
                                status_code,
                            ) = patient.get_specific_patient(
                                self.destination_json["patientid"]
                            )

                            if status_code == 404:
                                self.destination_response["potentialmatches"] = []
                                return {
                                        "detail": f"The patient id {self.destination_json['patientid']} does not exist",
                                        "statuscode": 400,
                                        }
                            elif status_code == 200:

                                self.destination_response["potentialmatches"].append(
                                    {
                                        "id": patient_response.get("id"),
                                        "firstname": (
                                            patient_response.get("name")[0].get(
                                                "given"
                                            )[0]
                                            if patient_response.get("name")[0].get(
                                                "given"
                                            )
                                            else None
                                        ),
                                        "lastname": (
                                            patient_response.get("name")[0].get(
                                                "family"
                                            )
                                            if patient_response.get("name")[0].get(
                                                "family"
                                            )
                                            else None
                                        ),
                                        "middlename": (
                                            patient_response.get("name")[0].get(
                                                "given"
                                            )[1]
                                            if len(
                                                patient_response.get("name")[0].get(
                                                    "given"
                                                )
                                            )
                                            > 1
                                            else None
                                        ),
                                        "dateofbirth": (
                                            patient_response.get("birthDate")
                                            if patient_response.get("birthDate")
                                            else None
                                        ),
                                        "sex": (
                                            patient_response.get("gender").title()
                                            if patient_response.get("gender")
                                            else None
                                        ),
                                        "mrn": None,  # Epic does not return this value
                                        "ssn": None,  # Epic does not return this value
                                        "status": patient_response.get("active"),
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
                self.destination_json["firstname"] = self.source_json.get("firstname")
                self.destination_json["lastname"] = self.source_json.get("lastname")
                self.destination_json["dob"] = self.source_json.get("dateofbirth")
                patient_response, status_code = patient.search_patient(
                    **self.destination_json
                )
                if status_code == 200:
                    if patient_response.get("total") == 0:
                        self.destination_response["potentialmatches"] = []
                    else:
                        for single_patient_data in patient_response.get("entry"):
                            try:
                                PatientModel.objects.get(
                                    ehr_id=single_patient_data.get("resource").get("id")
                                )
                            except PatientModel.DoesNotExist:
                                emailadress = None
                                if single_patient_data.get("resource").get("telecom"):
                                    for contacts in single_patient_data.get(
                                        "resource"
                                    ).get("telecom"):
                                        if contacts.get("system") == "email":
                                            emailadress = contacts.get("value")

                                self.destination_response["potentialmatches"].append(
                                    {
                                        "id": single_patient_data.get("resource").get(
                                            "id"
                                        ),
                                        "firstname": (
                                            single_patient_data.get("resource")
                                            .get("name")[0]
                                            .get("given")[0]
                                            if single_patient_data.get("resource")
                                            .get("name")[0]
                                            .get("given")
                                            else None
                                        ),
                                        "lastname": (
                                            single_patient_data.get("resource")
                                            .get("name")[0]
                                            .get("family")
                                            if single_patient_data.get("resource")
                                            .get("name")[0]
                                            .get("family")
                                            else None
                                        ),
                                        "middlename": (
                                            single_patient_data.get("resource")
                                            .get("name")[0]
                                            .get("given")[1]
                                            if len(
                                                single_patient_data.get("resource")
                                                .get("name")[0]
                                                .get("given")
                                            )
                                            > 1
                                            else None
                                        ),
                                        "dateofbirth": (
                                            single_patient_data.get("resource").get(
                                                "birthDate"
                                            )
                                            if single_patient_data.get("resource").get(
                                                "birthDate"
                                            )
                                            else None
                                        ),
                                        "sex": (
                                            single_patient_data.get("resource")
                                            .get("gender")
                                            .title()
                                            if single_patient_data.get("resource").get(
                                                "gender"
                                            )
                                            else None
                                        ),
                                        "mrn": None,  # Epic does not return this value
                                        "ssn": None,  # Epic does not return this value
                                        "status": single_patient_data.get("active"),
                                        "emailaddress": emailadress,
                                    }
                                )

                else:
                    del self.destination_response["potentialmatches"]
                    self.destination_response.update(
                        {"errormessage": patient_response, "statuscode": status_code}
                    )
            return self.destination_response
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
