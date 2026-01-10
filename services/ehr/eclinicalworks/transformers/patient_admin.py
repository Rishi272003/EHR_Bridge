import re

from rest_framework import status
from rest_framework.response import Response

from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.Patient import (
    Patient,
)
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class NewPatientTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_json = {}

    def transform(self):
        try:
            new_patient = Patient(self.customer_id, self.tenant_name)
            new_patient.authenticate()

            self.destination_json["resourceType"] = "Bundle"
            self.destination_json["type"] = "transaction"
            self.destination_json["entry"] = []
            if self.source_json.get("demography"):
                self.destination_json["entry"].append(
                    {
                        "resourceType": "Patient",
                        "active": True,
                        "name": [
                            {
                                "use": "official",
                                "family": self.source_json.get("demography").get(
                                    "last_name"
                                ),
                                "given": [
                                    self.source_json.get("demography").get("first_name")
                                ],
                            }
                        ],
                        "telecom": [
                            {
                                "system": "phone",
                                "value": re.sub(
                                    r"\D",
                                    "",
                                    self.source_json.get("demography").get(
                                        "home_phone"
                                    ),
                                ),
                                "use": "home",
                            },
                            {
                                "system": "phone",
                                "value": re.sub(
                                    r"\D",
                                    "",
                                    self.source_json.get("demography").get(
                                        "work_phone"
                                    ),
                                ),
                                "use": "work",
                            },
                            {
                                "system": "email",
                                "value": self.source_json.get("demography").get(
                                    "email"
                                ),
                                "use": "home",
                            },
                        ],
                        "gender": self.source_json.get("demography").get("gender"),
                        "birthDate": self.source_json.get("demography").get(
                            "date_of_birth"
                        ),
                        "communication": [
                            {
                                "language": {
                                    "coding": [
                                        {
                                            "system": "urn:ietf:bcp:47",
                                            "code": "eng",
                                            "display": "English",
                                        }
                                    ],
                                    "text": "English",
                                }
                            }
                        ],
                        "address": {
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
                        },
                    }
                )

                patient_created, status_code = new_patient.create_new_patient(
                    **self.destination_json
                )
                if status_code == 201 or status_code == 200:
                    patient_res = {
                        "TransactionId": patient_created.get("id"),
                    }
                    self.destination_response.update(patient_res)
                    self.destination_response.update({"statuscode": status_code})
                else:
                    self.destination_response.update({"errormessage": patient_created})
                    self.destination_response.update({"statuscode": status_code})
                return self.destination_response

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
