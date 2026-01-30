import logging

from services.ehr.transformer import Transformer
from services.ehr.practice_fusion.categories.Patient import Patient

logger = logging.getLogger(__name__)


class QueryTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.connection_obj = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "PatientSearch",
                "EventType": "Query",
                "Source": {"ID": str(self.connection_obj.uuid), "Name": "connectionid"},
                "Raw": [],
            },
            "Patients": [],
        }

    def transform(self):
        """
        Transform patient search request and fetch data from Practice Fusion.
        """
        try:
            patient = Patient(self.connection_obj)
            patient.authenticate()

            # Extract search parameters from source_json
            patient_data = self.source_json.get("Patient", {})
            demographics = patient_data.get("Demographics", {})

            # Build search parameters
            search_params = {}
            if demographics.get("FirstName") or demographics.get("LastName"):
                name_parts = []
                if demographics.get("FirstName"):
                    name_parts.append(demographics.get("FirstName"))
                if demographics.get("LastName"):
                    name_parts.append(demographics.get("LastName"))
                if name_parts:
                    search_params["name"] = " ".join(name_parts)

            if demographics.get("DOB"):
                search_params["birthdate"] = demographics.get("DOB")

            # Make API call
            patient_response, status_code = patient.search_patients(**search_params)

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(patient_response)

            if status_code == 200:
                # TODO: Transform FHIR Patient resources to unified format
                # Handle FHIR Bundle response
                if patient_response.get("resourceType") == "Bundle":
                    entries = patient_response.get("entry", [])
                    for entry_item in entries:
                        patient_resource = entry_item.get("resource", {})
                        if (
                            patient_resource
                            and patient_resource.get("resourceType") == "Patient"
                        ):
                            # TODO: Transform patient resource to unified format
                            pass
                # Handle single Patient resource
                elif patient_response.get("resourceType") == "Patient":
                    # TODO: Transform patient resource to unified format
                    pass

            else:
                self.destination_response["detail"] = "Failed to fetch patient data"
                self.destination_response["statuscode"] = status_code
                self.destination_response["error"] = patient_response

            return self.destination_response

        except Exception as e:
            logger.exception("QueryTransformer failed")
            self.destination_response["detail"] = f"Error processing patient search: {str(e)}"
            self.destination_response["statuscode"] = 500
            return self.destination_response
