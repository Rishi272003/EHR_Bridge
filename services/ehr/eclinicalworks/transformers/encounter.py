from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Chart import Chart
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
class VisitQuerTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.source_json = source_data
        self.connection = connection_obj
        self.destination_response = {
            "Meta": {
                "DataModel": "Clinical Summary",
                "EventType": "VisitQueryResponse",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            },
            "Header": {
                "Document": {
                    "Visit": {
                        "Type": {},
                        "Encounter": {},
                    }
                },
                "Patient": {
                    "Identifiers": [],
                    "Organization": {"Identifiers": []},
                },
            },
        }

    def transform(self):
        chart = Chart(self.connection)
        chart.authenticate()
        try:
            # Extract patient ID from source data
            patient_identifiers = self.source_json.get("Patient", {}).get("Identifiers", [])
            patient_id = patient_identifiers[0].get("ID") if patient_identifiers else None

            if not patient_id:
                return Response({"Error": "Patient ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract visit query parameters
            visit_number = self.source_json.get("Visit", {}).get("VisitNumber")
            start_date = self.source_json.get("Visit", {}).get("StartDateTime")
            end_date = self.source_json.get("Visit", {}).get("EndDateTime")
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            # Call appropriate API based on available parameters
            if visit_number:
                encounter_response, status_code = chart.get_patient_encounter(
                    patientid=None, visit_number=visit_number
                )
            elif start_date and end_date and patient_id:
                encounter_response, status_code = chart.get_patient_encounter(
                    patientid=patient_id, start_date=start_date, end_date=end_date
                )
            elif patient_id:
                print("patient_id", patient_id)
                encounter_response, status_code = chart.get_patient_encounter(
                    patientid=patient_id
                )
                print("encounter_response", encounter_response, status_code)
            else:
                return Response({"Error": "Invalid request parameters"}, status=status.HTTP_400_BAD_REQUEST)

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(encounter_response)

            if status_code == 200:
                # Transform FHIR Encounter Bundle response
                if (
                    isinstance(encounter_response, dict)
                    and encounter_response.get("resourceType") == "Bundle"
                ):
                    entries = encounter_response.get("entry", [])

                    if encounter_response.get("total", 0) == 0 or not entries:
                        # No encounters found
                        self.destination_response["Header"]["Document"]["Visit"] = {}
                    else:
                        # Process encounters - if visit_number provided, find specific one, otherwise use first
                        encounter_resource = None
                        if visit_number:
                            # Find the specific encounter by ID
                            for entry_item in entries:
                                resource = entry_item.get("resource", {})
                                if (
                                    resource.get("resourceType") == "Encounter"
                                    and resource.get("id") == visit_number
                                ):
                                    encounter_resource = resource
                                    break
                        else:
                            # Use first encounter
                            for entry_item in entries:
                                resource = entry_item.get("resource", {})
                                if resource.get("resourceType") == "Encounter":
                                    encounter_resource = resource
                                    break

                        if encounter_resource:
                            # Extract encounter ID
                            enc_id = encounter_resource.get("id", "")

                            # Extract status
                            enc_status = encounter_resource.get("status", "")

                            # Extract class (visit type)
                            enc_class = encounter_resource.get("class", {})
                            class_code = (
                                enc_class.get("code", "")
                                if isinstance(enc_class, dict)
                                else ""
                            )
                            class_display = (
                                enc_class.get("display", "")
                                if isinstance(enc_class, dict)
                                else ""
                            )
                            class_system = (
                                enc_class.get("system", "")
                                if isinstance(enc_class, dict)
                                else ""
                            )

                            # Extract type (service type)
                            enc_types = encounter_resource.get("type", [])
                            service_type = None
                            if enc_types:
                                first_type = enc_types[0]
                                type_codings = first_type.get("coding", [])
                                if type_codings:
                                    service_type = {
                                        "Code": type_codings[0].get("code"),
                                        "Name": type_codings[0].get("display"),
                                        "CodeSystem": type_codings[0].get("system"),
                                    }

                            # Extract period (start/end dates)
                            period = encounter_resource.get("period", {})
                            start_date_time = period.get("start")
                            end_date_time = period.get("end")

                            # Extract location
                            locations = encounter_resource.get("location", [])
                            location_id = None
                            location_display = None
                            if locations:
                                first_location = locations[0]
                                location_ref = first_location.get("location", {})
                                if isinstance(location_ref, dict) and location_ref.get(
                                    "reference"
                                ):
                                    location_ref_str = location_ref.get("reference", "")
                                    location_id = (
                                        location_ref_str.split("/")[-1]
                                        if "/" in location_ref_str
                                        else location_ref_str
                                    )
                                    location_display = location_ref.get("display")

                            # Extract participant (patient, practitioner, etc.)
                            participants = encounter_resource.get("participant", [])
                            for participant in participants:
                                actor_ref = participant.get("individual", {})
                                if isinstance(actor_ref, dict) and actor_ref.get(
                                    "reference"
                                ):
                                    ref_str = actor_ref.get("reference", "")
                                    ref_type = (
                                        ref_str.split("/")[0] if "/" in ref_str else ""
                                    )
                                    # Patient reference is already extracted from request
                                    # Practitioner reference could be used for Author if needed

                            # Build Header.Document.Visit
                            self.destination_response["Header"]["Document"]["Visit"] = {
                                "VisitNumber": enc_id,
                                "Status": enc_status,
                                "Type": service_type or {},
                                "StartDateTime": start_date_time,
                                "EndDateTime": end_date_time,
                                "Encounter": {
                                    "ID": enc_id,
                                    "Status": enc_status,
                                },
                            }

                            # Build Header.Patient
                            if patient_id:
                                self.destination_response["Header"]["Patient"][
                                    "Identifiers"
                                ].append(
                                    {
                                        "ID": patient_id,
                                        "IDType": "EHRID",
                                    }
                                )

                            # Add location to Organization
                            if location_id:
                                self.destination_response["Header"]["Patient"][
                                    "Organization"
                                ]["Identifiers"].append(
                                    {
                                        "ID": location_id,
                                        "IDType": "DepartmentID",
                                    }
                                )
                else:
                    # Non-Bundle response or error
                    if (
                        isinstance(encounter_response, dict)
                        and "error" in encounter_response
                    ):
                        self.destination_response.update(encounter_response)
                    self.destination_response.update({"statuscode": status_code})
            else:
                # Error response
                self.destination_response.update(encounter_response)
                self.destination_response.update({"statuscode": status_code})

            return self.destination_response
        except Exception as e:
            self.destination_response.update({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return self.destination_response
