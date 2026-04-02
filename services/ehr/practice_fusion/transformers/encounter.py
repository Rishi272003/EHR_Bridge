from services.ehr.transformer import Transformer
from services.ehr.practice_fusion.categories.Chart import Chart
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

            # Extract visit query parameters\
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
                    patient_id=None, visit_number=visit_number
                )
            elif start_date and end_date and patient_id:
                encounter_response, status_code = chart.get_patient_encounter(
                    patient_id=patient_id, start_date=start_date, end_date=end_date
                )
            elif patient_id:
                encounter_response, status_code = chart.get_patient_encounter(
                    patient_id=patient_id
                )
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
                        # Process encounters - if visit_number provided, find specific one, otherwise process all
                        encounters_to_process = []

                        if visit_number:
                            # Find the specific encounter by ID
                            for entry_item in entries:
                                resource = entry_item.get("resource", {})
                                if (
                                    resource.get("resourceType") == "Encounter"
                                    and resource.get("id") == visit_number
                                ):
                                    encounters_to_process.append(resource)
                                    break
                        else:
                            # Process all encounters
                            for entry_item in entries:
                                resource = entry_item.get("resource", {})
                                if resource.get("resourceType") == "Encounter":
                                    encounters_to_process.append(resource)

                        # Process each encounter
                        visits = []
                        for encounter_resource in encounters_to_process:
                            # Extract encounter ID
                            enc_id = encounter_resource.get("id", "")

                            # Extract status
                            enc_status = encounter_resource.get("status", "")

                            # Extract type (service type) - prefer type over class
                            enc_types = encounter_resource.get("type", [])
                            service_type = {}
                            if enc_types:
                                first_type = enc_types[0]
                                type_codings = first_type.get("coding", [])
                                if type_codings:
                                    first_coding = type_codings[0]
                                    service_type = {
                                        "Code": first_coding.get("code"),
                                        "Name": first_coding.get("display") or first_type.get("text"),
                                        "CodeSystem": first_coding.get("system"),
                                    }
                                elif first_type.get("text"):
                                    # Fallback to text if no coding
                                    service_type = {
                                        "Code": None,
                                        "Name": first_type.get("text"),
                                        "CodeSystem": None,
                                    }

                            # Extract period (start/end dates)
                            period = encounter_resource.get("period", {})
                            start_date_time = period.get("start") if period else None
                            end_date_time = period.get("end") if period else None

                            # Extract location - handle both regular references and contained resources
                            locations = encounter_resource.get("location", [])
                            location_id = None
                            location_display = None
                            if locations:
                                first_location = locations[0]
                                location_ref = first_location.get("location", {})
                                if isinstance(location_ref, dict):
                                    location_ref_str = location_ref.get("reference", "")
                                    if location_ref_str:
                                        # Handle contained resources (starts with #)
                                        if location_ref_str.startswith("#"):
                                            # Look for contained resource
                                            contained = encounter_resource.get("contained", [])
                                            contained_id = location_ref_str[1:]  # Remove #
                                            for contained_resource in contained:
                                                if (
                                                    contained_resource.get("resourceType") == "Location"
                                                    and contained_resource.get("id") == contained_id
                                                ):
                                                    # Extract identifier from contained Location
                                                    identifiers = contained_resource.get("identifier", [])
                                                    if identifiers:
                                                        location_id = identifiers[0].get("value")
                                                    break
                                        else:
                                            # Regular reference
                                            location_id = (
                                                location_ref_str.split("/")[-1]
                                                if "/" in location_ref_str
                                                else location_ref_str
                                            )
                                        location_display = location_ref.get("display")

                            # Extract patient ID from subject reference (for consistency)
                            subject = encounter_resource.get("subject", {})
                            encounter_patient_id = None
                            if isinstance(subject, dict) and subject.get("reference"):
                                subject_ref = subject.get("reference", "")
                                if "Patient/" in subject_ref:
                                    encounter_patient_id = subject_ref.split("Patient/")[-1]
                                elif "/" in subject_ref:
                                    encounter_patient_id = subject_ref.split("/")[-1]

                            # Use patient_id from request, fallback to encounter subject
                            final_patient_id = patient_id or encounter_patient_id

                            # Extract service provider (organization)
                            service_provider = encounter_resource.get("serviceProvider", {})
                            organization_id = None
                            if isinstance(service_provider, dict) and service_provider.get("reference"):
                                org_ref = service_provider.get("reference", "")
                                if "Organization/" in org_ref:
                                    organization_id = org_ref.split("Organization/")[-1]
                                elif "/" in org_ref:
                                    organization_id = org_ref.split("/")[-1]

                            # Build visit object for this encounter
                            visit_obj = {
                                "VisitNumber": enc_id,
                                "Status": enc_status,
                                "Type": service_type if service_type else {},
                                "StartDateTime": start_date_time,
                                "EndDateTime": end_date_time,
                                "Encounter": {
                                    "ID": enc_id,
                                    "Status": enc_status,
                                },
                            }
                            visits.append(visit_obj)

                        # Set visits in response - single object if one visit, array if multiple
                        if len(visits) == 1:
                            self.destination_response["Header"]["Document"]["Visit"] = visits[0]
                        elif len(visits) > 1:
                            self.destination_response["Header"]["Document"]["Visit"] = visits
                        else:
                            self.destination_response["Header"]["Document"]["Visit"] = {}

                        # Build Header.Patient (only once, using first encounter's patient or request patient)
                        if patient_id:
                            # Check if already added
                            existing_ids = [id_obj.get("ID") for id_obj in self.destination_response["Header"]["Patient"]["Identifiers"]]
                            if patient_id not in existing_ids:
                                self.destination_response["Header"]["Patient"][
                                    "Identifiers"
                                ].append(
                                    {
                                        "ID": patient_id,
                                        "IDType": "EHRID",
                                    }
                                )
                        elif encounters_to_process:
                            # Extract patient ID from first encounter
                            first_encounter = encounters_to_process[0]
                            subject = first_encounter.get("subject", {})
                            if isinstance(subject, dict) and subject.get("reference"):
                                subject_ref = subject.get("reference", "")
                                if "Patient/" in subject_ref:
                                    encounter_patient_id = subject_ref.split("Patient/")[-1]
                                elif "/" in subject_ref:
                                    encounter_patient_id = subject_ref.split("/")[-1]
                                else:
                                    encounter_patient_id = subject_ref

                                if encounter_patient_id:
                                    existing_ids = [id_obj.get("ID") for id_obj in self.destination_response["Header"]["Patient"]["Identifiers"]]
                                    if encounter_patient_id not in existing_ids:
                                        self.destination_response["Header"]["Patient"][
                                            "Identifiers"
                                        ].append(
                                            {
                                                "ID": encounter_patient_id,
                                                "IDType": "EHRID",
                                            }
                                        )

                        # Collect all unique organization and location IDs from all encounters
                        organization_ids = set()
                        location_ids = set()

                        for encounter_resource in encounters_to_process:
                            # Extract service provider (organization)
                            service_provider = encounter_resource.get("serviceProvider", {})
                            if isinstance(service_provider, dict) and service_provider.get("reference"):
                                org_ref = service_provider.get("reference", "")
                                if "Organization/" in org_ref:
                                    org_id = org_ref.split("Organization/")[-1]
                                elif "/" in org_ref:
                                    org_id = org_ref.split("/")[-1]
                                else:
                                    org_id = org_ref
                                if org_id:
                                    organization_ids.add(org_id)

                            # Extract location
                            locations = encounter_resource.get("location", [])
                            if locations:
                                first_location = locations[0]
                                location_ref = first_location.get("location", {})
                                if isinstance(location_ref, dict):
                                    location_ref_str = location_ref.get("reference", "")
                                    if location_ref_str:
                                        if location_ref_str.startswith("#"):
                                            # Contained resource
                                            contained = encounter_resource.get("contained", [])
                                            contained_id = location_ref_str[1:]
                                            for contained_resource in contained:
                                                if (
                                                    contained_resource.get("resourceType") == "Location"
                                                    and contained_resource.get("id") == contained_id
                                                ):
                                                    identifiers = contained_resource.get("identifier", [])
                                                    if identifiers:
                                                        location_ids.add(identifiers[0].get("value"))
                                                    break
                                        else:
                                            # Regular reference
                                            loc_id = (
                                                location_ref_str.split("/")[-1]
                                                if "/" in location_ref_str
                                                else location_ref_str
                                            )
                                            if loc_id:
                                                location_ids.add(loc_id)

                        # Add all unique organization IDs
                        existing_org_ids = [id_obj.get("ID") for id_obj in self.destination_response["Header"]["Patient"]["Organization"]["Identifiers"]]
                        for org_id in organization_ids:
                            if org_id not in existing_org_ids:
                                self.destination_response["Header"]["Patient"][
                                    "Organization"
                                ]["Identifiers"].append(
                                    {
                                        "ID": org_id,
                                        "IDType": "OrganizationID",
                                    }
                                )

                        # Add all unique location IDs
                        existing_all_ids = [id_obj.get("ID") for id_obj in self.destination_response["Header"]["Patient"]["Organization"]["Identifiers"]]
                        for loc_id in location_ids:
                            if loc_id not in existing_all_ids:
                                self.destination_response["Header"]["Patient"][
                                    "Organization"
                                ]["Identifiers"].append(
                                    {
                                        "ID": loc_id,
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
            self.destination_response.update({"Error": str(e)})
            self.destination_response.update({"statuscode": status.HTTP_400_BAD_REQUEST})
            return self.destination_response
