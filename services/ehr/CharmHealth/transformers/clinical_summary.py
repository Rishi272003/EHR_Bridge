import io
from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response

from ecaremd.careplan.models import Condition, ICDCode
from ecaremd.core.models.allergy import Allergy as PatientAllergyModel
from ecaremd.core.models.condition import PatientCondition
from ecaremd.core.models.lab import LabResult as PatientLabResult
from ecaremd.core.models.medication import Medication as PatientMedicationModel
from ecaremd.core.models.patient import CCDADocument
from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.core.models.vital import Vital as PatientVitalModel
from ecaremd.ehr_integrations.constants import SNOWMED_ICD_MAPPING
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.AllergyIntolerance import (
    AllergyIntolerance,
)
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.CCDA import CCDA
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.DocumentReference import (
    DocumentReference,
)
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.LabResults import (
    LabResults,
)
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.Medications import (
    Medications,
)
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.Problems import (
    Problems,
)
from ecaremd.ehr_integrations.ehr_services.CharmHealth.categories.Vitals import Vitals
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer
from ecaremd.provider_group.models import ProviderGroup


class PatientQueryTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.temp_response = {}
        self.ehr_name = self.source_json.get("ehr_name")
        self.patient_obj = None

    def transform(self, events):
        provider_group = self.source_json.get("pg_id")
        try:
            patient_provider_group = ProviderGroup.objects.get(id=provider_group)
        except ProviderGroup.DoesNotExist:
            return Response({"detail": "Provider Group not found"}, status=400)

        self.destination_json["start_date"] = self.source_json.get("startdate")
        self.destination_json["end_date"] = self.source_json.get("enddate")
        if isinstance(self.source_json.get("patientid"), list):
            for single_patient in self.source_json.get("patientid"):
                self.destination_json["patientid"] = single_patient

                try:
                    self.patient_obj = PatientModel.objects.get(ehr_id=single_patient)
                    return Response(
                        {
                            "detail": f"Patient  {self.patient_obj.first_name} {self.patient_obj.last_name} is already imported."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                except PatientModel.DoesNotExist:
                    # Process demographics first to create the patient
                    for event in events:
                        event = event.lower()

                        # Demographics Data
                        if event == "demographics" or event == "all":
                            patient = Patient(
                                self.customer_id, self.tenant_name, self.source_json
                            )
                            patient.authenticate()
                            patient_id = single_patient
                            (
                                patient_response,
                                status_code,
                            ) = patient.get_patient_demographics(patientid=patient_id)
                            if status_code == 200 and patient_response.get("data"):
                                patient_demographics = (
                                    self.extract_patient_demographics(
                                        patient_response.get("data")
                                    )
                                )
                                patient_demographics[
                                    "provider_group"
                                ] = patient_provider_group
                                patient_demographics["ehr_name"] = self.ehr_name

                                super().create_patient(**patient_demographics)

                                # Get the created patient object for subsequent processing
                                try:
                                    self.patient_obj = PatientModel.objects.get(
                                        ehr_id=single_patient
                                    )
                                except PatientModel.DoesNotExist:
                                    self.destination_response.update(
                                        {
                                            "errormessage": "Failed to create patient",
                                            "statuscode": 500,
                                        }
                                    )
                                    continue

                            else:
                                self.destination_response.update(
                                    {
                                        "errormessage": patient_response,
                                        "statuscode": status_code,
                                    }
                                )
                                continue

                    # Process other data types only if patient was created successfully
                    if self.patient_obj:
                        for event in events:
                            event = event.lower()

                            # Conditions Data
                            if event == "conditions" or event == "all":
                                created_repsonse = self.create_conditions_entries(
                                    self.patient_obj
                                )
                                self.destination_response.update(created_repsonse)

                            # Allergy Data
                            if event == "allergies" or event == "all":
                                created_repsonse = self.create_allergies_entries(
                                    self.patient_obj
                                )
                                self.destination_response.update(created_repsonse)

                            # Medication Data
                            if event == "medications" or event == "all":
                                created_repsonse = self.create_medications_entries(
                                    self.patient_obj
                                )
                                self.destination_response.update(created_repsonse)

                            # Lab Result Data
                            if event == "labresult" or event == "all":
                                created_repsonse = self.create_lab_result_entries(
                                    self.patient_obj
                                )
                                self.destination_response.update(created_repsonse)

                            # Vitals Data
                            if event == "vitals" or event == "all":
                                created_repsonse = self.create_vitals_entries(
                                    self.patient_obj
                                )
                                self.destination_response.update(created_repsonse)

            return self.destination_response

    def create_allergies_entries(self, patient_obj):
        patients_allergy = AllergyIntolerance(
            self.customer_id, self.tenant_name, self.source_json
        )
        patients_allergy.authenticate()

        allergies_response, status_code = patients_allergy.get_patient_allergy(
            patient=patient_obj.ehr_id
        )

        if status_code == 400:
            self.destination_response.update({"errormessage": allergies_response})
            self.destination_response.update({"statuscode": 200})

        if status_code == 200 and allergies_response.get("data", {}).get("entry"):
            entries = allergies_response.get("data", {}).get("entry", [])

            for entry in entries:
                resource = entry.get("resource", {})
                allergy_payload = {"patientid": patient_obj}

                # Basic allergy information - handle both coding and text fields
                code_data = resource.get("code", {})
                if code_data.get("coding"):
                    # Process coding array
                    for single_code in code_data.get("coding", []):
                        if single_code.get("display"):
                            allergy_payload["name"] = single_code.get("display")
                            break
                elif code_data.get("text"):
                    # Fallback to text field if no coding
                    allergy_payload["name"] = code_data.get("text")

                # Handle onset date - fix field name mismatch
                onset_date = resource.get("onSetDateTime") or resource.get(
                    "onsetDateTime"
                )
                if onset_date:
                    try:
                        # Handle date format without timezone
                        if "T" in onset_date:
                            date_obj = datetime.fromisoformat(
                                onset_date.replace("Z", "+00:00")
                            )
                        else:
                            date_obj = datetime.strptime(onset_date, "%Y-%m-%d")
                        allergy_payload["created_date"] = date_obj.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    except Exception as e:
                        print("e", e)
                        allergy_payload["created_date"] = onset_date

                # Handle reactions
                reactions = resource.get("reaction", [])
                if reactions:
                    for reaction in reactions:
                        manifestations = reaction.get("manifestation", [])
                        if manifestations:
                            allergy_payload["reaction"] = manifestations[0].get(
                                "text", ""
                            )
                        allergy_payload["severity"] = reaction.get("severity", "")
                        break  # Take first reaction
                # Only add if we have a name
                if allergy_payload.get("name"):
                    exists = PatientAllergyModel.objects.filter(
                        patient=patient_obj, name=allergy_payload["name"]
                    ).exists()
                    if not exists:
                        super().add_allergies(**allergy_payload)
        else:
            self.destination_response.update({"errormessage": allergies_response})
            self.destination_response.update({"statuscode": status_code})
        return self.destination_response

    def create_medications_entries(self, patient_obj):
        patient_medications = Medications(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_medications.authenticate()
        (
            medications_response,
            status_code,
        ) = patient_medications.get_patient_medications(patient=patient_obj.ehr_id)
        if status_code == 400:
            self.destination_response.update({"errormessage": medications_response})
            self.destination_response.update({"statuscode": 200})

        if status_code == 200 and medications_response.get("data", {}).get("entry"):
            for medication in medications_response.get("data", {}).get("entry"):
                resource = medication.get("resource", {})
                medication_payload = {"patientid": patient_obj}

                # Basic medication information - handle both coding and text fields
                medication_concept = resource.get("medicationCodeableConcept", {})
                if medication_concept.get("coding"):
                    for single_code in medication_concept.get("coding", []):
                        if single_code.get("display"):
                            medication_payload["name"] = single_code.get("display")
                            break
                elif medication_concept.get("text"):
                    # Fallback to text field if no coding
                    medication_payload["name"] = medication_concept.get("text")

                # Status mapping
                if resource.get("status"):
                    medication_payload["status"] = (
                        "historical"
                        if resource.get("status") == "completed"
                        else "active"
                    )

                # Handle effective period dates - fix date parsing
                effective_period = resource.get("effectivePeriod", {})
                if effective_period:
                    start_date_str = effective_period.get("start")
                    end_date_str = effective_period.get("end")

                    if start_date_str:
                        try:
                            # Handle date format without timezone
                            if "T" in start_date_str:
                                start_date = datetime.fromisoformat(
                                    start_date_str.replace("Z", "+00:00")
                                )
                            else:
                                start_date = datetime.strptime(
                                    start_date_str, "%Y-%m-%d"
                                )
                            medication_payload["created_date"] = make_aware(start_date)
                            # medication_payload["created_date"] = start_date.strftime(
                            #     "%Y-%m-%d %H:%M:%S"
                            # )
                        except Exception as e:
                            print("e", e)
                            medication_payload["created_date"] = start_date_str

                    if end_date_str:
                        try:
                            # Handle date format without timezone
                            if "T" in end_date_str:
                                end_date = datetime.fromisoformat(
                                    end_date_str.replace("Z", "+00:00")
                                )
                            else:
                                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                            medication_payload["deleted_date"] = make_aware(end_date)
                            # medication_payload["deleted_date"] = end_date.strftime(
                            #     "%Y-%m-%d %H:%M:%S"
                            # )
                        except Exception as e:
                            print("e", e)
                            medication_payload["deleted_date"] = end_date_str

                # Handle dosage information
                dosage_list = resource.get("dosage", [])
                if dosage_list:
                    for dosage in dosage_list:
                        if dosage.get("text"):
                            medication_payload["comment"] = dosage.get("text")
                            break  # Take first dosage text

                # Only add if we have a name
                if medication_payload.get("name"):
                    exists = PatientMedicationModel.objects.filter(
                        patient=patient_obj, medicine=medication_payload["name"]
                    ).exists()

                    if not exists:
                        super().add_medications(**medication_payload)

        else:
            self.destination_response.update({"errormessage": medications_response})
            self.destination_response.update({"statuscode": status_code})
        return self.destination_response

    def create_conditions_entries(self, patient_obj):
        patient_conditions = Problems(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_conditions.authenticate()

        (
            conditions_response,
            status_code,
        ) = patient_conditions.get_patient_condition(patient=patient_obj.ehr_id)
        if status_code == 400:
            self.destination_response.update({"errormessage": conditions_response})
            self.destination_response.update({"statuscode": 200})

        elif status_code == 200 and conditions_response.get("data", {}).get("entry"):
            entries = conditions_response.get("data", {}).get("entry", [])

            for entry in entries:
                resource = entry.get("resource", {})
                condition_payload = {"patientid": patient_obj}

                # Fix data access - use resource instead of entry
                code_data = resource.get("code", {})
                if code_data.get("coding"):
                    for single_code in code_data.get("coding", []):
                        if single_code.get("system") == "http://snomed.info/sct":
                            snomed_code = single_code.get("code")
                            ehr_icd_name = single_code.get("display")

                            # Handle SNOWMED to ICD mapping safely
                            ehr_icd_code = SNOWMED_ICD_MAPPING.get(
                                snomed_code, snomed_code
                            )
                            # Create or get condition
                            existing_code_name = Condition.objects.filter(
                                title=ehr_icd_name
                            ).first()
                            if existing_code_name:
                                condition_payload["condition"] = existing_code_name
                            else:
                                new_code_name = Condition.objects.create(
                                    title=ehr_icd_name,
                                )
                                condition_payload["condition"] = new_code_name

                            # Create or get ICD code
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
                            break  # Take first SNOMED code

                # Handle onset date - fix data access
                onset_date_str = resource.get("onsetDateTime")
                if onset_date_str:
                    try:
                        onset_date = datetime.fromisoformat(onset_date_str)
                        condition_payload["start_date"] = onset_date.strftime(
                            "%Y-%m-%d"
                        )
                    except (ValueError, TypeError):
                        condition_payload["start_date"] = None
                else:
                    condition_payload["start_date"] = None
                if resource.get("note"):
                    for note in resource.get("note"):
                        condition_payload["note"] = note.get("text")
                # Only add if we have a condition
                if condition_payload.get("condition"):
                    exists = PatientCondition.objects.filter(
                        patient=patient_obj,
                        condition=condition_payload["condition"],
                        icd_codes=condition_payload["icdcode"],
                    ).exists()
                    if not exists:
                        super().add_conditions(**condition_payload)

        else:
            self.destination_response.update({"errormessage": conditions_response})
            self.destination_response.update({"statuscode": 200})
        return self.destination_response

    def extract_patient_demographics(self, patient_data):
        """
        Extract patient demographics data from CharmHealth FHIR response
        """
        demographics = {}

        # Basic patient information
        demographics["id"] = patient_data.get("identifier", [{}])[0].get("value")
        demographics["mrn"] = None  # Using identifier as MRN

        # Name extraction
        name_data = patient_data.get("name", [{}])[0]
        demographics["first_name"] = (
            name_data.get("given", [""])[0] if name_data.get("given") else ""
        )
        demographics["last_name"] = name_data.get("family", "")
        demographics["middle_name"] = (
            name_data.get("given", [""])[1]
            if len(name_data.get("given", [])) > 1
            else ""
        )

        # Demographics
        demographics["sex"] = patient_data.get("gender", "")
        demographics["dob"] = patient_data.get("birthDate", "")
        demographics["marital_status"] = patient_data.get("maritalStatus", {}).get(
            "text", ""
        )

        # Race and ethnicity from extensions
        extensions = patient_data.get("extension", [])
        race = ""
        ethnicity = ""
        for ext in extensions:
            if ext.get("url") == "http://hl7.org/fhir/StructureDefinition/us-core-race":
                coding = ext.get("valueCodeableConcept", {}).get("coding", [])
                if coding:
                    race = coding[0].get("display", "")
            elif (
                ext.get("url")
                == "http://hl7.org/fhir/StructureDefinition/us-core-ethnicity"
            ):
                coding = ext.get("valueCodeableConcept", {}).get("coding", [])
                if coding:
                    ethnicity = coding[0].get("display", "")

        demographics["race"] = (
            f"{race} - {ethnicity}" if race and ethnicity else race or ethnicity
        )

        # Address extraction
        address_data = patient_data.get("address", [{}])[0]
        demographics["address_line_1"] = (
            address_data.get("line", [""])[0] if address_data.get("line") else ""
        )
        demographics["city"] = address_data.get("city", "")
        demographics["state"] = address_data.get("state", "")
        demographics["zip"] = address_data.get("postalCode", "")
        demographics["country"] = address_data.get("country", "")

        # Phone numbers
        telecom = patient_data.get("telecom", [])
        primary_phone = ""
        secondary_phone = ""
        home_phone = ""
        work_phone = ""

        for contact in telecom:
            if contact.get("system") == "phone":
                use = contact.get("use", "")
                value = contact.get("value", "")
                if use == "mobile":
                    primary_phone = value
                elif use == "home":
                    home_phone = value
                elif use == "work":
                    work_phone = value
                else:
                    secondary_phone = value

        demographics["primary_phone"] = primary_phone
        demographics["secondary_phone"] = secondary_phone
        demographics["home_phone"] = home_phone
        demographics["work_phone"] = work_phone

        # Language
        communication = patient_data.get("communication", [{}])[0]
        demographics["language"] = (
            communication.get("language", {})
            .get("coding", [{}])[0]
            .get("display", "English")
        )
        return demographics

    def create_vitals_entries(self, patient_obj):
        patient_vitals = Vitals(self.customer_id, self.tenant_name, self.source_json)
        patient_vitals.authenticate()
        vitals_response, status_code = patient_vitals.get_patient_vitals(
            patient=patient_obj.ehr_id
        )
        print("vital_response>>>>>>>>", vitals_response, status_code)
        if status_code == 400:
            self.destination_response.update({"errormessage": vitals_response})
            self.destination_response.update({"statuscode": 200})

        elif status_code == 200 and vitals_response.get("data", {}).get("entry"):
            # Store blood pressure components to combine them later
            blood_pressure_data = {}
            for vital in vitals_response.get("data", {}).get("entry"):
                resource = vital.get("resource", {})
                vital_name = resource.get("code", {}).get("text", "")
                vital_quantity = resource.get("valueQuantity", {})
                effective_date = resource.get("effectiveDateTime", "")

                # Skip if no vital name
                if not vital_name:
                    continue

                vital_obj = {"patient": patient_obj, "diastolic": None, "units": ""}

                # Parse effective date
                if effective_date:
                    try:
                        created_date = datetime.fromisoformat(
                            effective_date.replace("Z", "+00:00")
                        )
                        vital_obj["created_date"] = created_date.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    except Exception as e:
                        print("e", e)
                        continue
                else:
                    continue

                # Temperature processing
                if "temperature" in vital_name.lower():
                    vital_obj["type"] = "body_temperature"
                    temp_value = vital_quantity.get("value")
                    if temp_value is not None:
                        # Convert Fahrenheit to Celsius
                        vital_obj["value"] = (temp_value - 32) * 5 / 9
                        vital_obj["units"] = "c"

                        exists = PatientVitalModel.objects.filter(
                            patient=patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=vital_obj["created_date"],
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                # BMI processing
                elif vital_name.lower() == "body mass index":
                    vital_obj["type"] = "bmi"
                    vital_obj["value"] = float(vital_quantity.get("value", 0.0))
                    vital_obj["units"] = vital_quantity.get("unit", "")

                    exists = PatientVitalModel.objects.filter(
                        patient=patient_obj,
                        type=vital_obj["type"],
                        value=vital_obj["value"],
                        recorded_at=vital_obj["created_date"],
                    ).exists()
                    if not exists:
                        super().add_vitals(**vital_obj)

                # Height processing
                elif "height" in vital_name.lower():
                    vital_obj["type"] = "height"
                    height_value = float(vital_quantity.get("value"))
                    if height_value is not None:
                        # Convert inches to meters
                        vital_obj["value"] = height_value / 39.37
                        vital_obj["units"] = "m"
                        exists = PatientVitalModel.objects.filter(
                            patient=patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=vital_obj["created_date"],
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                # Weight processing
                elif "weight" in vital_name.lower():
                    vital_obj["type"] = "weight"
                    weight_value = float(vital_quantity.get("value"))
                    unit = vital_quantity.get("unit", "")

                    if weight_value is not None:
                        if unit == "kg":
                            # Convert kg to lbs
                            vital_obj["value"] = weight_value * 2.20462
                        else:  # Assume lbs
                            vital_obj["value"] = weight_value
                        vital_obj["units"] = "lbs"
                        exists = PatientVitalModel.objects.filter(
                            patient=patient_obj,
                            type=vital_obj["type"],
                            value=vital_obj["value"],
                            recorded_at=vital_obj["created_date"],
                        ).exists()
                        if not exists:
                            super().add_vitals(**vital_obj)

                # Pulse rate processing
                elif "pulse rate" in vital_name.lower():
                    vital_obj["type"] = "heart_rate"
                    vital_obj["value"] = vital_quantity.get("value", 0.0)
                    vital_obj["units"] = vital_quantity.get("unit", "bpm")
                    exists = PatientVitalModel.objects.filter(
                        patient=patient_obj,
                        type=vital_obj["type"],
                        value=vital_obj["value"],
                        recorded_at=vital_obj["created_date"],
                    ).exists()
                    if not exists:
                        super().add_vitals(**vital_obj)

                # Blood pressure processing - handle separate systolic and diastolic entries
                elif "systolic blood pressure" in vital_name.lower():
                    # Store systolic data for later combination
                    bp_key = vital_obj["created_date"]
                    if bp_key not in blood_pressure_data:
                        blood_pressure_data[bp_key] = {}
                    blood_pressure_data[bp_key]["systolic"] = vital_quantity.get(
                        "value", 0.0
                    )
                    blood_pressure_data[bp_key]["effective_date"] = effective_date
                elif "diastolic blood pressure" in vital_name.lower():
                    # Store diastolic data for later combination
                    bp_key = vital_obj["created_date"]
                    if bp_key not in blood_pressure_data:
                        blood_pressure_data[bp_key] = {}
                    blood_pressure_data[bp_key]["diastolic"] = vital_quantity.get(
                        "value", 0.0
                    )
                    blood_pressure_data[bp_key]["effective_date"] = effective_date
                # Oximetry processing
                elif vital_name.lower() == "oximetry":
                    vital_obj["type"] = "o2_saturation"
                    vital_obj["value"] = vital_quantity.get("value", 0.0)
                    vital_obj["units"] = vital_quantity.get("unit", "%")
                    exists = PatientVitalModel.objects.filter(
                        patient=patient_obj,
                        type=vital_obj["type"],
                        value=vital_obj["value"],
                        recorded_at=vital_obj["created_date"],
                    ).exists()
                    if not exists:
                        super().add_vitals(**vital_obj)

                # Respiratory rate processing
                elif "respiratory rate" in vital_name.lower():
                    vital_obj["type"] = "respiration_rate"
                    vital_obj["value"] = vital_quantity.get("value", 0.0)
                    vital_obj["units"] = "BPM"
                    exists = PatientVitalModel.objects.filter(
                        patient=patient_obj,
                        type=vital_obj["type"],
                        value=vital_obj["value"],
                        recorded_at=vital_obj["created_date"],
                    ).exists()
                    if not exists:
                        super().add_vitals(**vital_obj)

            # Process combined blood pressure entries
            for bp_date, bp_data in blood_pressure_data.items():
                if "systolic" in bp_data and "diastolic" in bp_data:
                    bp_vital_obj = {
                        "patient": patient_obj,
                        "type": "blood_pressure",
                        "value": bp_data["systolic"],
                        "diastolic": bp_data["diastolic"],
                        "units": "mmHg",
                        "created_date": bp_date,
                    }
                    exists = PatientVitalModel.objects.filter(
                        patient=patient_obj,
                        type=bp_vital_obj["type"],
                        value=bp_vital_obj["value"],
                        diastolic=bp_vital_obj["diastolic"],
                        recorded_at=bp_vital_obj["created_date"],
                    ).exists()
                    if not exists:
                        super().add_vitals(**bp_vital_obj)

            self.destination_response.update({"success": True})
        else:
            self.destination_response.update({"errormessage": vitals_response})
            self.destination_response.update({"statuscode": status_code})

        return self.destination_response

    def create_lab_result_entries(self, patient_obj):
        patients_chart = LabResults(
            self.customer_id, self.tenant_name, self.source_json
        )
        patients_chart.authenticate()

        lab_result_response, status_code = patients_chart.get_lab_report(
            patient=patient_obj.ehr_id
        )
        if status_code == 400:
            self.destination_response.update({"errormessage": lab_result_response})
            self.destination_response.update({"statuscode": 200})
        elif status_code == 200 and lab_result_response.get("data", {}).get("entry"):
            for lab_result in lab_result_response.get("data", {}).get("entry"):
                resource = lab_result.get("resource", {})
                # Handle different lab result structures
                if resource.get("component"):
                    # Standard lab result with components
                    for component in resource.get("component", []):
                        lab_result_payload = {"patient": patient_obj}
                        lab_result_payload["lab_result_for"] = component.get(
                            "code", {}
                        ).get("text", "")
                        lab_result_payload["value"] = component.get(
                            "valueQuantity", {}
                        ).get("value", "")

                        # Handle effective date
                        effective_date = resource.get("effectiveDateTime", "")
                        if effective_date:
                            try:
                                if "T" in effective_date:
                                    issued_date = datetime.fromisoformat(
                                        effective_date.replace("Z", "+00:00")
                                    )
                                else:
                                    issued_date = datetime.strptime(
                                        effective_date, "%Y-%m-%d"
                                    )
                                lab_result_payload["issued"] = issued_date.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                            except Exception as e:
                                print("e", e)
                                lab_result_payload["issued"] = effective_date
                        if lab_result_payload["value"]:
                            exists = PatientLabResult.objects.filter(
                                patient=patient_obj,
                                lab_result_for=lab_result_payload["lab_result_for"],
                                value=lab_result_payload["value"],
                            ).exists()
                            if not exists:
                                super().add_lab_result(**lab_result_payload)

                elif resource.get("resourceType") == "Observation":
                    # Direct observation lab result
                    lab_result_payload = {"patient": patient_obj}
                    # Get lab result name from code
                    code_data = resource.get("code", {})
                    if code_data.get("coding"):
                        for coding in code_data.get("coding", []):
                            if coding.get("display"):
                                lab_result_payload["lab_result_for"] = coding.get(
                                    "display"
                                )
                                break
                    elif code_data.get("text"):
                        lab_result_payload["lab_result_for"] = code_data.get("text")

                    # Get value
                    value_quantity = resource.get("valueQuantity", {})
                    if value_quantity.get("value") is not None:
                        lab_result_payload["value"] = value_quantity.get("value")
                    elif resource.get("valueString"):
                        lab_result_payload["value"] = resource.get("valueString")
                    # Handle effective date
                    effective_date = resource.get("effectiveDateTime", "")
                    if effective_date:
                        try:
                            if "T" in effective_date:
                                issued_date = datetime.fromisoformat(
                                    effective_date.replace("Z", "+00:00")
                                )
                            else:
                                issued_date = datetime.strptime(
                                    effective_date, "%Y-%m-%d"
                                )
                            lab_result_payload["issued"] = issued_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        except Exception as e:
                            print("e", e)
                            lab_result_payload["issued"] = effective_date
                    if lab_result_payload.get("value") and lab_result_payload.get(
                        "lab_result_for"
                    ):
                        exists = PatientLabResult.objects.filter(
                            patient=patient_obj,
                            lab_result_for=lab_result_payload["lab_result_for"],
                            value=lab_result_payload["value"],
                        ).exists()
                        if not exists:
                            super().add_lab_result(**lab_result_payload)

        else:
            self.destination_response.update({"errormessage": lab_result_response})
            self.destination_response.update({"statuscode": status_code})
        return self.destination_response


class PatientCCDA(Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_response = {}

    def transform(self):
        patientid = self.source_json.get("patientid")

        patient_ccda = CCDA(self.customer_id, self.tenant_name, self.source_json)
        patient_ccda.authenticate()

        self.destination_json["category"] = "clinical-note"
        self.destination_json["patientid"] = patientid
        patient_ccda_record, status_code = patient_ccda.search_patient_documents(
            **self.destination_json
        )
        if status_code == 200 and patient_ccda_record.get("entry"):
            for single_clinical_docs in patient_ccda_record.get("entry"):
                if single_clinical_docs.get("resource").get("resourceType") == "Binary":
                    CCDA_record_id = single_clinical_docs.get("resource").get("id")
            binaryid = CCDA_record_id
            patient_ccda_actual_record, status_code = patient_ccda.get_patient_ccda(
                binaryid, **self.destination_json
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


class PatientQuerySyncTransformer(PatientQueryTransformer, Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.temp_response = {}
        self.patient_obj = None

    def transform(self, events):
        provider_group = self.source_json.get("pg_id")
        print("provider group>>>>", provider_group)
        try:
            patient_provider_group = ProviderGroup.objects.get(id=provider_group)

        except ProviderGroup.DoesNotExist:
            return Response({"detail": "Provider Group not found"}, status=400)
        patient_id = self.source_json.get("patientid")
        try:
            self.patient_obj = PatientModel.objects.get(
                id=patient_id, provider_group=patient_provider_group
            )
        except PatientModel.DoesNotExist:
            return Response({"detail": "Patient does not found"}, status=400)
        for event in events:
            # Conditions Data
            if event == "conditions" or event == "all":
                created_repsonse = self.create_conditions_entries(self.patient_obj)
                self.destination_response.update(created_repsonse)

            # Allergy Data
            if event == "allergies" or event == "all":
                created_repsonse = self.create_allergies_entries(self.patient_obj)
                self.destination_response.update(created_repsonse)

            # Medication Data
            if event == "medications" or event == "all":
                created_repsonse = self.create_medications_entries(self.patient_obj)
                self.destination_response.update(created_repsonse)

            # Lab Result Data
            if event == "labresult" or event == "all":
                created_repsonse = self.create_lab_result_entries(self.patient_obj)
                self.destination_response.update(created_repsonse)

            # Vitals Data
            if event == "vitals" or event == "all":
                created_repsonse = self.create_vitals_entries(self.patient_obj)
                self.destination_response.update(created_repsonse)
        return self.destination_response
