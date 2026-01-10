from ecaremd.ehr_integrations.ehr_services.athena.client import AthenaHealthClient
from ecaremd.ehr_integrations.ehr_services.athena.urls import ATHENA_URLS


class Encounter(AthenaHealthClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_order_groups(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_order_groups"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            orderingproviderid=kwargs.get("orderingproviderid"),
            patientcaseid=kwargs.get("patientcaseid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_facilities(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["facilities"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "name": kwargs.get("name"),
                "patientid": kwargs.get("patientid"),
                "ordertype": kwargs.get("ordertype"),
            },
        )

    def get_office_order_types(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["office_order_types"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_patient_locations(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["patient_locations"]["path"], practiceid=practiceid
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def get_patient_statuses(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["patient_statuses"]["path"], practiceid=practiceid
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_configured_questionnaire_screeners(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["configured_questionnaire_screeners"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "appointmentid": kwargs.get("appointmentid"),
                "departmentid": kwargs.get("departmentid"),
                "patientid": kwargs.get("patientid"),
                "encounterid": kwargs.get("encounterid"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_encounter_information(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["encounter_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def update_encounter_information(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_encounter_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            patientlocationid=kwargs.get("patientlocationid"),
            patientstatusid=kwargs.get("patientstatusid"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_encounter_assessment(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["encounter_assessment"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={"showstructured": kwargs.get("showstructured")})

    def update_encounter_assessment(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_encounter_assessment"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            assessmenttext=kwargs.get("assessmenttext"),
            replacetext=kwargs.get("replacetext"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_default_search_facility(self, practiceid, encounterid):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["default_search_facility"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url)

    def create_diagnosis(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_diagnosis"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            icd10codes=kwargs.get("icd10codes"),
            icd9codes=kwargs.get("icd9codes"),
            laterality=kwargs.get("laterality"),
            note=kwargs.get("note"),
            snomedcode=kwargs.get("snomedcode"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_diagnoses(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["diagnoses"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def update_selected_diagnoses(self, practiceid, encounterid, diagnosisid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_selected_diagnoses"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            diagnosisid=diagnosisid,
        )

        payload = self.build_payload(
            icd10codes=kwargs.get("icd10codes"),
            icd9codes=kwargs.get("icd9codes"),
            laterality=kwargs.get("laterality"),
            note=kwargs.get("note"),
            snomedcode=kwargs.get("snomedcode"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_selected_diagnoses(self, practiceid, encounterid, diagnosisid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["delete_selected_diagnoses"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            diagnosisid=diagnosisid,
        )
        return self.delete(url, params={})

    def get_dictatable_sections(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["dictatable_sections"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_dictation_status(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["dictation_status"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def get_documents_review(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["documents_review"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def encounter_reason_note(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["encounter_reason_note"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            appendtext=kwargs.get("appendtext"),
            notetext=kwargs.get("notetext"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_encounter_reasons(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["encounter_reasons"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def delete_encounter_reasons(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["delete_encounter_reasons"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.delete(
            url, params={"encounterreasonid": kwargs.get("encounterreasonid")}
        )

    def add_encounter_reasons(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["add_encounter_reasons"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            encounterreasonid=kwargs.get("encounterreasonid"),
            laterality=kwargs.get("laterality"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def submit_external_dictation_request(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["submit_external_dictation_request"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            encountersection=kwargs.get("encountersection"),
            field=kwargs.get("field"),
            totalmessagecount=kwargs.get("totalmessagecount"),
            transcriptiontext=kwargs.get("transcriptiontext"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_hpi(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["hpi"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showstructured": kwargs.get("showstructured"),
                "templateids": kwargs.get("templateids"),
            },
        )

    def update_hpi(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_hpi"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            hpi=kwargs.get("hpi"),
            hpitoros=kwargs.get("hpitoros"),
            replacesectionnote=kwargs.get("replacesectionnote"),
            sectionnote=kwargs.get("sectionnote"),
            templatedata=kwargs.get("templatedata"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_hpi_reference_template(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["hpi_reference_template"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_orders(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orders"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showdeclinedorders": kwargs.get("showdeclinedorders"),
                "allowdischargetype": kwargs.get("allowdischargetype"),
                "showdiagnoseswithoutorders": kwargs.get("showdiagnoseswithoutorders"),
                "showclinicalprovider": kwargs.get("showclinicalprovider"),
                "showexternalcodes": kwargs.get("showexternalcodes"),
            },
        )

    def create_sction_note_to_selected_order(
        self, practiceid, encounterid, orderid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_sction_note_to_selected_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            orderid=orderid,
        )

        payload = self.build_payload(
            actionnote=kwargs.get("actionnote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def deny_specific_order(self, practiceid, encounterid, orderid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["deny_specific_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            orderid=orderid,
        )

        payload = self.build_payload(
            denyreasonid=kwargs.get("denyreasonid"),
            username=kwargs.get("username"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_deny_selected_order(self, practiceid, encounterid, orderid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["deny_selected_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            orderid=orderid,
        )
        return self.get(url, params={"username": kwargs.get("username")})

    def return_to_submit(self, practiceid, encounterid, orderid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["return_to_submit"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            orderid=orderid,
        )

        payload = self.build_payload()
        return self.post(url, content_type="", data=payload)

    def submit_order(self, practiceid, encounterid, orderid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["submit_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            orderid=orderid,
        )

        payload = self.build_payload(
            submitvia=kwargs.get("submitvia"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_dme_order(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_dme_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            dispenseaswritten=kwargs.get("dispenseaswritten"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            numrefillsallowed=kwargs.get("numrefillsallowed"),
            orderingmode=kwargs.get("orderingmode"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
            totalquantity=kwargs.get("totalquantity"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_imaging_order(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_imaging_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            futuresubmitdate=kwargs.get("futuresubmitdate"),
            highpriority=kwargs.get("highpriority"),
            loinc=kwargs.get("loinc"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_lab_orders(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_lab_orders"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            futuresubmitdate=kwargs.get("futuresubmitdate"),
            highpriority=kwargs.get("highpriority"),
            loinc=kwargs.get("loinc"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_non_standard_order(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_non_standard_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            highpriority=kwargs.get("highpriority"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_outstanding_orders(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["outstanding_orders"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showdeclinedorders": kwargs.get("showdeclinedorders"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def create_patient_info(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_patient_info"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            externalnote=kwargs.get("externalnote"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_prescription(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_prescription"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            additionalinstructions=kwargs.get("additionalinstructions"),
            administernote=kwargs.get("administernote"),
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            dispenseaswritten=kwargs.get("dispenseaswritten"),
            dosagequantity=kwargs.get("dosagequantity"),
            dosagequantityunit=kwargs.get("dosagequantityunit"),
            duration=kwargs.get("duration"),
            externalnote=kwargs.get("externalnote"),
            facilityid=kwargs.get("facilityid"),
            frequency=kwargs.get("frequency"),
            ndc=kwargs.get("ndc"),
            numrefillsallowed=kwargs.get("numrefillsallowed"),
            orderingmode=kwargs.get("orderingmode"),
            ordertypeid=kwargs.get("ordertypeid"),
            pharmacyncpdpid=kwargs.get("pharmacyncpdpid"),
            pharmacynote=kwargs.get("pharmacynote"),
            providernote=kwargs.get("providernote"),
            rxnormid=kwargs.get("rxnormid"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_procedure(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_procedure"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            futuresubmitdate=kwargs.get("futuresubmitdate"),
            highpriority=kwargs.get("highpriority"),
            ordertypeid=kwargs.get("ordertypeid"),
            providernote=kwargs.get("providernote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_referral_request(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_referral_request"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            facilityid=kwargs.get("facilityid"),
            facilitynote=kwargs.get("facilitynote"),
            futuresubmitdate=kwargs.get("futuresubmitdate"),
            highpriority=kwargs.get("highpriority"),
            notetopatient=kwargs.get("notetopatient"),
            ordertypeid=kwargs.get("ordertypeid"),
            procedurecode=kwargs.get("procedurecode"),
            providernote=kwargs.get("providernote"),
            reasonforreferral=kwargs.get("reasonforreferral"),
            startdate=kwargs.get("startdate"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_vaccine_order(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_vaccine_order"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            administernote=kwargs.get("administernote"),
            declineddate=kwargs.get("declineddate"),
            declinedreason=kwargs.get("declinedreason"),
            diagnosissnomedcode=kwargs.get("diagnosissnomedcode"),
            dispenseaswritten=kwargs.get("dispenseaswritten"),
            facilityid=kwargs.get("facilityid"),
            ndc=kwargs.get("ndc"),
            numrefillsallowed=kwargs.get("numrefillsallowed"),
            orderingmode=kwargs.get("orderingmode"),
            ordertypeid=kwargs.get("ordertypeid"),
            performondate=kwargs.get("performondate"),
            pharmacynote=kwargs.get("pharmacynote"),
            providernote=kwargs.get("providernote"),
            unstructuredsig=kwargs.get("unstructuredsig"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_goals(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["patient_goals"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def update_discussion_notes(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_discussion_notes"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            discussionnotes=kwargs.get("discussionnotes"),
            replacediscussionnotes=kwargs.get("replacediscussionnotes"),
            versiontoken=kwargs.get("versiontoken"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_free_text_goal(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_free_text_goal"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            freetextgoal=kwargs.get("freetextgoal"),
            replacefreetextgoal=kwargs.get("replacefreetextgoal"),
            versiontoken=kwargs.get("versiontoken"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_patient_instructions(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_patient_instructions"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            patientinstructions=kwargs.get("patientinstructions"),
            replaceinstructions=kwargs.get("replaceinstructions"),
            versiontoken=kwargs.get("versiontoken"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_physical_exam(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["physical_exam"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showstructured": kwargs.get("showstructured"),
                "ccdaoutputformat": kwargs.get("ccdaoutputformat"),
                "templateids": kwargs.get("templateids"),
            },
        )

    def update_physical_exam(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_physical_exam"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            physicalexam=kwargs.get("physicalexam"),
            replacesectionnote=kwargs.get("replacesectionnote"),
            sectionnote=kwargs.get("sectionnote"),
            templateids=kwargs.get("templateids"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_physical_exam_template(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["physical_exam_template"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_procedure_documentation(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["procedure_documentation"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showhtml": kwargs.get("showhtml"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def submit_questionnaire_screeners(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["submit_questionnaire_screeners"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            templateid=kwargs.get("templateid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_encounter_questionnaire_screeners(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["encounter_questionnaire_screeners"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def update_questionnaire_screeners(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_questionnaire_screeners"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            declinedreason=kwargs.get("declinedreason"),
            documentids=kwargs.get("documentids"),
            guidelines=kwargs.get("guidelines"),
            metaquestions=kwargs.get("metaquestions"),
            note=kwargs.get("note"),
            questionnaireid=kwargs.get("questionnaireid"),
            questions=kwargs.get("questions"),
            score=kwargs.get("score"),
            state=kwargs.get("state"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_score_only(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_score_only"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            declinedreason=kwargs.get("declinedreason"),
            documentids=kwargs.get("documentids"),
            metaquestions=kwargs.get("metaquestions"),
            note=kwargs.get("note"),
            questionnaireid=kwargs.get("questionnaireid"),
            score=kwargs.get("score"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_review_of_systems(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["review_of_systems"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "showstructured": kwargs.get("showstructured"),
                "wellchildtemplateids": kwargs.get("wellchildtemplateids"),
                "templateids": kwargs.get("templateids"),
            },
        )

    def update_review_of_systems(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_review_of_systems"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            hpitoros=kwargs.get("hpitoros"),
            replacesectionnote=kwargs.get("replacesectionnote"),
            reportedby=kwargs.get("reportedby"),
            reviewofsystems=kwargs.get("reviewofsystems"),
            sectionnote=kwargs.get("sectionnote"),
            templateids=kwargs.get("templateids"),
            wellchildreplacesectionnote=kwargs.get("wellchildreplacesectionnote"),
            wellchildreportedby=kwargs.get("wellchildreportedby"),
            wellchildros=kwargs.get("wellchildros"),
            wellchildsectionnote=kwargs.get("wellchildsectionnote"),
            wellchildtemplateids=kwargs.get("wellchildtemplateids"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_review_of_systems_templates(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["review_of_systems_templates"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def start_external_dictation(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["start_external_dictation"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            dictatedby=kwargs.get("dictatedby"),
            dictationrecordeddatetime=kwargs.get("dictationrecordeddatetime"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def add_vital_information(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["add_vital_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            vitals=kwargs.get("vitals"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_vitals(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["vitals"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "enddate": kwargs.get("enddate"),
                "startdate": kwargs.get("startdate"),
                "showemptyvitals": kwargs.get("showemptyvitals"),
            },
        )

    def update_vital_information(self, practiceid, encounterid, vitalid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_vital_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            vitalid=vitalid,
        )

        payload = self.build_payload(
            value=kwargs.get("value"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_vital_information(self, practiceid, encounterid, vitalid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["delete_vital_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            vitalid=vitalid,
        )
        return self.delete(url, params={})

    def get_questionnaire_screeners(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["questionnaire_screeners"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_configured_encounter_reasons(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["configured_encounter_reasons"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_ordersets(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["ordersets"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "username": kwargs.get("username"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_ordertype(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["ordertype"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "labfacilityid": kwargs.get("labfacilityid"),
                "imagingfacilityid": kwargs.get("imagingfacilityid"),
                "providerid": kwargs.get("providerid"),
                "searchterm": kwargs.get("searchterm"),
                "limit": kwargs.get("limit"),
                "snomedcode": kwargs.get("snomedcode"),
                "encounterid": kwargs.get("encounterid"),
            },
        )

    def get_procedure_codes(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["procedure_codes"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(
            url,
            params={
                "searchvalue": kwargs.get("searchvalue"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_services(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["services"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )
        return self.get(url, params={})

    def create_service(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["create_service"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            billforservice=kwargs.get("billforservice"),
            icd10codes=kwargs.get("icd10codes"),
            modifiers=kwargs.get("modifiers"),
            procedurecode=kwargs.get("procedurecode"),
            units=kwargs.get("units"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_service_information(self, practiceid, encounterid, serviceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["service_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            serviceid=serviceid,
        )
        return self.get(url, params={})

    def update_service_information(self, practiceid, encounterid, serviceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_service_information"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            serviceid=serviceid,
        )

        payload = self.build_payload(
            billforservice=kwargs.get("billforservice"),
            icd10codes=kwargs.get("icd10codes"),
            modifiers=kwargs.get("modifiers"),
            units=kwargs.get("units"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_specific_service(self, practiceid, encounterid, serviceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["delete_specific_service"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
            serviceid=serviceid,
        )
        return self.delete(url, params={})

    def update_services_notes(self, practiceid, encounterid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["update_services_notes"]["path"],
            practiceid=practiceid,
            encounterid=encounterid,
        )

        payload = self.build_payload(
            note=kwargs.get("note"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_affecting_modifiers(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["affecting_modifiers"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def hpi_feedback(self, practiceid, transactionid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["hpi_feedback"]["path"],
            practiceid=practiceid,
            transactionid=transactionid,
        )

        payload = self.build_payload(
            accountbalance=kwargs.get("accountbalance"),
            authorizationcharacteristics=kwargs.get("authorizationcharacteristics"),
            authorizationcode=kwargs.get("authorizationcode"),
            authorizationtransactiondate=kwargs.get("authorizationtransactiondate"),
            authorizationtransactiontime=kwargs.get("authorizationtransactiontime"),
            businessdate=kwargs.get("businessdate"),
            cardname=kwargs.get("cardname"),
            cardtype=kwargs.get("cardtype"),
            cashbackamount=kwargs.get("cashbackamount"),
            cashierid=kwargs.get("cashierid"),
            customercode=kwargs.get("customercode"),
            deviceid=kwargs.get("deviceid"),
            devicestate=kwargs.get("devicestate"),
            emvreceiptstring=kwargs.get("emvreceiptstring"),
            expirationdate=kwargs.get("expirationdate"),
            fundinginfo=kwargs.get("fundinginfo"),
            gatewayapiresponsestring=kwargs.get("gatewayapiresponsestring"),
            hpimerchantid=kwargs.get("hpimerchantid"),
            hpitransactionid=kwargs.get("hpitransactionid"),
            invoicenumber=kwargs.get("invoicenumber"),
            issuertransactionid=kwargs.get("issuertransactionid"),
            itemlist=kwargs.get("itemlist"),
            merchantnumber=kwargs.get("merchantnumber"),
            posdatacode=kwargs.get("posdatacode"),
            posentrymode=kwargs.get("posentrymode"),
            posreferencenumber=kwargs.get("posreferencenumber"),
            response=kwargs.get("response"),
            retrievalreferencenumber=kwargs.get("retrievalreferencenumber"),
            systemtraceauditnumber=kwargs.get("systemtraceauditnumber"),
            taxamount=kwargs.get("taxamount"),
            tendertype=kwargs.get("tendertype"),
            token=kwargs.get("token"),
            totalamount=kwargs.get("totalamount"),
            transactiontype=kwargs.get("transactiontype"),
            truncatedpan=kwargs.get("truncatedpan"),
            type=kwargs.get("type"),
            validationcode=kwargs.get("validationcode"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_cpot_image_studies(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["cpot_image_studies"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "searchvalue": kwargs.get("searchvalue"),
                "facilityid": kwargs.get("facilityid"),
            },
        )

    def get_cpot_labs(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["cpot_labs"]["path"], practiceid=practiceid
        )
        return self.get(
            url,
            params={
                "searchvalue": kwargs.get("searchvalue"),
                "facilityid": kwargs.get("facilityid"),
            },
        )

    def get_orderable_dme(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orderable_dme"]["path"], practiceid=practiceid
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_orderable_imaging_orders(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orderable_imaging_orders"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_orderable_labs(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orderable_labs"]["path"], practiceid=practiceid
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_other_order_types(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["other_order_types"]["path"], practiceid=practiceid
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_patient_info(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["patient_info"]["path"], practiceid=practiceid
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_orderable_medication(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orderable_medication"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_dosage_quantity_units(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["dosage_quantity_units"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_dosage_frequencies(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["dosage_frequencies"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_procedures_and_surgeries(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["procedures_and_surgeries"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_referral_order_types(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["referral_order_types"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={"searchvalue": kwargs.get("searchvalue")})

    def get_orderable_vaccines(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["orderable_vaccines"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={"searchvalue": kwargs.get("searchvalue"), "cvx": kwargs.get("cvx")},
        )

    def get_vaccine_decline_reasons(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Encounter"]["vaccine_decline_reasons"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "showinactive": kwargs.get("showinactive"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )
