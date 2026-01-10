from datetime import datetime
import logging
import uuid

from services.ehr.athena.categories.Patient import Patient
from services.ehr.athena.categories.Chart import Chart
from services.ehr.athena.categories.Appointment import Appointment
from services.ehr.athena.transformers.clinical_summary import PatientQueryTransformer

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
    "CPT": "2.16.840.1.113883.6.12",
}


class VisitQueryTransformer:
    def __init__(self, connection_obj, visit_data, connection_data, meta_data):
        self.connection_obj = connection_obj
        self.visit_data = visit_data  # Contains VisitNumber or startdate/enddate/departmentid
        self.departmentid = visit_data.get("departmentid") if visit_data.get("departmentid") else None
        self.meta_data = meta_data  # Original meta from request
        self.destination_response = {}
        self.patient_id = None
        self.appointment_data = None

    @staticmethod
    def _parse_date_to_iso(date_str, date_format="%m/%d/%Y"):
        """Parse date string to ISO format."""
        if not date_str:
            return None
        try:
            if isinstance(date_str, datetime):
                return date_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")
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
        """Parse ISO datetime strings."""
        if not dt_str:
            return None
        try:
            if isinstance(dt_str, datetime):
                return dt_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            if str(dt_str).endswith("Z"):
                dt_str = str(dt_str).replace("Z", "+00:00")
            date_obj = datetime.fromisoformat(str(dt_str))
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except (ValueError, TypeError, AttributeError) as e:
            logger.warning(f"Failed to parse ISO datetime '{dt_str}': {e}")
            return None

    def _build_base_response(self):
        """Build the base VisitQueryResponse structure."""
        # Generate IDs for response
        message_id = self.meta_data.get("Message", {}).get("ID") if isinstance(self.meta_data.get("Message"), dict) else None
        transmission_id = self.meta_data.get("Transmission", {}).get("ID") if isinstance(self.meta_data.get("Transmission"), dict) else None

        return {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "VisitQueryResponse",
                "EventDateTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "Test": self.meta_data.get("Test", True),
                "Source": {
                    "ID": str(uuid.uuid4()),
                    "Name": "EHR Bridge Dev Tools"
                },
                "Destinations": self.meta_data.get("Destinations", []),
                "Logs": self.meta_data.get("Logs", []),
                "Message": {"ID": message_id} if message_id else None,
                "Transmission": {"ID": transmission_id} if transmission_id else None,
                "FacilityCode": self.meta_data.get("FacilityCode")
            },
            "Header": {
                "Document": {
                    "Author": {
                        "ID": None,
                        "IDType": None,
                        "FirstName": None,
                        "LastName": None,
                        "Credentials": [],
                        "Address": {
                            "StreetAddress": None,
                            "City": None,
                            "State": None,
                            "ZIP": None,
                            "County": None,
                            "Country": None
                        },
                        "EmailAddresses": [],
                        "PhoneNumber": {"Office": None},
                        "Type": None,
                        "Location": {
                            "Type": None,
                            "Facility": None,
                            "Department": None,
                            "Room": None
                        }
                    },
                    "ID": str(uuid.uuid4()),
                    "Locale": "US",
                    "Title": None,
                    "DateTime": None,
                    "Type": "Progress Note",
                    "TypeCode": {
                        "Code": "18842-5",
                        "CodeSystem": CODE_SYSTEMS["LOINC"],
                        "CodeSystemName": "LOINC",
                        "Name": "Progress Note"
                    },
                    "Confidentiality": {
                        "Code": "R",
                        "CodeSystem": "2.16.840.1.113883.5.25",
                        "CodeSystemName": "Confidentiality",
                        "Name": "restricted"
                    },
                    "Custodian": {
                        "Identifiers": [],
                        "Name": None,
                        "Type": {
                            "Code": None,
                            "CodeSystem": None,
                            "CodeSystemName": None,
                            "Name": None,
                            "AltCodes": []
                        },
                        "Address": {
                            "StreetAddress": None,
                            "City": None,
                            "State": None,
                            "ZIP": None,
                            "County": None,
                            "Country": None
                        },
                        "Telecom": []
                    },
                    "Visit": []
                },
                "Patient": {
                    "Identifiers": [],
                    "Demographics": {
                        "FirstName": None,
                        "MiddleName": None,
                        "LastName": None,
                        "DOB": None,
                        "SSN": None,
                        "Sex": None,
                        "Address": {
                            "StreetAddress": None,
                            "City": None,
                            "State": None,
                            "County": None,
                            "Country": None,
                            "ZIP": None
                        },
                        "PhoneNumber": {
                            "Home": None,
                            "Mobile": None
                        },
                        "EmailAddresses": [],
                        "Language": None,
                        "Race": None,
                        "RaceCodes": [],
                        "Ethnicity": None,
                        "EthnicGroupCodes": [],
                        "Religion": None,
                        "MaritalStatus": None,
                        "IsDeceased": False,
                        "DeathDateTime": None
                    },
                    "Organization": {
                        "Identifiers": [],
                        "Name": None,
                        "Type": {
                            "Code": None,
                            "CodeSystem": None,
                            "CodeSystemName": None,
                            "Name": None,
                            "AltCodes": []
                        },
                        "Address": {
                            "StreetAddress": None,
                            "City": None,
                            "State": None,
                            "ZIP": None,
                            "County": None,
                            "Country": None
                        },
                        "Telecom": []
                    }
                },
                "PCP": {
                    "ID": None,
                    "IDType": None,
                    "FirstName": None,
                    "LastName": None,
                    "Credentials": [],
                    "Address": {
                        "StreetAddress": None,
                        "City": None,
                        "State": None,
                        "ZIP": None,
                        "County": None,
                        "Country": None
                    },
                    "EmailAddresses": [],
                    "PhoneNumber": {"Office": None},
                    "Type": None,
                    "Location": {
                        "Type": None,
                        "Facility": None,
                        "Department": None,
                        "Room": None
                    }
                }
            },
            "AdmissionDiagnosisText": None,
            "AdmissionDiagnosis": [],
            "AdvanceDirectivesText": None,
            "AdvanceDirectives": [],
            "AllergyText": None,
            "Allergies": [],
            "AssessmentText": None,
            "Assessment": {"Diagnoses": []},
            "CareTeams": [],
            "ChiefComplaintText": None,
            "DischargeDiagnosisText": None,
            "DischargeDiagnosis": [],
            "DischargeMedicationsText": None,
            "DischargeMedications": [],
            "EncountersText": None,
            "Encounters": [],
            "FamilyHistoryText": None,
            "FamilyHistory": [],
            "FunctionalStatusText": None,
            "FunctionalStatus": {"Observations": [], "Supplies": []},
            "GoalsText": None,
            "Goals": [],
            "HealthConcernsText": None,
            "HealthConcerns": [],
            "HistoryOfPresentIllnessText": None,
            "ImmunizationText": None,
            "Immunizations": [],
            "InstructionsText": None,
            "InsurancesText": None,
            "Insurances": [],
            "InterventionsText": None,
            "MedicalEquipmentText": None,
            "MedicalEquipment": [],
            "MedicationsText": None,
            "Medications": [],
            "MedicationsAdministeredText": None,
            "MedicationsAdministered": [],
            "ObjectiveText": None,
            "PhysicalExamText": None,
            "PlanOfCareText": None,
            "PlanOfCare": {
                "Orders": [],
                "Procedures": [],
                "Encounters": [],
                "MedicationAdministration": [],
                "Supplies": [],
                "Services": []
            },
            "ProblemsText": None,
            "Problems": [],
            "ProceduresText": None,
            "Procedures": {
                "Observations": [],
                "Procedures": [],
                "Services": []
            },
            "ResolvedProblemsText": None,
            "ResolvedProblems": [],
            "ReasonForReferralText": None,
            "ReasonForVisitText": None,
            "ReasonForVisit": [],
            "ResultText": None,
            "Results": [],
            "ReviewOfSystemsText": None,
            "SocialHistoryText": None,
            "SocialHistory": {
                "Observations": [],
                "Pregnancy": [],
                "TobaccoUse": []
            },
            "SubjectiveText": None,
            "VitalSignsText": None,
            "VitalSigns": []
        }

    def _parse_appointment_datetime(self, appointment, field_type="start"):
        """
        Parse appointment datetime from various possible field names and formats.
        field_type: "start" or "end"
        Handles: ISO format, MM/DD/YYYY, MM/DD/YYYY HH:MM:SS, and separate date/time fields
        """
        date_value = appointment.get("date")

        if field_type == "start":
            # Try combined datetime fields first
            dt_value = (appointment.get("appointmentdatetime") or
                       appointment.get("startdatetime") or
                       appointment.get("datetime"))

            # Get time value
            time_value = appointment.get("starttime") or appointment.get("time")
        else:  # field_type == "end"
            dt_value = appointment.get("enddatetime")
            time_value = appointment.get("endtime")

        # If we have a combined datetime value, try parsing it
        if dt_value:
            # Try ISO format first
            result = self._parse_iso_datetime(dt_value)
            if result:
                return result

            # Try MM/DD/YYYY format
            result = self._parse_date_to_iso(dt_value)
            if result:
                return result

            # Try MM/DD/YYYY HH:MM:SS format
            if isinstance(dt_value, str) and " " in dt_value and "/" in dt_value:
                try:
                    parts = dt_value.split()
                    if len(parts) >= 2:
                        date_part = parts[0]
                        time_part = parts[1]
                        if "/" in date_part:
                            date_obj = datetime.strptime(date_part, "%m/%d/%Y")
                            if ":" in time_part:
                                time_parts = time_part.split(":")
                                hour = int(time_parts[0])
                                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                                second = int(time_parts[2]) if len(time_parts) > 2 else 0
                                date_obj = date_obj.replace(hour=hour, minute=minute, second=second)
                            return date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                except (ValueError, TypeError, AttributeError, IndexError):
                    pass

        # If we have separate date and time, combine them
        if date_value and time_value:
            try:
                date_str = str(date_value)
                time_str = str(time_value)

                # If date already has time, use it as is
                if " " in date_str:
                    dt_str = date_str
                else:
                    dt_str = f"{date_str} {time_str}"

                # Parse MM/DD/YYYY HH:MM:SS format
                if "/" in dt_str:
                    parts = dt_str.split()
                    if len(parts) >= 1:
                        date_part = parts[0]
                        date_obj = datetime.strptime(date_part, "%m/%d/%Y")

                        # Add time if available
                        if len(parts) >= 2:
                            time_part = parts[1]
                            if ":" in time_part:
                                time_parts = time_part.split(":")
                                hour = int(time_parts[0])
                                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                                second = int(time_parts[2]) if len(time_parts) > 2 else 0
                                date_obj = date_obj.replace(hour=hour, minute=minute, second=second)

                        return date_obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except (ValueError, TypeError, AttributeError, IndexError):
                pass

        # Fallback: try date alone (will default to 00:00:00)
        if date_value:
            result = self._parse_date_to_iso(date_value) or self._parse_iso_datetime(date_value)
            if result:
                return result

        return None

    def _map_appointment_to_visit(self, appointment):
        """Map Athena appointment data to Visit structure."""
        visit = {
            "StartDateTime": self._parse_appointment_datetime(appointment, "start"),
            "EndDateTime": self._parse_appointment_datetime(appointment, "end"),
            "Reason": appointment.get("appointmenttype", {}).get("name") if isinstance(appointment.get("appointmenttype"), dict) else appointment.get("appointmenttype"),
            "VisitNumber": str(appointment.get("appointmentid", "")),
            "Type": {
                "Code": str(appointment.get("appointmenttypeid", "")),
                "CodeSystem": CODE_SYSTEMS["CPT"],
                "CodeSystemName": "CPT",
                "Name": appointment.get("appointmenttype", {}).get("name") if isinstance(appointment.get("appointmenttype"), dict) else appointment.get("appointmenttype"),
                "AltCodes": []
            },
            "Location": {
                "Type": "Outpatient Clinic",
                "Facility": appointment.get("department", {}).get("name") if isinstance(appointment.get("department"), dict) else None,
                "Department": appointment.get("department", {}).get("name") if isinstance(appointment.get("department"), dict) else None,
                "Room": appointment.get("roomname")
            },
            "DischargeDisposition": {
                "Code": None,
                "CodeSystem": None,
                "CodeSystemName": None,
                "Name": None,
                "AltCodes": []
            }
        }
        return visit

    def _map_patient_demographics(self, patient_response):
        """Map patient demographics using PatientQueryTransformer pattern."""
        from services.patientQ_response import patient_query

        # Reset patient_query demographics
        patient_query["Patient"]["Demographics"] = {}

        # Use PatientQueryTransformer's demographic_map method
        transformer = PatientQueryTransformer(self.connection_obj, self.patient_id, {"department_id": self.departmentid})
        transformer.demographic_map(patient_response)

        # Extract demographics from patient_query
        demographics = patient_query.get("Patient", {}).get("Demographics", {})

        return demographics

    def transform(self):
        """Main transform method."""
        try:
            # Initialize base response
            self.destination_response = self._build_base_response()

            # Initialize clients
            appointment = Appointment(self.connection_obj)
            appointment.authenticate()
            print("visit_data till here>>>",self.visit_data)
            # Determine query method
            visit_number = self.visit_data.get("VisitNumber")

            if visit_number:
                # Get appointment by ID
                appointment_response, status_code = appointment.get_appointment_by_id(visit_number)
                if status_code != 200:
                    logger.error(f"Failed to fetch appointment {visit_number}: status {status_code}")
                    return self.destination_response

                # Handle single appointment or list
                if isinstance(appointment_response, list) and len(appointment_response) > 0:
                    self.appointment_data = appointment_response[0]
                elif isinstance(appointment_response, dict):
                    self.appointment_data = appointment_response
                else:
                    logger.warning(f"Unexpected appointment response format")
                    return self.destination_response

                # Map single appointment to visit
                visit = self._map_appointment_to_visit(self.appointment_data)
                self.destination_response["Header"]["Document"]["Visit"] = [visit]

                # Update document metadata
                self.destination_response["Header"]["Document"]["DateTime"] = visit.get("StartDateTime")
                self.destination_response["Header"]["Document"]["Title"] = visit.get("Reason")
            else:
                # Get appointments by date range
                startdate = self.visit_data.get("StartDateTime")
                enddate = self.visit_data.get("EndDateTime")
                departmentid = self.departmentid
                print("startdate till here>>>",startdate)
                print("enddate till here>>>",enddate)
                print("departmentid till here>>>",departmentid)
                if not startdate or not enddate or not departmentid:
                    logger.error("Missing required fields: startdate, enddate, or departmentid")
                    return self.destination_response

                # Format dates for Athena API (MM/DD/YYYY)
                if isinstance(startdate, datetime):
                    startdate_str = startdate.strftime("%m/%d/%Y")
                elif isinstance(startdate, str):
                    # Try to parse ISO format or other formats
                    try:
                        if "T" in startdate:
                            dt = datetime.fromisoformat(startdate.replace("Z", "+00:00"))
                        else:
                            dt = datetime.strptime(startdate, "%Y-%m-%d")
                        startdate_str = dt.strftime("%m/%d/%Y")
                    except (ValueError, AttributeError):
                        # If parsing fails, try direct format
                        startdate_str = startdate
                else:
                    startdate_str = str(startdate)

                if isinstance(enddate, datetime):
                    enddate_str = enddate.strftime("%m/%d/%Y")
                elif isinstance(enddate, str):
                    # Try to parse ISO format or other formats
                    try:
                        if "T" in enddate:
                            dt = datetime.fromisoformat(enddate.replace("Z", "+00:00"))
                        else:
                            dt = datetime.strptime(enddate, "%Y-%m-%d")
                        enddate_str = dt.strftime("%m/%d/%Y")
                    except (ValueError, AttributeError):
                        # If parsing fails, try direct format
                        enddate_str = enddate
                else:
                    enddate_str = str(enddate)

                appointment_response, status_code = appointment.get_appointments_by_dates(
                    startdate=startdate_str,
                    enddate=enddate_str,
                    departmentid=str(departmentid)
                )

                if status_code != 200:
                    logger.error(f"Failed to fetch appointments: status {status_code}")
                    return self.destination_response

                # Get all appointments from list
                appointments = appointment_response.get("appointments", []) if isinstance(appointment_response, dict) else appointment_response
                if not appointments or len(appointments) == 0:
                    logger.warning("No appointments found")
                    return self.destination_response

                # Ensure appointments is a list
                if not isinstance(appointments, list):
                    appointments = [appointments]

                # Map all appointments to visits
                visits = []
                for apt in appointments:
                    visit = self._map_appointment_to_visit(apt)
                    visits.append(visit)

                # Set all visits in the response
                self.destination_response["Header"]["Document"]["Visit"] = visits

                # Use first appointment for patient ID and document metadata
                self.appointment_data = appointments[0]

                # Update document metadata from first visit
                if visits:
                    self.destination_response["Header"]["Document"]["DateTime"] = visits[0].get("StartDateTime")
                    self.destination_response["Header"]["Document"]["Title"] = visits[0].get("Reason")

            # Extract patient ID from appointment
            self.patient_id = self.appointment_data.get("patientid")
            if not self.patient_id:
                logger.error("No patient ID found in appointment data")
                return self.destination_response

            # Fetch and map patient data
            patient = Patient(self.connection_obj)
            patient.authenticate()
            patient_response, status_code = patient.get_patient_by_id(self.patient_id)
            if status_code == 200:
                # Use PatientQueryTransformer to map demographics
                demographics = self._map_patient_demographics(patient_response)
                self.destination_response["Header"]["Patient"]["Demographics"] = demographics
                # Map patient identifiers
                self.destination_response["Header"]["Patient"]["Identifiers"] = [
                    {
                        "ID": str(self.patient_id),
                        "IDType": "2.16.840.1.113883.4.6",
                        "Type": None
                    }
                ]

            # Fetch clinical data (allergies, medications, problems, vitals)
            charts = Chart(self.connection_obj)
            charts.authenticate()

            # Initialize PatientQueryTransformer for mapping
            from services.ehr.athena.transformers.clinical_summary import PatientQueryTransformer
            from services.patientQ_response import patient_query

            transformer = PatientQueryTransformer(self.connection_obj, self.patient_id, {"department_id": self.departmentid})

            # Get allergies
            allergy_response, status_code = charts.get_patient_allergies(self.patient_id, departmentid=self.departmentid)
            print("allergy_response till here>>>",allergy_response)
            if status_code == 200:
                # Reset allergies in patient_query before mapping
                patient_query["Allergies"] = []
                allergies = transformer.allergies_map(allergy_response)
                # allergies_map modifies patient_query and returns the list
                self.destination_response["Allergies"] = allergies if isinstance(allergies, list) else []

            # Get medications
            medication_response, status_code = charts.get_patient_medications(
                self.patient_id,
                departmentid=self.departmentid,
                showrxnorm=True
            )
            print("medication_response till here>>>",medication_response)
            if status_code == 200:
                # Reset medications in patient_query before mapping
                patient_query["Medications"] = []
                medications = transformer.medications_map(medication_response)
                # medications_map modifies patient_query and returns the list
                self.destination_response["Medications"] = medications if isinstance(medications, list) else []

            # Get problems/conditions
            condition_response, status_code = charts.get_patient_problems(self.patient_id, departmentid=self.departmentid)
            print("condition_response till here>>>",condition_response)
            if status_code == 200:
                # Reset problems in patient_query before mapping
                patient_query["Problems"] = []
                problems = transformer.conditions_map(condition_response)
                # conditions_map modifies patient_query and returns the list
                self.destination_response["Problems"] = problems if isinstance(problems, list) else []

            # Get vitals
            vitals_response, status_code = charts.get_patient_vitals(self.patient_id, departmentid=self.departmentid)
            print("vitals_response till here>>>",vitals_response)
            if status_code == 200:
                # Reset vitals in patient_query before mapping
                patient_query["VitalSigns"] = []
                vitals = transformer.vitals_map(vitals_response)
                # vitals_map modifies patient_query and returns the list
                self.destination_response["VitalSigns"] = vitals if isinstance(vitals, list) else []

            return self.destination_response

        except Exception as e:
            logger.error(f"Error in VisitQueryTransformer.transform: {str(e)}", exc_info=True)
            return self.destination_response
