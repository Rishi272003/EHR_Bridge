from datetime import datetime
from collections import defaultdict
import logging

from services.ehr.athena.categories.Patient import Patient
from services.ehr.athena.categories.Chart import Chart
from services.patientQ_response import patient_query

logger = logging.getLogger(__name__)

# Code System OIDs
CODE_SYSTEMS = {
    "SNOMED_CT": "2.16.840.1.113883.6.96",
    "LOINC": "2.16.840.1.113883.6.1",
    "RxNorm": "2.16.840.1.113883.6.88",
    "ICD10_CM": "2.16.840.1.113883.6.90",
    "ICD9_CM": "2.16.840.1.113883.6.103",
    "NCI_THESAURUS": "2.16.840.1.113883.3.26.1.1",
    "OBSERVATION_VALUE": "2.16.840.1.113883.5.1063",
}

class PatientQueryTransformer():
    def __init__(self,connection_obj,patient_id,source_data):
        self.connection_obj = connection_obj
        self.patient_id = patient_id
        self.departmentid = source_data.get("Location").get("Department") if source_data.get("Location") else None
        self.source_data = source_data
        self.destination_response = {}

    @staticmethod
    def _parse_date(date_str, date_format="%m/%d/%Y"):
        """
        Utility method to parse date strings to ISO format.
        Returns ISO formatted string or None if parsing fails.
        """
        if not date_str:
            return None

        try:
            # Handle datetime strings with time component
            if " " in str(date_str):
                date_part = str(date_str).split()[0]
                date_obj = datetime.strptime(date_part, date_format)
            else:
                date_obj = datetime.strptime(str(date_str), date_format)
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return None

    @staticmethod
    def _parse_iso_datetime(dt_str):
        """
        Utility method to parse ISO datetime strings.
        Handles both Z and timezone offset formats.
        """
        if not dt_str:
            return None

        try:
            # Handle Z format
            if str(dt_str).endswith("Z"):
                dt_str = str(dt_str).replace("Z", "+00:00")
            date_obj = datetime.fromisoformat(str(dt_str))
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Failed to parse ISO datetime '{dt_str}': {e}")
            return None
    def transform(self,events):
        charts = Chart(self.connection_obj)
        charts.authenticate()
        for event in events:
            if event=="patients":
                patient = Patient(self.connection_obj)
                patient.authenticate()
                patient_response,status_code = patient.get_patient_by_id(self.patient_id)
                if status_code == 200:
                    self.destination_response["patient"]=self.demographic_map(patient_response)
                else:
                    logger.warning(f"Failed to fetch patient: status {status_code}")
            if event=="allergies":
                allergy_response,status_code = charts.get_patient_allergies(self.patient_id,departmentid=self.departmentid)
                if status_code == 200:
                    self.destination_response["allergies"]=self.allergies_map(allergy_response)
                else:
                    logger.warning(f"Failed to fetch allergies: status {status_code}")
            if event=="medications":
                medication_response,status_code = charts.get_patient_medications(
                    self.patient_id,
                    departmentid=self.departmentid,
                    showrxnorm=True  # Request RxNorm codes for proper mapping
                )
                if status_code == 200:
                    self.destination_response["medication"]=self.medications_map(medication_response)
                else:
                    logger.warning(f"Failed to fetch medications: status {status_code}")
            if event=="conditions":
                condition_response,status_code = charts.get_patient_problems(self.patient_id,departmentid=self.departmentid)
                if status_code == 200:
                    self.destination_response["conditions"]=self.conditions_map(condition_response)
                else:
                    logger.warning(f"Failed to fetch conditions: status {status_code}")
            if event=="vitals":
                vitals_response,status_code = charts.get_patient_vitals(self.patient_id,departmentid=self.departmentid)
                if status_code == 200:
                    self.destination_response["vitals"]=self.vitals_map(vitals_response)
                else:
                    logger.warning(f"Failed to fetch vitals: status {status_code}")

        return patient_query
    def demographic_map(self,patient_response):
        print("patient response>>>>",patient_response)
        ethnicitycodes = []
        for patient in patient_response:
            if patient.get("ethnicitycodes"):
                print("ethnicity codes>>>>",patient.get("ethnicitycodes"))
                if isinstance(codes:=patient.get("ethnicitycodes"),list):
                    for code in codes:
                        ethnicitycode={
                            "code":code,
                            "system":None,
                            "CodeSystemName":"CDC Race and Ethnicity",
                            "Name":patient.get("racename")
                        }
                        ethnicitycodes.append(ethnicitycode)
            patient_query["Patient"]["Demographics"] = {
                "FirstName":patient.get("firstname"),
                "MiddleName":patient.get("middlename"),
                "LastName":patient.get("lastname"),
                "DOB":patient.get("dob"),
                "SSN":patient.get("ssn"),
                "Sex":patient.get("sex"),
                "Address":{
                "StreetAddress":patient.get("address2"),
                "City":patient.get("city"),
                "State":patient.get("state"),
                "County":patient.get("county"),
                "Country":patient.get("countrycode"),
                "ZIP":patient.get("zip")},
                "PhoneNumber":{
                "Home":patient.get("homephone"),
                "Mobile":patient.get("mobilephone")},
                "EmailAddresses":[
                    {"Address":patient.get("email")}
                    ],
                "Language":patient.get("language6392code"),
                "Race":patient.get("racename"),
                "RaceCodes":[
                    {"Code":patient.get("racecode"),
                    "CodeSystem":patient.get("racecodesystem"),
                    "CodeSystemName":patient.get("racecodesystemname"),
                    "Name":patient.get("racename")}
                    ],
                "Ethnicity":patient.get("ethnicity"),
                "EthnicGroupCodes":ethnicitycodes if ethnicitycodes else None,
                "Religion":patient.get("religion"),
                "MaritalStatus":patient.get("maritalstatus"),
                "IsDeceased":patient.get("isdeceased"),
                "DeathDateTime":patient.get("deathdatetime")
            }

    def allergies_map(self, allergy_response):
        """
        Maps Athena allergies response to standard patient query format.
        Athena response structure: {"allergies": [{allergy1}, {allergy2}, ...]}
        """
        allergies = allergy_response.get("allergies", [])

        if not allergies:
            return patient_query["Allergies"]

        for allergy in allergies:
            reactions = []

            # Extract reactions from allergy (not from allergy_response)
            if allergy.get("reactions") and isinstance(allergy.get("reactions"), list):
                for reaction in allergy.get("reactions"):
                    reaction_payload = {
                        "Code": reaction.get("snomedcode"),
                        "CodeSystem": CODE_SYSTEMS["SNOMED_CT"] if reaction.get("snomedcode") else None,
                        "CodeSystemName": "SNOMED CT",
                        "Name": reaction.get("reactioname") or reaction.get("reactionname"),
                        "AltCodes": [],
                        "Severity": {
                            "Code": reaction.get("severitycode"),
                            "CodeSystem": "2.16.840.1.113883.6.96" if reaction.get("severitycode") else None,
                            "CodeSystemName": "SNOMED CT" if reaction.get("severitycode") else None,
                            "Name": reaction.get("severityname")
                        },
                        "Text": reaction.get("reactioname") or reaction.get("reactionname")
                    }
                    reactions.append(reaction_payload)

            # Build comments array from sectionnote if available
            comments = []
            section_note = allergy.get("sectionnote") or allergy_response.get("sectionnote")
            if section_note:
                if isinstance(section_note, str):
                    # Split by newlines if multiple comments
                    comment_lines = section_note.split("\n")
                    for line in comment_lines:
                        if line.strip():
                            comments.append({"Text": line.strip()})
                elif isinstance(section_note, list):
                    comments = [{"Text": str(note)} for note in section_note if note]

            allergy_payload = {
                "Type": {
                    "Code": allergy.get("allergytypeid"),
                    "CodeSystem": "2.16.840.1.113883.6.96" if allergy.get("allergytypeid") else None,
                    "CodeSystemName": "SNOMED CT",
                    "Name": allergy.get("allergenname"),
                    "AltCodes": []
                },
                "Substance": {
                    "Code": allergy.get("rxnormcode"),
                    "CodeSystem": CODE_SYSTEMS["RxNorm"] if allergy.get("rxnormcode") else None,
                    "CodeSystemName": "RxNorm",
                    "Name": allergy.get("allergenname"),
                    "AltCodes": []
                },
                "Reaction": reactions,
                "Severity": {
                    "Code": allergy.get("severitycode"),
                    "CodeSystem": CODE_SYSTEMS["SNOMED_CT"] if allergy.get("severitycode") else None,
                    "CodeSystemName": "SNOMED CT" if allergy.get("severitycode") else None,
                    "Name": allergy.get("severityname")
                },
                "Criticality": {
                    "Code": allergy.get("criticalitycode"),
                    "CodeSystem": CODE_SYSTEMS["OBSERVATION_VALUE"] if allergy.get("criticalitycode") else None,
                    "CodeSystemName": "ObservationValue" if allergy.get("criticalitycode") else None,
                    "Name": allergy.get("criticalityname")
                },
                "Status": {
                    "Code": allergy.get("statuscode"),
                    "CodeSystem": CODE_SYSTEMS["SNOMED_CT"] if allergy.get("statuscode") else None,
                    "CodeSystemName": "SNOMED CT" if allergy.get("statuscode") else None,
                    "Name": allergy.get("statusname")
                },
                "StartDate": allergy.get("startdate"),
                "EndDate": allergy.get("lastmodifieddatetime") or allergy.get("enddate"),
                "Comment": allergy.get("note"),
                "Comments": comments
            }
            patient_query["Allergies"].append(allergy_payload)

        return patient_query["Allergies"]
    def medications_map(self,medication_response):
        """
        Maps Athena medication response to standard patient query format.
        Athena response structure: {"medications": [[{medication1}, {medication2}, ...]]}
        """

        # Handle nested array structure from Athena
        medications_list = medication_response.get("medications", [])

        # Flatten the nested array structure
        all_medications = []
        for medication_group in medications_list:
            if isinstance(medication_group, list):
                all_medications.extend(medication_group)
            else:
                all_medications.append(medication_group)

        for medication in all_medications:
            # Extract start date from events array
            start_date = None
            if medication.get("events") and isinstance(medication.get("events"), list):
                for event in medication.get("events"):
                    if event.get("type") == "ENTER" and event.get("eventdate"):
                        try:
                            # Convert MM/DD/YYYY to ISO format
                            date_obj = datetime.strptime(event.get("eventdate"), "%m/%d/%Y")
                            start_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                        except (ValueError, TypeError):
                            start_date = None
                        break

            # Extract end date from lastmodifieddate if discontinued
            end_date = None
            if medication.get("isdiscontinued") and medication.get("lastmodifieddate"):
                try:
                    date_obj = datetime.strptime(medication.get("lastmodifieddate"), "%m/%d/%Y")
                    end_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                except (ValueError, TypeError):
                    end_date = None

            # Map status
            status = None
            if medication.get("isdiscontinued"):
                status = "discontinued"
            elif medication.get("status"):
                status = medication.get("status").lower()

            # Determine if prescription based on orderingmode
            is_prescription = medication.get("orderingmode") == "PRESCRIBE" if medication.get("orderingmode") else False

            # Map route - Athena provides route as string, need to map to standard codes
            # Note: "FAX" is an ordering method, not a route, so we set route to None in that case
            route_code = None
            route_name = medication.get("route")
            route_code_system = "2.16.840.1.113883.3.26.1.1"  # NCI Thesaurus
            route_code_system_name = "NCI Thesaurus"

            # Common route mappings (can be expanded)
            route_mapping = {
                "ORAL": {"code": "C38288", "name": "Oral"},
                "INHALATION": {"code": "C38216", "name": "RESPIRATORY (INHALATION)"},
                "TOPICAL": {"code": "C38299", "name": "Topical"},
                "INJECTION": {"code": "C38238", "name": "Injection"},
                "INTRAVENOUS": {"code": "C38276", "name": "Intravenous"},
                "INTRAMUSCULAR": {"code": "C38245", "name": "Intramuscular"},
                "SUBCUTANEOUS": {"code": "C38288", "name": "Subcutaneous"},
            }

            # Handle special cases where route is actually an ordering method
            ordering_methods = ["FAX", "ELECTRONIC", "PHONE", "MAIL"]

            if route_name:
                route_upper = route_name.upper()
                if route_upper in ordering_methods:
                    # This is an ordering method, not a route
                    route_name = None
                    route_code = None
                elif route_upper in route_mapping:
                    route_code = route_mapping[route_upper]["code"]
                    route_name = route_mapping[route_upper]["name"]
                else:
                    # Use the route name as-is if not in mapping
                    route_code = None

            # Build medication payload according to standard format
            medication_payload = {
                "Prescription": is_prescription,
                "FreeTextSig": None,  # Athena doesn't provide this in the sample
                "Dose": {
                    "Quantity": None,  # Not available in Athena response
                    "Units": None
                },
                "Rate": {
                    "Quantity": None,
                    "Units": None
                },
                "Route": {
                    "Code": route_code,
                    "CodeSystem": route_code_system if route_code else None,
                    "CodeSystemName": route_code_system_name if route_code else None,
                    "Name": route_name,
                    "AltCodes": []
                },
                "Status": status,
                "StartDate": start_date,
                "EndDate": end_date,
                "Frequency": {
                    "Period": None,
                    "PeriodMax": None,
                    "Unit": None,
                    "EventCode": None,
                    "InstitutionSpecified": None
                },
                "NumberOfRefillsRemaining": medication.get("refillsallowed") if medication.get("refillsallowed") is not None else None,
                "IsPRN": None,  # Not directly available in Athena response
                "Product": self._build_product_info(medication),
                "Indications": [],  # Not available in Athena response
                "SupplyOrder": {
                    "StartDate": None,
                    "EndDate": None,
                    "Quantity": None,
                    "Units": None,
                    "NumberOfRefillsRemaining": medication.get("refillsallowed") if medication.get("refillsallowed") is not None else None
                }
            }

            patient_query["Medications"].append(medication_payload)

        return patient_query["Medications"]

    def _build_product_info(self, medication):
        """
        Helper method to build Product information from medication data.
        Extracts RxNorm codes and alternative codes.
        """
        # Extract RxNorm code if available (when showrxnorm=True in API call)
        # Common field names: rxnormcode, rxnorm, rxnormcodeid
        rxnorm_code = (
            medication.get("rxnormcode") or
            medication.get("rxnorm") or
            medication.get("rxnormcodeid") or
            None
        )

        alt_codes = []
        if medication.get("fdbmedicationid"):
            alt_codes.append({
                "Code": str(medication.get("fdbmedicationid")),
                "CodeSystem": None,  # FDB uses proprietary system
                "CodeSystemName": "First Databank",
                "Name": medication.get("medicationtallmanname") or medication.get("medication")
            })

        return {
            "Code": str(rxnorm_code) if rxnorm_code else None,
                    "CodeSystem": CODE_SYSTEMS["RxNorm"] if rxnorm_code else None,
            "CodeSystemName": "RxNorm" if rxnorm_code else None,
            "Name": medication.get("medicationtallmanname") or medication.get("medication"),
            "AltCodes": alt_codes
        }

    def conditions_map(self, problems_response):
        """
        Maps Athena problems/conditions response to standard patient query format.
        Athena response structure: {"problems": [{problem1}, {problem2}, ...]}
        """

        # Get problems list from response
        problems_list = problems_response.get("problems", [])

        for problem in problems_list:
            # Extract start date from events array
            start_date = None
            end_date = None
            status_code = None
            status_name = None
            comment = None

            if problem.get("events") and isinstance(problem.get("events"), list):
                for event in problem.get("events"):
                    event_type = event.get("eventtype", "").upper()

                    if event_type == "START":
                        # Try startdate first, then onsetdate
                        date_str = event.get("startdate") or event.get("onsetdate")
                        if date_str:
                            try:
                                # Convert MM/DD/YYYY to ISO format
                                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                                start_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                            except (ValueError, TypeError):
                                start_date = None

                        # Get status from event
                        event_status = event.get("status")
                        if event_status:
                            status_code, status_name = self._map_problem_status(event_status)

                        # Get comment/note from event
                        if not comment:  # Only set if not already set
                            comment = event.get("note")

                    elif event_type in ["STOP", "RESOLVED", "END"]:
                        # Try to extract end date from stop/resolved events
                        date_str = event.get("startdate") or event.get("enddate") or event.get("createddate")
                        if date_str and not end_date:
                            try:
                                # Convert MM/DD/YYYY to ISO format
                                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                                end_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                            except (ValueError, TypeError):
                                pass

                        # Update status if resolved
                        if event_type == "RESOLVED":
                            status_code = "413322009"
                            status_name = "Resolved"

            # If no start date from events, try lastmodifieddatetime
            if not start_date and problem.get("lastmodifieddatetime"):
                try:
                    # Parse ISO format datetime (handles both Z and timezone offset formats)
                    dt_str = problem.get("lastmodifieddatetime")
                    if dt_str.endswith("Z"):
                        dt_str = dt_str.replace("Z", "+00:00")
                    date_obj = datetime.fromisoformat(dt_str)
                    start_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                except (ValueError, TypeError, AttributeError):
                    start_date = None

            # Map code system
            codeset = problem.get("codeset", "").upper()
            code_system = None
            code_system_name = None

            if codeset == "SNOMED":
                code_system = CODE_SYSTEMS["SNOMED_CT"]
                code_system_name = "SNOMED CT"
            elif codeset in ["ICD10", "ICD-10"]:
                code_system = CODE_SYSTEMS["ICD10_CM"]
                code_system_name = "ICD-10-CM"
            elif codeset in ["ICD9", "ICD-9"]:
                code_system = CODE_SYSTEMS["ICD9_CM"]
                code_system_name = "ICD-9-CM"

            # Build comments array from sectionnote if available
            comments = []
            section_note = problems_response.get("sectionnote")
            if section_note:
                # Split by newlines if multiple comments
                comment_lines = section_note.split("\n")
                for line in comment_lines:
                    if line.strip():
                        comments.append({"Text": line.strip()})

            # Build problem payload according to standard format
            problem_payload = {
                "StartDate": start_date,
                "EndDate": end_date,  # Athena doesn't provide end date in sample
                "Code": problem.get("code"),
                "CodeSystem": code_system,
                "CodeSystemName": code_system_name,
                "Name": problem.get("name"),
                "AltCodes": [],  # Athena doesn't provide alternative codes in sample
                "Category": {
                    "Code": "409586006",  # Default: Complaint (SNOMED CT)
                    "CodeSystem": CODE_SYSTEMS["SNOMED_CT"],
                    "CodeSystemName": "SNOMED CT",
                    "Name": "Complaint",
                    "AltCodes": []
                },
                "Status": {
                    "Code": status_code,
                    "CodeSystem": CODE_SYSTEMS["SNOMED_CT"] if status_code else None,
                    "CodeSystemName": "SNOMED CT" if status_code else None,
                    "Name": status_name
                },
                "Comment": comment,
                "Comments": comments,
                "HealthStatus": {
                    "Code": None,  # Not available in Athena response
                    "CodeSystem": None,
                    "CodeSystemName": None,
                    "Name": None,
                    "AltCodes": []
                }
            }

            patient_query["Problems"].append(problem_payload)

        return patient_query["Problems"]

    def _map_problem_status(self, athena_status):
        """
        Maps Athena problem status to SNOMED CT codes.
        Returns tuple: (code, name)
        """
        status_mapping = {
            "CHRONIC": {
                "code": "55561003",
                "name": "Active"
            },
            "ACTIVE": {
                "code": "55561003",
                "name": "Active"
            },
            "RESOLVED": {
                "code": "413322009",
                "name": "Resolved"
            },
            "INACTIVE": {
                "code": "73425007",
                "name": "Inactive"
            },
            "REMISSION": {
                "code": "73425007",
                "name": "Inactive"
            }
        }

        status_upper = athena_status.upper() if athena_status else ""
        mapped_status = status_mapping.get(status_upper)

        if mapped_status:
            return mapped_status["code"], mapped_status["name"]
        else:
            # Default to Active if status not recognized
            return "55561003", "Active"

    def vitals_map(self, vitals_response):
        """
        Maps Athena vitals response to standard patient query format.
        Athena response structure: {"vitals": [{vital_type1}, {vital_type2}, ...]}
        Each vital type has readings array (nested array structure).
        """

        # Get vitals list from response
        vitals_list = vitals_response.get("vitals", [])

        # Group observations by readingtaken date (DateTime)
        # Structure: {datetime: [observations]}
        vitals_by_datetime = defaultdict(list)

        for vital_type in vitals_list:
            readings = vital_type.get("readings", [])

            # Flatten nested readings array
            all_readings = []
            for reading_group in readings:
                if isinstance(reading_group, list):
                    all_readings.extend(reading_group)
                else:
                    all_readings.append(reading_group)

            for reading in all_readings:
                # Extract date from readingtaken
                reading_date = None
                reading_datetime_str = reading.get("readingtaken")

                if reading_datetime_str:
                    try:
                        # Try MM/DD/YYYY format first
                        if " " in reading_datetime_str:
                            # Has time component: "MM/DD/YYYY HH:MM:SS"
                            date_obj = datetime.strptime(reading_datetime_str.split()[0], "%m/%d/%Y")
                        else:
                            # Just date: "MM/DD/YYYY"
                            date_obj = datetime.strptime(reading_datetime_str, "%m/%d/%Y")
                        reading_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    except (ValueError, TypeError):
                        reading_date = None

                # If no readingtaken, try createddate
                if not reading_date:
                    created_date_str = reading.get("createddate")
                    if created_date_str:
                        try:
                            # Format: "MM/DD/YYYY HH:MM:SS"
                            date_obj = datetime.strptime(created_date_str.split()[0], "%m/%d/%Y")
                            reading_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                        except (ValueError, TypeError):
                            reading_date = None

                # Use a default date if still no date found
                if not reading_date:
                    reading_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

                # Map code system
                codeset = reading.get("codeset", "").upper()
                code_system = None
                code_system_name = None

                if codeset == "LOINC":
                    code_system = CODE_SYSTEMS["LOINC"]
                    code_system_name = "LOINC"
                elif codeset == "SNOMED":
                    code_system = CODE_SYSTEMS["SNOMED_CT"]
                    code_system_name = "SNOMED CT"

                # Build observation
                observation = {
                    "Code": reading.get("code"),
                    "CodeSystem": code_system,
                    "CodeSystemName": code_system_name,
                    "Name": reading.get("codedescription") or reading.get("clinicalelementid", "").split(".")[-1],
                    "AltCodes": [],
                    "Status": "completed",  # Default status
                    "Interpretation": None,  # Not available in Athena response
                    "DateTime": reading_date,
                    "Value": reading.get("value"),
                    "Units": reading.get("unit") or self._get_default_unit(reading.get("code")),
                    "TargetSite": {
                        "Code": None,
                        "CodeSystem": None,
                        "CodeSystemName": None,
                        "Name": None,
                        "AltCodes": []
                    },
                    "Comments": []
                }

                # Add observation to the appropriate datetime group
                vitals_by_datetime[reading_date].append(observation)

        # Build VitalSigns array grouped by DateTime
        for datetime_key in sorted(vitals_by_datetime.keys()):
            vital_sign_entry = {
                "DateTime": datetime_key,
                "Observations": vitals_by_datetime[datetime_key]
            }
            patient_query["VitalSigns"].append(vital_sign_entry)

        return patient_query["VitalSigns"]

    def _get_default_unit(self, loinc_code):
        """
        Returns default unit for common LOINC codes if unit is not provided.
        """
        unit_mapping = {
            "8302-2": "cm",  # Height
            "3141-9": "kg",  # Weight
            "8480-6": "mm[Hg]",  # Systolic BP
            "8462-4": "mm[Hg]",  # Diastolic BP
            "8867-4": "bpm",  # Heart rate
            "9279-1": "breaths/min",  # Respiration rate
            "8310-5": "Cel",  # Temperature
            "2708-6": "%",  # O2 Saturation
            "39156-5": "kg/m2",  # BMI
        }
        return unit_mapping.get(loinc_code)
