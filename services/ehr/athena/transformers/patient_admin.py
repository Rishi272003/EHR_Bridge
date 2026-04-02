from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from services.ehr.transformer import Transformer
from services.ehr.athena.categories.Patient import Patient

class NewPatientTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.source_json = source_data
        self.connection = connection_obj
        self.destination_json = {}
        self.destination_response = {
            "Meta": {
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            }
        }

    def transform(self):
        try:
            patient = Patient(self.connection)
            patient.authenticate()

            self.destination_json["address1"] = self.source_json["Patient"][
                "Demographics"
            ]["Address"].get("StreetAddress")
            self.destination_json["address2"] = None
            self.destination_json["agriculturalworker"] = None
            self.destination_json["agriculturalworkertype"] = None
            self.destination_json["altfirstname"] = None
            self.destination_json["assignedsexatbirth"] = None
            self.destination_json["caresummarydeliverypreference"] = None
            self.destination_json["city"] = self.source_json["Patient"]["Demographics"][
                "Address"
            ].get("City")
            self.destination_json["clinicalordertypegroupid"] = None
            self.destination_json["consenttocall"] = None
            self.destination_json["consenttotext"] = None
            # Handle Contacts - check if exists and has elements
            contacts = self.source_json["Patient"].get("Contacts", [])
            if contacts and len(contacts) > 0:
                contact = contacts[0]
                contact_phone = contact.get("PhoneNumber", {})
                self.destination_json["contacthomephone"] = contact_phone.get("Home")
                self.destination_json["contactmobilephone"] = contact_phone.get("Mobile")
                self.destination_json["contactname"] = "{} {}".format(
                    contact.get("FirstName", ""),
                    contact.get("LastName", "")
                )
                self.destination_json["contactrelationship"] = (
                    "PARENT"
                    if contact.get("RelationToPatient") in ["Mother", "Father"]
                    else "GUARDIAN"
                )
            else:
                self.destination_json["contacthomephone"] = None
                self.destination_json["contactmobilephone"] = None
                self.destination_json["contactname"] = None
                self.destination_json["contactrelationship"] = None
            self.destination_json["contactpreference"] = None
            self.destination_json["contactpreference_announcement_email"] = None
            self.destination_json["contactpreference_announcement_phone"] = None
            self.destination_json["contactpreference_announcement_sms"] = None
            self.destination_json["contactpreference_appointment_email"] = None
            self.destination_json["contactpreference_appointment_phone"] = None
            self.destination_json["contactpreference_appointment_sms"] = None
            self.destination_json["contactpreference_billing_email"] = None
            self.destination_json["contactpreference_billing_phone"] = None
            self.destination_json["contactpreference_billing_sms"] = None
            self.destination_json["contactpreference_lab_email"] = None
            self.destination_json["contactpreference_lab_phone"] = None
            self.destination_json["contactpreference_lab_sms"] = None
            self.destination_json["countrycode3166"] = self.source_json["Patient"][
                "Demographics"
            ]["Address"].get("Country")
            self.destination_json["deceaseddate"] = None
            self.destination_json["defaultpharmacyncpdpid"] = None
            # Check for both departmentid and orgid
            department_ids = [
                x["ID"]
                for x in self.source_json["Patient"].get("Identifiers", [])
                if x.get("IDType", "").lower() in ["departmentid", "orgid"]
            ]
            self.destination_json["departmentid"] = department_ids[0] if department_ids else None
            self.destination_json["dob"] = datetime.strptime(
                self.source_json["Patient"]["Demographics"]["DOB"], "%Y-%m-%d"
            ).strftime("%m/%d/%Y")
            self.destination_json["donotcallyn"] = None
            self.destination_json["driverslicenseexpirationdate"] = None
            self.destination_json["driverslicensenumber"] = None
            self.destination_json["driverslicensestateid"] = None
            # Extract first email from array or None
            email_addresses = self.source_json["Patient"]["Demographics"].get("EmailAddresses", [])
            self.destination_json["email"] = email_addresses[0] if email_addresses else None
            self.destination_json["employerid"] = None
            self.destination_json["employerphone"] = None
            self.destination_json["ethnicitycode"] = None
            self.destination_json["ethnicitycodes"] = None
            self.destination_json["firstname"] = self.source_json["Patient"][
                "Demographics"
            ].get("FirstName")
            self.destination_json["genderidentity"] = None
            self.destination_json["genderidentityother"] = None
            # Handle Guarantor - check if exists
            guarantor = self.source_json["Patient"].get("Guarantor")
            if guarantor:
                guarantor_address = guarantor.get("Address", {})
                patient_address = self.source_json["Patient"]["Demographics"].get("Address", {})
                self.destination_json["guarantoraddress1"] = guarantor_address.get("StreetAddress")
                self.destination_json["guarantoraddress2"] = None
                self.destination_json["guarantoraddresssameaspatient"] = (
                    guarantor_address.get("StreetAddress") == patient_address.get("StreetAddress")
                )
                self.destination_json["guarantorcity"] = guarantor_address.get("City")
                self.destination_json["guarantorcountrycode3166"] = guarantor_address.get("Country")
                self.destination_json["guarantordob"] = guarantor.get("DOB")
                guarantor_emails = guarantor.get("EmailAddresses", [])
                self.destination_json["guarantoremail"] = guarantor_emails[0] if guarantor_emails else None
                self.destination_json["guarantoremployerid"] = None
                self.destination_json["guarantorfirstname"] = guarantor.get("FirstName")
                self.destination_json["guarantorlastname"] = guarantor.get("LastName")
                self.destination_json["guarantormiddlename"] = guarantor.get("MiddleName")
                guarantor_phone = guarantor.get("PhoneNumber", {})
                self.destination_json["guarantorphone"] = (
                    guarantor_phone.get("Mobile") or
                    guarantor_phone.get("Home") or
                    guarantor_phone.get("Business")
                )
                self.destination_json["guarantorssn"] = guarantor.get("SSN")
                self.destination_json["guarantorstate"] = guarantor_address.get("State")
                self.destination_json["guarantorsuffix"] = None
                self.destination_json["guarantorzip"] = guarantor_address.get("ZIP")
            else:
                # Set all guarantor fields to None if Guarantor doesn't exist
                self.destination_json["guarantoraddress1"] = None
                self.destination_json["guarantoraddress2"] = None
                self.destination_json["guarantoraddresssameaspatient"] = None
                self.destination_json["guarantorcity"] = None
                self.destination_json["guarantorcountrycode3166"] = None
                self.destination_json["guarantordob"] = None
                self.destination_json["guarantoremail"] = None
                self.destination_json["guarantoremployerid"] = None
                self.destination_json["guarantorfirstname"] = None
                self.destination_json["guarantorlastname"] = None
                self.destination_json["guarantormiddlename"] = None
                self.destination_json["guarantorphone"] = None
                self.destination_json["guarantorssn"] = None
                self.destination_json["guarantorstate"] = None
                self.destination_json["guarantorsuffix"] = None
                self.destination_json["guarantorzip"] = None
            self.destination_json["guardianfirstname"] = None
            self.destination_json["guardianlastname"] = None
            self.destination_json["guardianmiddlename"] = None
            self.destination_json["guardiansuffix"] = None
            self.destination_json["hasmobileyn"] = None
            self.destination_json["homeboundyn"] = None
            self.destination_json["homeless"] = None
            self.destination_json["homelesstype"] = None
            self.destination_json["homephone"] = None
            self.destination_json["ignorerestrictions"] = None
            self.destination_json["industrycode"] = None
            self.destination_json["lastname"] = self.source_json["Patient"][
                "Demographics"
            ].get("LastName")
            self.destination_json["middlename"] = self.source_json["Patient"][
                "Demographics"
            ].get("MiddleName")
            self.destination_json["mobilecarrierid"] = None
            self.destination_json["mobilephone"] = self.source_json["Patient"][
                "Demographics"
            ]["PhoneNumber"].get("Mobile")
            self.destination_json["nextkinname"] = None
            self.destination_json["nextkinphone"] = None
            self.destination_json["nextkinrelationship"] = None
            self.destination_json["notes"] = self.source_json["Patient"].get("Notes")
            self.destination_json["occupationcode"] = None
            self.destination_json["onlinestatementonlyyn"] = None
            self.destination_json["portalaccessgiven"] = None
            self.destination_json["povertylevelcalculated"] = None
            self.destination_json["povertylevelfamilysize"] = None
            self.destination_json["povertylevelfamilysizedeclined"] = None
            self.destination_json["povertylevelincomedeclined"] = None
            self.destination_json["povertylevelincomepayperiod"] = None
            self.destination_json["povertylevelincomeperpayperiod"] = None
            self.destination_json["povertylevelincomerangedeclined"] = None
            self.destination_json["preferredname"] = None
            self.destination_json["preferredpronouns"] = None
            self.destination_json["primarydepartmentid"] = None
            self.destination_json["primaryproviderid"] = None
            self.destination_json["publichousing"] = None
            self.destination_json["referralsourceid"] = None
            self.destination_json["referralsourceother"] = None
            self.destination_json["schoolbasedhealthcenter"] = None
            self.destination_json["sex"] = (
                "M"
                if self.source_json["Patient"]["Demographics"].get("Sex") == "Male"
                else "F"
            )
            self.destination_json["sexualorientation"] = None
            self.destination_json["sexualorientationother"] = None
            self.destination_json["showerrormessage"] = None
            self.destination_json["ssn"] = self.source_json["Patient"][
                "Demographics"
            ].get("SSN")
            self.destination_json["state"] = self.source_json["Patient"][
                "Demographics"
            ]["Address"].get("State")
            self.destination_json["status"] = None
            self.destination_json["suffix"] = None
            self.destination_json["veteran"] = None
            self.destination_json["workphone"] = self.source_json["Patient"][
                "Demographics"
            ]["PhoneNumber"].get("Office")
            self.destination_json["zip"] = self.source_json["Patient"]["Demographics"][
                "Address"
            ].get("ZIP")
            self.destination_json["departmentid"] = self.source_json["Location"].get("Department",None)
            patient_created, status_code = patient.create_patient(
                **self.destination_json
            )
            if self.source_json["Meta"].get("Test"):
                self.destination_response["Meta"]["Raw"].append(patient_created)
            if status_code == 200:
                # Handle response - could be list or dict
                if isinstance(patient_created, list) and len(patient_created) > 0:
                    patient_id = patient_created[0].get("patientid")
                elif isinstance(patient_created, dict):
                    patient_id = patient_created.get("patientid")
                else:
                    patient_id = None

                if patient_id:
                    patient_res = {
                        "Patient": {
                            "Identifier": {
                                "ID": patient_id,
                                "IDType": "PatientID",
                            }
                        }
                    }
                    self.destination_response.update(patient_res)
                else:
                    self.destination_response.update(patient_created)
            else:
                self.destination_response.update(patient_created)

            return self.destination_response

        except Exception as e:
            self.destination_response.update({"Error": str(e)})
            return self.destination_response


# class ArrivalTransformer(Transformer):
#     def __init__(self, source_data, customer_id, ehrid, **kwargs):
#         self.source_json = source_data
#         self.customer_id = customer_id
#         self.connection = ehrid
#         self.destination_json = {"patients": [], "appointmentid": []}
#         self.destination_response = {
#             "Meta": {
#                 "DataModel": "PatientAdmin",
#                 "EventType": "Arrival",
#                 "Source": {"ID": self.customer_id, "Name": kwargs.get("name")},
#                 "Raw": [],
#             },
#         }

#     def transform(self):
#         try:

#             Arrival(**self.source_json)

#             appointment = Appointments(self.customer_id, self.connection)
#             appointment.getAuthToken()
#             appt_practiceid = appointment.practice_id

#             appointmentid = self.source_json["Visit"].get("VisitNumber")
#             if self.source_json.get("Meta").get("Event").lower() == "check-in":
#                 check_in, status_code = appointment.appointment_checkin(
#                     appt_practiceid, appointmentid
#                 )
#             else:
#                 check_in, status_code = appointment.start_checkin(
#                     appt_practiceid, appointmentid
#                 )

#             if self.source_json["Meta"].get("Test"):
#                 self.destination_response["Meta"]["Raw"].append(check_in)
#             if status_code == 200:
#                 self.destination_response.update({"Success": check_in.get("success")})
#                 if check_in.get("message"):
#                     self.destination_response.update(
#                         {"Message": check_in.get("message")}
#                     )
#             else:
#                 self.destination_response.update(check_in)
#             return self.destination_response
#         except Exception as e:
#             return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class DischargeTransformer(Transformer):
#     def __init__(self, source_data, customer_id, ehrid, **kwargs):
#         self.source_json = source_data
#         self.customer_id = customer_id
#         self.connection = ehrid
#         self.destination_json = {"patients": [], "appointmentid": []}
#         self.destination_response = {
#             "Meta": {
#                 "DataModel": "PatientAdmin",
#                 "EventType": "CheckOut",
#                 "Source": {"ID": self.customer_id, "Name": kwargs.get("name")},
#                 "Raw": [],
#             },
#         }

#     def transform(self):
#         try:

#             Discharge(**self.source_json)

#             appointment = Appointments(self.customer_id, self.connection)
#             appointment.getAuthToken()
#             appt_practiceid = appointment.practice_id

#             appointmentid = self.source_json["Visit"].get("VisitNumber")

#             check_out, status_code = appointment.checkout(
#                 appt_practiceid, appointmentid
#             )

#             if self.source_json["Meta"].get("Test"):
#                 self.destination_response["Meta"]["Raw"].append(check_out)
#             if status_code == 200:
#                 self.destination_response.update({"Success": check_out.get("success")})
#             else:
#                 self.destination_response.update(check_out)
#             return self.destination_response

#         except Exception as e:
#             return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
