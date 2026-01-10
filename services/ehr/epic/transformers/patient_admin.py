import re

from rest_framework import status
from rest_framework.response import Response

from ecaremd.ehr_integrations.ehr_services.epic.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class NewPatientTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_json = {}

    def transform(self):
        try:
            new_patient = Patient(self.customer_id, self.tenant_name)
            new_patient.authenticate()

            self.destination_json["resourceType"] = "Patient"
            self.destination_json["active"] = True

            if self.source_json.get("demography"):
                self.destination_json["name"] = [
                    {
                        "use": "official",
                        "family": self.source_json.get("demography").get("last_name"),
                        "given": [self.source_json.get("demography").get("first_name")],
                    }
                ]
                self.destination_json["generalPractitioner"] = [
                    {
                        "reference": f"Practitioner/{new_patient.customer.ehr_provider.ehr_id}"
                    }
                ]
                self.destination_json["telecom"] = [
                    {
                        "system": "phone",
                        "value": re.sub(
                            r"\D",
                            "",
                            self.source_json.get("demography").get("home_phone"),
                        ),
                        "use": "home",
                    },
                    {
                        "system": "phone",
                        "value": re.sub(
                            r"\D",
                            "",
                            self.source_json.get("demography").get("work_phone"),
                        ),
                        "use": "work",
                    },
                    {
                        "system": "email",
                        "value": self.source_json.get("demography").get("email"),
                        "use": "home",
                    },
                ]
                self.destination_json["gender"] = self.source_json.get(
                    "demography"
                ).get("gender")
                self.destination_json["birthDate"] = self.source_json.get(
                    "demography"
                ).get("date_of_birth")
                if self.source_json.get("demography").get("address"):
                    self.destination_json["address"] = [
                        {
                            "use": "home",
                            "line": [
                                self.source_json.get("demography")
                                .get("address")
                                .get("address_line_1")
                                if self.source_json.get("demography").get("address")
                                else None
                            ],
                            "city": self.source_json.get("demography")
                            .get("address")
                            .get("city")
                            if self.source_json.get("demography").get("address")
                            else None,
                            "state": self.source_json.get("demography")
                            .get("address")
                            .get("state")
                            if self.source_json.get("demography").get("address")
                            else None,
                            "postalCode": self.source_json.get("demography")
                            .get("address")
                            .get("zip")
                            if self.source_json.get("demography").get("address")
                            else None,
                            "country": "US",
                        }
                    ]

                self.destination_json["maritalStatus"] = {
                    "text": self.source_json.get("demography").get("marital_status"),
                }
                self.destination_json["communication"] = [
                    {
                        "language": {
                            "coding": [
                                {
                                    "system": "urn:ietf:bcp:47",
                                    "code": "en",
                                    "display": "English",
                                }
                            ],
                            "text": "English",
                        },
                        "preferred": True,
                    }
                ]
                self.destination_json["identifier"] = []
                self.destination_json["identifier"].append(
                    {
                        "use": "usual",
                        "system": "urn:oid:2.16.840.1.113883.4.1",
                        "value": self.source_json.get("demography").get("ssn"),
                    }
                )
                patient_created, status_code = new_patient.create_new_patient(
                    **self.destination_json
                )
                if status_code == 201:
                    patient_res = {
                        "PatientID": patient_created.get("Location").split("/")[-1],
                    }
                    self.destination_response.update(patient_res)
                    self.destination_response.update({"statuscode": status_code})
                else:
                    self.destination_response.update({"errormessage": patient_created})
                    self.destination_response.update({"statuscode": status_code})
                return self.destination_response

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
