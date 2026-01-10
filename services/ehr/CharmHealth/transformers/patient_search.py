from rest_framework import status
from rest_framework.response import Response

from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class QueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_response["potentialmatches"] = []

    def transform(self):
        firstname = self.source_json.get("firstname")
        lastname = self.source_json.get("lastname")
        self.destination_json["dob"] = self.source_json.get("dateofbirth")
        if self.source_json.get("patientid"):
            patient_chart = Patient(
                self.customer_id, self.tenant_name, self.source_json
            )
            patient_chart.authenticate()

            patient_list = [pid for pid in self.source_json.get("patientid").split(",")]
            if len(patient_list) > 0:
                for single_patient in patient_list:
                    self.destination_json["patientid"] = single_patient
                    try:
                        PatientModel.objects.get(ehr_id=single_patient)
                        return Response(
                            {"detail": "Patient already imported"}, status=400
                        )
                    except PatientModel.DoesNotExist:
                        (
                            patient_response,
                            status_code,
                        ) = patient_chart.get_patient_demographics(
                            patientid=single_patient
                        )
                        if status_code != 200:
                            return Response(
                                {"detail": "Patient already imported"}, status=400
                            )
                        elif status_code == 200:
                            patient_id = patient_response.get("data", {"data": {}}).get(
                                "identifier", []
                            )
                            for identifier in patient_id:
                                if identifier.get("use") == "usual":
                                    patient_id = identifier.get("value")
                            if patient_response.get("total") == 0:
                                self.destination_response["potentialmatches"] = []
                            else:
                                try:
                                    PatientModel.objects.get(ehr_id=patient_id)
                                except PatientModel.DoesNotExist:
                                    emailadress = None
                                    patient_details = patient_response.get(
                                        "data", {"data": {}}
                                    ).get("name", [])
                                    for detail in patient_details:
                                        firstname = detail.get("given", [])[0]
                                        lastname = detail.get("family", None)
                                    self.destination_response[
                                        "potentialmatches"
                                    ].append(
                                        {
                                            "id": patient_id,
                                            "firstname": firstname,
                                            "lastname": lastname,
                                            "dateofbirth": (
                                                patient_response.get(
                                                    "data", {"data": {}}
                                                ).get("birthDate", None)
                                            ),
                                            "sex": (
                                                patient_response.get(
                                                    "data", {"data": {}}
                                                ).get("gender", None)
                                            ),
                                            "mrn": None,
                                            "ssn": None,
                                            "status": patient_response.get(
                                                "data", {"data": {}}
                                            ).get("active", None),
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
            self.destination_json["firstname"] = firstname
            self.destination_json["lastname"] = lastname
            self.destination_json["dob"] = self.destination_json["dob"]
            self.destination_json["gender"] = self.source_json.get("gender").lower()
            patient_response, status_code = patient.get_patient_by_name(
                **self.destination_json
            )
            if status_code != 200:
                return Response(
                    {"detail": "Not data found in EHR", "statuscode": status_code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            patient_id = patient_response.get("data", {"data": {}}).get(
                "identifier", []
            )
            for identifier in patient_id:
                if identifier.get("use") == "usual":
                    patient_id = identifier.get("value")
            try:
                PatientModel.objects.get(ehr_id=patient_id)
                return Response({"detail": "Patient already imported"}, status=400)
            except PatientModel.DoesNotExist:
                if status_code == 200:
                    if patient_response.get("total") == 0:
                        self.destination_response["potentialmatches"] = []
                    else:
                        try:
                            PatientModel.objects.get(ehr_id=patient_id)
                        except PatientModel.DoesNotExist:
                            emailadress = None
                            patient_details = patient_response.get(
                                "data", {"data": {}}
                            ).get("name", [])
                            for detail in patient_details:
                                firstname = detail.get("given", [])[0]
                                lastname = detail.get("family", None)
                            self.destination_response["potentialmatches"].append(
                                {
                                    "id": str(patient_id),
                                    "firstname": firstname,
                                    "lastname": lastname,
                                    "dateofbirth": (
                                        patient_response.get("data", {"data": {}}).get(
                                            "birthDate", None
                                        )
                                    ),
                                    "sex": (
                                        patient_response.get("data", {"data": {}}).get(
                                            "gender", None
                                        )
                                    ),
                                    "mrn": None,
                                    "ssn": None,
                                    "status": patient_response.get(
                                        "data", {"data": {}}
                                    ).get("active", None),
                                    "emailaddress": emailadress,
                                }
                            )
                else:
                    del self.destination_response["potentialmatches"]
                    self.destination_response.update(
                        {"errormessage": patient_response, "statuscode": status_code}
                    )

        return self.destination_response
