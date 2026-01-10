from rest_framework.response import Response

from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class PatientSearchTransformer(Transformer):
    def __init__(self, source_json, customer_id, tenant_name):
        super().__init__(source_json, customer_id, tenant_name)
        self.destination_json = {}
        self.destination_response["potentialmatches"] = []

    def transform(self):
        if self.source_json.get("patientid"):
            try:
                PatientModel.objects.get(ehr_id=self.source_json.get("patientid"))
                return Response({"detail": "Patient already imported"}, status=400)
            except PatientModel.DoesNotExist:
                patientid = self.source_json.get("patientid")
                patient = Patient(self.customer_id, self.tenant_name, self.source_json)
                self.destination_json["patientid"] = patientid
                patient.authenticate()
                (
                    patient_response,
                    status_code,
                ) = patient.get_patient_demographics_by_id(**self.destination_json)
                if status_code == 401:
                    return Response({"detail": "Provider Unauthorized"}, status=401)
                elif status_code == 200:
                    for patient in patient_response.get("entry"):
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
                                    patient.get("resource").get("name")[0].get("family")
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
        elif self.source_json.get("firstname") or self.source_json.get("lastname"):
            data = {}
            patient = Patient(self.customer_id, self.tenant_name, self.source_json)
            patient.authenticate()
            firstname = self.source_json.get("firstname")
            lastname = self.source_json.get("lastname")
            if firstname and not lastname:
                data = {"param": "given", "value": firstname}
            elif lastname and not firstname:
                data = {"param": "family", "value": lastname}
            else:
                data = {"param": "name", "value": firstname + " " + lastname}
            (
                patient_response,
                status_code,
            ) = patient.get_patient_demographics_by_name(data)
            if status_code == 401:
                return Response({"detail": "Provider Unauthorized"}, status=401)
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
                                    "status": patient.get("active"),
                                    "emailaddress": emailadress,
                                }
                            )

            else:
                del self.destination_response["potentialmatches"]
                self.destination_response.update(
                    {"errormessage": patient_response, "statuscode": status_code}
                )

        else:
            return Response(
                {"detail": "Fill at least any one patient information"}, status=400
            )

        return self.destination_response
