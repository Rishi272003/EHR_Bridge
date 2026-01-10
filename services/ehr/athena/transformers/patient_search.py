from datetime import datetime
from services.ehr.athena.categories.Patient import Patient
from services.ehr.athena.categories.Chart import Chart
from services.patientQ_response import patient_query


class PatientSearchTransformer:
    def __init__(self, connection_obj,source_data,connection_data):
        self.connection_obj = connection_obj
        self.source_data = source_data
        self.connection_data = connection_data
        self.destination_response = {"potentialmatches":[]}

    def transform(self):
        patient = Patient(self.connection_obj)
        patient.authenticate()
        if self.source_data.get("ehr_id"):
            patient_list = [
                int(pid)
                for pid in self.source_data.get("ehr_id").split(",")
                if pid.isnumeric()
            ]
            if len(patient_list) > 0:
                for single_patient in patient_list:
                    patientid = single_patient
                    (
                        demographics_responses,
                        status_code,
                    ) = patient.get_patient_by_id(
                        patientid
                    )
                    if status_code == 200:
                        for patients in demographics_responses:
                            patient_status = (
                                patients.get("status").lower()
                                if patients.get("status")
                                else None
                            )
                            DOB = None
                            if patients.get("dob"):
                                date_obj = datetime.strptime(
                                    patients.get("dob"), "%m/%d/%Y"
                                )
                                DOB = date_obj.strftime("%Y-%m-%d")
                            self.destination_response["potentialmatches"].append(
                                {
                                    "id": patientid,
                                    "firstname": patients.get("firstname"),
                                    "lastname": patients.get("lastname"),
                                    "middlename": patients.get("middlename"),
                                    "dateofbirth": DOB,
                                    "sex": (
                                        "Male"
                                        if patients.get("sex") == "M"
                                        else "Female"
                                        if patients.get("sex") == "F"
                                        else None
                                    ),
                                    "mrn": patients.get("id"),
                                    "ssn": patients.get("ssn"),
                                    "status": True
                                    if patient_status == "active"
                                    else False,
                                    "emailaddress": patients.get("email"),
                                }
                            )
        else:
            if self.source_data.get("fname") and self.source_data.get("lname"):
                searchterm = self.source_data.get("fname") + " " + self.source_data.get("lname")
            elif self.source_data.get("fname"):
                searchterm = self.source_data.get("fname")
            elif self.source_data.get("lname"):
                searchterm = self.source_data.get("lname")
            else:
                searchterm = ""
            patient_response, status_code = patient.get_patient_by_name(
            searchterm=searchterm
            )
            print("patient_response till here>>>",patient_response)
            print("status_code till here>>>",status_code)
            print("type of patient_response till here>>>",type(patient_response))
            if status_code == 200:
                for patients in patient_response.get("patients"):
                    if patients.get("dob"):
                        date_obj = datetime.strptime(patients.get("dob"), "%m/%d/%Y")
                        DOB = date_obj.strftime("%Y-%m-%d")
                    self.destination_response["potentialmatches"].append(
                        {
                            "id": patients.get("patientid"),
                            "firstname": patients.get("firstname"),
                            "lastname": patients.get("lastname"),
                            "middlename": patients.get("middlename"),
                            "dateofbirth": DOB,
                            "sex": (
                                "Male"
                                if patients.get("sex") == "M"
                                else "Female"
                                if patients.get("sex") == "F"
                                else None
                            ),
                            "mrn": patients.get("id"),
                            "ssn": patients.get("ssn"),
                            "emailaddress": patients.get("email"),
                        }
                    )
            else:
                del self.destination_response["potentialmatches"]
                self.destination_response.update(
                    {"errormessage": patient_response, "statuscode": status_code}
                )
        print("destination_response till here>>>",type(self.destination_response))
        return self.destination_response
