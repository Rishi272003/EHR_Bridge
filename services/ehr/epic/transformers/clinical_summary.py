from datetime import datetime

from django.db import transaction
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response

from ecaremd.careplan.models import Condition as PatientConditions
from ecaremd.careplan.models import ICDCode
from ecaremd.core.constants import ADDRESS_STATE_CHOICES
from ecaremd.core.models.allergy import Allergy as PatientAllergyModel
from ecaremd.core.models.condition import PatientCondition as PatientConditionModel
from ecaremd.core.models.lab import LabResult as PatientLabResult
from ecaremd.core.models.medication import Medication as PatientMedicationModel
from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.core.models.vital import Vital as PatientVitalModel
from ecaremd.ehr_integrations.ehr_services.epic.categories.Administration import Patient
from ecaremd.ehr_integrations.ehr_services.epic.categories.Clinic import (
    AllergyIntolerance,
    Condition,
)
from ecaremd.ehr_integrations.ehr_services.epic.categories.Diagnostic import Observation
from ecaremd.ehr_integrations.ehr_services.epic.categories.List import List
from ecaremd.ehr_integrations.ehr_services.epic.categories.MedicationRequest import (
    MedicationRequest,
)
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer
from ecaremd.provider_group.models import ProviderGroup


class PatientQueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, ehr_name, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.temp_response = {}
        self.ehr_name = ehr_name

    def transform(self, events):
        try:
            if isinstance(self.source_json.get("patientid"), list):
                for single_patient in self.source_json.get("patientid"):
                    self.destination_json["patientid"] = single_patient
                    try:
                        provider_group = self.source_json.get("pg_id")
                    except ProviderGroup.DoesNotExist:
                        return Response(
                            {"detail": "Provider Group not found"}, status=400
                        )
                    try:
                        patient_obj = PatientModel.objects.get(
                            ehr_id=self.destination_json["patientid"]
                        )
                        return Response(
                            {
                                "detail": f"Patient  {patient_obj.first_name} {patient_obj.last_name} is already imported."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    except PatientModel.DoesNotExist:
                        for event in events:
                            event = event.lower()

                            # Demographic Data
                            if event == "demographics" or event == "all":
                                patient = Patient(
                                    self.customer_id, self.tenant_name, self.source_json
                                )
                                for single_pg in patient.customer.provider_group.all():
                                    provider_group = single_pg
                                patient.authenticate()

                                (
                                    patient_response,
                                    status_code,
                                ) = patient.get_specific_patient(
                                    self.destination_json["patientid"]
                                )

                                if status_code == 200:
                                    self.temp_response = {}
                                    self.temp_response["id"] = patient_response.get(
                                        "id"
                                    )
                                    for patient_name in patient_response.get("name"):
                                        if "given" in patient_name:
                                            self.temp_response[
                                                "first_name"
                                            ] = patient_name.get("given")[0]
                                            self.temp_response["middle_name"] = (
                                                patient_name.get("given")[1]
                                                if len(patient_name.get("given")) > 1
                                                else None
                                            )
                                            self.temp_response[
                                                "last_name"
                                            ] = patient_name.get("family")

                                    self.temp_response["dob"] = patient_response.get(
                                        "birthDate"
                                    )
                                    self.temp_response["sex"] = (
                                        patient_response.get("gender").title()
                                        if patient_response.get("gender")
                                        else "Other"
                                    )
                                    self.temp_response["marital_status"] = (
                                        patient_response.get("maritalStatus").get(
                                            "text"
                                        )
                                        if patient_response.get("maritalStatus")
                                        else None
                                    )

                                    if patient_response.get("extension"):
                                        for code in patient_response.get("extension"):
                                            if "race" in code.get("url").split("/")[-1]:
                                                for race_code in code.get("extension"):
                                                    if race_code.get("url") == "text":
                                                        self.temp_response["race"] = (
                                                            race_code.get(
                                                                "valueString"
                                                            ).title()
                                                            if race_code.get(
                                                                "valueString"
                                                            )
                                                            else None
                                                        )

                                    if patient_response.get("address"):
                                        for patient_address in patient_response.get(
                                            "address"
                                        ):
                                            if patient_address.get("use") == "home":
                                                self.temp_response[
                                                    "address_line_1"
                                                ] = patient_address.get("line")[0]
                                                self.temp_response[
                                                    "city"
                                                ] = patient_address.get("city")
                                                patient_state = {
                                                    name: abbreviation
                                                    for abbreviation, name in ADDRESS_STATE_CHOICES
                                                }
                                                self.temp_response["state"] = (
                                                    patient_state.get(
                                                        patient_address.get(
                                                            "state"
                                                        ).title()
                                                    )
                                                    if patient_address.get("state")
                                                    else None
                                                )

                                                self.temp_response[
                                                    "country"
                                                ] = patient_address.get("country")
                                                self.temp_response[
                                                    "zip"
                                                ] = patient_address.get("postalCode")

                                    if patient_response.get("telecom"):
                                        for contacts in patient_response.get("telecom"):
                                            if contacts.get("system") == "email":
                                                self.temp_response[
                                                    "email"
                                                ] = contacts.get("value")
                                            if contacts.get("use") == "mobile":
                                                self.temp_response["primary_phone"] = (
                                                    contacts.get("value").replace(
                                                        "-", ""
                                                    )
                                                    if contacts.get("value")
                                                    else None
                                                )
                                            if contacts.get("use") == "home":
                                                self.temp_response["home_phone"] = (
                                                    contacts.get("value").replace(
                                                        "-", ""
                                                    )
                                                    if contacts.get("value")
                                                    else None
                                                )
                                            if contacts.get("use") == "work":
                                                self.temp_response["work_phone"] = (
                                                    contacts.get("value").replace(
                                                        "-", ""
                                                    )
                                                    if contacts.get("value")
                                                    else None
                                                )

                                    self.temp_response[
                                        "provider_group"
                                    ] = provider_group
                                    self.temp_response["ehr_name"] = self.ehr_name
                                    super().create_patient(**self.temp_response)

                                else:
                                    self.destination_response.update(
                                        {
                                            "errormessage": patient_response,
                                            "statuscode": status_code,
                                        }
                                    )
                            # Allergy Data
                            if event == "allergies" or event == "all":
                                patientid = self.destination_json["patientid"]
                                created_response = self.create_allergies_entries(
                                    patientid
                                )
                                self.destination_response.update(created_response)

                                # Vitals
                                if event == "vitals" or event == "all":
                                    patientid = self.destination_json["patientid"]
                                    created_response = self.create_vitals_entries(
                                        patientid
                                    )
                                    self.destination_response.update(created_response)

                            # Medications
                            if event == "medications" or event == "all":
                                patientid = self.destination_json["patientid"]
                                created_response = self.create_medications_entries(
                                    patientid
                                )
                                self.destination_response.update(created_response)

                            # Conditions
                            if event == "conditions" or event == "all":
                                patientid = self.destination_json["patientid"]
                                created_response = self.create_conditions_entries(
                                    patientid
                                )
                                self.destination_response.update(created_response)

                            # Lab results
                            if event == "lab_result" or event == "all":
                                patientid = self.destination_json["patientid"]
                                created_response = self.create_lab_entries(patientid)
                                self.destination_response.update(created_response)

                return self.destination_response

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create_lab_entries(self, patient_id):
        patient_lab_entries = Observation(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_lab_entries.authenticate()
        self.destination_json["patientid"] = patient_id
        self.destination_json["category"] = "laboratory"
        (lab_result_response, status_code) = patient_lab_entries.search_labs(
            **self.destination_json
        )
        if status_code == 200 and lab_result_response.get("entry"):
            patient_obj = PatientModel.objects.get(ehr_id=patient_id)
            for labresult in lab_result_response.get("entry", []):
                resource = labresult.get("resource", {})
                lab_result_payload = {}

                # Prefer valueQuantity if present, fallback to valueString
                value = None
                if "valueQuantity" in resource:
                    value = resource["valueQuantity"].get("value")
                elif "valueString" in resource:
                    value = resource.get("valueString")
                lab_result_payload["value"] = value

                lab_result_payload["patient"] = patient_obj

                # Lab test name
                code = resource.get("code", {})
                lab_result_payload["lab_result_for"] = code.get("text")

                # Issued date
                if "issued" in resource:
                    lab_result_payload["issued"] = resource["issued"]

                # Optional text.div (not present in your sample, so default to None)
                text_section = resource.get("text", {})
                lab_result_payload["file"] = (
                    text_section.get("div") if text_section else None
                )

                if lab_result_payload["value"]:
                    try:
                        with transaction.atomic():
                            super().add_lab_result(**lab_result_payload)

                    except Exception as e:
                        return Response(
                            {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                        )

        else:
            self.destination_response.update({"errormessage": lab_result_response})
            self.destination_response.update({"statuscode": status_code})
        return self.destination_response

    def create_conditions_entries(self, patient_id):
        patient_problem = Condition(
            self.customer_id, self.tenant_name, self.source_json
        )
        self.destination_json["patientid"] = patient_id
        patient_problem.authenticate()
        (
            conditions_response,
            status_code,
        ) = patient_problem.search_problems(**self.destination_json)

        if (
            status_code == 200
            and conditions_response.get("entry")
            and conditions_response.get("total") >= 1
        ):
            patient_obj = PatientModel.objects.get(ehr_id=patient_id)
            condition_payload = {}
            for single_record in conditions_response.get("entry"):
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
                                existing_code_name = PatientConditions.objects.filter(
                                    title=ehr_icd_name
                                ).first()
                                if existing_code_name:
                                    condition_payload["condition"] = existing_code_name

                                else:
                                    new_code_name = PatientConditions.objects.create(
                                        title=ehr_icd_name,
                                    )
                                    condition_payload["condition"] = new_code_name

                                if single_record.get("resource").get("recordedDate"):
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
                                condition_payload["patientid"] = patient_obj

                                exists = PatientConditionModel.objects.filter(
                                    patient=patient_obj,
                                    condition=condition_payload["condition"],
                                ).exists()
                                if not exists:
                                    super().add_conditions(**condition_payload)

            self.destination_response["success"] = True

        else:
            self.destination_response.update(
                {
                    "errormessage": conditions_response,
                    "statuscode": status_code,
                }
            )
        return self.destination_response

    def create_allergies_entries(self, patient_id):
        patient = AllergyIntolerance(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient.authenticate()
        data = {
            "patient": self.destination_json["patientid"],
            "clinical-status": "active",
        }
        (
            allergies_response,
            status_code,
        ) = patient.search_allergy_intolerance(**data)

        if status_code == 200 and allergies_response.get("entry"):
            patient_obj = PatientModel.objects.get(ehr_id=patient_id)
            for allergy in allergies_response.get("entry"):
                allergies_payload = {}
                if allergy.get("resource").get("code"):
                    allergies_payload["name"] = (
                        allergy.get("resource").get("code").get("text")
                        if allergy.get("resource").get("code")
                        else None
                    )
                    if allergy.get("resource").get("code").get("coding"):
                        for single_allergy in (
                            allergy.get("resource").get("code").get("coding")
                        ):
                            if single_allergy.get("display"):
                                allergies_payload["name"] = single_allergy.get(
                                    "display"
                                )

                severity = None
                reaction = None
                if allergy.get("resource").get("reaction"):
                    for single_reaction in allergy.get("resource").get("reaction"):
                        for single_reaction_name in single_reaction.get(
                            "manifestation"
                        ):
                            reaction = single_reaction_name.get("text")

                formatted_date = None
                if allergy.get("resource").get("recordedDate"):
                    date_obj = datetime.fromisoformat(
                        allergy.get("resource")
                        .get("recordedDate")
                        .replace("Z", "+00:00")
                    )

                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                allergies_payload["patientid"] = patient_obj
                allergies_payload["created_date"] = formatted_date
                allergies_payload["severity"] = severity
                allergies_payload["reaction"] = reaction
                super().add_allergies(**allergies_payload)

        else:
            self.destination_response.update({"errormessage": allergies_response})
            self.destination_response.update({"statuscode": status_code})

        return self.destination_response

    def create_medications_entries(self, patient):
        patient_chart = List(self.customer_id, self.tenant_name, self.source_json)
        patient_medications = MedicationRequest(
            self.customer_id, self.tenant_name, self.source_json
        )

        # Authenticate for both services
        patient_medications.authenticate()
        patient_chart.authenticate()

        self.destination_json["patientid"] = patient
        medications_response, status_code = patient_chart.search_medications(
            **self.destination_json
        )

        if status_code != 200 or not medications_response.get("entry"):
            self.destination_response.update(
                {"errormessage": medications_response, "statuscode": status_code}
            )
            return self.destination_response

        patient_obj = PatientModel.objects.get(ehr_id=patient)
        inserted_count = 0

        for entry in medications_response["entry"]:
            list_resource = entry.get("resource")
            list_entries = list_resource.get("entry", [])

            for list_item in list_entries:
                medication_ref = list_item.get("item", {}).get(
                    "reference"
                )  # e.g., "MedicationRequest/xyz"
                if not medication_ref:
                    continue

                # Fetch MedicationRequest data
                med_request, med_status = patient_medications.get_orders(
                    medication_ref.split("/")[1]
                )
                if med_status != 200 or not med_request:
                    continue

                resource = med_request

                name = resource.get("medicationReference", {}).get("display")
                status = resource.get("status")
                route = None
                dosage = None
                dosage_text = None
                start_date = None

                dosage_instructions = resource.get("dosageInstruction", [])
                if dosage_instructions:
                    dosage_info = dosage_instructions[0]
                    dosage_text = dosage_info.get("text")
                    route = dosage_info.get("route", {}).get("text")

                    # Get the first valid doseQuantity
                    dose_and_rate = dosage_info.get("doseAndRate", [])
                    for rate in dose_and_rate:
                        dq = rate.get("doseQuantity")
                        if dq:
                            value = dq.get("value")
                            unit = dq.get("unit")
                            if value and unit:
                                dosage = f"{value} {unit}"
                                break

                    # Start date from timing boundsPeriod
                    start_date = (
                        dosage_info.get("timing", {})
                        .get("repeat", {})
                        .get("boundsPeriod", {})
                        .get("start")
                    )

                # Fallback to authoredOn if no start_date found
                if not start_date:
                    start_date = resource.get("authoredOn")

                medication_payload = {
                    "patient": patient_obj,
                    "name": name,
                    "status": "active" if status == "active" else "historical",
                    "route": route,
                    "dose": dosage,
                    "note": dosage_text,
                    "start_date": start_date,
                    "source": "FHIR",
                }

                # Prevent duplicates
                exists = PatientMedicationModel.objects.filter(
                    patient=patient_obj, medicine=name
                ).exists()

                if not exists:
                    super().add_medications(**medication_payload)

                    inserted_count += 1

        # Return response summary
        self.destination_response.update(
            {
                "message": f"Medication sync complete. {inserted_count} new entries added.",
                "statuscode": 200,
            }
        )
        return self.destination_response

    def create_vitals_entries(self, patientid):
        patient = Observation(self.customer_id, self.tenant_name, self.source_json)
        patient.authenticate()
        self.destination_json["patientid"] = patientid
        vitals_response, status_code = patient.search_vitals(**self.destination_json)

        if status_code == 200 and vitals_response.get("entry"):
            if vitals_response.get("total") != 0:
                patient_obj = PatientModel.objects.get(ehr_id=patientid)
                vital_obj = {}
                for vital in vitals_response.get("entry"):
                    if "Temp" in vital.get("resource").get("code").get("text"):
                        vital_obj["type"] = "body_temperature"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = patient_obj
                        vital_obj["value"] = (
                            vital.get("resource").get("valueQuantity").get("value")
                        )
                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "c"
                        super().add_vitals(**vital_obj)

                    if "Height" in vital.get("resource").get("code").get("text"):
                        vital_obj["type"] = "height"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = patient_obj
                        vital_obj["value"] = (
                            vital.get("resource").get("valueQuantity").get("value")
                            / 100.0
                        )
                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "m"
                        super().add_vitals(**vital_obj)

                    if vital.get("resource").get("code").get("text") == "BP":
                        if vital.get("resource").get("component"):
                            for single_vital in vital.get("resource").get("component"):
                                if single_vital.get("code").get("coding"):
                                    for single_coding_vital in single_vital.get(
                                        "code"
                                    ).get("coding"):
                                        if (
                                            single_coding_vital.get("display")
                                            == "Systolic blood pressure"
                                        ):
                                            vital_obj["value"] = single_vital.get(
                                                "valueQuantity"
                                            ).get("value")

                                        if (
                                            single_coding_vital.get("display")
                                            == "Diastolic blood pressure"
                                        ):
                                            vital_obj["diastolic"] = single_vital.get(
                                                "valueQuantity"
                                            ).get("value")

                            vital_obj["type"] = "blood_pressure"
                            vital_obj["units"] = "mmHg"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            super().add_vitals(**vital_obj)

                    if "Weight" in vital.get("resource").get("code").get("text"):
                        vital_obj["type"] = "weight"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = patient_obj
                        if (
                            vital.get("resource").get("valueQuantity").get("unit")
                            == "kg"
                        ):
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                                * 2.205
                            )
                        elif (
                            vital.get("resource").get("valueQuantity").get("unit")
                            == "lbs"
                        ):
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                            )
                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "lbs"
                        super().add_vitals(**vital_obj)

                    if "Pulse" in vital.get("resource").get("code").get("text"):
                        vital_obj["type"] = "heart_rate"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = patient_obj
                        vital_obj["value"] = (
                            vital.get("resource").get("valueQuantity").get("value")
                        )
                        vital_obj["diastolic"] = None
                        vital_obj["units"] = (
                            vital.get("resource").get("valueQuantity").get("unit")
                        )
                        super().add_vitals(**vital_obj)

                    if vital.get("resource").get("code").get("text") == "Resp":
                        vital_obj["type"] = "respiration_rate"
                        vital_obj["created_date"] = vital.get("resource").get(
                            "effectiveDateTime"
                        )
                        vital_obj["patient"] = patient_obj
                        vital_obj["value"] = (
                            vital.get("resource").get("valueQuantity").get("value")
                        )
                        vital_obj["diastolic"] = None
                        vital_obj["units"] = "BPM"
                        super().add_vitals(**vital_obj)

        else:
            self.destination_response.update({"errormessage": vitals_response})
            self.destination_response.update({"statuscode": status_code})
        return self.destination_response


class PatientPushTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name=None):
        super().__init__(source_data, customer_id, tenant_name)
        self.source_json = source_data
        self.customer_id = customer_id

        self.destination_json = {}

    def transform(self, event):
        try:
            patient_id = None

            patient_id = self.source_json.get("patientid")

            if event == "conditions":
                patient_conditions = Condition(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_conditions.authenticate()

                self.destination_json["resourceType"] = "Condition"
                self.destination_json["category"] = [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                "code": "problem-list-item",
                            }
                        ],
                        "text": "problem-list-item",
                    }
                ]
                self.destination_json["subject"] = {
                    "reference": f"Patient/{patient_id}"
                }
                self.destination_json["verificationStatus"] = {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "provisional",
                        }
                    ]
                }
                self.destination_json["severity"] = {"text": "High"}
                self.destination_json["note"] = [
                    {"text": self.source_json.get("notes")}
                ]
                self.destination_json["code"] = {"coding": []}
                if self.source_json.get("icd_codes_list"):
                    for single_code in self.source_json.get("icd_codes_list"):
                        self.destination_json["code"]["coding"].append(
                            {
                                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": single_code.get("code"),
                                "display": self.source_json.get("condition_title"),
                            }
                        )

                (
                    patient_conditions_response,
                    status_code,
                ) = patient_conditions.create_new_problems(**self.destination_json)
                if status_code == 201:
                    patient_res = {
                        "ConditionId": patient_conditions_response.get(
                            "Location"
                        ).split("/")[-1],
                    }
                    self.destination_response.update(patient_res)
                    self.destination_response.update({"statuscode": status_code})
                else:
                    self.destination_response.update(
                        {"errormessage": patient_conditions_response}
                    )
                    self.destination_response.update({"statuscode": status_code})
            return self.destination_response
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PatientQuerySyncTransformer(Transformer):
    def __init__(self, source_data, customer_id, ehr_name, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.temp_response = {}
        self.ehr_name = ehr_name

    def transform(self, events):
        provider_group = self.source_json.get("pg_id")

        try:
            patient_provider_group = ProviderGroup.objects.get(id=provider_group)
        except ProviderGroup.DoesNotExist:
            return Response({"detail": "Provider Group not found"}, status=400)
        patient_id = self.source_json.get("patientid")

        try:
            internal_patient = PatientModel.objects.get(
                id=patient_id, provider_group=patient_provider_group
            )
        except PatientModel.DoesNotExist:
            return Response({"detail": "Patient does not found"}, status=400)
        self.destination_json["patientid"] = internal_patient.ehr_id
        for event in events:
            if event == "allergies" or event == "all":
                patient = AllergyIntolerance(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient.authenticate()
                data = {
                    "patient": self.destination_json["patientid"],
                    "clinical-status": "active",
                }
                (
                    allergies_response,
                    status_code,
                ) = patient.search_allergy_intolerance(**data)
                if status_code == 200 and allergies_response.get("entry"):
                    patient_obj = PatientModel.objects.get(ehr_id=data["patient"])
                    for allergy in allergies_response.get("entry"):
                        allergies_payload = {}
                        if allergy.get("resource").get("code"):
                            allergies_payload["name"] = (
                                allergy.get("resource").get("code").get("text")
                                if allergy.get("resource").get("code")
                                else None
                            )
                            if allergy.get("resource").get("code").get("coding"):
                                for single_allergy in (
                                    allergy.get("resource").get("code").get("coding")
                                ):
                                    if single_allergy.get("display"):
                                        allergies_payload["name"] = single_allergy.get(
                                            "display"
                                        )

                        severity = None
                        reaction = None
                        if allergy.get("resource").get("reaction"):
                            for single_reaction in allergy.get("resource").get(
                                "reaction"
                            ):
                                for single_reaction_name in single_reaction.get(
                                    "manifestation"
                                ):
                                    reaction = single_reaction_name.get("text")

                        formatted_date = None
                        if allergy.get("resource").get("recordedDate"):
                            date_obj = datetime.fromisoformat(
                                allergy.get("resource")
                                .get("recordedDate")
                                .replace("Z", "+00:00")
                            )

                            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                        allergies_payload["patientid"] = patient_obj
                        allergies_payload["created_date"] = formatted_date
                        allergies_payload["severity"] = severity
                        allergies_payload["reaction"] = reaction

                        exists = PatientAllergyModel.objects.filter(
                            patient=patient_obj, name=allergies_payload["name"]
                        ).exists()
                        if not exists:
                            super().add_allergies(**allergies_payload)

                    self.destination_response.update({"Success": allergies_response})

                else:
                    self.destination_response.update(
                        {"errormessage": allergies_response}
                    )
                    self.destination_response.update({"statuscode": status_code})

            if event == "medications" or event == "all":
                self.destination_json["patientid"] = internal_patient.ehr_id

                if self.destination_json["patientid"]:
                    patient_chart = List(
                        self.customer_id, self.tenant_name, self.source_json
                    )
                    patient_chart.authenticate()
                    (
                        medications_response,
                        status_code,
                    ) = patient_chart.search_medications(**self.destination_json)
                    medication_payload = {}
                    if status_code == 200 and medications_response.get("entry"):
                        patient_obj = PatientModel.objects.get(
                            ehr_id=internal_patient.ehr_id
                        )

                        for medication in medications_response.get("entry"):
                            if medication.get("resource"):
                                route = (
                                    medication.get("resource").get("route")
                                    if medication.get("resource").get("route")
                                    else None
                                )
                                medication_payload["route"] = (
                                    medication.get("resource").get("route").get("text")
                                    if route
                                    else None
                                )
                                medication_payload["patientid"] = patient_obj
                                names = (
                                    medication.get("resource").get("code").get("coding")
                                    if medication.get("resource").get("code")
                                    else []
                                )
                                for name in names:
                                    medication_payload["name"] = name.get("display")

                            if medication.get("resource").get(
                                "medicationCodeableConcept"
                            ):
                                medication_payload["name"] = (
                                    medication.get("resource")
                                    .get("medicationCodeableConcept")
                                    .get("text")
                                )
                            medication_payload["status"] = (
                                "historical"
                                if medication.get("resource").get("status") == "retired"
                                else "active"
                            )
                            exists = PatientMedicationModel.objects.filter(
                                patient=patient_obj, medicine=medication_payload["name"]
                            ).exists()
                            if not exists:
                                super().add_medications(**medication_payload)
                        self.destination_response.update(
                            {"success": medications_response}
                        )
            else:
                self.destination_response.update({"errormessage": medications_response})
                self.destination_response.update({"statuscode": status_code})

            if event == "labresult" or event == "all":
                patient_lab_entries = Observation(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_lab_entries.authenticate()
                self.destination_json["category"] = "laboratory"
                (lab_result_response, status_code) = patient_lab_entries.search_labs(
                    **self.destination_json
                )
                if status_code == 200 and lab_result_response.get("entry"):
                    patient_obj = PatientModel.objects.get(
                        ehr_id=internal_patient.ehr_id
                    )
                    for labresult in lab_result_response.get("entry", []):
                        resource = labresult.get("resource", {})
                        lab_result_payload = {}

                        # Prefer valueQuantity if present, fallback to valueString
                        value = None
                        if "valueQuantity" in resource:
                            value = resource["valueQuantity"].get("value")
                        elif "valueString" in resource:
                            value = resource.get("valueString")
                        lab_result_payload["value"] = value

                        lab_result_payload["patient"] = patient_obj

                        # Lab test name
                        code = resource.get("code", {})
                        lab_result_payload["lab_result_for"] = code.get("text")

                        # Issued date
                        if "issued" in resource:
                            lab_result_payload["issued"] = resource["issued"]

                        # Optional text.div (not present in your sample, so default to None)
                        text_section = resource.get("text", {})
                        lab_result_payload["file"] = (
                            text_section.get("div") if text_section else None
                        )

                        if lab_result_payload["value"]:
                            try:
                                with transaction.atomic():
                                    exists = PatientLabResult.objects.filter(
                                        patient=patient_obj,
                                        lab_result_for=lab_result_payload[
                                            "lab_result_for"
                                        ],
                                    ).exists()
                                    if not exists:
                                        super().add_lab_result(**lab_result_payload)
                            except Exception as e:
                                return Response(
                                    {"detail": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST,
                                )
                    self.destination_json.update({"success": lab_result_payload})

                else:
                    self.destination_response.update(
                        {"errormessage": lab_result_response}
                    )
                    self.destination_response.update({"statuscode": status_code})

            if event == "conditions" or event == "all":
                patient_problem = Condition(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_problem.authenticate()
                (
                    conditions_response,
                    status_code,
                ) = patient_problem.search_problems(**self.destination_json)
                if (
                    status_code == 200
                    and conditions_response.get("entry")
                    and conditions_response.get("total") >= 1
                ):
                    patient_obj = PatientModel.objects.get(
                        ehr_id=internal_patient.ehr_id
                    )
                    condition_payload = {}
                    for single_record in conditions_response.get("entry"):
                        if single_record.get("resource").get("code"):
                            if single_record.get("resource").get("code").get("coding"):
                                for single_code in (
                                    single_record.get("resource")
                                    .get("code")
                                    .get("coding")
                                ):
                                    if (
                                        single_code.get("system")
                                        == "http://hl7.org/fhir/sid/icd-10-cm"
                                    ):
                                        ehr_icd_code = single_code.get("code")
                                        ehr_icd_name = single_code.get("display")
                                        existing_code_name = (
                                            PatientConditions.objects.filter(
                                                title=ehr_icd_name
                                            ).first()
                                        )
                                        if existing_code_name:
                                            condition_payload[
                                                "condition"
                                            ] = existing_code_name

                                        else:
                                            new_code_name = (
                                                PatientConditions.objects.create(
                                                    title=ehr_icd_name,
                                                )
                                            )
                                            condition_payload[
                                                "condition"
                                            ] = new_code_name

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
                                            condition_payload[
                                                "icdcode"
                                            ] = existing_icd_code

                                        else:
                                            new_icd_code = ICDCode.objects.create(
                                                title=ehr_icd_name,
                                                code=ehr_icd_code,
                                            )
                                            condition_payload["icdcode"] = new_icd_code
                                        condition_payload["patientid"] = patient_obj
                                        exists = PatientConditionModel.objects.filter(
                                            patient=patient_obj,
                                            condition=condition_payload["condition"],
                                        ).exists()
                                        if not exists:
                                            super().add_conditions(**condition_payload)
                    self.destination_response["success"] = True
                else:
                    self.destination_response.update(
                        {
                            "errormessage": conditions_response,
                            "statuscode": status_code,
                        }
                    )

            if event == "vitals" or event == "all":
                patient = Observation(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient.authenticate()
                vitals_response, status_code = patient.search_vitals(
                    **self.destination_json
                )
                self.destination_json["patientid"] = internal_patient.ehr_id
                if vitals_response.get("total") != 0:
                    patient_obj = PatientModel.objects.get(
                        ehr_id=internal_patient.ehr_id
                    )
                    vital_obj = {}
                    for vital in vitals_response.get("entry"):
                        if "Temp" in vital.get("resource").get("code").get("text"):
                            vital_obj["type"] = "body_temperature"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                            )
                            vital_obj["diastolic"] = None
                            vital_obj["units"] = "c"
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)

                        if "Height" in vital.get("resource").get("code").get("text"):
                            vital_obj["type"] = "height"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                                / 100.0
                            )
                            vital_obj["diastolic"] = None
                            vital_obj["units"] = "m"
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)

                        if "BP" in vital.get("resource").get("code").get("text"):
                            if vital.get("resource").get("component"):
                                for single_vital in vital.get("resource").get(
                                    "component"
                                ):
                                    if single_vital.get("code").get("coding"):
                                        for single_coding_vital in single_vital.get(
                                            "code"
                                        ).get("coding"):
                                            if (
                                                single_coding_vital.get("display")
                                                == "Systolic blood pressure"
                                            ):
                                                vital_obj["value"] = single_vital.get(
                                                    "valueQuantity"
                                                ).get("value")

                                            if (
                                                single_coding_vital.get("display")
                                                == "Diastolic blood pressure"
                                            ):
                                                vital_obj[
                                                    "diastolic"
                                                ] = single_vital.get(
                                                    "valueQuantity"
                                                ).get(
                                                    "value"
                                                )

                                vital_obj["type"] = "blood_pressure"
                                vital_obj["units"] = "mmHg"
                                vital_obj["created_date"] = vital.get("resource").get(
                                    "effectiveDateTime"
                                )
                                vital_obj["patient"] = patient_obj
                                recorded_at = parse_datetime(vital_obj["created_date"])
                                exists = PatientVitalModel.objects.filter(
                                    patient=patient_obj,
                                    type=vital_obj["type"],
                                    value=vital_obj["value"],
                                    recorded_at=recorded_at,
                                ).exists()
                                if not exists:
                                    super().add_vitals(**vital_obj)

                        if "Weight" in vital.get("resource").get("code").get("text"):
                            vital_obj["type"] = "weight"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            if (
                                vital.get("resource").get("valueQuantity").get("unit")
                                == "kg"
                            ):
                                vital_obj["value"] = (
                                    vital.get("resource")
                                    .get("valueQuantity")
                                    .get("value")
                                    * 2.205
                                )
                            elif (
                                vital.get("resource").get("valueQuantity").get("unit")
                                == "lbs"
                            ):
                                vital_obj["value"] = (
                                    vital.get("resource")
                                    .get("valueQuantity")
                                    .get("value")
                                )
                            vital_obj["diastolic"] = None
                            vital_obj["units"] = "lbs"
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)

                        if "Pulse" in vital.get("resource").get("code").get("text"):
                            vital_obj["type"] = "heart_rate"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                            )
                            vital_obj["diastolic"] = None
                            vital_obj["units"] = (
                                vital.get("resource").get("valueQuantity").get("unit")
                            )
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)

                        if "Resp" in vital.get("resource").get("code").get("text"):
                            vital_obj["type"] = "respiration_rate"
                            vital_obj["created_date"] = vital.get("resource").get(
                                "effectiveDateTime"
                            )
                            vital_obj["patient"] = patient_obj
                            vital_obj["value"] = (
                                vital.get("resource").get("valueQuantity").get("value")
                            )
                            vital_obj["diastolic"] = None
                            vital_obj["units"] = "BPM"
                            recorded_at = parse_datetime(vital_obj["created_date"])
                            exists = PatientVitalModel.objects.filter(
                                patient=patient_obj,
                                type=vital_obj["type"],
                                value=vital_obj["value"],
                                recorded_at=recorded_at,
                            ).exists()
                            if not exists:
                                super().add_vitals(**vital_obj)
                    self.destination_json.update(
                        {
                            "Sucess": "Vital sync successfully",
                            "response": vitals_response,
                        }
                    )

                else:
                    self.destination_response.update({"errormessage": vitals_response})
                    self.destination_response.update({"statuscode": status_code})

        return self.destination_response
