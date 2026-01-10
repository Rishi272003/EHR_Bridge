from datetime import datetime

from rest_framework.response import Response

from ecaremd.careplan.models import Condition, ICDCode
from ecaremd.core.models.allergy import Allergy as PatientAllergyModel
from ecaremd.core.models.condition import PatientCondition
from ecaremd.core.models.medication import Medication as PatientMedicationModel
from ecaremd.core.models.patient import Patient as PatientModel
from ecaremd.core.models.provider import ProviderGroup
from ecaremd.ehr_integrations.constants import SNOWMED_ICD_MAPPING
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.AllergyIntolerance import (
    AllergyIntolerance,
)
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.Condition import (
    Conditions,
)
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.MedicationRequest import (
    MedicationRequest,
)
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.Observation import (
    Observation,
)
from ecaremd.ehr_integrations.ehr_services.advance_md.categories.Patient import Patient
from ecaremd.ehr_integrations.ehr_services.transformer import Transformer


class PatientClinicalTransformer(Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.ehr_name = self.source_json.get("ehr_name")
        self.provider_group = self.source_json.get("pg_id")
        self.patient_obj = None

    def transform(self, events):
        all_patients = self.source_json.get("patientid")
        try:
            self.provider_group = ProviderGroup.objects.get(id=self.provider_group)
        except ProviderGroup.DoesNotExist:
            return {
                "success": False,
                "status_code": 404,
                "error": "Provider Group not found",
            }

        for single_patient in all_patients or []:
            try:
                self.patient_obj = PatientModel.objects.get(ehr_id=single_patient)
                return Response({"detail": "Patient already imported"}, status=400)
            except PatientModel.DoesNotExist:
                for event in events:
                    if event == "demographics" or event == "all":
                        self.destination_response.update(
                            self.patient_demographics(single_patient)
                        )
                    if self.patient_obj:
                        if event == "allergies" or event == "all":
                            self.destination_response.update(
                                self.patient_allergies(single_patient)
                            )
                        if event == "medications" or event == "all":
                            self.destination_response.update(
                                self.patient_medications(single_patient)
                            )
                        if event == "conditions" or event == "all":
                            self.destination_response.update(
                                self.patient_conditions(single_patient)
                            )
                        if event == "vitals" or event == "all":
                            self.destination_response.update(
                                self.patient_vitals(single_patient)
                            )

                        if event == "lab_results" or event == "all":
                            self.destination_response.update(
                                self.patient_lab_results(single_patient)
                            )
        return self.destination_response

    def patient_demographics(self, patientid):
        patient_demographics = Patient(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_demographics.authenticate()
        (
            patient_response,
            status_code,
        ) = patient_demographics.get_patient_demographics_by_id(patientid=patientid)
        patient_payload = {}
        if status_code == 200 and patient_response:
            if patient_response.get("entry", []):
                entries = patient_response.get("entry", [])
                for entry in entries:
                    if entry.get("resource", {}):
                        resources = entry.get("resource", {})
                        if resources.get("name", []):
                            names = resources.get("name", [])
                            for name in names:
                                patient_payload["first_name"] = (
                                    name.get("given", [])[0]
                                    if name.get("given", [])
                                    else None
                                )
                                patient_payload["last_name"] = (
                                    name.get("family")
                                    if name.get("family", None)
                                    else None
                                )
                        patient_payload["dob"] = resources.get("birthDate", None)
                        patient_payload["sex"] = resources.get("gender", None)
                        if resources.get("address", []):
                            address = resources.get("address", [])
                            for patient_address in address:
                                for line_number, address_line in enumerate(
                                    patient_address.get("line", []), start=1
                                ):
                                    patient_payload[
                                        f"address_line_{line_number}"
                                    ] = address_line
                                if patient_address.get("city", None):
                                    patient_payload["city"] = patient_address.get(
                                        "city", None
                                    )
                                if patient_address.get("state", None):
                                    patient_payload["state"] = patient_address.get(
                                        "state", None
                                    )
                                if patient_address.get("postalCode", None):
                                    patient_payload["zip"] = patient_address.get(
                                        "postalCode", None
                                    )
                            if resources.get("telecom", None):
                                telecom = resources.get("telecom", [])
                                for patient_telecom in telecom:
                                    if patient_telecom.get("system", None) == "phone":
                                        patient_payload[
                                            "primary_phone"
                                        ] = patient_telecom.get("value", None)
                                    if patient_telecom.get("system", None) == "email":
                                        patient_payload["email"] = patient_telecom.get(
                                            "value", None
                                        )
            patient_payload["provider_group"] = self.provider_group
            patient_payload["ehr_name"] = self.ehr_name
            patient_payload["id"] = patientid
            super().create_patient(**patient_payload)
            try:
                self.patient_obj = PatientModel.objects.get(ehr_id=patientid)
            except PatientModel.DoesNotExist:
                return {
                    "success": False,
                    "status_code": 404,
                    "error": "Patient not found",
                }
        else:
            return {
                "success": False,
                "status_code": status_code,
                "error": patient_response,
            }
        return {
            "success": True,
            "status_code": status_code,
            "data": patient_response,
        }

    def patient_allergies(self, patientid):
        patient_allergies = AllergyIntolerance(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_allergies.authenticate()
        (
            patient_allergies_response,
            status_code,
        ) = patient_allergies.get_patient_allergies(patientid)
        allergy_payload = {}
        if status_code == 200 and patient_allergies_response:
            if patient_allergies_response.get("entry", []):
                entries = patient_allergies_response.get("entry", [])
                for single_allergy in entries:
                    resource = single_allergy.get("resource", {})
                    if resource.get("code", {}):
                        allergy_payload["name"] = resource.get(
                            "code", {"code": None}
                        ).get("text", None)
                    if resource.get("reaction", None):
                        for single_reaction in resource.get("reaction", []):
                            for single_reaction_name in single_reaction.get(
                                "manifestation", []
                            ):
                                allergy_payload["reaction"] = single_reaction_name.get(
                                    "text", None
                                )
                    allergy_payload["severity"] = single_reaction.get("severity", None)
                    if resource.get("recordedDate", None):
                        date_obj = datetime.fromisoformat(
                            resource.get("recordedDate", None).replace("Z", "00:00")
                        )
                        allergy_payload["created_date"] = date_obj.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

            allergy_payload["patientid"] = self.patient_obj
            allergy_payload["is_source_ehr"] = True
            if allergy_payload.get("name"):
                super().add_allergies(**allergy_payload)
            else:
                return {
                    "success": False,
                    "status_code": status_code,
                    "error": patient_allergies_response,
                }
        else:
            {
                "success": False,
                "status_code": status_code,
                "error": patient_allergies_response,
            }
        return {
            "success": True,
            "status_code": status_code,
            "data": patient_allergies_response,
        }

    def patient_medications(self, patientid):
        patient_medications = MedicationRequest(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_medications.authenticate()
        (
            patient_medications_response,
            status_code,
        ) = patient_medications.get_patient_medications(patientid)
        medication_payload = {}
        if status_code == 200 and patient_medications_response:
            if patient_medications_response.get("entry", []):
                entries = patient_medications_response.get("entry", [])
                for single_medication in entries:
                    resource = single_medication.get("resource", {})
                    if medication_name := resource.get(
                        "medicationCodeableConcept", {"medicationCodeableConcept": {}}
                    ).get("text", None):
                        medication_payload["name"] = medication_name
                    if resource.get("authoredOn", None):
                        # date_obj = datetime.fromisoformat(
                        #     resource.get("authoredOn", None).replace(
                        #         "Z", "00:00"
                        #     )
                        # )
                        medication_payload["created_date"] = resource.get(
                            "authoredOn", None
                        )
                    medication_payload["status"] = resource.get("status", None)
                    if resource.get("dosageInstruction", None):
                        for single_dosage_instruction in resource.get(
                            "dosageInstruction", None
                        ):
                            if single_dosage_instruction.get("text", None):
                                medication_payload[
                                    "comment"
                                ] = single_dosage_instruction.get("text", None)
                    medication_payload["patientid"] = self.patient_obj
                    super().add_medications(**medication_payload)
        else:
            return {
                "success": False,
                "status_code": status_code,
                "error": patient_medications_response,
            }
        return {
            "success": True,
            "status_code": status_code,
            "data": patient_medications_response,
        }

    def patient_vitals(self, patientid):
        patient_vitals = Observation(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_vitals.authenticate()
        self.destination_json["category"] = "vital-signs"
        self.destination_json["patient"] = patientid
        (
            patient_vitals_response,
            status_code,
        ) = patient_vitals.get_patient_observations(**self.destination_json)
        print("vital response>>>>>", patient_vitals_response)
        return {  # Not implemented due to lack of test data.
            "success": True,
            "status_code": status_code,
            "data": patient_vitals_response,
        }

    def patient_lab_results(self, patientid):
        patient_lab = Observation(self.customer_id, self.tenant_name, self.source_json)
        patient_lab.authenticate()
        self.destination_json["patient"] = patientid
        self.destination_json["category"] = "laboratory"
        (
            patient_lab_result_response,
            status_code,
        ) = patient_lab.get_patient_observations(**self.destination_json)
        print("patient lab result>>>>", patient_lab_result_response)
        return {
            "success": True,
            "status_code": status_code,
            "data": patient_lab_result_response,
        }

    def patient_conditions(self, patientid):
        patient_conditions = Conditions(
            self.customer_id, self.tenant_name, self.source_json
        )
        patient_conditions.authenticate()
        (
            patient_conditions_response,
            status_code,
        ) = patient_conditions.get_patient_conditions(patientid)
        condition_payload = {}
        if status_code == 200 and patient_conditions_response:
            if entries := patient_conditions_response.get("entry", []):
                for single_condition in entries:
                    icd_code = None
                    resource = single_condition.get("resource", {})
                    condition_name = resource.get("code", None).get("text", None)
                    if resource.get("code", None).get("coding", None):
                        for single_coding in resource.get("code", None).get(
                            "coding", []
                        ):
                            if (
                                single_coding.get("system", None)
                                == "http://snomed.info/sct"
                            ):
                                snomed_code = single_coding.get("code", None)
                                icd_code = SNOWMED_ICD_MAPPING.get(f"{snomed_code}")
                            else:
                                icd_code = single_coding.get("code", None)
                    if icd_code:
                        existing_icd_code = ICDCode.objects.filter(
                            code=icd_code
                        ).first()
                        if existing_icd_code:
                            condition_payload["icdcode"] = existing_icd_code
                        else:
                            new_icd_code = ICDCode.objects.create(
                                code=icd_code, title=condition_name
                            )
                            condition_payload["icdcode"] = new_icd_code
                    if condition_name:
                        existing_condition = Condition.objects.filter(
                            title=condition_name
                        ).first()
                        if existing_condition:
                            condition_payload["condition"] = existing_condition
                        else:
                            new_condition = Condition.objects.create(
                                title=condition_name
                            )
                            condition_payload["condition"] = new_condition
                    if recordedDate := resource.get("recordedDate", None):
                        condition_payload["start_date"] = recordedDate

                    condition_payload["patientid"] = self.patient_obj
                    super().add_conditions(**condition_payload)
        else:
            return {
                "success": False,
                "status_code": status_code,
                "error": patient_conditions_response,
            }
        return {
            "success": True,
            "status_code": status_code,
            "data": patient_conditions_response,
        }


class PatientClinicalSync(Transformer):
    def __init__(self, source_data, customer_id, tenant_name):
        super().__init__(source_data, customer_id, tenant_name)
        self.destination_json = {}
        self.destination_response = {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "PatientClinicalSync",
                "Source": {"ID": self.customer_id, "Name": self.tenant_name},
                "Raw": [],
            },
        }

    def transform(self, events):
        try:
            patient_obj = PatientModel.objects.get(
                ehr_id=self.source_json.get("patientid")
            )
        except PatientModel.DoesNotExist:
            self.destination_response.update(
                {
                    "success": False,
                    "status_code": 404,
                    "error": "Patient not found",
                }
            )
        for event in events:
            if event == "allergies" or event == "all":
                patient_allergies = AllergyIntolerance(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_allergies.authenticate()
                (
                    patient_allergies_response,
                    status_code,
                ) = patient_allergies.search_patient_allergies(patient_obj.ehr_id)
                if status_code == 200 and patient_allergies_response:
                    allergy_payload = {}
                    allergy_payload["patient"] = patient_obj
                    allergy_payload["name"] = patient_allergies_response.get(
                        "code", None
                    ).get("text", None)
                    if patient_allergies_response.get("reaction", None):
                        for single_reaction in patient_allergies_response.get(
                            "reaction", []
                        ):
                            for single_reaction_name in single_reaction.get(
                                "manifestation", []
                            ):
                                allergy_payload["reaction"] = single_reaction_name.get(
                                    "text", None
                                )
                            allergy_payload["severity"] = single_reaction.get(
                                "severity", None
                            )
                    if patient_allergies_response.get("recordedDate", None):
                        date_obj = datetime.fromisoformat(
                            patient_allergies_response.get(
                                "recordedDate", None
                            ).replace("Z", "00:00")
                        )
                        allergy_payload["created_date"] = date_obj.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    exists = PatientAllergyModel.objects.filter(
                        patient=patient_obj, name=allergy_payload["name"]
                    ).exists()
                    if not exists:
                        super().add_allergies(**allergy_payload)
                else:
                    self.destination_response.update(
                        {
                            "success": False,
                            "status_code": status_code,
                            "error": patient_allergies_response,
                        }
                    )
                self.destination_response.update(
                    {
                        "success": True,
                        "status_code": status_code,
                        "data": patient_allergies_response,
                    }
                )
                if event == "medications" or event == "all":
                    patient_medications = MedicationRequest(
                        self.customer_id, self.tenant_name, self.source_json
                    )
                    patient_medications.authenticate()
                    (
                        patient_medications_response,
                        status_code,
                    ) = patient_medications.search_patient_medications(
                        patient_obj.ehr_id
                    )
                    if status_code == 200 and patient_medications_response:
                        medication_payload = {}
                        medication_payload["patient"] = patient_obj
                        medication_payload["name"] = patient_medications_response.get(
                            "medicationCodeableConcept", None
                        ).get("text", None)
                        if patient_medications_response.get("authoredOn", None):
                            date_obj = datetime.fromisoformat(
                                patient_medications_response.get(
                                    "authoredOn", None
                                ).replace("Z", "00:00")
                            )
                            medication_payload["created_date"] = date_obj.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        medication_payload["status"] = patient_medications_response.get(
                            "status", None
                        )
                        exists = PatientMedicationModel.objects.filter(
                            patient=patient_obj, name=medication_payload["name"]
                        ).exists()
                        if not exists:
                            super().add_medications(**medication_payload)
                    else:
                        self.destination_response.update(
                            {
                                "success": False,
                                "status_code": status_code,
                                "error": patient_medications_response,
                            }
                        )
                    self.destination_response.update(
                        {
                            "success": True,
                            "status_code": status_code,
                            "data": patient_medications_response,
                        }
                    )
            if event == "vitals" or event == "all":
                patient_vitals = Observation(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_vitals.authenticate()
                self.destination_json["patient"] = patient_obj.ehr_id
                self.destination_json["category"] = "vital-signs"
                (
                    patient_vitals_response,
                    status_code,
                ) = patient_vitals.search_patient_vitals(**self.destination_json)
                self.destination_response.update(patient_vitals_response)
            if event == "conditions" or event == "all":
                patient_conditions = Condition(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_conditions.authenticate()
                (
                    patient_conditions_response,
                    status_code,
                ) = patient_conditions.search_patient_conditions(patient_obj.ehr_id)
                if status_code == 200 and patient_conditions_response:
                    condition_payload = {}
                    condition_payload["patient"] = patient_obj
                    condition_name = patient_conditions_response.get("code", None).get(
                        "text", None
                    )
                    if patient_conditions_response.get("code", None).get(
                        "coding", None
                    ):
                        for single_coding in patient_conditions_response.get(
                            "code", None
                        ).get("coding", []):
                            snomed_code = single_coding.get("code", None)
                            icd_code = SNOWMED_ICD_MAPPING[snomed_code]
                    if icd_code:
                        existing_icd_code = ICDCode.objects.filter(
                            code=icd_code
                        ).first()
                        if existing_icd_code:
                            condition_payload["icdcode"] = existing_icd_code
                        else:
                            new_icd_code = ICDCode.objects.create(
                                code=icd_code, title=condition_name
                            )
                            condition_payload["icdcode"] = new_icd_code
                    if condition_name:
                        existing_condition = Condition.objects.filter(
                            title=condition_name
                        ).first()
                        if existing_condition:
                            condition_payload["condition"] = existing_condition
                        else:
                            new_condition = Condition.objects.create(
                                title=condition_name
                            )
                            condition_payload["condition"] = new_condition
                    if patient_conditions_response.get("recordedDate", None):
                        date_obj = datetime.fromisoformat(
                            patient_conditions_response.get(
                                "recordedDate", None
                            ).replace("Z", "00:00")
                        )
                        condition_payload["start_date"] = date_obj.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    exists = PatientCondition.objects.filter(
                        patient=patient_obj, condition=condition_payload["condition"]
                    ).exists()
                    if not exists:
                        super().add_conditions(**condition_payload)
                else:
                    self.destination_response.update(
                        {
                            "success": False,
                            "status_code": status_code,
                            "error": patient_conditions_response,
                        }
                    )
                self.destination_response.update(
                    {
                        "success": True,
                        "status_code": status_code,
                        "data": patient_conditions_response,
                    }
                )
            if event == "lab_results" or event == "all":
                patient_lab = Observation(
                    self.customer_id, self.tenant_name, self.source_json
                )
                patient_lab.authenticate()
                self.destination_json["patient"] = patient_obj.ehr_id
                self.destination_json["category"] = "laboratory"
                (
                    patient_lab_result_response,
                    status_code,
                ) = patient_lab.search_patient_lab_results(**self.destination_json)
        return self.destination_response


class PatientDocument(Transformer):
    def __init__(self, customer_id, tenant_name, source_json):
        super().__init__(customer_id, tenant_name, source_json)
        self.destination_json = {}
        self.destination_response = {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "PatientDocument",
                "Source": {"ID": self.customer_id, "Name": self.tenant_name},
            }
        }

    def transform(self):
        pass


class PatientCCDA(Transformer):
    def __init__(self, customer_id, tenant_name, source_json):
        super().__init__(customer_id, tenant_name, source_json)
        self.destination_json = {}
        self.destination_response = {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "PatientCCDA",
                "Source": {"ID": self.customer_id, "Name": self.tenant_name},
            }
        }

    def transform(self):
        pass
