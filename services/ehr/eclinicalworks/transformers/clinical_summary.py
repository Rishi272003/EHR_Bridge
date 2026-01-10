import base64
import io
import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

from django.db import transaction
from django.utils.dateparse import parse_datetime
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from ecaremd.careplan.models import Condition, ICDCode
from ecaremd.core.api.serializers.lab import LabResultFileSerializer
from ecaremd.core.constants import ADDRESS_STATE_CHOICES
from ecaremd.core.models.allergy import Allergy as PatientAllergyModel
from ecaremd.core.models.condition import PatientCondition
from ecaremd.core.models.lab import LabResult as PatientLabResult
from ecaremd.core.models.medication import Medication as PatientMedicationModel
from ecaremd.core.models.patient import CCDADocument
from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.core.models.vital import Vital as PatientVitalModel
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.Chart import Chart
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.DiagnosticReport import (
    DiagnosticReport,
)
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.DocumentReference import (
    DocumentReference,
)
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.categories.Organization import (
    Organization,
)
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer
from ecaremd.provider_group.models import ProviderGroup


class PatientQueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, ehr_name, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.temp_response = {}
        self.ehr_name = ehr_name
        self.patient_provider_group = None
        self.patient_obj = None

    def transform(self, events):
        patient = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient.authenticate()

        provider_group = self.source_json.get("pg_id")
        try:
            self.patient_provider_group = ProviderGroup.objects.get(id=provider_group)
        except ProviderGroup.DoesNotExist:
            return Response({"detail": "Provider Group not found"}, status=400)
        self.destination_json["start_date"] = self.source_json.get("startdate")
        self.destination_json["end_date"] = self.source_json.get("enddate")
        if isinstance(self.source_json.get("patientid"), list):
            for single_patient in self.source_json.get("patientid"):
                self.destination_json["patientid"] = single_patient

                try:
                    self.patient_obj = PatientModel.objects.get(
                        ehr_id=self.destination_json["patientid"]
                    )
                    return Response(
                        {
                            "detail": f"Patient  {self.patient_obj.first_name} {self.patient_obj.last_name} is already imported."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                except PatientModel.DoesNotExist:
                    for event in events:
                        event = event.lower()

                        # Demographics Data
                        if event == "demographics" or event == "all":
                            self.patient_demographics_status = (
                                self.get_patient_demographics()
                            )
                            print(
                                "Self.patient demographics status",
                                self.patient_demographics_status,
                                self.patient_obj,
                            )
                        if self.patient_demographics_status == 201 and self.patient_obj:
                            try:
                                # Conditions Data
                                if event == "conditions" or event == "all":
                                    created_repsonse = self.create_conditions_entries()
                                    self.destination_response.update(created_repsonse)
                                # Allergy Data
                                if event == "allergies" or event == "all":
                                    created_repsonse = self.create_allergies_entries()
                                    self.destination_response.update(created_repsonse)
                                # Medication Data
                                if event == "medications" or event == "all":
                                    created_repsonse = (
                                        self.medication_from_ccda()
                                    )  # function changed
                                    self.destination_response.update(created_repsonse)
                                # Lab Result Data
                                if event == "labresult" or event == "all":
                                    created_repsonse = self.create_lab_result_entries()
                                    self.destination_response.update(created_repsonse)
                                # Vitals Data
                                if event == "vitals" or event == "all":
                                    created_repsonse = self.create_vitals_entries()
                                    self.destination_response.update(created_repsonse)
                                # Document Data
                                if event == "Documents" or event == "all":
                                    created_repsonse = self.patient_document()
                                    self.destination_response.update(created_repsonse)
                            except Exception as e:
                                PatientModel.objects.get(
                                    ehr_id=self.patient_obj.ehr_id
                                ).delete()
                                self.destination_response.update(
                                    {"erromsg": str(e), "status_code": 400}
                                )
                                return Response(
                                    {
                                        "detail": f"Patient not imported due to some error {str(e)}"
                                    },
                                    status=400,
                                )
                        else:
                            self.destination_response.update(
                                {"errormsg": "Patient not imported", "status_code": 400}
                            )
            return self.destination_response

    def get_patient_demographics(self):
        result = None
        patient = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient.authenticate()
        (
            patient_response,
            status_code,
        ) = patient.get_patient_demographics(
            patient.practice_id, **self.destination_json
        )
        if status_code == 200 and patient_response.get("entry"):
            for patient_data in patient_response.get("entry"):
                self.temp_response = {}
                patient_info = patient_data.get("resource")
                self.temp_response["id"] = patient_info.get("id")
                if "identifier" in patient_info:
                    for ids in patient_info.get("identifier"):
                        if ids["use"] == "secondary":
                            self.temp_response["mrn"] = ids["value"]
                for patient_name in patient_info.get("name"):
                    if "given" in patient_name:
                        self.temp_response["first_name"] = patient_name.get("given")[0]
                        self.temp_response["middle_name"] = (
                            patient_name.get("given")[1]
                            if len(patient_name.get("given")) > 1
                            else None
                        )
                        self.temp_response["last_name"] = patient_name.get("family")

                        self.temp_response["dob"] = patient_info.get("birthDate")
                        self.temp_response["sex"] = (
                            patient_info.get("gender").title()
                            if patient_info.get("gender")
                            else None
                        )
                        self.temp_response["marital_status"] = (
                            patient_info.get("maritalStatus").get("text")
                            if patient_info.get("maritalStatus")
                            else None
                        )

                if patient_info.get("address"):
                    for patient_address in patient_info.get("address"):
                        if patient_address.get("use") == "home":
                            if patient_address.get("line"):
                                for line, address in enumerate(
                                    patient_address.get("line"),
                                    start=1,
                                ):
                                    self.temp_response[f"address_line_{line}"] = address
                            self.temp_response["city"] = patient_address.get("city")
                            patient_state = {
                                name: abbreviation
                                for abbreviation, name in ADDRESS_STATE_CHOICES
                            }
                            self.temp_response["state"] = (
                                patient_state.get(patient_address.get("state").title())
                                if patient_address.get("state")
                                else None
                            )
                            self.temp_response["country"] = patient_address.get(
                                "country"
                            )
                            self.temp_response["zip"] = patient_address.get(
                                "postalCode"
                            )

                if patient_info.get("telecom"):
                    for contacts in patient_info.get("telecom"):
                        if contacts.get("system") == "email":
                            self.temp_response["email"] = contacts.get("value")
                        if contacts.get("use") == "mobile":
                            self.temp_response["primary_phone"] = (
                                contacts.get("value").replace("-", "")
                                if contacts.get("value")
                                else None
                            )
                        if contacts.get("use") == "home":
                            self.temp_response["home_phone"] = (
                                contacts.get("value").replace("-", "")
                                if contacts.get("value")
                                else None
                            )
                        if contacts.get("use") == "work":
                            self.temp_response["work_phone"] = (
                                contacts.get("value").replace("-", "")
                                if contacts.get("value")
                                else None
                            )

            self.temp_response["provider_group"] = self.patient_provider_group
            self.temp_response["ehr_name"] = self.ehr_name
            self.destination_response.update(
                {
                    "success": patient_response,
                    "statuscode": status_code,
                }
            )
            result = super().create_patient(**self.temp_response)
            try:
                self.patient_obj = PatientModel.objects.get(
                    ehr_id=self.destination_json["patientid"]
                )
            except Exception as e:
                return Response(
                    {"detail": f"Patient not imported.{str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return result
        else:
            self.destination_response.update(
                {
                    "errormessage": patient_response,
                    "statuscode": status_code,
                }
            )
        return 400

    def create_patient_insurance_payload(self):
        patients_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patients_chart.authenticate()
        self.destination_json["patient"] = self.patient_obj

        insurance_response, status_code = patients_chart.get_patient_insurance(
            patients_chart.practice_id, **self.destination_json
        )
        insurance_payloads = []
        if status_code == 200 and insurance_response.get("entry"):
            if insurance_response.get("entry"):
                for insurance in insurance_response.get("entry"):
                    resource = insurance.get("resource", {})
                    insurance_payload = {}

                    insurance_payload["effective_date"] = resource.get("meta", {}).get(
                        "lastUpdated"
                    )
                    type_info = resource.get("type", {})

                    insurance_payload["name"] = type_info.get("text")

                    relatable = (
                        resource.get("relationship", {}).get("text")
                        if resource.get("relationship")
                        else None
                    )
                    if relatable:
                        insurance_payload["relation_to_insured"] = resource.get(
                            "relationship", {}
                        ).get("text")

                    payors = resource.get("payor", [])
                    insurance_organization = Organization(
                        self.customer_id, self.tenant_name, self.source_json
                    )
                    insurance_organization.authenticate()
                    if isinstance(payors, list) and payors:
                        for payor in payors:
                            reference = payors[0].get("reference", "")
                            organizatio_id = (
                                reference.split("/")[1] if "/" in reference else None
                            )
                            if not organizatio_id:
                                continue
                            (
                                organization_response,
                                status_code,
                            ) = insurance_organization.get_organization(
                                insurance_organization.practice_id, organizatio_id
                            )
                            if status_code == 200 and organization_response:
                                insurance_payload[
                                    "company_name"
                                ] = organization_response.get("name")
                                telecoms = organization_response.get("telecom", [])
                                for contact in telecoms:
                                    system = contact.get("system")
                                    value = (
                                        contact.get("value", "")
                                        .replace(" ", "")
                                        .strip()
                                    )
                                    use = contact.get("use", "")

                                    if (
                                        system == "phone"
                                        and not insurance_payload["company_phone"]
                                    ):
                                        # Prioritize phone with 'home' use
                                        if use == "home":
                                            insurance_payload["company_phone"] = value
                                        elif not any(
                                            t.get("use") == "home" for t in telecoms
                                        ):
                                            # Fallback to first phone if no 'home' phone exists
                                            insurance_payload["company_phone"] = value

                                    if (
                                        system == "email"
                                        and not insurance_payload["company_email"]
                                    ):
                                        insurance_payload["company_email"] = value

                    # Append only if we got something useful
                    if any(insurance_payload.values()):
                        insurance_payloads.append(insurance_payload)
            return insurance_payloads
        else:
            return False

    def create_allergies_entries(self):
        patients_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patients_chart.authenticate()
        self.destination_json["patient"] = self.patient_obj.ehr_id

        allergies_response, status_code = patients_chart.get_patient_allergy(
            patients_chart.practice_id, **self.destination_json
        )
        if status_code == 200:
            if allergies_response.get("total") > 0:
                for allergy in allergies_response.get("entry"):
                    allergies_payload = {}
                    code = allergy.get("resource", {}).get("code", {})
                    if code:
                        allergies_payload["name"] = code.get("text")
                        for coding in code.get("coding", []):
                            if coding.get("display"):
                                allergies_payload["name"] = coding["display"]

                    severity = None
                    reaction = None
                    for reaction_item in allergy.get("resource", {}).get(
                        "reaction", []
                    ):
                        for manifestation in reaction_item.get("manifestation", []):
                            reaction = manifestation.get("text")

                    recorded_date = allergy.get("resource", {}).get("recordedDate")
                    formatted_date = None
                    if recorded_date:
                        date_obj = datetime.fromisoformat(
                            recorded_date.replace("Z", "+00:00")
                        )
                        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

                    allergies_payload.update(
                        {
                            "patientid": self.patient_obj,
                            "created_date": formatted_date,
                            "severity": severity,
                            "reaction": reaction,
                        }
                    )
                    exists = PatientAllergyModel.objects.filter(
                        patient=self.patient_obj, name=allergies_payload["name"]
                    ).exists()
                    if not exists:
                        super().add_allergies(**allergies_payload)
                self.destination_response.update(
                    {"message": "Allergies imported successfully", "statuscode": 200}
                )

        else:
            self.destination_response.update(
                {"erromsg": allergies_response, "status_code": status_code}
            )
        return self.destination_response

    def create_medications_entries(self):
        patient_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient_chart.authenticate()
        self.destination_json["patient"] = self.patient_obj.ehr_id

        medications_response, status_code = patient_chart.get_patient_medication(
            patient_chart.practice_id, **self.destination_json
        )

        if status_code == 200 and medications_response.get("entry"):
            for medication in medications_response.get("entry"):
                resource = medication.get("resource", {})
                dosage = resource.get("dosage", {})
                route_text = dosage.get("route", {}).get("text", "").lower()

                medication_payload = {
                    "patientid": self.patient_obj,
                    "status": "historical"
                    if resource.get("status") == "completed"
                    else "active",
                }

                # Set route
                route_map = {
                    "iv": "Intravenous",
                    "im": "Intramuscular",
                    "oral": "Oral",
                }
                medication_payload["route"] = route_map.get(route_text)

                # Set medication name
                med_codeable = resource.get("medicationCodeableConcept", {})
                medication_payload["name"] = med_codeable.get("text")

                # Set dose + unit
                dose = dosage.get("dose", {})
                medication_payload["unit"] = dose.get("code")
                medication_payload["sig"] = dose.get("value")

                # Save medication
                super().add_medications(**medication_payload)
            self.destination_response.update(
                {
                    "message": "Medications imported successfully",
                    "statuscode": 200,
                }
            )

        else:
            self.destination_response.update(
                {"erromsg": medications_response, "status_code": status_code}
            )
        return self.destination_response

    def create_conditions_entries(self):
        patient_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient_chart.authenticate()
        self.destination_json["patient"] = self.patient_obj.ehr_id
        self.destination_json["category"] = "problem-list-item"
        (
            conditions_response,
            status_code,
        ) = patient_chart.get_patient_diagnoses(
            patient_chart.practice_id, **self.destination_json
        )
        if status_code == 200:
            if conditions_response.get("total") > 0:
                for single_record in conditions_response.get("entry"):
                    condition_payload = {}
                    if single_record.get("resource").get("code"):
                        if single_record.get("resource").get("code").get("coding"):
                            for single_code in (
                                single_record.get("resource").get("code").get("coding")
                            ):
                                if (
                                    single_code.get("system")
                                    == "http://hl7.org/fhir/sid/icd-10-cm"
                                ):
                                    ehr_icd_code = single_code.get("code")
                                    ehr_icd_name = single_code.get("display")
                                    existing_code_name = Condition.objects.filter(
                                        title=ehr_icd_name
                                    ).first()
                                    if existing_code_name:
                                        condition_payload[
                                            "condition"
                                        ] = existing_code_name

                                    else:
                                        new_code_name = Condition.objects.create(
                                            title=ehr_icd_name,
                                        )
                                        condition_payload["condition"] = new_code_name
                                    if single_record.get("resource").get(
                                        "recordedDate"
                                    ):
                                        converted_date = datetime.fromisoformat(
                                            single_record.get("resource").get(
                                                "recordedDate"
                                            )
                                        )
                                        condition_payload[
                                            "start_date"
                                        ] = converted_date.strftime("%Y-%m-%d")

                                    else:
                                        condition_payload["start_date"] = None
                                    existing_icd_code = ICDCode.objects.filter(
                                        code=ehr_icd_code
                                    ).first()
                                    if existing_icd_code:
                                        condition_payload["icdcode"] = existing_icd_code

                                    else:
                                        new_icd_code = ICDCode.objects.create(
                                            title=ehr_icd_name,
                                            code=ehr_icd_code,
                                        )
                                        condition_payload["icdcode"] = new_icd_code
                                    condition_payload["patientid"] = self.patient_obj

                                    if single_record["resource"]["category"][0][
                                        "text"
                                    ] in ["Problem List Item", "Encounter Diagnosis"]:
                                        exists = PatientCondition.objects.filter(
                                            patient=self.patient_obj,
                                            condition__title=condition_payload[
                                                "condition"
                                            ].title,
                                        ).exists()
                                        if not exists:
                                            super().add_conditions(**condition_payload)
        else:
            self.destination_response.update(
                {"conditions": conditions_response, "status_code": status_code}
            )
        return self.destination_response

    def extract_medications(self, xml_string):
        ns = {"hl7": "urn:hl7-org:v3"}
        medications = []

        try:
            root = ET.fromstring(xml_string)

            # Find all medication entries using the LOINC code "10160-0" which maps to Medications
            for section in root.findall(".//hl7:section", ns):
                code = section.find("hl7:code", ns)
                if code is not None and code.attrib.get("code") == "10160-0":
                    # Now process medication table under this section
                    rows = section.findall(".//hl7:table//hl7:tbody//hl7:tr", ns)
                    for row in rows:
                        cells = row.findall("hl7:td", ns)
                        if len(cells) >= 6:
                            medication = {
                                "name": cells[0].text.strip()
                                if cells[0].text
                                else None,
                                "comment": cells[1].text.strip()
                                if cells[1].text
                                else None,
                                "notes": cells[2].text.strip()
                                if cells[2].text
                                else None,
                                "created_date": cells[3].text.strip()
                                if cells[3].text
                                else None,
                                "deleted_date": cells[4].text.strip()
                                if cells[4].text
                                else None,
                                "status": cells[5].text.strip()
                                if cells[5].text
                                else None,
                            }
                            medications.append(medication)
                    break
        except Exception as e:
            print(f"Error while parsing XML: {str(e)}")
        return medications

    def medication_from_ccda(self):
        patient_ccda = DocumentReference(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_ccda.authenticate()

        self.destination_json["category"] = "clinical-note"
        self.destination_json["patientid"] = self.patient_obj.ehr_id
        patient_ccda_record, status_code = patient_ccda.search_patient_documents(
            patient_ccda.practice_id, **self.destination_json
        )
        actual_medication = None
        if status_code == 200:
            if patient_ccda_record.get("total") >= 1:
                ccda_entries = patient_ccda_record.get("entry")
                if ccda_entries:
                    for single_ccda in ccda_entries:
                        data = (
                            single_ccda.get("resource").get("data")
                            if single_ccda.get("resource")
                            else None
                        )
                        if data is not None:
                            decoded_bytes = base64.b64decode(data)
                            xml_string = decoded_bytes.decode("utf-8")
                            actual_medication = self.extract_medications(xml_string)

            else:
                self.destination_response.update(
                    {"errormessage": "No medication found"}
                )
                self.destination_response.update({"statuscode": status_code})
                return self.destination_response
            for single_medication in actual_medication:
                single_medication["patientid"] = self.patient_obj
                single_medication["status"] = (
                    "active"
                    if single_medication.get("status") == "In Progress"
                    else "historical"
                )
                if single_medication.get("created_date"):
                    single_medication["created_date"] = datetime.strptime(
                        single_medication["created_date"], "%m/%d/%Y"
                    )

                if single_medication.get("deleted_date"):
                    single_medication["deleted_date"] = datetime.strptime(
                        single_medication["deleted_date"], "%m/%d/%Y"
                    )
                exists = PatientMedicationModel.objects.filter(
                    patient=self.patient_obj, medicine=single_medication["name"]
                ).exists()
                if not exists:
                    super().add_medications(**single_medication)
        else:
            self.destination_response.update(
                {"medication response": patient_ccda_record, "status_code": status_code}
            )
        return self.destination_response

    def create_vitals_entries(self):
        patient_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient_chart.authenticate()
        self.destination_json["category"] = "vital-signs"
        self.destination_json["patient"] = self.patient_obj.ehr_id
        vitals_response, status_code = patient_chart.get_patient_vitals(
            patient_chart.practice_id, **self.destination_json
        )
        if status_code == 200:
            if vitals_response.get("total") > 0:
                vital_obj = {}
                for vital in vitals_response.get("entry"):
                    vital_name = vital.get("resource").get("code").get("text")
                    vital_quantity = (
                        vital.get("resource").get("valueQuantity")
                        if vital.get("resource").get("valueQuantity")
                        else None
                    )
                    if "temperature" in vital_name.lower():
                        vital_obj["type"] = "body_temperature"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj

                        vital_obj["value"] = (
                            (
                                (
                                    vital.get("resource")
                                    .get("valueQuantity")
                                    .get("value")
                                    - 32
                                )
                                * 5
                                / 9
                            )
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "c"
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if vital_name == "BMI":
                        vital_obj["type"] = "bmi"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj
                        vital_obj["value"] = (
                            (vital.get("resource").get("valueQuantity").get("value"))
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = (
                            vital_quantity.get("unit")
                            if vital_quantity and vital_quantity.get("unit")
                            else ""
                        )
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if "Height" in vital_name:
                        vital_obj["type"] = "height"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj
                        vital_obj["value"] = (
                            (
                                vital.get("resource").get("valueQuantity").get("value")
                                / 39.37
                            )
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "m"
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if vital_name == "Blood pressure":
                        if vital.get("resource").get("component"):
                            for single_vital in vital.get("resource").get("component"):
                                if single_vital.get("code").get("coding"):
                                    for single_coding_vital in single_vital.get(
                                        "code"
                                    ).get("coding"):
                                        vital_quantity = single_vital.get(
                                            "valueQuantity"
                                        )
                                        if (
                                            single_coding_vital.get("display")
                                            == "Systolic blood pressure"
                                        ):
                                            vital_obj["value"] = (
                                                single_vital.get("valueQuantity").get(
                                                    "value"
                                                )
                                                if vital_quantity
                                                and vital_quantity.get("value")
                                                else 0.0
                                            )

                                        if (
                                            single_coding_vital.get("display")
                                            == "Diastolic blood pressure"
                                        ):
                                            vital_obj["diastolic"] = (
                                                single_vital.get("valueQuantity").get(
                                                    "value"
                                                )
                                                if vital_quantity
                                                and vital_quantity.get("value")
                                                else 0.0
                                            )

                            vital_obj["type"] = "blood_pressure"
                            vital_obj["units"] = "mmHg"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = self.patient_obj
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=self.patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)

                    if "Weight" in vital_name:
                        vital_obj["type"] = "weight"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj
                        if vital_quantity.get("unit") == "kg":
                            vital_obj["value"] = (
                                (
                                    vital.get("resource")
                                    .get("valueQuantity")
                                    .get("value")
                                    * 0.453592
                                )
                                if vital_quantity and vital_quantity.get("value")
                                else 0.0
                            )

                        elif vital_quantity.get("unit") == "lbs":
                            vital_obj["value"] = (
                                (
                                    vital.get("resource")
                                    .get("valueQuantity")
                                    .get("value")
                                )
                                if vital_quantity and vital_quantity.get("value")
                                else 0.0
                            )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "lbs"
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if "Heart Rate" in vital_name:
                        vital_obj["type"] = "heart_rate"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj

                        vital_obj["value"] = (
                            (vital.get("resource").get("valueQuantity").get("value"))
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = (
                            (vital.get("resource").get("valueQuantity").get("unit"))
                            if vital_quantity and vital_quantity.get("unit")
                            else ""
                        )
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if vital_name == "Oximetry":
                        vital_obj["type"] = "o2_saturation"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj

                        vital_obj["value"] = (
                            (vital.get("resource").get("valueQuantity").get("value"))
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = (
                            vital.get("resource").get("valueQuantity").get("unit")
                        )
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                    if vital_name == "Respiratory Rate":
                        vital_obj["type"] = "respiration_rate"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = self.patient_obj

                        vital_obj["value"] = (
                            (vital.get("resource").get("valueQuantity").get("value"))
                            if vital_quantity and vital_quantity.get("value")
                            else 0.0
                        )

                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "BPM"
                        recorded_at = parse_datetime(vital_obj["created_date"])
                        exists = PatientVitalModel.objects.filter(
                            patient=self.patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=recorded_at,
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

        else:
            self.destination_response.update(
                {"erromsg": vitals_response, "status_code": status_code}
            )
        return self.destination_response

    def create_lab_result_entries(self):
        patients_chart = Chart(self.customer_id, self.tenant_name, self.source_json)
        patients_chart.authenticate()
        self.destination_json["patient"] = self.patient_obj.ehr_id
        lab_result_response, status_code = patients_chart.get_patient_lab_result(
            patients_chart.practice_id, **self.destination_json
        )
        if status_code == 200:
            if lab_result_response.get("total") > 0:
                for labresult in lab_result_response.get("entry"):
                    lab_result_payload = {}
                    lab_result_payload["value"] = (
                        labresult.get("resource", {})
                        .get("valueQuantity", {})
                        .get("value")
                    )
                    lab_result_payload["patient"] = self.patient_obj
                    lab_result_payload["lab_result_for"] = (
                        labresult.get("resource").get("code").get("text")
                        if labresult.get("resource").get("code")
                        else None
                    )
                    if labresult.get("resource").get("issued"):
                        lab_result_payload["issued"] = labresult.get("resource").get(
                            "issued"
                        )
                    if lab_result_payload["value"]:
                        try:
                            with transaction.atomic():
                                exists = PatientLabResult.objects.filter(
                                    patient=self.patient_obj,
                                    lab_result_for=lab_result_payload["lab_result_for"],
                                ).exists()
                                if not exists:
                                    super().add_lab_result(**lab_result_payload)
                        except Exception as e:
                            return Response(
                                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                            )

        else:
            self.destination_response.update(
                {"erromsg": lab_result_response, "status_code": status_code}
            )
        return self.destination_response

    def convert_plain_text_base64_to_pdf(self, encoded_str: str) -> str:
        # Remove the data URI scheme (if any)
        _, base64_data = encoded_str.split(
            ",", 1
        )  # split the encoded base64 data from data uri
        decoded_text = base64.b64decode(base64_data).decode("utf-8")
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        text_obj = c.beginText(40, 800)  # make a on fly pdf document

        for line in decoded_text.splitlines():
            text_obj.textLine(line)  # adding each line of decoded text into pdf file

        c.drawText(text_obj)
        c.save()

        buffer.seek(0)
        pdf_base64 = base64.b64encode(buffer.read()).decode(
            "utf-8"
        )  # making a data uri for .pdf file.
        return f"data:application/pdf;base64,{pdf_base64}"

    def patient_document(self):
        patient_document = DiagnosticReport(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_document.authenticate()

        self.destination_json["patient"] = self.patient_obj.ehr_id
        self.destination_json["category"] = "LAB"
        document_response, status_code = patient_document.get_diagnostic_report(
            patient_document.practice_id, **self.destination_json
        )
        if status_code == 200:
            if document_response.get("total") > 0:
                for document in document_response.get("entry"):
                    resource = document.get("resource", {})
                    document_payload = {}
                    document_payload["patient"] = self.patient_obj

                    if resource.get("code"):
                        document_payload["name"] = resource["code"].get("text")
                    if resource.get("issued"):
                        document_payload["created_date"] = resource["issued"]
                    if "presentedForm" in resource:
                        base64_data = resource.get("presentedForm")
                        for encoded_data in base64_data:
                            content_type = encoded_data.get(
                                "contentType"
                            )  # e.g., text/plain
                            base64_str = encoded_data.get("data")
                            encoded_str = f"data:{content_type};base64,{base64_str}"

                            # Convert only if it's a plain text file
                            if content_type == "text/plain":
                                encoded_str = self.convert_plain_text_base64_to_pdf(
                                    encoded_str
                                )
                                content_type = "application/pdf"  # update content type

                            serialized_file = LabResultFileSerializer(
                                data={"file": encoded_str}
                            )
                            serialized_file.is_valid(raise_exception=True)
                            document_payload[
                                "file"
                            ] = serialized_file.validated_data.get("file")

                        # Save document using method - assuming this uses a serializer or model save
                        self.add_documents(**document_payload)
                        self.destination_response.update(
                            {"document_response": document_response, "status_code": 200}
                        )
        else:
            self.destination_response.update(
                {"patient_documents": document_response, "status_code": status_code}
            )
        return self.destination_response


class PatientCCDA(Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_response = {}

    def transform(self):
        patientid = self.source_json.get("patientid")

        patient_ccda = DocumentReference(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_ccda.authenticate()

        self.destination_json["category"] = "clinical-note"
        self.destination_json["patientid"] = patientid
        patient_ccda_record, status_code = patient_ccda.search_patient_documents(
            patient_ccda.practice_id, **self.destination_json
        )
        if status_code == 200 and patient_ccda_record.get("entry"):
            for single_clinical_docs in patient_ccda_record.get("entry"):
                if single_clinical_docs.get("resource").get("resourceType") == "Binary":
                    CCDA_record_id = single_clinical_docs.get("resource").get("id")
            binaryid = CCDA_record_id
            patient_ccda_actual_record, status_code = patient_ccda.get_patient_ccda(
                patient_ccda.practiceid, binaryid, **self.destination_json
            )
            if status_code == 200:
                patient_obj = PatientModel.objects.get(ehr_id=patientid)
                file_name = f"CCDA_{patientid}.xml"
                ccda_data_io = io.BytesIO(patient_ccda_actual_record)
                ccda_doc = CCDADocument(patient=patient_obj)
                ccda_doc.file.save(file_name, ccda_data_io, save=True)

                self.destination_response.update({"success": True})

        else:
            self.destination_response.update(
                {"errormesssage": patient_ccda_record, "statuscode": status_code}
            )
        return self.destination_response


class DocumentNewTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)

    def transform(self):
        document_object = {}
        self.destination_json = {"entry": []}
        patientid = self.source_json.get("patientid")
        filecontents = self.source_json.get("filecontents")
        providerid = self.source_json.get("providerid")
        creation_date = self.source_json.get("created_date")
        documenttype = self.source_json.get("documenttype")
        document_object["resourceType"] = "DocumentReference"
        document_object["status"] = "final"
        document_object["subject"] = {"reference": f"Patient/{patientid}"}
        document_object["author"] = [{"reference": f"Practitioner/{providerid}"}]
        document_object["content"] = [
            {
                "attachment": {
                    "contentType": f"application/{documenttype}",
                    "data": filecontents,
                    "creation": creation_date,
                }
            }
        ]

        document_object["authenticator"] = {"reference": f"Practitioner/{providerid}"}
        self.destination_json["resourceType"] = "Bundle"
        self.destination_json["type"] = "transaction"
        self.destination_json["entry"].append(document_object)
        document_reference = DocumentReference(
            self.customer_id, self.tenant_name, self.source_json
        )
        document_reference.authenticate()
        document_push_response, status_code = document_reference.new_clinical_note(
            **self.destination_json
        )
        if status_code == 200:
            self.destination_response["documentid"] = document_push_response.get("id")
        else:
            self.destination_response.update(
                {
                    "errormessage": document_push_response,
                    "status_code": status_code,
                },
            )
        return self.destination_response


class PatientQuerySyncTransformer(PatientQueryTransformer):
    def __init__(self, source_data, customer_id, ehr_name, tenant_name):
        super().__init__(source_data, customer_id, ehr_name, tenant_name)
        self.temp_response = {}
        self.ehr_name = ehr_name
        self.patient_provider_group = None
        self.patient_obj = None

    def transform(self, events):
        patient = Chart(self.customer_id, self.tenant_name, self.source_json)
        patient.authenticate()
        provider_group = self.source_json.get("pg_id")

        try:
            self.patient_provider_group = ProviderGroup.objects.get(id=provider_group)
        except ProviderGroup.DoesNotExist:
            return Response({"detail": "Provider Group not found"}, status=400)
        patient_id = self.source_json.get("patientid")

        try:
            self.patient_obj = PatientModel.objects.get(
                id=patient_id, provider_group=self.patient_provider_group
            )
        except PatientModel.DoesNotExist:
            return Response({"detail": "Patient does not found"}, status=400)

        for event in events:
            if event == "allergies" or event == "all":
                created_repsonse = self.create_allergies_entries()
                self.destination_response.update(created_repsonse)
            if event == "medications" or event == "all":
                created_repsonse = self.medication_from_ccda()  # function changed
                self.destination_response.update(created_repsonse)
            if event == "labresult" or event == "all":
                created_repsonse = self.create_lab_result_entries()
                self.destination_response.update(created_repsonse)
            if event == "conditions" or event == "all":
                created_repsonse = self.create_conditions_entries()
                self.destination_response.update(created_repsonse)
            if event == "vitals" or event == "all":
                created_repsonse = self.create_vitals_entries()
                self.destination_response.update(created_repsonse)

        return self.destination_response
