import json

from services.ehr.athena.client import AthenaHealthClient
from services.ehr.athena.urls import ATHENA_URLS


class Chart(AthenaHealthClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_ccda_doc(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_ccda_doc"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "version": kwargs.get("version"),
                "chartsharinggroupid": kwargs.get("chartsharinggroupid"),
                "startdate": kwargs.get("startdate"),
                "encounterid": kwargs.get("encounterid"),
                "enterpriseid": kwargs.get("enterpriseid"),
                "documentid": kwargs.get("documentid"),
                "enddate": kwargs.get("enddate"),
                "departmentid": kwargs.get("departmentid"),
                "documenttype": kwargs.get("documenttype"),
                "inpatient": kwargs.get("inpatient"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def get_care_plan(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_care_plan"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "chartid": kwargs.get("chartid"),
                "stayid": kwargs.get("stayid"),
                "inpatient": kwargs.get("inpatient"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def get_vitals(self, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_vitals"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "format": kwargs.get("format"),
                "enddate": kwargs.get("enddate"),
                "xmloutput": kwargs.get("xmloutput"),
                "departmentid": kwargs.get("departmentid"),
                "startdate": kwargs.get("startdate"),
                "encounterid": kwargs.get("encounterid"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def get_past_screening_questionnaires(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_past_screening_questionnaires"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_patient_allergies(self, patientid,**kwargs):
        url = self.build_url(
            ATHENA_URLS["Chart"]["get_patient_allergies"]["path"],
            patientId=patientid,
        )
        print(kwargs)
        return self.get(
            url,
            payload={
                "showinactive": kwargs.get("showinactive"),
                "departmentid": kwargs.get("departmentid"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_patient_allergies(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_patient_allergies"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            allergies=json.dumps(kwargs.get("allergies")),
            departmentid=kwargs.get("departmentid"),
            nkda=kwargs.get("nkda"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_labs(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_labs"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "allresultsbyencounterid": kwargs.get("allresultsbyencounterid"),
                "exactduplicatedocumentid": kwargs.get("exactduplicatedocumentid"),
                "supersededdocumentid": kwargs.get("supersededdocumentid"),
                "startdate": kwargs.get("startdate"),
                "labresultstatus": kwargs.get("labresultstatus"),
                "showtemplate": kwargs.get("showtemplate"),
                "showportalonly": kwargs.get("showportalonly"),
                "showhidden": kwargs.get("showhidden"),
                "showabnormaldetails": kwargs.get("showabnormaldetails"),
                "enddate": kwargs.get("enddate"),
                "departmentid": kwargs.get("departmentid"),
                "hideduplicate": kwargs.get("hideduplicate"),
                "analyteresultstatus": kwargs.get("analyteresultstatus"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_care_team_members(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_care_team_members"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_care_team_members(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_care_team_members"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            clinicalproviderid=kwargs.get("clinicalproviderid"),
            departmentid=kwargs.get("departmentid"),
            recipientclassid=kwargs.get("recipientclassid"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_care_team_members(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["delete_care_team_members"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.delete(
            url,
            params={
                "memberid": kwargs.get("memberid"),
                "departmentid": kwargs.get("departmentid"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def export_document(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["export_document"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            createfromdatedocumentclass=kwargs.get("createfromdatedocumentclass"),
            createfromdaterangeend=kwargs.get("createfromdaterangeend"),
            createfromdaterangestart=kwargs.get("createfromdaterangestart"),
            departmentid=kwargs.get("departmentid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_chart_document(self, practiceid, patientid, documentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_chart_document"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            documentid=documentid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def get_encounters(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_encounters"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "startdate": kwargs.get("startdate"),
                "showallstatuses": kwargs.get("showallstatuses"),
                "showalltypes": kwargs.get("showalltypes"),
                "appointmentid": kwargs.get("appointmentid"),
                "enddate": kwargs.get("enddate"),
                "showdiagnoses": kwargs.get("showdiagnoses"),
                "providerid": kwargs.get("providerid"),
                "departmentid": kwargs.get("departmentid"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_appointment_encounters(
        self, practiceid, patientid, appointmentid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_appointment_encounters"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            appointmentid=appointmentid,
        )
        return self.get(
            url,
            params={
                "mobile": kwargs.get("mobile"),
                "skipamendments": kwargs.get("skipamendments"),
            },
        )

    def get_family_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_family_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def update_family_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_family_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            relatives=kwargs.get("relatives"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_flowsheet_by_code(self, practiceid, patientid, snomedcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_flowsheet_by_code"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            snomedcode=snomedcode,
        )
        return self.get(
            url,
            params={
                "enddate": kwargs.get("enddate"),
                "departmentid": kwargs.get("departmentid"),
                "providerid": kwargs.get("providerid"),
                "showglobalflowsheetelementsonly": kwargs.get(
                    "showglobalflowsheetelementsonly"
                ),
                "startdate": kwargs.get("startdate"),
            },
        )

    def get_gpal_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_gpal_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def get_gyn_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_gyn_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def update_gyn_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_gyn_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            questions=kwargs.get("questions"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_lab_results(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_lab_results"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "allresultsbyencounterid": kwargs.get("allresultsbyencounterid"),
                "exactduplicatedocumentid": kwargs.get("exactduplicatedocumentid"),
                "supersededdocumentid": kwargs.get("supersededdocumentid"),
                "startdate": kwargs.get("startdate"),
                "labresultstatus": kwargs.get("labresultstatus"),
                "showtemplate": kwargs.get("showtemplate"),
                "showportalonly": kwargs.get("showportalonly"),
                "showhidden": kwargs.get("showhidden"),
                "showabnormaldetails": kwargs.get("showabnormaldetails"),
                "enddate": kwargs.get("enddate"),
                "departmentid": kwargs.get("departmentid"),
                "hideduplicate": kwargs.get("hideduplicate"),
                "analyteresultstatus": kwargs.get("analyteresultstatus"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def get_medical_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_medical_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def update_medical_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_medical_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            questions=kwargs.get("questions"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def add_medication(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_medication"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            hidden=kwargs.get("hidden"),
            medicationid=kwargs.get("medicationid"),
            patientnote=kwargs.get("patientnote"),
            providernote=kwargs.get("providernote"),
            startdate=kwargs.get("startdate"),
            stopdate=kwargs.get("stopdate"),
            stopreason=kwargs.get("stopreason"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_medications(self, patientid, **kwargs):

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_patient_medications"]["path"],
            patientId=patientid,
        )
        return self.get(
            url,
            payload={
                "showpend": kwargs.get("showpend"),
                "showrxnorm": kwargs.get("showrxnorm"),
                "departmentid": kwargs.get("departmentid"),
                "medicationtype": kwargs.get("medicationtype"),
                "showndc": kwargs.get("showndc"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_medications(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_medications"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            hidden=kwargs.get("hidden"),
            patientnote=kwargs.get("patientnote"),
            providernote=kwargs.get("providernote"),
            startdate=kwargs.get("startdate"),
            stopdate=kwargs.get("stopdate"),
            stopreason=kwargs.get("stopreason"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_medication(self, practiceid, patientid, medicationentryid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_medication"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            medicationentryid=medicationentryid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            hidden=kwargs.get("hidden"),
            patientnote=kwargs.get("patientnote"),
            providernote=kwargs.get("providernote"),
            startdate=kwargs.get("startdate"),
            stopdate=kwargs.get("stopdate"),
            stopreason=kwargs.get("stopreason"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_medication(self, practiceid, patientid, medicationentryid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["delete_medication"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            medicationentryid=medicationentryid,
        )
        return self.delete(url, params={"departmentid": kwargs.get("departmentid")})

    def get_charts(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_charts"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_perinatelhistory(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_perinatelhistory"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "showunansweredquestions": kwargs.get("showunansweredquestions"),
            },
        )

    def add_problems(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_problems"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            laterality=kwargs.get("laterality"),
            note=kwargs.get("note"),
            snomedcode=kwargs.get("snomedcode"),
            startdate=kwargs.get("startdate"),
            status=kwargs.get("status"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_problems(self, patientid, **kwargs):

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_patient_problems"]["path"],
            patientId=patientid,
        )
        return self.get(
            url,
            payload={
                "showinactive": kwargs.get("showinactive"),
                "departmentid": kwargs.get("departmentid"),
                "showdiagnosisinfo": kwargs.get("showdiagnosisinfo"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_problems(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_problems"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            replacenote=kwargs.get("replacenote"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_problem_details(self, practiceid, patientid, problemid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_problem_details"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            problemid=problemid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            laterality=kwargs.get("laterality"),
            note=kwargs.get("note"),
            startdate=kwargs.get("startdate"),
            status=kwargs.get("status"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_problem(self, practiceid, patientid, problemid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["delete_problem"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            problemid=problemid,
        )
        return self.delete(
            url,
            params={
                "remove": kwargs.get("remove"),
                "departmentid": kwargs.get("departmentid"),
            },
        )

    def update_section_note(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_section_note"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            replacenote=kwargs.get("replacenote"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_social_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_social_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "recipientcategory": kwargs.get("recipientcategory"),
                "departmentid": kwargs.get("departmentid"),
                "shownotperformedquestions": kwargs.get("shownotperformedquestions"),
                "showunansweredquestions": kwargs.get("showunansweredquestions"),
            },
        )

    def update_social_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_social_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            procedures=kwargs.get("procedures"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_social_history_templates(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_social_history_templates"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def update_social_history_templates(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_social_history_templates"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            templateids=kwargs.get("templateids"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def add_surgical_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_surgical_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            procedures=kwargs.get("procedures"),
            sectionnote=kwargs.get("sectionnote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_surgical_history(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_patient_surgical_history"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def add_vaccine(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_vaccine"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            administerdate=kwargs.get("administerdate"),
            cvx=kwargs.get("cvx"),
            departmentid=kwargs.get("departmentid"),
            ndc=kwargs.get("ndc"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_vaccines(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_vaccines"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "showdeleted": kwargs.get("showdeleted"),
                "showdeclinedorders": kwargs.get("showdeclinedorders"),
                "departmentid": kwargs.get("departmentid"),
                "showprescribednotadministered": kwargs.get(
                    "showprescribednotadministered"
                ),
                "showrefused": kwargs.get("showrefused"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_vaccine(self, practiceid, patientid, vaccineid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_vaccine"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            vaccineid=vaccineid,
        )

        payload = self.build_payload(
            administerdate=kwargs.get("administerdate"),
            cvx=kwargs.get("cvx"),
            departmentid=kwargs.get("departmentid"),
            ndc=kwargs.get("ndc"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_vaccine(self, practiceid, patientid, vaccineid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["delete_vaccine"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            vaccineid=vaccineid,
        )
        return self.delete(
            url,
            params={
                "deleteddate": kwargs.get("deleteddate"),
                "departmentid": kwargs.get("departmentid"),
            },
        )

    def add_vitals(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_vitals"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            departmentid=kwargs.get("departmentid"),
            source=kwargs.get("source"),
            vitals=json.dumps(kwargs.get("vitals")),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_vitals(self, patientid, **kwargs):

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_patient_vitals"]["path"],
            patientId=patientid,
        )
        return self.get(
            url,
            payload={
                "enddate": kwargs.get("enddate"),
                "departmentid": kwargs.get("departmentid"),
                "startdate": kwargs.get("startdate"),
                "showemptyvitals": kwargs.get("showemptyvitals"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def update_vital(self, practiceid, patientid, vitalid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_vital"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            vitalid=vitalid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            value=kwargs.get("value"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_flowsheet_templates_by_problem_code(self, practiceid, snomedcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_flowsheet_templates_by_problem_code"]["path"],
            practiceid=practiceid,
            snomedcode=snomedcode,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "providerid": kwargs.get("providerid"),
            },
        )

    def get_gyn_history_questions(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_gyn_history_questions"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "showdeleted": kwargs.get("showdeleted"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_medical_history_questions(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_medical_history_questions"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "showdeleted": kwargs.get("showdeleted"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_care_team_recipient_classes(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_care_team_recipient_classes"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_social_history_questions_and_templates(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_social_history_questions_and_templates"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_configured_vital_fields(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_configured_vital_fields"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "specialtyid": kwargs.get("specialtyid"),
                "showunconfigured": kwargs.get("showunconfigured"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_encounter_details(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_encounter_details"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def get_entounter_summary(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_entounter_summary"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "mobile": kwargs.get("mobile"),
                "skipamendments": kwargs.get("skipamendments"),
            },
        )

    def get_allergies_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_allergies_delta"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_allergies_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["subscribe_to_allergies_events"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_allergies_subscriptions_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_allergies_subscriptions_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_allergies_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["unsubscribe_to_allergies_events"]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_subscribe_to_allergies_change_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_allergies_change_events"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_family_history_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_family_history_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_family_history_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["subscribe_to_family_history_events"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_family_history_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_family_history_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_family_history_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["unsubscribe_to_family_history_events"]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_subscribe_to_family_hisotry_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_family_hisotry_events"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_medication_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_medication_delta"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "patientid": kwargs.get("patientid"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_medication_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["subscribe_to_medication_events"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_medication_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_medication_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_medication_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["unsubscribe_to_medication_events"]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_subscribe_to_medication_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_medication_events"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_subscribe_problems_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_problems_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "patientid": kwargs.get("patientid"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_problems_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["subscribe_to_problems_events"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_problems_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_problems_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_problems_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["unsubscribe_to_problems_events"]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_subscribe_to_problems_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_problems_events"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_subscribe_vaccines_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_vaccines_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_vaccines_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["subscribe_to_vaccines_events"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_vaccine_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_vaccine_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_vaccines_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["unsubscribe_to_vaccines_events"]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_subscribe_to_vaccine_events(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_subscribe_to_vaccine_events"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def update_ccda_doc(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["update_ccda_doc"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            patientfacingcall=kwargs.get("patientfacingcall"),
            thirdpartyusername=kwargs.get("thirdpartyusername"),
            ccda=kwargs.get("ccda"),
            departmentid=kwargs.get("departmentid"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_ccda_record(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_ccda_record"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "format": kwargs.get("format"),
                "enddate": kwargs.get("enddate"),
                "xmloutput": kwargs.get("xmloutput"),
                "purpose": kwargs.get("purpose"),
                "departmentid": kwargs.get("departmentid"),
                "startdate": kwargs.get("startdate"),
                "THIRDPARTYUSERNAME": kwargs.get("THIRDPARTYUSERNAME"),
                "PATIENTFACINGCALL": kwargs.get("PATIENTFACINGCALL"),
            },
        )

    def get_available_allergies(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_available_allergies"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_allergy_reactions(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_allergy_reactions"]["path"], practiceid=practiceid
        )
        return self.get(url, params={})

    def get_allergy_severities(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_allergy_severities"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_available_medications(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_available_medications"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_mediation_stop_reasons(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["get_mediation_stop_reasons"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def add_risk_adjustment(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Chart"]["add_risk_adjustment"]["path"], practiceid=practiceid
        )

        payload = self.build_payload(
            entry=kwargs.get("entry"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )
