from datetime import datetime
from rest_framework import status
from rest_framework.response import Response

from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Patient import Patient


class NewPatientTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.source_json = source_data
        self.connection = connection_obj
        self.destination_response = {
            "Meta": {
                "DataModel": "PatientAdmin",
                "EventType": "NewPatient",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            }
        }
        self.destination_json = {}

    def transform(self):
        try:
            # Extract Patient resource from FHIR Bundle or source data
            patient_resource = None

            # Handle different input formats
            # Format 1: Direct FHIR Bundle or Patient resource
            if isinstance(self.source_json, dict):
                if self.source_json.get("resourceType") == "Bundle":
                    entries = self.source_json.get("entry", [])
                    if entries:
                        # Find Patient resource in the bundle
                        for entry in entries:
                            resource = entry.get("resource", {})
                            if resource.get("resourceType") == "Patient":
                                patient_resource = resource
                                break
                elif self.source_json.get("resourceType") == "Patient":
                    # Direct Patient resource
                    patient_resource = self.source_json
                # Format 2: Nested in patient_data (from API view)
                elif self.source_json.get("patient_data"):
                    patient_data = self.source_json.get("patient_data")
                    if isinstance(patient_data, dict):
                        if patient_data.get("resourceType") == "Bundle":
                            entries = patient_data.get("entry", [])
                            if entries:
                                for entry in entries:
                                    resource = entry.get("resource", {})
                                    if resource.get("resourceType") == "Patient":
                                        patient_resource = resource
                                        break
                        elif patient_data.get("resourceType") == "Patient":
                            patient_resource = patient_data
                # Format 3: Legacy format (old structure)
                elif self.source_json.get("Patient"):
                    # Legacy format - convert to FHIR if needed
                    # For now, we'll skip this and require FHIR format
                    pass

            if not patient_resource:
                return Response(
                    {"Error": "Patient resource not found in request"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Initialize Patient client
            new_patient = Patient(self.connection)
            new_patient.authenticate()

            # Build FHIR Patient resource for eClinicalWorks
            self.destination_json = {}

            # Required: active (boolean)
            self.destination_json["active"] = patient_resource.get("active", True)

            # Required: name (HumanName) - 1..*
            names = patient_resource.get("name", [])
            if not names:
                return Response(
                    {"Error": "Patient name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use first name entry
            name = names[0]
            name_obj = {
                "use": name.get("use", "usual"),
            }

            if name.get("family"):
                name_obj["family"] = name.get("family")

            if name.get("given"):
                name_obj["given"] = name.get("given") if isinstance(name.get("given"), list) else [name.get("given")]

            if name.get("prefix"):
                name_obj["prefix"] = name.get("prefix") if isinstance(name.get("prefix"), list) else [name.get("prefix")]

            if name.get("suffix"):
                name_obj["suffix"] = name.get("suffix") if isinstance(name.get("suffix"), list) else [name.get("suffix")]

            if name.get("text"):
                name_obj["text"] = name.get("text")

            self.destination_json["name"] = [name_obj]

            # Required: identifier (Identifier) - 1..*
            identifiers = patient_resource.get("identifier", [])
            if identifiers:
                self.destination_json["identifier"] = []
                for identifier in identifiers:
                    identifier_obj = {
                        "use": identifier.get("use", "usual"),
                    }
                    if identifier.get("system"):
                        identifier_obj["system"] = identifier.get("system")
                    if identifier.get("value"):
                        identifier_obj["value"] = identifier.get("value")
                    if identifier.get("type"):
                        identifier_obj["type"] = identifier.get("type")
                    self.destination_json["identifier"].append(identifier_obj)

            # Required: gender (code) - 1..1
            gender = patient_resource.get("gender", "").lower()
            if not gender:
                return Response(
                    {"Error": "Patient gender is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.destination_json["gender"] = gender

            # Optional: birthDate (date) - 0..1
            if patient_resource.get("birthDate"):
                self.destination_json["birthDate"] = patient_resource.get("birthDate")

            # Optional: telecom (ContactPoint) - 0..*
            telecom = patient_resource.get("telecom", [])
            if telecom:
                self.destination_json["telecom"] = []
                for contact in telecom:
                    telecom_obj = {
                        "system": contact.get("system"),  # phone, email, etc.
                    }
                    if contact.get("value"):
                        telecom_obj["value"] = contact.get("value")
                    if contact.get("use"):
                        telecom_obj["use"] = contact.get("use")
                    if contact.get("rank"):
                        telecom_obj["rank"] = contact.get("rank")
                    self.destination_json["telecom"].append(telecom_obj)

            # Optional: address (Address) - 0..*
            addresses = patient_resource.get("address", [])
            if addresses:
                self.destination_json["address"] = []
                for address in addresses:
                    address_obj = {
                        "use": address.get("use", "home"),
                    }
                    if address.get("type"):
                        address_obj["type"] = address.get("type")
                    if address.get("text"):
                        address_obj["text"] = address.get("text")
                    if address.get("line"):
                        address_obj["line"] = address.get("line") if isinstance(address.get("line"), list) else [address.get("line")]
                    if address.get("city"):
                        address_obj["city"] = address.get("city")
                    if address.get("state"):
                        address_obj["state"] = address.get("state")
                    if address.get("postalCode"):
                        address_obj["postalCode"] = address.get("postalCode")
                    if address.get("country"):
                        address_obj["country"] = address.get("country")
                    self.destination_json["address"].append(address_obj)

            # Optional: maritalStatus (CodeableConcept) - 0..1
            if patient_resource.get("maritalStatus"):
                marital_status = patient_resource.get("maritalStatus")
                marital_obj = {}
                if marital_status.get("coding"):
                    marital_obj["coding"] = marital_status.get("coding")
                if marital_status.get("text"):
                    marital_obj["text"] = marital_status.get("text")
                self.destination_json["maritalStatus"] = marital_obj

            # Optional: communication (BackboneElement) - 0..*
            communication = patient_resource.get("communication", [])
            if communication:
                self.destination_json["communication"] = []
                for comm in communication:
                    comm_obj = {}
                    if comm.get("language"):
                        comm_obj["language"] = comm.get("language")
                    if comm.get("preferred"):
                        comm_obj["preferred"] = comm.get("preferred")
                    self.destination_json["communication"].append(comm_obj)

            # Optional: deceased[x] - 0..1
            if patient_resource.get("deceasedBoolean") is not None:
                self.destination_json["deceasedBoolean"] = patient_resource.get("deceasedBoolean")
            elif patient_resource.get("deceasedDateTime"):
                self.destination_json["deceasedDateTime"] = patient_resource.get("deceasedDateTime")

            # US Core Extensions
            extensions = patient_resource.get("extension", [])
            if extensions:
                self.destination_json["extension"] = []
                for ext in extensions:
                    ext_obj = {
                        "url": ext.get("url"),
                    }

                    # Handle us-core-race
                    if "us-core-race" in ext.get("url", ""):
                        if ext.get("extension"):
                            ext_obj["extension"] = ext.get("extension")

                    # Handle us-core-ethnicity
                    elif "us-core-ethnicity" in ext.get("url", ""):
                        if ext.get("extension"):
                            ext_obj["extension"] = ext.get("extension")

                    # Handle us-core-birthsex
                    elif "us-core-birthsex" in ext.get("url", ""):
                        if ext.get("valueCode"):
                            ext_obj["valueCode"] = ext.get("valueCode")

                    # Handle other extensions (e.g., defaultFacility)
                    elif ext.get("valueReference"):
                        ext_obj["valueReference"] = ext.get("valueReference")
                    elif ext.get("valueCode"):
                        ext_obj["valueCode"] = ext.get("valueCode")
                    elif ext.get("valueString"):
                        ext_obj["valueString"] = ext.get("valueString")

                    self.destination_json["extension"].append(ext_obj)

            # Optional: contact (BackboneElement) - 0..*
            contact = patient_resource.get("contact", [])
            if contact:
                self.destination_json["contact"] = []
                for cont in contact:
                    contact_obj = {}
                    if cont.get("relationship"):
                        contact_obj["relationship"] = cont.get("relationship")
                    if cont.get("name"):
                        contact_obj["name"] = cont.get("name")
                    if cont.get("telecom"):
                        contact_obj["telecom"] = cont.get("telecom")
                    if cont.get("address"):
                        contact_obj["address"] = cont.get("address")
                    if cont.get("gender"):
                        contact_obj["gender"] = cont.get("gender")
                    if cont.get("organization"):
                        contact_obj["organization"] = cont.get("organization")
                    if cont.get("period"):
                        contact_obj["period"] = cont.get("period")
                    self.destination_json["contact"].append(contact_obj)

            # Optional: generalPractitioner (Reference) - 0..*
            general_practitioner = patient_resource.get("generalPractitioner", [])
            if general_practitioner:
                self.destination_json["generalPractitioner"] = general_practitioner

            # Add resourceType and meta if present
            if patient_resource.get("resourceType"):
                self.destination_json["resourceType"] = patient_resource.get("resourceType")

            if patient_resource.get("meta"):
                self.destination_json["meta"] = patient_resource.get("meta")

            # Add id if present (for updates, not creates)
            if patient_resource.get("id"):
                self.destination_json["id"] = patient_resource.get("id")

            print("FHIR Patient payload for eClinicalWorks:", self.destination_json)

            # Create patient via eClinicalWorks API
            # Pass the entire FHIR Patient resource as a single resource
            # The create_new_patient method will handle the payload formatting
            patient_created, status_code = new_patient.create_new_patient(**self.destination_json)

            # Add raw response if Test mode is enabled
            if self.source_json.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(patient_created)

            # Add response to destination
            if status_code == 200 or status_code == 201:
                self.destination_response.update(patient_created)
            else:
                self.destination_response.update(patient_created)
                self.destination_response["statuscode"] = status_code

            return self.destination_response

        except Exception as e:
            self.destination_response.update({"detail": str(e)})
            return self.destination_response
