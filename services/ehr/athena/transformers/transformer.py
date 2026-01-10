from services.ehr.athena.categories.Providers import Providers

patient_transformer = {
    "patientid": "ID",
    "patienttypeid": "IDType",
    "departmentid": "Department",
    "firstname": "FirstName",
    "lastname": "LastName",
    "middlename": "MiddleName",
    "sex": "Sex",
    "race": "Race",
    "dob": "DOB",
    "ssn": "SSN",
    "maritalstatus": "MaritalStatus",
    "homenumber": "Home",
    "phonenumber": "Mobile",
    "worknumber": "Office",
    "address": "StreetAddress",
    "city": "City",
    "state": "State",
    "country": "Country",
    "zip": "ZIP",
    "providerid": "ID",
    "providertypeid": "IDType",
    "language": "Language",
    "startdate": "StartDateTime",
    "enddate": "EndDateTime",
    "duration": "Duration",
    "description": "Description",
    "appointmenttype": "Reasons",
    "name": "Name",
    "providertype": "Type",
}


athena_json = {}


def source_data_to_athena(source_json):
    global athena_json

    if isinstance(source_json, dict):
        for key, value in source_json.items():
            if key == "Meta":
                continue
            for pt_key, pt_value in patient_transformer.items():
                if pt_key not in athena_json:
                    if key == pt_value:
                        athena_json[pt_key] = value
            source_data_to_athena(value)

    elif isinstance(source_json, list):
        for element in source_json:
            for pt_key, pt_value in patient_transformer.items():
                if pt_value in element:
                    if pt_key == "patienttypeid" or pt_key == "providertypeid":
                        if element.get("IDType") == "EHRID":
                            athena_json[pt_key] = element.get("IDType")
                    elif element.get("IDType") == "EHRID":
                        athena_json[pt_key] = element.get("ID")
            source_data_to_athena(element)

    return athena_json


class ProvidersTransformer:
    def __init__(self, connection_obj, connection_data,source_data):
        self.connection_obj = connection_obj
        self.connection_data = connection_data
        self.destination_response = {}
        self.source_data = source_data

    def transform(self):
        provider_obj = Providers(self.connection_obj)
        provider_obj.authenticate()
        if self.source_data.get("type") == "all":
            response = provider_obj.get_all_providers()
        elif self.source_data.get("type") == "single":
            response = provider_obj.get_provider_by_id(self.source_data.get("provider_id"))
        elif self.source_data.get("type") == "create":
            response = provider_obj.create_provider(self.source_data.get("provider_data"))
        else:
            raise ValueError(f"Invalid type: {self.source_data.get('type')}")
        return response
