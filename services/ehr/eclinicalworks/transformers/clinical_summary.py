import logging
import uuid
import json
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Chart import Chart
from services.ehr.eclinicalworks.categories.Patient import Patient
from services.ehr.eclinicalworks.categories.DiagnosticReport import DiagnosticReport
from services.schemas import *

logger = logging.getLogger(__name__)


class PatientQueryTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.source_json = source_data
        self.connection = connection_obj
        self.patient_id = None
        self.destination_response = {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "PatientQueryResponse",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            },
        }

    def transform(self, events):
        try:
            idtype = self.source_json.get("Patient").get("Identifiers")[0].get("IDType")
            if idtype == "EHRID":
                self.patient_id = self.source_json.get("Patient").get("Identifiers")[0].get("ID")
            else:
                return Response({"error": "Invalid ID Type"}, status=status.HTTP_400_BAD_REQUEST)
            patients_chart = Chart(self.connection)
            patients_chart.authenticate()
            for event in events:
                event = event.lower()
                # Demographics Data (also handles "patient" event)
                if event == "demographics" or event == "patient" or event == "all":
                    demographics_json = {
                        "Header": {
                            "Patient": {
                                "Identifiers": [{}],
                                "Demographics": {
                                    "EmailAddresses": [{}],
                                    "PhoneNumber": {},
                                    "Address": {},
                                },
                            }
                        }
                    }
                    (
                        demographics_response,
                        status_code,
                    ) = patients_chart.get_patient_demographics(self.patient_id)
                    print("demographics_response", demographics_response, status_code)

                    # Add raw response if Test mode is enabled
                    if self.source_json.get("Meta", {}).get("Test"):
                        self.destination_response["Meta"]["Raw"].append(
                            demographics_response
                        )

                    if status_code == 200:
                        # Extract Patient resource from FHIR Bundle
                        patient_resource = None
                        if isinstance(demographics_response, dict):
                            if demographics_response.get("resourceType") == "Bundle":
                                entries = demographics_response.get("entry", [])
                                if entries and len(entries) > 0:
                                    patient_resource = entries[0].get("resource", {})
                            elif demographics_response.get("resourceType") == "Patient":
                                patient_resource = demographics_response

                        if patient_resource:
                            # Extract identifiers
                            identifiers = patient_resource.get("identifier", [])
                            if identifiers:
                                # Use the first identifier with 'usual' use, or first one
                                usual_id = next((id for id in identifiers if id.get("use") == "usual"), identifiers[0] if identifiers else None)
                                if usual_id:
                                    demographics_json["Header"]["Patient"]["Identifiers"][0]["ID"] = usual_id.get("value")
                                    demographics_json["Header"]["Patient"]["Identifiers"][0]["IDType"] = "EHRID"

                            # Extract name
                            names = patient_resource.get("name", [])
                            if names:
                                name = names[0]  # Use first name entry
                                given_names = name.get("given", [])
                                demographics_json["Header"]["Patient"]["Demographics"]["FirstName"] = given_names[0] if len(given_names) > 0 else None
                                demographics_json["Header"]["Patient"]["Demographics"]["MiddleName"] = given_names[1] if len(given_names) > 1 else None
                                demographics_json["Header"]["Patient"]["Demographics"]["LastName"] = name.get("family")

                            # Extract DOB
                            birth_date = patient_resource.get("birthDate")
                            if birth_date:
                                demographics_json["Header"]["Patient"]["Demographics"]["DOB"] = birth_date

                            # Extract gender
                            gender = patient_resource.get("gender", "").lower()
                            if gender == "male" or gender == "m":
                                demographics_json["Header"]["Patient"]["Demographics"]["Sex"] = "Male"
                            elif gender == "female" or gender == "f":
                                demographics_json["Header"]["Patient"]["Demographics"]["Sex"] = "Female"

                            # Extract telecom (phone and email)
                            telecom = patient_resource.get("telecom", [])
                            for contact in telecom:
                                system = contact.get("system", "")
                                value = contact.get("value", "")
                                use = contact.get("use", "")

                                if system == "phone":
                                    if use == "home":
                                        demographics_json["Header"]["Patient"]["Demographics"]["PhoneNumber"]["Home"] = value
                                    elif use == "mobile":
                                        demographics_json["Header"]["Patient"]["Demographics"]["PhoneNumber"]["Mobile"] = value
                                elif system == "email":
                                    demographics_json["Header"]["Patient"]["Demographics"]["EmailAddresses"][0]["Address"] = value

                            # Extract address
                            addresses = patient_resource.get("address", [])
                            if addresses:
                                address = addresses[0]  # Use first address
                                address_lines = address.get("line", [])
                                demographics_json["Header"]["Patient"]["Demographics"]["Address"]["StreetAddress"] = address_lines[0] if address_lines else None
                                demographics_json["Header"]["Patient"]["Demographics"]["Address"]["City"] = address.get("city")
                                demographics_json["Header"]["Patient"]["Demographics"]["Address"]["State"] = address.get("state")
                                demographics_json["Header"]["Patient"]["Demographics"]["Address"]["ZIP"] = address.get("postalCode")
                                demographics_json["Header"]["Patient"]["Demographics"]["Address"]["Country"] = address.get("country")

                            # Extract race and ethnicity from extensions (if available)
                            extensions = patient_resource.get("extension", [])
                            for ext in extensions:
                                url = ext.get("url", "")
                                if "us-core-race" in url:
                                    race_extensions = ext.get("extension", [])
                                    for race_ext in race_extensions:
                                        if race_ext.get("url") == "text":
                                            demographics_json["Header"]["Patient"]["Demographics"]["Race"] = race_ext.get("valueString")
                                elif "us-core-ethnicity" in url:
                                    ethnicity_extensions = ext.get("extension", [])
                                    for eth_ext in ethnicity_extensions:
                                        if eth_ext.get("url") == "text":
                                            demographics_json["Header"]["Patient"]["Demographics"]["Ethnicity"] = eth_ext.get("valueString")

                        self.destination_response.update(demographics_json)
                        print("destination_response", self.destination_response)
                        print("status_code", status_code)
                    else:
                        self.destination_response.update(demographics_response)
                        self.destination_response.update({"statuscode": status_code})
                # Allergies Data
                if event == "allergies" or event == "all":
                    allergies_json = {"Allergies": []}
                    (
                        allergies_response,
                        status_code,
                    ) = patients_chart.get_patient_allergy(self.patient_id)
                    print("allergies_response", allergies_response, status_code)
                    # Add raw response if Test mode is enabled
                    if self.source_json.get("Meta", {}).get("Test"):
                        self.destination_response["Meta"]["Raw"].append(
                            allergies_response
                        )
                    if status_code == 200:
                        # Check if response is a FHIR Bundle
                        if (
                            isinstance(allergies_response, dict)
                            and allergies_response.get("resourceType") == "Bundle"
                        ):
                            entries = allergies_response.get("entry", [])
                            # Handle empty Bundle (total: 0)
                            if allergies_response.get("total", 0) == 0 or not entries:
                                # Return empty Allergies array
                                self.destination_response.update(allergies_json)
                            else:
                                # Process each AllergyIntolerance resource from Bundle
                                for entry_item in entries:
                                    allergy_resource = entry_item.get("resource", {})
                                    if (
                                        not allergy_resource
                                        or allergy_resource.get("resourceType")
                                        != "AllergyIntolerance"
                                    ):
                                        continue

                                    # Extract Type/Substance from code
                                    code = allergy_resource.get("code", {})
                                    codings = code.get("coding", [])
                                    substance_code = None
                                    substance_name = None
                                    substance_code_system = None
                                    allergen_code = None
                                    allergen_name = None
                                    allergen_code_system = None

                                    # Get substance name from text as fallback
                                    substance_name = code.get("text")

                                    if codings:
                                        # Prefer RxNorm coding if available, otherwise use first
                                        rxnorm_coding = next(
                                            (c for c in codings if "rxnorm" in c.get("system", "").lower()),
                                            None
                                        )
                                        preferred_coding = rxnorm_coding if rxnorm_coding else codings[0]

                                        substance_code = preferred_coding.get("code")
                                        substance_code_system = preferred_coding.get("system")
                                        # Use display from coding, fallback to text from code
                                        substance_name = preferred_coding.get("display") or code.get("text") or substance_name
                                        allergen_code = substance_code
                                        allergen_name = substance_name
                                        allergen_code_system = substance_code_system
                                    elif substance_name:
                                        # If no coding but we have text, use that
                                        allergen_name = substance_name

                                    # Extract allergy type from category or type field
                                    categories = allergy_resource.get("category", [])
                                    allergy_type = allergy_resource.get("type", "")
                                    if categories:
                                        # Use first category
                                        allergy_type = categories[0] if isinstance(categories, list) else categories

                                    # Extract reactions
                                    reactions = []
                                    fhir_reactions = allergy_resource.get(
                                        "reaction", []
                                    )
                                    for fhir_reaction in fhir_reactions:
                                        reaction_manifestations = fhir_reaction.get(
                                            "manifestation", []
                                        )
                                        for manifestation in reaction_manifestations:
                                            manifestation_codings = manifestation.get(
                                                "coding", []
                                            )
                                            reaction_code = None
                                            reaction_name = None
                                            reaction_code_system = None

                                            # Handle both coded and text-only manifestations
                                            if manifestation_codings:
                                                reaction_coding = manifestation_codings[0]
                                                reaction_code = reaction_coding.get("code")
                                                reaction_code_system = reaction_coding.get("system")
                                                reaction_name = reaction_coding.get("display") or manifestation.get("text")
                                            else:
                                                # Fallback to text if no coding available
                                                reaction_name = manifestation.get("text")

                                            severity = fhir_reaction.get("severity", "")
                                            severity_code = None
                                            # Map FHIR severity to expected format
                                            if severity:
                                                severity_lower = severity.lower()
                                                if severity_lower == "mild":
                                                    severity_code = (
                                                        "255604002"  # Mild SNOMED code
                                                    )
                                                elif severity_lower == "moderate":
                                                    severity_code = "6736007"  # Moderate SNOMED code
                                                elif severity_lower == "severe":
                                                    severity_code = (
                                                        "24484000"  # Severe SNOMED code
                                                    )

                                            # Only add reaction if we have a name
                                            if reaction_name:
                                                reactions.append(
                                                    {
                                                        "Code": reaction_code,
                                                        "CodeSystem": reaction_code_system,
                                                        "CodeSystemName": None,
                                                        "Name": reaction_name,
                                                        "Severity": {
                                                            "Name": (
                                                                severity.title()
                                                                if severity
                                                                else None
                                                            ),
                                                            "Code": severity_code,
                                                            "CodeSystem": None,
                                                            "CodeSystemName": None,
                                                        },
                                                        "Text": reaction_name if not reaction_code else None,
                                                    }
                                                )

                                    # Extract criticality
                                    criticality = allergy_resource.get(
                                        "criticality", ""
                                    )

                                    # Extract dates
                                    onset_date = None
                                    if allergy_resource.get("onsetDateTime"):
                                        onset_date = allergy_resource.get(
                                            "onsetDateTime"
                                        )
                                    elif allergy_resource.get("onsetAge"):
                                        # Handle age-based onset if needed
                                        pass

                                    # Extract note/comment
                                    note = None
                                    notes = allergy_resource.get("note", [])
                                    if notes:
                                        note = (
                                            notes[0].get("text")
                                            if isinstance(notes[0], dict)
                                            else str(notes[0])
                                        )

                                    # Extract end date from clinicalStatus or recordDate
                                    end_date = None
                                    clinical_status = allergy_resource.get(
                                        "clinicalStatus", {}
                                    )
                                    if clinical_status:
                                        status_codings = clinical_status.get(
                                            "coding", []
                                        )
                                        if status_codings:
                                            status_code = status_codings[0].get(
                                                "code", ""
                                            )
                                            # If status indicates resolved/inactive
                                            if status_code in [
                                                "resolved",
                                                "inactive",
                                                "entered-in-error",
                                            ]:
                                                # Try to get lastUpdated from meta
                                                meta = allergy_resource.get("meta", {})
                                                if meta.get("lastUpdated"):
                                                    end_date = meta.get("lastUpdated")

                                    # Determine code system name
                                    code_system_name = None
                                    if substance_code_system:
                                        if "rxnorm" in substance_code_system.lower():
                                            code_system_name = "RxNorm"
                                        elif "snomed" in substance_code_system.lower():
                                            code_system_name = "SNOMED CT"
                                        elif "loinc" in substance_code_system.lower():
                                            code_system_name = "LOINC"

                                    allergies_json["Allergies"].append(
                                        {
                                            "Type": {
                                                "Code": allergen_code,
                                                "CodeSystem": allergen_code_system,
                                                "CodeSystemName": code_system_name,
                                                "Name": allergen_name or substance_name,
                                            },
                                            "Substance": {
                                                "Code": substance_code,
                                                "CodeSystem": substance_code_system,
                                                "CodeSystemName": code_system_name,
                                                "Name": substance_name,
                                            },
                                            "Reaction": reactions if reactions else [],
                                            "Criticality": {
                                                "Name": (
                                                    criticality.title()
                                                    if criticality
                                                    else None
                                                )
                                            },
                                            "StartDate": onset_date,
                                            "EndDate": end_date,
                                            "Comment": note,
                                        }
                                    )
                                self.destination_response.update(allergies_json)
                        else:
                            # Legacy format - try to access allergies key
                            if (
                                isinstance(allergies_response, dict)
                                and "allergies" in allergies_response
                            ):
                                for allergy in allergies_response["allergies"]:
                                    allergies_json["Allergies"].append(
                                        {
                                            "Type": {
                                                "Code": allergy.get("allergenid"),
                                                "CodeSystem": None,
                                                "CodeSystemName": None,
                                                "Name": allergy.get("allergenname"),
                                            },
                                            "Substance": {
                                                "Code": allergy.get("rxnormcode"),
                                                "CodeSystem": None,
                                                "CodeSystemName": None,
                                                "Name": allergy.get(
                                                    "rxnormdescription"
                                                ),
                                            },
                                            "Reaction": [
                                                {
                                                    "Code": reaction.get("snomedcode"),
                                                    "CodeSystem": None,
                                                    "CodeSystemName": None,
                                                    "Name": reaction.get(
                                                        "reactionname"
                                                    ),
                                                    "Severity": {
                                                        "Name": reaction.get(
                                                            "severity"
                                                        ),
                                                        "Code": reaction.get(
                                                            "severitysnomedcode"
                                                        ),
                                                        "CodeSystem": None,
                                                        "CodeSystemName": None,
                                                    },
                                                    "Text": None,
                                                }
                                                for reaction in allergy.get(
                                                    "reactions", []
                                                )
                                            ],
                                            "Criticality": {
                                                "Name": allergy.get("criticality")
                                            },
                                            "StartDate": allergy.get("onsetdate"),
                                            "EndDate": allergy.get("deactivatedate"),
                                            "Comment": allergy.get("note"),
                                        }
                                    )
                                self.destination_response.update(allergies_json)
                            else:
                                # Empty response - return empty Allergies array
                                self.destination_response.update(allergies_json)
                    else:
                        self.destination_response.update(allergies_response)
                        self.destination_response.update({"statuscode": status_code})
                if event == "medications" or event == "all":
                    medications_json = {"Medications": []}
                    medications_response, status_code = (
                        patients_chart.get_patient_medication(self.patient_id)
                    )
                    print("medications_response", medications_response, status_code)
                    # Add raw response if Test mode is enabled
                    if self.source_json.get("Meta", {}).get("Test"):
                        self.destination_response["Meta"]["Raw"].append(
                            medications_response
                        )

                    if status_code == 200:
                        # Check if response is a FHIR Bundle
                        if (
                            isinstance(medications_response, dict)
                            and medications_response.get("resourceType") == "Bundle"
                        ):
                            entries = medications_response.get("entry", [])
                            # Handle empty Bundle (total: 0)
                            if medications_response.get("total", 0) == 0 or not entries:
                                # Return empty Medications array
                                self.destination_response.update(medications_json)
                            else:
                                # Process each medication resource from Bundle
                                # Can be MedicationAdministration, MedicationStatement, or MedicationRequest
                                for entry_item in entries:
                                    medication_resource = entry_item.get("resource", {})
                                    resource_type = medication_resource.get("resourceType", "")
                                    if (
                                        not medication_resource
                                        or resource_type not in [
                                            "MedicationAdministration",
                                            "MedicationStatement",
                                            "MedicationRequest"
                                        ]
                                    ):
                                        continue

                                    # Extract encounter ID from context
                                    encounter_id = None
                                    context = medication_resource.get("context", {})
                                    if isinstance(context, dict) and context.get(
                                        "reference"
                                    ):
                                        encounter_ref = context.get("reference", "")
                                        encounter_id = (
                                            encounter_ref.split("/")[-1]
                                            if "/" in encounter_ref
                                            else None
                                        )

                                    # Extract medication information
                                    # Can be medicationCodeableConcept or medicationReference
                                    medication_codeable = medication_resource.get(
                                        "medicationCodeableConcept", {}
                                    )
                                    medication_reference = medication_resource.get(
                                        "medicationReference", {}
                                    )

                                    medication_name = medication_codeable.get("text") if medication_codeable else None
                                    medication_code = None
                                    medication_code_system = None

                                    # Extract from coding array if available
                                    if medication_codeable:
                                        codings = medication_codeable.get("coding", [])
                                        if codings:
                                            # Prefer RxNorm coding if available, otherwise use first
                                            rxnorm_coding = next(
                                                (c for c in codings if "rxnorm" in c.get("system", "").lower()),
                                                None
                                            )
                                            preferred_coding = rxnorm_coding if rxnorm_coding else codings[0]
                                            medication_code = preferred_coding.get("code")
                                            medication_code_system = preferred_coding.get("system")
                                            medication_name = preferred_coding.get("display") or medication_name or medication_codeable.get("text")

                                    # If medication is a reference, extract display name
                                    if medication_reference and not medication_name:
                                        medication_name = medication_reference.get("display")

                                    # Extract dosage information
                                    # MedicationAdministration uses "dosage" (single object)
                                    # MedicationStatement uses "dosage" (array)
                                    # MedicationRequest uses "dosageInstruction" (array)
                                    dosage = medication_resource.get("dosage", {})
                                    dosage_instruction = medication_resource.get("dosageInstruction", [])

                                    # Handle different resource types
                                    dosage_obj = None
                                    if resource_type == "MedicationRequest" and dosage_instruction:
                                        # Use first dosage instruction
                                        dosage_obj = dosage_instruction[0] if isinstance(dosage_instruction, list) else dosage_instruction
                                    elif resource_type == "MedicationStatement" and isinstance(dosage, list) and len(dosage) > 0:
                                        # Use first dosage from array
                                        dosage_obj = dosage[0]
                                    elif dosage and isinstance(dosage, dict):
                                        # Single dosage object
                                        dosage_obj = dosage

                                    dose_value = None
                                    dose_unit = None
                                    route_name = None

                                    if dosage_obj:
                                        # Extract dose
                                        dose = dosage_obj.get("doseAndRate", [{}])[0].get("doseQuantity", {}) if isinstance(dosage_obj.get("doseAndRate"), list) else dosage_obj.get("dose", {})
                                        if dose:
                                            if isinstance(dose, dict):
                                                dose_value = dose.get("value")
                                                dose_unit = dose.get("unit")
                                            else:
                                                dose_value = dose

                                        # Extract route
                                        route = dosage_obj.get("route", {})
                                        if route:
                                            route_codings = route.get("coding", [])
                                            if route_codings:
                                                route_name = route_codings[0].get(
                                                    "display"
                                                ) or route.get("text")
                                            else:
                                                route_name = route.get("text")

                                    # Extract status
                                    status = (
                                        medication_resource.get("status", "").upper()
                                        if medication_resource.get("status")
                                        else None
                                    )

                                    # Extract effective date (varies by resource type)
                                    effective_date = None
                                    if resource_type == "MedicationAdministration":
                                        effective_date = medication_resource.get("effectiveDateTime")
                                    elif resource_type == "MedicationStatement":
                                        effective_date = medication_resource.get("effectiveDateTime")
                                        if not effective_date:
                                            effective_period = medication_resource.get("effectivePeriod", {})
                                            effective_date = effective_period.get("start") if effective_period else None
                                    elif resource_type == "MedicationRequest":
                                        effective_date = medication_resource.get("authoredOn")
                                        if not effective_date:
                                            occurrence = medication_resource.get("occurrenceDateTime")
                                            effective_date = occurrence

                                    # Extract medication ID
                                    medication_id = medication_resource.get("id", "")

                                    # Determine code system name
                                    code_system_name = None
                                    if medication_code_system:
                                        if "rxnorm" in medication_code_system.lower():
                                            code_system_name = "RxNorm"
                                        elif "snomed" in medication_code_system.lower():
                                            code_system_name = "SNOMED CT"
                                        elif "ndc" in medication_code_system.lower():
                                            code_system_name = "NDC"

                                    medications_json["Medications"].append(
                                        {
                                            "Identifiers": (
                                                [
                                                    {
                                                        "ID": encounter_id,
                                                        "IDType": "EncounterID",
                                                    }
                                                ]
                                                if encounter_id
                                                else []
                                            ),
                                            "Dose": {
                                                "Quantity": dose_value,
                                                "Units": dose_unit,
                                            },
                                            "Route": {"Name": route_name},
                                            "Status": status,
                                            "StartDate": effective_date,
                                            "EndDate": None,  # MedicationAdministration doesn't have end date
                                            "Frequency": {
                                                "Period": None,  # Not available in MedicationAdministration
                                                "Unit": None,
                                            },
                                            "NumberOfRefillsRemaining": None,  # Not applicable for MedicationAdministration
                                            "Product": {
                                                "Code": medication_code or medication_id,
                                                "CodeSystem": medication_code_system,
                                                "CodeSystemName": code_system_name,
                                                "Name": medication_name,
                                            },
                                        }
                                    )

                                self.destination_response.update(medications_json)
                                print("medications_json updated", medications_json)
                        else:
                            # Legacy format - try to access medications key
                            if (
                                isinstance(medications_response, dict)
                                and "medications" in medications_response
                            ):
                                for medications in medications_response["medications"]:
                                    for medication in medications:
                                        medications_json["Medications"].append(
                                            {
                                                "Identifiers": [
                                                    {
                                                        "ID": medication.get(
                                                            "encounterid"
                                                        ),
                                                        "IDType": "EncounterID",
                                                    }
                                                ],
                                                "Dose": {
                                                    "Quantity": (
                                                        medication.get(
                                                            "structuredsig"
                                                        ).get("dosagequantityvalue")
                                                        if medication.get(
                                                            "structuredsig"
                                                        )
                                                        is not None
                                                        else None
                                                    ),
                                                    "Units": (
                                                        medication.get(
                                                            "structuredsig"
                                                        ).get("dosagequantityunit")
                                                        if medication.get(
                                                            "structuredsig"
                                                        )
                                                        is not None
                                                        else None
                                                    ),
                                                },
                                                "Route": {
                                                    "Name": medication.get("route")
                                                },
                                                "Status": medication.get("status"),
                                                "StartDate": (
                                                    (
                                                        [
                                                            (
                                                                md_start_date[
                                                                    "eventdate"
                                                                ]
                                                                if md_start_date["type"]
                                                                == "START"
                                                                else None
                                                            )
                                                            for md_start_date in medication.get(
                                                                "events", []
                                                            )
                                                        ]
                                                    )[0]
                                                    if medication.get("events")
                                                    else None
                                                ),
                                                "EndDate": (
                                                    (
                                                        [
                                                            (
                                                                md_start_date[
                                                                    "eventdate"
                                                                ]
                                                                if md_start_date["type"]
                                                                == "END"
                                                                else None
                                                            )
                                                            for md_start_date in medication.get(
                                                                "events", []
                                                            )
                                                        ]
                                                    )[0]
                                                    if medication.get("events")
                                                    else None
                                                ),
                                                "Frequency": {
                                                    "Period": (
                                                        medication.get(
                                                            "structuredsig"
                                                        ).get("dosagefrequencyvalue")
                                                        if medication.get(
                                                            "structuredsig"
                                                        )
                                                        is not None
                                                        else None
                                                    ),
                                                    "Unit": (
                                                        medication.get(
                                                            "structuredsig"
                                                        ).get("dosagefrequencyunit")
                                                        if medication.get(
                                                            "structuredsig"
                                                        )
                                                        is not None
                                                        else None
                                                    ),
                                                },
                                                "NumberOfRefillsRemaining": medication.get(
                                                    "refillsallowed"
                                                ),
                                                "Product": {
                                                    "Code": medication.get(
                                                        "medicationid"
                                                    ),
                                                    "Name": medication.get(
                                                        "medication"
                                                    ),
                                                },
                                            }
                                        )
                                self.destination_response.update(medications_json)
                            else:
                                # Empty response - return empty Medications array
                                self.destination_response.update(medications_json)
                    else:
                        self.destination_response.update(medications_response)
                        self.destination_response.update({"statuscode": status_code})
                if event == "vitals" or event == "all":
                    if self.source_json.get("StartDate") and self.source_json.get(
                        "EndDate"
                    ):
                        self.destination_json["startdate"] = datetime.strptime(
                            self.source_json.get("StartDate"),
                            "%Y-%m-%d",
                        ).strftime("%m/%d/%Y")
                        self.destination_json["enddate"] = datetime.strptime(
                            self.source_json.get("EndDate"),
                            "%Y-%m-%d",
                        ).strftime("%m/%d/%Y")

                    vitals_json = {"VitalSigns": []}
                    vitals_response, status_code = patients_chart.get_patient_vitals(
                        self.patient_id
                    )
                    if self.source_json["Meta"].get("Test"):
                        self.destination_response["Meta"]["Raw"].append(vitals_response)
                    if status_code == 200:
                        # Check if response is a FHIR Bundle
                        if (
                            isinstance(vitals_response, dict)
                            and vitals_response.get("resourceType") == "Bundle"
                        ):
                            entries = vitals_response.get("entry", [])
                            # Handle empty Bundle (total: 0)
                            if vitals_response.get("total", 0) == 0 or not entries:
                                # Return empty VitalSigns array
                                self.destination_response.update(vitals_json)
                            else:
                                # Group observations by effectiveDateTime (same time = same reading session)
                                vitals_by_datetime = {}

                                for entry_item in entries:
                                    observation_resource = entry_item.get(
                                        "resource", {}
                                    )
                                    if (
                                        not observation_resource
                                        or observation_resource.get("resourceType")
                                        != "Observation"
                                    ):
                                        continue

                                    # Extract datetime for grouping
                                    effective_datetime = observation_resource.get(
                                        "effectiveDateTime"
                                    )
                                    if not effective_datetime:
                                        continue

                                    # Initialize group if not exists
                                    if effective_datetime not in vitals_by_datetime:
                                        vitals_by_datetime[effective_datetime] = {
                                            "identifiers": [],
                                            "datetime": effective_datetime,
                                            "observations": [],
                                        }

                                    # Extract observation ID
                                    observation_id = observation_resource.get("id", "")

                                    # Extract encounter reference
                                    encounter_ref = observation_resource.get(
                                        "encounter", {}
                                    )
                                    encounter_id = None
                                    if isinstance(encounter_ref, dict):
                                        encounter_id = (
                                            encounter_ref.get("reference", "").split(
                                                "/"
                                            )[-1]
                                            if encounter_ref.get("reference")
                                            else None
                                        )

                                    # Add identifiers
                                    if observation_id:
                                        vitals_by_datetime[effective_datetime][
                                            "identifiers"
                                        ].append(
                                            {"ID": observation_id, "IDType": "VitalID"}
                                        )
                                    if encounter_id:
                                        vitals_by_datetime[effective_datetime][
                                            "identifiers"
                                        ].append(
                                            {
                                                "ID": encounter_id,
                                                "IDType": "EncounterID",
                                            }
                                        )

                                    # Extract code information
                                    code = observation_resource.get("code", {})
                                    code_codings = code.get("coding", [])
                                    code_value = None
                                    code_system = None
                                    code_display = code.get("text") or None

                                    if code_codings:
                                        first_coding = code_codings[0]
                                        code_value = first_coding.get("code")
                                        code_system = first_coding.get("system")
                                        if not code_display:
                                            code_display = first_coding.get("display")

                                    # Extract value
                                    value = None
                                    unit = None

                                    if observation_resource.get("valueQuantity"):
                                        value_quantity = observation_resource.get(
                                            "valueQuantity"
                                        )
                                        value = value_quantity.get("value")
                                        unit = value_quantity.get("unit")
                                    elif observation_resource.get("valueString"):
                                        value = observation_resource.get("valueString")
                                        unit = None

                                    # Handle simple observations (single value)
                                    if value is not None:
                                        vitals_by_datetime[effective_datetime][
                                            "observations"
                                        ].append(
                                            {
                                                "DateTime": effective_datetime,
                                                "Value": (
                                                    str(value).strip()
                                                    if value
                                                    else None
                                                ),
                                                "Units": unit,
                                                "TargetSite": {
                                                    "Code": code_value,
                                                    "CodeSystem": code_system,
                                                    "CodeSystemName": None,
                                                    "Name": code_display,
                                                },
                                            }
                                        )

                                    # Handle complex observations with components (e.g., blood pressure, pulse oximetry)
                                    components = observation_resource.get(
                                        "component", []
                                    )
                                    for component in components:
                                        component_code = component.get("code", {})
                                        component_codings = component_code.get(
                                            "coding", []
                                        )
                                        component_code_value = None
                                        component_code_system = None
                                        component_code_display = (
                                            component_code.get("text") or None
                                        )

                                        if component_codings:
                                            first_component_coding = component_codings[
                                                0
                                            ]
                                            component_code_value = (
                                                first_component_coding.get("code")
                                            )
                                            component_code_system = (
                                                first_component_coding.get("system")
                                            )
                                            if not component_code_display:
                                                component_code_display = (
                                                    first_component_coding.get(
                                                        "display"
                                                    )
                                                )

                                        component_value = None
                                        component_unit = None

                                        if component.get("valueQuantity"):
                                            component_value_quantity = component.get(
                                                "valueQuantity"
                                            )
                                            component_value = (
                                                component_value_quantity.get("value")
                                            )
                                            component_unit = (
                                                component_value_quantity.get("unit")
                                            )
                                        elif component.get("valueString"):
                                            component_value = component.get(
                                                "valueString"
                                            )

                                        if component_value is not None:
                                            vitals_by_datetime[effective_datetime][
                                                "observations"
                                            ].append(
                                                {
                                                    "DateTime": effective_datetime,
                                                    "Value": (
                                                        str(component_value).strip()
                                                        if component_value
                                                        else None
                                                    ),
                                                    "Units": component_unit,
                                                    "TargetSite": {
                                                        "Code": component_code_value,
                                                        "CodeSystem": component_code_system,
                                                        "CodeSystemName": None,
                                                        "Name": component_code_display,
                                                    },
                                                }
                                            )

                                # Convert grouped vitals to expected format
                                for (
                                    datetime_key,
                                    vital_data,
                                ) in vitals_by_datetime.items():
                                    # Remove duplicate identifiers
                                    unique_identifiers = []
                                    seen_ids = set()
                                    for ident in vital_data["identifiers"]:
                                        ident_key = (
                                            f"{ident.get('ID')}_{ident.get('IDType')}"
                                        )
                                        if ident_key not in seen_ids:
                                            unique_identifiers.append(ident)
                                            seen_ids.add(ident_key)

                                    vitals_json["VitalSigns"].append(
                                        {
                                            "Identifiers": (
                                                unique_identifiers
                                                if unique_identifiers
                                                else [{"ID": None, "IDType": "VitalID"}]
                                            ),
                                            "DateTime": vital_data["datetime"],
                                            "Observations": vital_data["observations"],
                                        }
                                    )

                                self.destination_response.update(vitals_json)
                        else:
                            # Legacy format - try to access vitals key
                            if (
                                isinstance(vitals_response, dict)
                                and "vitals" in vitals_response
                            ):
                                for vital in vitals_response["vitals"]:
                                    for reading in vital.get("readings", []):
                                        for observation in reading:
                                            vitals_json["VitalSigns"].append(
                                                {
                                                    "Identifiers": [
                                                        {
                                                            "ID": observation.get(
                                                                "vitalid"
                                                            ),
                                                            "IDType": "VitalID",
                                                        },
                                                        {
                                                            "ID": observation.get(
                                                                "clinicalelementid"
                                                            ),
                                                            "IDType": "Clinical Element ID",
                                                        },
                                                    ],
                                                    "DateTime": observation.get(
                                                        "createddate"
                                                    ),
                                                    "Observations": [
                                                        {
                                                            "DateTime": observation.get(
                                                                "readingtaken"
                                                            ),
                                                            "Value": observation.get(
                                                                "value"
                                                            ),
                                                            "Units": observation.get(
                                                                "unit"
                                                            ),
                                                            "TargetSite": {
                                                                "Code": observation.get(
                                                                    "code"
                                                                ),
                                                                "CodeSystem": None,
                                                                "CodeSystemName": observation.get(
                                                                    "codeset"
                                                                ),
                                                                "Name": observation.get(
                                                                    "codedescription"
                                                                ),
                                                            },
                                                        }
                                                    ],
                                                }
                                            )
                                    self.destination_response.update(vitals_json)
                            else:
                                # Empty response - return empty VitalSigns array
                                self.destination_response.update(vitals_json)
                    else:
                        self.destination_response.update(vitals_response)
                        self.destination_response.update({"statuscode": status_code})

                # Conditions/Problems Data
                if event == "conditions" or event == "problems" or event == "diagnoses" or event == "all":
                    conditions_json = {"Problems": []}

                    # Get category filter from source if provided (defaults to None for all conditions)
                    condition_category = self.source_json.get("ConditionCategory")

                    # Get onset date filters from source if provided
                    onset_date_start = self.source_json.get("StartDate")
                    onset_date_end = self.source_json.get("EndDate")

                    (
                        conditions_response,
                        status_code,
                    ) = patients_chart.get_patient_conditions(
                        patient_id=self.patient_id,
                        category=condition_category,
                        onset_date_start=onset_date_start,
                        onset_date_end=onset_date_end
                    )

                    # Add raw response if Test mode is enabled
                    if self.source_json.get("Meta", {}).get("Test"):
                        self.destination_response["Meta"]["Raw"].append(conditions_response)

                    if status_code == 200:
                        # Check if response is a FHIR Bundle
                        if (
                            isinstance(conditions_response, dict)
                            and conditions_response.get("resourceType") == "Bundle"
                        ):
                            entries = conditions_response.get("entry", [])

                            # Handle empty Bundle (total: 0)
                            if conditions_response.get("total", 0) == 0 or not entries:
                                # Return empty Problems array
                                self.destination_response.update(conditions_json)
                            else:
                                # Process each Condition resource from Bundle
                                for entry_item in entries:
                                    condition_resource = entry_item.get("resource", {})

                                    if (
                                        not condition_resource
                                        or condition_resource.get("resourceType") != "Condition"
                                    ):
                                        continue

                                    # Extract Condition ID
                                    condition_id = condition_resource.get("id", "")

                                    # Extract clinical status
                                    clinical_status = condition_resource.get("clinicalStatus", {})
                                    clinical_status_codings = clinical_status.get("coding", [])
                                    clinical_status_code = None
                                    clinical_status_display = clinical_status.get("text")

                                    if clinical_status_codings:
                                        first_status_coding = clinical_status_codings[0]
                                        clinical_status_code = first_status_coding.get("code")
                                        if not clinical_status_display:
                                            clinical_status_display = first_status_coding.get("display")

                                    # Extract verification status
                                    verification_status = condition_resource.get("verificationStatus", {})
                                    verification_status_codings = verification_status.get("coding", [])
                                    verification_status_code = None
                                    verification_status_display = verification_status.get("text")

                                    if verification_status_codings:
                                        first_ver_coding = verification_status_codings[0]
                                        verification_status_code = first_ver_coding.get("code")
                                        if not verification_status_display:
                                            verification_status_display = first_ver_coding.get("display")

                                    # Extract category
                                    categories = condition_resource.get("category", [])
                                    category_code = None
                                    category_display = None

                                    if categories:
                                        first_category = categories[0]
                                        category_codings = first_category.get("coding", [])
                                        category_display = first_category.get("text")

                                        if category_codings:
                                            first_cat_coding = category_codings[0]
                                            category_code = first_cat_coding.get("code")
                                            if not category_display:
                                                category_display = first_cat_coding.get("display")

                                    # Extract code (diagnosis code)
                                    code_data = condition_resource.get("code", {})
                                    code_codings = code_data.get("coding", [])
                                    code_text = code_data.get("text")

                                    # Process all codings to get ICD-10 and SNOMED codes
                                    icd10_code = None
                                    icd10_system = None
                                    snomed_code = None
                                    snomed_system = None
                                    primary_code = None
                                    primary_system = None
                                    primary_display = None

                                    for coding in code_codings:
                                        system = coding.get("system", "")
                                        code_val = coding.get("code")
                                        display = coding.get("display")

                                        if "icd-10" in system.lower():
                                            icd10_code = code_val
                                            icd10_system = system
                                            # Use ICD-10 as primary if available
                                            if not primary_code:
                                                primary_code = code_val
                                                primary_system = system
                                                primary_display = display
                                        elif "snomed" in system.lower():
                                            snomed_code = code_val
                                            snomed_system = system
                                        else:
                                            # Fallback to first coding
                                            if not primary_code:
                                                primary_code = code_val
                                                primary_system = system
                                                primary_display = display

                                    # Use ICD-10 code as primary, then SNOMED, then fallback
                                    if icd10_code:
                                        primary_code = icd10_code
                                        primary_system = icd10_system
                                    elif snomed_code:
                                        primary_code = snomed_code
                                        primary_system = snomed_system

                                    # Extract dates
                                    recorded_date = condition_resource.get("recordedDate")
                                    onset_datetime = condition_resource.get("onsetDateTime")
                                    abatement_datetime = condition_resource.get("abatementDateTime")

                                    # Extract encounter reference
                                    encounter_ref = condition_resource.get("encounter", {})
                                    encounter_id = None
                                    if isinstance(encounter_ref, dict) and encounter_ref.get("reference"):
                                        encounter_id = encounter_ref.get("reference", "").replace("Encounter/", "")

                                    # Extract recorder reference
                                    recorder_ref = condition_resource.get("recorder", {})
                                    recorder_id = None
                                    if isinstance(recorder_ref, dict) and recorder_ref.get("reference"):
                                        recorder_id = recorder_ref.get("reference", "").replace("Practitioner/", "")

                                    # Build the condition object
                                    condition_obj = {
                                        "Identifiers": [
                                            {
                                                "ID": condition_id,
                                                "IDType": "ConditionID",
                                            }
                                        ],
                                        "Code": primary_code,
                                        "CodeSystem": primary_system,
                                        "CodeSystemName": (
                                            "ICD-10-CM" if primary_system and "icd-10" in primary_system.lower()
                                            else "SNOMED CT" if primary_system and "snomed" in primary_system.lower()
                                            else None
                                        ),
                                        "Name": code_text or primary_display,
                                        "Category": {
                                            "Code": category_code,
                                            "Name": category_display,
                                        },
                                        "ClinicalStatus": {
                                            "Code": clinical_status_code,
                                            "Name": clinical_status_display,
                                        },
                                        "VerificationStatus": {
                                            "Code": verification_status_code,
                                            "Name": verification_status_display,
                                        },
                                        "OnsetDate": onset_datetime,
                                        "RecordedDate": recorded_date,
                                        "AbatementDate": abatement_datetime,
                                        "Encounter": {
                                            "ID": encounter_id,
                                        } if encounter_id else None,
                                        "Recorder": {
                                            "ID": recorder_id,
                                        } if recorder_id else None,
                                        "AlternateCodes": [],
                                    }

                                    # Add alternate codes (ICD-10 and SNOMED)
                                    if icd10_code:
                                        condition_obj["AlternateCodes"].append({
                                            "Code": icd10_code,
                                            "CodeSystem": icd10_system,
                                            "CodeSystemName": "ICD-10-CM",
                                        })
                                    if snomed_code:
                                        condition_obj["AlternateCodes"].append({
                                            "Code": snomed_code,
                                            "CodeSystem": snomed_system,
                                            "CodeSystemName": "SNOMED CT",
                                        })

                                    conditions_json["Problems"].append(condition_obj)

                                self.destination_response.update(conditions_json)
                        else:
                            # Legacy format - try to handle non-Bundle response
                            self.destination_response.update(conditions_json)
                    else:
                        self.destination_response.update(conditions_response)
                        self.destination_response.update({"statuscode": status_code})

            # Lab Results Data
                if event == "labresults" or event == "results" or event == "all":
                    results_json = {"Results": []}

                    diagnostic_report = DiagnosticReport(
                        self.connection
                    )
                    diagnostic_report.authenticate()
                    # Search for lab results by patient and category
                    lab_results_response, status_code = (
                        diagnostic_report.search_by_patient(
                            self.patient_id, category="LAB"
                        )
                    )
                    if self.source_json["Meta"].get("Test"):
                        self.destination_response["Meta"]["Raw"].append(
                            lab_results_response
                        )

                    if status_code == 200:
                        # Check if response is a FHIR Bundle
                        if (
                            isinstance(lab_results_response, dict)
                            and lab_results_response.get("resourceType") == "Bundle"
                        ):
                            entries = lab_results_response.get("entry", [])

                            # Handle empty Bundle
                            if lab_results_response.get("total", 0) == 0 or not entries:
                                # Return empty Results array
                                self.destination_response.update(results_json)
                            else:
                                # Process each DiagnosticReport resource from Bundle
                                for entry_item in entries:
                                    diagnostic_report_resource = entry_item.get(
                                        "resource", {}
                                    )
                                    if (
                                        not diagnostic_report_resource
                                        or diagnostic_report_resource.get(
                                            "resourceType"
                                        )
                                        != "DiagnosticReport"
                                    ):
                                        continue

                                    # Extract DiagnosticReport ID
                                    report_id = diagnostic_report_resource.get("id", "")

                                    # Extract status
                                    report_status = diagnostic_report_resource.get(
                                        "status", ""
                                    )

                                    # Extract code (test/panel name)
                                    code = diagnostic_report_resource.get("code", {})
                                    code_codings = code.get("coding", [])
                                    code_value = None
                                    code_system = None
                                    code_name = code.get("text") or None

                                    if code_codings:
                                        first_coding = code_codings[0]
                                        code_value = first_coding.get("code")
                                        code_system = first_coding.get("system")
                                        if not code_name:
                                            code_name = first_coding.get("display")

                                    # Extract effective date/time
                                    effective_datetime = diagnostic_report_resource.get(
                                        "effectiveDateTime"
                                    )

                                    # Extract encounter reference
                                    encounter_ref = diagnostic_report_resource.get(
                                        "encounter", {}
                                    )
                                    encounter_id = None
                                    if isinstance(
                                        encounter_ref, dict
                                    ) and encounter_ref.get("reference"):
                                        encounter_ref_str = encounter_ref.get(
                                            "reference", ""
                                        )
                                        encounter_id = (
                                            encounter_ref_str.split("/")[-1]
                                            if "/" in encounter_ref_str
                                            else encounter_ref_str
                                        )

                                    # Extract performer (lab/producer)
                                    performers = diagnostic_report_resource.get(
                                        "performer", []
                                    )
                                    producer = None
                                    if performers:
                                        first_performer = performers[0]
                                        if isinstance(
                                            first_performer, dict
                                        ) and first_performer.get("reference"):
                                            performer_ref = first_performer.get(
                                                "reference", ""
                                            )
                                            producer_id = (
                                                performer_ref.split("/")[-1]
                                                if "/" in performer_ref
                                                else performer_ref
                                            )
                                            producer_display = first_performer.get(
                                                "display"
                                            )
                                            producer = {
                                                "ID": producer_id,
                                                "IDType": "OrganizationID",
                                                "Name": producer_display,
                                            }

                                    # Extract specimen
                                    specimens = diagnostic_report_resource.get(
                                        "specimen", []
                                    )
                                    specimen = None
                                    if specimens:
                                        first_specimen = specimens[0]
                                        if isinstance(
                                            first_specimen, dict
                                        ) and first_specimen.get("reference"):
                                            specimen_ref = first_specimen.get(
                                                "reference", ""
                                            )
                                            specimen_id = (
                                                specimen_ref.split("/")[-1]
                                                if "/" in specimen_ref
                                                else specimen_ref
                                            )
                                            specimen = {
                                                "ID": specimen_id,
                                                "Source": None,  # Could be extracted from Specimen resource if needed
                                            }

                                    # Extract results (Observation references)
                                    result_observations = []
                                    results = diagnostic_report_resource.get(
                                        "result", []
                                    )
                                    for result_ref in results:
                                        if isinstance(
                                            result_ref, dict
                                        ) and result_ref.get("reference"):
                                            observation_ref = result_ref.get(
                                                "reference", ""
                                            )
                                            observation_id = (
                                                observation_ref.split("/")[-1]
                                                if "/" in observation_ref
                                                else observation_ref
                                            )

                                            # Try to find the Observation resource in the Bundle
                                            observation_resource = None
                                            for obs_entry in entries:
                                                obs_res = obs_entry.get("resource", {})
                                                if (
                                                    obs_res.get("resourceType")
                                                    == "Observation"
                                                    and obs_res.get("id")
                                                    == observation_id
                                                ):
                                                    observation_resource = obs_res
                                                    break

                                            if observation_resource:
                                                # Extract observation code
                                                obs_code = observation_resource.get(
                                                    "code", {}
                                                )
                                                obs_code_codings = obs_code.get(
                                                    "coding", []
                                                )
                                                obs_code_value = None
                                                obs_code_system = None
                                                obs_code_name = (
                                                    obs_code.get("text") or None
                                                )

                                                if obs_code_codings:
                                                    first_obs_coding = obs_code_codings[
                                                        0
                                                    ]
                                                    obs_code_value = (
                                                        first_obs_coding.get("code")
                                                    )
                                                    obs_code_system = (
                                                        first_obs_coding.get("system")
                                                    )
                                                    if not obs_code_name:
                                                        obs_code_name = (
                                                            first_obs_coding.get(
                                                                "display"
                                                            )
                                                        )

                                                # Extract observation value
                                                obs_value = None
                                                obs_value_type = None
                                                obs_units = None

                                                if observation_resource.get(
                                                    "valueQuantity"
                                                ):
                                                    value_quantity = (
                                                        observation_resource.get(
                                                            "valueQuantity"
                                                        )
                                                    )
                                                    obs_value = str(
                                                        value_quantity.get("value", "")
                                                    )
                                                    obs_units = value_quantity.get(
                                                        "unit"
                                                    )
                                                    obs_value_type = "Quantity"
                                                elif observation_resource.get(
                                                    "valueString"
                                                ):
                                                    obs_value = (
                                                        observation_resource.get(
                                                            "valueString"
                                                        )
                                                    )
                                                    obs_value_type = "String"
                                                elif observation_resource.get(
                                                    "valueCodeableConcept"
                                                ):
                                                    value_codeable = (
                                                        observation_resource.get(
                                                            "valueCodeableConcept"
                                                        )
                                                    )
                                                    value_codings = value_codeable.get(
                                                        "coding", []
                                                    )
                                                    if value_codings:
                                                        obs_value = value_codings[
                                                            0
                                                        ].get(
                                                            "display"
                                                        ) or value_codings[
                                                            0
                                                        ].get(
                                                            "code"
                                                        )
                                                    else:
                                                        obs_value = value_codeable.get(
                                                            "text"
                                                        )
                                                    obs_value_type = "CodeableConcept"
                                                elif observation_resource.get(
                                                    "valueBoolean"
                                                ):
                                                    obs_value = str(
                                                        observation_resource.get(
                                                            "valueBoolean"
                                                        )
                                                    )
                                                    obs_value_type = "Boolean"

                                                # Extract interpretation
                                                interpretation = None
                                                interpretations = (
                                                    observation_resource.get(
                                                        "interpretation", []
                                                    )
                                                )
                                                if interpretations:
                                                    first_interp = interpretations[0]
                                                    if isinstance(first_interp, dict):
                                                        interp_codings = (
                                                            first_interp.get(
                                                                "coding", []
                                                            )
                                                        )
                                                        if interp_codings:
                                                            interpretation = (
                                                                interp_codings[0].get(
                                                                    "display"
                                                                )
                                                                or interp_codings[
                                                                    0
                                                                ].get("code")
                                                            )
                                                        else:
                                                            interpretation = (
                                                                first_interp.get("text")
                                                            )
                                                    elif isinstance(first_interp, str):
                                                        interpretation = first_interp

                                                # Extract reference range
                                                reference_range = None
                                                ref_ranges = observation_resource.get(
                                                    "referenceRange", []
                                                )
                                                if ref_ranges:
                                                    first_range = ref_ranges[0]
                                                    low = None
                                                    high = None
                                                    text = None

                                                    if isinstance(first_range, dict):
                                                        low_quantity = first_range.get(
                                                            "low", {}
                                                        )
                                                        if low_quantity:
                                                            low = str(
                                                                low_quantity.get(
                                                                    "value", ""
                                                                )
                                                            )

                                                        high_quantity = first_range.get(
                                                            "high", {}
                                                        )
                                                        if high_quantity:
                                                            high = str(
                                                                high_quantity.get(
                                                                    "value", ""
                                                                )
                                                            )

                                                        text = first_range.get("text")

                                                    if low or high or text:
                                                        reference_range = {
                                                            "Low": low,
                                                            "High": high,
                                                            "Text": text,
                                                        }

                                                # Extract comments
                                                comments = []
                                                obs_notes = observation_resource.get(
                                                    "note", []
                                                )
                                                for note in obs_notes:
                                                    if isinstance(note, dict):
                                                        note_text = note.get("text")
                                                        if note_text:
                                                            comments.append(
                                                                {"Text": note_text}
                                                            )

                                                # Extract observation status
                                                obs_status = observation_resource.get(
                                                    "status", ""
                                                )

                                                # Extract effective date/time
                                                obs_datetime = observation_resource.get(
                                                    "effectiveDateTime"
                                                )

                                                result_observations.append(
                                                    {
                                                        "Code": obs_code_value,
                                                        "CodeSystem": obs_code_system,
                                                        "CodeSystemName": None,
                                                        "Name": obs_code_name,
                                                        "DateTime": obs_datetime,
                                                        "Status": obs_status,
                                                        "Value": obs_value,
                                                        "ValueType": obs_value_type,
                                                        "Units": obs_units,
                                                        "Interpretation": interpretation,
                                                        "ReferenceRange": reference_range,
                                                        "Comments": (
                                                            comments
                                                            if comments
                                                            else None
                                                        ),
                                                    }
                                                )

                                    # Build Result entry
                                    result_entry = {
                                        "Code": code_value,
                                        "CodeSystem": code_system,
                                        "CodeSystemName": None,
                                        "Name": code_name,
                                        "Status": report_status,
                                        "Observations": (
                                            result_observations
                                            if result_observations
                                            else []
                                        ),
                                    }

                                    # Add encounter if available
                                    if encounter_id:
                                        result_entry["Encounter"] = {
                                            "Identifiers": [
                                                {
                                                    "ID": encounter_id,
                                                    "IDType": "EncounterID",
                                                }
                                            ],
                                        }

                                    # Add producer if available
                                    if producer:
                                        result_entry["Producer"] = producer

                                    # Add specimen if available
                                    if specimen:
                                        result_entry["Specimen"] = specimen

                                    results_json["Results"].append(result_entry)

                                self.destination_response.update(results_json)
                        else:
                            # Non-Bundle response or error
                            if (
                                isinstance(lab_results_response, dict)
                                and "error" in lab_results_response
                            ):
                                self.destination_response.update(lab_results_response)
                            self.destination_response.update(
                                {"statuscode": status_code}
                            )
                    else:
                        # Error response
                        self.destination_response.update(lab_results_response)
                        self.destination_response.update({"statuscode": status_code})

        except Exception as e:
            logger.exception("PatientQueryTransformer failed for patient %s", self.patient_id)
            self.destination_response["Meta"]["Error"] = str(e)
            return self.destination_response

        return self.destination_response

class MedicationNewTransformer(Transformer):

    def __init__(self, connection_obj,source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {}


    def transform_medication(self):
        """
        Placeholder for medication transformation.
        """
        self.destination_response.update({"detail": "Medication transformation not yet implemented"})
        return self.destination_response

class ClinicalsPushTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {}

    def transform(self,event):
        match event:
            case "allergies":
                return self.transform_allergies()
            case "conditions":
                return self.transform_medication()
            case _:
                self.destination_response.update({"detail":"Not have apporpriate access to push clinical summary"})
        return self.destination_response

    def transform_allergies(self):
        """
        Transform source JSON from create_allergies API to FHIR AllergyIntolerance Bundle format.
        """
        try:
            # Get patient ID from source data
            patient_id = None
            patient_identifiers = self.source_json.get("Patient", {}).get("Identifiers", [])
            if patient_identifiers:
                for identifier in patient_identifiers:
                    if identifier.get("IDType") == "EHRID":
                        patient_id = identifier.get("ID")
                        break

            if not patient_id:
                self.destination_response.update({"error": "Patient ID not found in source data"})
                return self.destination_response

            # Get allergies from source data
            allergies = self.source_json.get("Allergies", [])

            if not allergies:
                self.destination_response.update({"error": "No allergies found in source data"})
                return self.destination_response

            # Build FHIR Bundle entries
            entries = []

            for allergy in allergies:
                # Generate unique ID for the resource
                resource_id = str(uuid.uuid4())

                # Extract substance/code information
                substance = allergy.get("Substance", {})
                allergy_type = allergy.get("Type", {})

                # Build coding list for code
                codings = []
                if substance.get("Code"):
                    coding_system = substance.get("CodeSystem") or "http://www.nlm.nih.gov/research/umls/rxnorm"
                    codings.append(
                        Coding(
                            system=coding_system,
                            code=str(substance.get("Code")),
                            display=substance.get("Name")
                        )
                    )
                elif allergy_type.get("Code"):
                    coding_system = allergy_type.get("CodeSystem") or "http://www.nlm.nih.gov/research/umls/rxnorm"
                    codings.append(
                        Coding(
                            system=coding_system,
                            code=str(allergy_type.get("Code")),
                            display=allergy_type.get("Name")
                        )
                    )

                # Build CodeableConcept for code
                code_text = substance.get("Name") or allergy_type.get("Name")
                code = CodeableConcept(
                    coding=codings if codings else None,
                    text=code_text
                )

                # Build clinical status
                clinical_status = CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                            code="active",
                            display="Active"
                        )
                    ]
                )

                # Build verification status
                verification_status = CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                            code="confirmed",
                            display="Confirmed"
                        )
                    ]
                )

                # Build reactions
                fhir_reactions = []
                source_reactions = allergy.get("Reaction", [])
                for source_reaction in source_reactions:
                    reaction_name = source_reaction.get("Name") or source_reaction.get("Text")
                    if reaction_name:
                        manifestation = Manifestation(text=reaction_name)
                        fhir_reactions.append(Reaction(manifestation=[manifestation]))

                # Map criticality
                criticality = None
                criticality_data = allergy.get("Criticality", {})
                if criticality_data.get("Name"):
                    criticality_name = criticality_data.get("Name", "").lower()
                    print("criticality_name", criticality_name)
                    if "hight" in criticality_name or "severe" in criticality_name:
                        criticality = "high"
                    elif "low" in criticality_name or "mild" in criticality_name:
                        criticality = "low"
                    else:
                        criticality = "unable-to-assess"

                # Map category based on type
                category = None
                type_name = allergy_type.get("Name", "").lower() if allergy_type.get("Name") else ""
                if "medication" in type_name or "drug" in type_name:
                    category = ["medication"]
                elif "food" in type_name:
                    category = ["food"]
                elif "environment" in type_name:
                    category = ["environment"]
                else:
                    category = ["medication"]  # Default to medication

                # Parse onset datetime
                onset_datetime = None
                start_date = allergy.get("StartDate")
                if start_date:
                    try:
                        # Try parsing different date formats
                        if isinstance(start_date, str):
                            for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%m/%d/%Y"]:
                                try:
                                    onset_datetime = datetime.strptime(start_date, fmt)
                                    break
                                except ValueError:
                                    continue
                    except Exception:
                        onset_datetime = None

                # Build the Resource
                resource = Resource(
                    resourceType="AllergyIntolerance",
                    id=resource_id,
                    meta=MetaData(
                        profile=["http://hl7.org/fhir/us/core/StructureDefinition/us-core-allergyintolerance"]
                    ),
                    clinicalStatus=clinical_status,
                    verificationStatus=verification_status,
                    category=category,
                    criticality=criticality,
                    code=code,
                    patient=Patient(reference=f"Patient/{patient_id}"),
                    onsetDateTime=onset_datetime,
                    reaction=fhir_reactions if fhir_reactions else None
                )

                # Build the Entry
                entry = Entry(
                    resource=resource,
                    request=Request(
                        method="POST",
                        url="AllergyIntolerance"
                    )
                )

                entries.append(entry)

            # Build the FHIR Bundle
            fhir_bundle = FHIRBundle(
                resourceType="Bundle",
                id=str(uuid.uuid4()),
                meta=MetaData(lastUpdated=datetime.now()),
                type="transaction",
                entry=entries
            )

            # Convert to JSON and print
            fhir_json = json.loads(fhir_bundle.model_dump_json(exclude_none=True))
            self.destination_response = fhir_json
            return self.destination_response

        except Exception as e:
            logger.exception("Error transforming allergies")
            self.destination_response.update({"error": str(e)})
            return self.destination_response
