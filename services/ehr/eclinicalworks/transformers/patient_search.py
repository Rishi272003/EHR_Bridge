from rest_framework import status
from rest_framework.response import Response

from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Patient import Patient

class QueryTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        self.connection_obj = connection_obj
        self.source_data = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "PatientSearch",
                "EventType": "Response",
                "Source": {"ID": self.connection_obj.uuid, "Name": "connectionid"},
                "Raw": [],
            },
            "PotentialMatches": [],
        }
        self.destination_json = {}

    def transform(self):
        try:
            patient = Patient(self.connection_obj)
            patient.authenticate()
            print("source_data",self.source_data)
            demographics  = self.source_data.get("Patient",{}).get("Demographics",{})
            print("demographics",demographics)
            if demographics.get("FirstName") and demographics.get("LastName"):
                self.destination_json["name"] = (
                    f"{demographics.get('LastName')} {demographics.get('FirstName')}"
                )

            elif demographics.get("FirstName"):
                self.destination_json["name"] = f"{demographics.get('FirstName')}"

            elif demographics.get("LastName"):
                self.destination_json["name"] = f"{demographics.get('LastName')}"

            patient_response, status_code = patient.get_search_criteria(**self.destination_json)

            if self.source_data["Meta"].get("Test"):
                self.destination_response["Meta"]["Raw"].append(patient_response)

            print(f"Patient response status: {status_code}")
            print(f"Patient response type: {type(patient_response)}")
            print(f"Patient response keys: {patient_response.keys() if isinstance(patient_response, dict) else 'Not a dict'}")

            if status_code == 200:
                # Handle FHIR Bundle response
                entries = patient_response.get("entry", [])
                print(f"Number of entries found: {len(entries)}")

                if entries:
                    for entry_item in entries:
                        # Extract Patient resource from FHIR Bundle entry
                        patient_resource = entry_item.get("resource", {})
                        print(f"Patient resource type: {patient_resource.get('resourceType')}")

                        if (
                            not patient_resource
                            or patient_resource.get("resourceType") != "Patient"
                        ):
                            continue

                        # Extract patient data from FHIR Patient resource
                        patient_id = patient_resource.get("id", "")

                        # Extract name
                        names = patient_resource.get("name", [])
                        first_name = None
                        middle_name = None
                        last_name = None
                        if names:
                            name = names[0]  # Use first name entry
                            given = name.get("given", [])
                            if given:
                                first_name = given[0]
                                if len(given) > 1:
                                    middle_name = " ".join(given[1:])  # Join all middle names
                            last_name = name.get("family")

                        # Extract DOB
                        dob = patient_resource.get("birthDate")

                        # Extract gender (convert to M/F)
                        gender = patient_resource.get("gender", "").lower()
                        sex = (
                            "M" if gender == "male" else "F" if gender == "female" else None
                        )

                        # Extract phone numbers from telecom
                        home_phone = None
                        mobile_phone = None
                        work_phone = None
                        email = None
                        telecom = patient_resource.get("telecom", [])
                        for contact in telecom:
                            system = contact.get("system", "")
                            value = contact.get("value", "")
                            if system == "phone":
                                use = contact.get("use", "")
                                if use == "home":
                                    home_phone = value
                                elif use == "mobile":
                                    mobile_phone = value
                                elif use == "work":
                                    work_phone = value
                                elif not home_phone:  # Default to home if no use specified
                                    home_phone = value
                            elif system == "email":
                                email = value

                        # Extract address
                        addresses = patient_resource.get("address", [])
                        street_address = None
                        city = None
                        state = None
                        zip_code = None
                        country = None
                        if addresses:
                            # Prefer home address, otherwise use first address
                            address = None
                            for addr in addresses:
                                if addr.get("use") == "home":
                                    address = addr
                                    break
                            if not address:
                                address = addresses[0]

                            line = address.get("line", [])
                            if line:
                                street_address = " ".join(line) if isinstance(line, list) else line
                            city = address.get("city")
                            state = address.get("state")
                            zip_code = address.get("postalCode")
                            country = address.get("country")

                        # Extract identifiers - prefer usual, then secondary, then any
                        identifiers = patient_resource.get("identifier", [])
                        patient_identifier = patient_id  # Default to resource id
                        identifier_type = "EHRID"

                        for identifier in identifiers:
                            use = identifier.get("use", "")
                            if use == "usual":
                                patient_identifier = identifier.get("value", patient_id)
                                # Try to determine ID type from system
                                system = identifier.get("system", "")
                                if "ssn" in system.lower() or identifier.get("type", {}).get("coding", [{}])[0].get("code") == "SS":
                                    identifier_type = "SSN"
                                else:
                                    identifier_type = "EHRID"
                                break

                        # If no usual identifier, try secondary
                        if patient_identifier == patient_id:
                            for identifier in identifiers:
                                if identifier.get("use") == "secondary":
                                    patient_identifier = identifier.get("value", patient_id)
                                    identifier_type = "MRN"  # Secondary is often MRN
                                    break

                        # Extract SSN from identifiers
                        ssn = None
                        for identifier in identifiers:
                            system = identifier.get("system", "")
                            if "ssn" in system.lower() or (identifier.get("type", {}) and identifier.get("type", {}).get("coding", [{}])[0].get("code") == "SS"):
                                ssn = identifier.get("value")
                                break

                        # Extract race and ethnicity from extensions
                        race = None
                        ethnicity = None
                        extensions = patient_resource.get("extension", [])
                        for ext in extensions:
                            url = ext.get("url", "")
                            if "race" in url.lower():
                                # Extract race from extension
                                race_extensions = ext.get("extension", [])
                                for race_ext in race_extensions:
                                    if race_ext.get("url") == "text":
                                        race = race_ext.get("valueString")
                                        break
                                    elif race_ext.get("url") == "ombCategory":
                                        value_coding = race_ext.get("valueCoding", {})
                                        if value_coding:
                                            race = value_coding.get("display")
                                            break
                            elif "ethnicity" in url.lower():
                                # Extract ethnicity from extension
                                ethnicity_extensions = ext.get("extension", [])
                                for eth_ext in ethnicity_extensions:
                                    if eth_ext.get("url") == "text":
                                        ethnicity = eth_ext.get("valueString")
                                        break
                                    elif eth_ext.get("url") == "ombCategory":
                                        value_coding = eth_ext.get("valueCoding", {})
                                        if value_coding:
                                            ethnicity = value_coding.get("display")
                                            break

                        # Extract language
                        language = None
                        communication = patient_resource.get("communication", [])
                        if communication and len(communication) > 0:
                            lang_coding = communication[0].get("language", {})
                            if lang_coding:
                                language = lang_coding.get("text") or (lang_coding.get("coding", [{}])[0].get("display") if lang_coding.get("coding") else None)

                        self.destination_response["PotentialMatches"].append(
                            {
                                "Patient": {
                                    "Identifiers": [
                                        {
                                            "ID": patient_identifier,
                                            "IDType": identifier_type
                                        }
                                    ],
                                    "Demographics": {
                                        "FirstName": first_name,
                                        "MiddleName": middle_name,
                                        "LastName": last_name,
                                        "DOB": dob,
                                        "SSN": ssn,
                                        "Sex": (
                                            "Male"
                                            if sex == "M"
                                            else "Female" if sex == "F" else None
                                        ),
                                        "PhoneNumber": {
                                            "Home": home_phone,
                                            "Mobile": mobile_phone,
                                            "Office": work_phone,
                                        },
                                        "EmailAddresses": [{"Address": email}] if email else [],
                                        "Address": {
                                            "StreetAddress": street_address,
                                            "City": city,
                                            "State": state,
                                            "ZIP": zip_code,
                                            "Country": country,
                                        },
                                        "Race": race,
                                        "Ethnicity": ethnicity,
                                        "Language": language,
                                    },
                                    "Guarantor": {
                                        "FirstName": None,
                                        "MiddleName": None,
                                        "LastName": None,
                                        "SSN": None,
                                        "DOB": None,
                                        "Sex": None,
                                        "Address": {
                                            "StreetAddress": None,
                                            "City": None,
                                            "State": None,
                                            "ZIP": None,
                                            "Country": None,
                                        },
                                        "PhoneNumber": {
                                            "Home": None,
                                            "Mobile": None,
                                        },
                                        "EmailAddresses": [],
                                    },
                                }
                            }
                        )
                else:
                    # No entries found
                    print("No entries in response")
                    self.destination_response["PotentialMatches"] = []
            else:
                self.destination_response.update(patient_response)
                self.destination_response.update({"statuscode": status_code})



        except Exception as e:
            self.destination_response.update({"Error": str(e)})
            self.destination_response.update({"statuscode": status.HTTP_400_BAD_REQUEST})
        print("destination_response",self.destination_response)
        return self.destination_response
