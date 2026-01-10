from ecaremd.ehr_integrations.ehr_services.athena.client import AthenaHealthClient
from ecaremd.ehr_integrations.ehr_services.athena.urls import ATHENA_URLS


class InsuranceFinancial(AthenaHealthClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_claim(self, practiceid, appointmentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_claim"]["path"],
            practiceid=practiceid,
            appointmentid=appointmentid,
        )

        payload = self.build_payload(
            claimcharges=kwargs.get("claimcharges"),
            supervisingproviderid=kwargs.get("supervisingproviderid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_insurance_package_details(self, practiceid, appointmentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["insurance_package_details"]["path"],
            practiceid=practiceid,
            appointmentid=appointmentid,
        )
        return self.get(
            url,
            params={
                "showcancelled": kwargs.get("showcancelled"),
                "showfullssn": kwargs.get("showfullssn"),
                "ignorerestrictions": kwargs.get("ignorerestrictions"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def update_insurance_package_details(self, practiceid, appointmentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_insurance_package_details"][
                "path"
            ],
            practiceid=practiceid,
            appointmentid=appointmentid,
        )

        payload = self.build_payload(
            primaryinsuranceid=kwargs.get("primaryinsuranceid"),
            secondaryinsuranceid=kwargs.get("secondaryinsuranceid"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_ccm_enrollment_status_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["ccm_enrollment_status_delta"][
                "path"
            ],
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

    def subscribe_to_ccm_enrollment_status(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"][
                "subscribe_to_ccm_enrollment_status"
            ]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            eventname=kwargs.get("eventname"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_ccm_enrollment_status_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"][
                "subscribe_to_ccm_enrollment_status_delta"
            ]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def unsubscribe_to_ccm_enrollment_status(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"][
                "unsubscribe_to_ccm_enrollment_status"
            ]["path"],
            practiceid=practiceid,
        )
        return self.delete(url, params={"eventname": kwargs.get("eventname")})

    def get_all_subscribe_to_ccm_enrollment_status(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"][
                "all_subscribe_to_ccm_enrollment_status"
            ]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def create_financial_claim(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_financial_claim"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            claimcharges=kwargs.get("claimcharges"),
            customfields=kwargs.get("customfields"),
            departmentid=kwargs.get("departmentid"),
            orderingproviderid=kwargs.get("orderingproviderid"),
            patientid=kwargs.get("patientid"),
            primarypatientinsuranceid=kwargs.get("primarypatientinsuranceid"),
            referralauthid=kwargs.get("referralauthid"),
            referringproviderid=kwargs.get("referringproviderid"),
            renderingproviderid=kwargs.get("renderingproviderid"),
            reserved19=kwargs.get("reserved19"),
            secondarypatientinsuranceid=kwargs.get("secondarypatientinsuranceid"),
            servicedate=kwargs.get("servicedate"),
            supervisingproviderid=kwargs.get("supervisingproviderid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_claim_details(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claim_details"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "createdstartdate": kwargs.get("createdstartdate"),
                "patientid": kwargs.get("patientid"),
                "procedurecodes": kwargs.get("procedurecodes"),
                "appointmentid": kwargs.get("appointmentid"),
                "serviceenddate": kwargs.get("serviceenddate"),
                "providerid": kwargs.get("providerid"),
                "departmentid": kwargs.get("departmentid"),
                "createdenddate": kwargs.get("createdenddate"),
                "servicestartdate": kwargs.get("servicestartdate"),
                "showcustomfields": kwargs.get("showcustomfields"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_individual_claim_details(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["individual_claim_details"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )
        return self.get(
            url, params={"showcustomfields": kwargs.get("showcustomfields")}
        )

    def update_individual_claim_details(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_individual_claim_details"][
                "path"
            ],
            practiceid=practiceid,
            claimid=claimid,
        )

        payload = self.build_payload(
            claimcharges=kwargs.get("claimcharges"),
            customfields=kwargs.get("customfields"),
            orderingproviderid=kwargs.get("orderingproviderid"),
            referralauthid=kwargs.get("referralauthid"),
            referringproviderid=kwargs.get("referringproviderid"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def upload_attachment(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["upload_attachment"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )

        payload = self.build_payload(
            attachmentcontents=kwargs.get("attachmentcontents"),
            attachmenttype=kwargs.get("attachmenttype"),
            filename=kwargs.get("filename"),
            note=kwargs.get("note"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_claim_attachments(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claim_attachments"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )
        return self.get(url, params={})

    def update_claim_attachment(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_claim_attachment"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )

        payload = self.build_payload(
            attachmenttype=kwargs.get("attachmenttype"),
            claimattachmentid=kwargs.get("claimattachmentid"),
            note=kwargs.get("note"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_claim_attachments(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_claim_attachments"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )
        return self.delete(
            url, params={"claimattachmentid": kwargs.get("claimattachmentid")}
        )

    def get_claim_notes(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claim_notes"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )
        return self.get(
            url,
            params={
                "showholdonly": kwargs.get("showholdonly"),
                "pendingflags": kwargs.get("pendingflags"),
            },
        )

    def update_claim_notes(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_claim_notes"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )

        payload = self.build_payload(
            claimnoteids=kwargs.get("claimnoteids"),
            overrideall=kwargs.get("overrideall"),
            undooverrides=kwargs.get("undooverrides"),
            username=kwargs.get("username"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_claim_transactions(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claim_transactions"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )
        return self.get(url, params={})

    def create_claim_notes(self, practiceid, claimid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_claim_notes"]["path"],
            practiceid=practiceid,
            claimid=claimid,
        )

        payload = self.build_payload(
            claimnote=kwargs.get("claimnote"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_attachment_type_class(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["attachment_type_class"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_claims_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claims_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "leaveunprocessed": kwargs.get("leaveunprocessed"),
                "departmentid": kwargs.get("departmentid"),
                "showprocessedenddatetime": kwargs.get("showprocessedenddatetime"),
                "patientid": kwargs.get("patientid"),
                "showprocessedstartdatetime": kwargs.get("showprocessedstartdatetime"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def subscribe_to_claims(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["subscribe_to_claims"]["path"],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            departmentids=kwargs.get("departmentids"),
            eventname=kwargs.get("eventname"),
            showadditionalevents=kwargs.get("showadditionalevents"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_subscribe_to_claims_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["subscribe_to_claims_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"showadditionalevents": kwargs.get("showadditionalevents")}
        )

    def unsubscribe_to_claims(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["unsubscribe_to_claims"]["path"],
            practiceid=practiceid,
        )
        return self.delete(
            url,
            params={
                "eventname": kwargs.get("eventname"),
                "showadditionalevents": kwargs.get("showadditionalevents"),
            },
        )

    def get_claims_event_delta(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claims_event_delta"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"showadditionalevents": kwargs.get("showadditionalevents")}
        )

    def get_custom_fields(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["custom_fields"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_non_ccp_credit_card_methods(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["non_ccp_credit_card_methods"][
                "path"
            ],
            practiceid=practiceid,
        )
        return self.get(
            url, params={"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        )

    def get_fee_schedule_procedure(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["fee_schedule_procedure"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "insurancepackageid": kwargs.get("insurancepackageid"),
                "servicedate": kwargs.get("servicedate"),
                "departmentid": kwargs.get("departmentid"),
                "procedurecode": kwargs.get("procedurecode"),
            },
        )

    def create_fee_schedule_procedure(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_fee_schedule_procedure"][
                "path"
            ],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            amount=kwargs.get("amount"),
            feescheduleid=kwargs.get("feescheduleid"),
            procedurecode=kwargs.get("procedurecode"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_fee_schedule_procedure(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_fee_schedule_procedure"][
                "path"
            ],
            practiceid=practiceid,
        )
        return self.delete(
            url,
            params={
                "feescheduleid": kwargs.get("feescheduleid"),
                "procedurecode": kwargs.get("procedurecode"),
            },
        )

    def record_inventory_consumption(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_inventory_consumption"][
                "path"
            ],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            datecreated=kwargs.get("datecreated"),
            inventory=kwargs.get("inventory"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_standard_insurance_packages(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["standard_insurance_packages"][
                "path"
            ],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "insurancezip": kwargs.get("insurancezip"),
                "insuranceaddress": kwargs.get("insuranceaddress"),
                "insuranceplanname": kwargs.get("insuranceplanname"),
                "memberid": kwargs.get("memberid"),
                "insurancestate": kwargs.get("insurancestate"),
                "insurancecity": kwargs.get("insurancecity"),
                "producttypeid": kwargs.get("producttypeid"),
                "insurancephone": kwargs.get("insurancephone"),
                "stateofcoverage": kwargs.get("stateofcoverage"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def get_case_policies(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["case_policies"]["path"],
            practiceid=practiceid,
        )
        return self.get(
            url,
            params={
                "insurancezip": kwargs.get("insurancezip"),
                "insuranceaddress": kwargs.get("insuranceaddress"),
                "insuranceplanname": kwargs.get("insuranceplanname"),
                "insurancestate": kwargs.get("insurancestate"),
                "insurancecity": kwargs.get("insurancecity"),
                "casepolicytypeid": kwargs.get("casepolicytypeid"),
                "insurancephone": kwargs.get("insurancephone"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def create_local_insurance_package(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_local_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
        )

        payload = self.build_payload(
            address=kwargs.get("address"),
            address2=kwargs.get("address2"),
            city=kwargs.get("city"),
            claimformat=kwargs.get("claimformat"),
            contactname=kwargs.get("contactname"),
            countryid=kwargs.get("countryid"),
            effectivedate=kwargs.get("effectivedate"),
            expirationdate=kwargs.get("expirationdate"),
            fax=kwargs.get("fax"),
            frequency=kwargs.get("frequency"),
            invoicecoversheet=kwargs.get("invoicecoversheet"),
            invoiceemailaddress=kwargs.get("invoiceemailaddress"),
            invoiceoverduedays=kwargs.get("invoiceoverduedays"),
            invoicepurchaseordernumber=kwargs.get("invoicepurchaseordernumber"),
            invoicesendviaemail=kwargs.get("invoicesendviaemail"),
            invoiceshowadjustments=kwargs.get("invoiceshowadjustments"),
            invoicesubmitcorrected=kwargs.get("invoicesubmitcorrected"),
            invoicesubmitoverdue=kwargs.get("invoicesubmitoverdue"),
            name=kwargs.get("name"),
            note=kwargs.get("note"),
            phone=kwargs.get("phone"),
            state=kwargs.get("state"),
            switchoverdate=kwargs.get("switchoverdate"),
            zip=kwargs.get("zip"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_local_insurance_package(self, practiceid, insurancepackageid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_local_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
            insurancepackageid=insurancepackageid,
        )

        payload = self.build_payload(
            address=kwargs.get("address"),
            address2=kwargs.get("address2"),
            city=kwargs.get("city"),
            claimformat=kwargs.get("claimformat"),
            contactname=kwargs.get("contactname"),
            countryid=kwargs.get("countryid"),
            effectivedate=kwargs.get("effectivedate"),
            expirationdate=kwargs.get("expirationdate"),
            fax=kwargs.get("fax"),
            frequency=kwargs.get("frequency"),
            invoicecoversheet=kwargs.get("invoicecoversheet"),
            invoiceemailaddress=kwargs.get("invoiceemailaddress"),
            invoiceoverduedays=kwargs.get("invoiceoverduedays"),
            invoicepurchaseordernumber=kwargs.get("invoicepurchaseordernumber"),
            invoicesendviaemail=kwargs.get("invoicesendviaemail"),
            invoiceshowadjustments=kwargs.get("invoiceshowadjustments"),
            invoicesubmitcorrected=kwargs.get("invoicesubmitcorrected"),
            invoicesubmitoverdue=kwargs.get("invoicesubmitoverdue"),
            name=kwargs.get("name"),
            note=kwargs.get("note"),
            phone=kwargs.get("phone"),
            state=kwargs.get("state"),
            switchoverdate=kwargs.get("switchoverdate"),
            zip=kwargs.get("zip"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def disable_local_insurance_package(self, practiceid, insurancepackageid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["disable_local_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
            insurancepackageid=insurancepackageid,
        )

        payload = self.build_payload(
            expirationdate=kwargs.get("expirationdate"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def reenable_local_insurance_package(
        self, practiceid, insurancepackageid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["reenable_local_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
            insurancepackageid=insurancepackageid,
        )

        payload = self.build_payload(
            expirationdate=kwargs.get("expirationdate"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_one_year_contractterms(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["one_year_contractterms"]["path"],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def get_single_appointment_contract_terms(self, practiceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["single_appointment_contract_terms"][
                "path"
            ],
            practiceid=practiceid,
        )
        return self.get(url, params={})

    def record_adjusting_charges(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_adjusting_charges"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            charges=kwargs.get("charges"),
            patientid=kwargs.get("patientid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def changeage_in_gownership(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["changeage_in_gownership"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            action=kwargs.get("action"),
            claims=kwargs.get("claims"),
            patientid=kwargs.get("patientid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def claim_collections(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["claim_collections"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            claimids=kwargs.get("claimids"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def patient_enrollment(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["patient_enrollment"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            action=kwargs.get("action"),
            patients=kwargs.get("patients"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def record_patient_payment(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_patient_payment"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            appointmentid=kwargs.get("appointmentid"),
            bankdepositdate=kwargs.get("bankdepositdate"),
            cardnumberlast4=kwargs.get("cardnumberlast4"),
            checknumber=kwargs.get("checknumber"),
            claimpayment=kwargs.get("claimpayment"),
            copayamount=kwargs.get("copayamount"),
            departmentid=kwargs.get("departmentid"),
            externalrefid=kwargs.get("externalrefid"),
            movetounappliedifoverpay=kwargs.get("movetounappliedifoverpay"),
            otheramount=kwargs.get("otheramount"),
            patientid=kwargs.get("patientid"),
            paymentmethod=kwargs.get("paymentmethod"),
            postdate=kwargs.get("postdate"),
            todayservice=kwargs.get("todayservice"),
            vendorterminalid=kwargs.get("vendorterminalid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def record_patient_refund(self, practiceid, vendorcode, patientpaymentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_patient_refund"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
            patientpaymentid=patientpaymentid,
        )

        payload = self.build_payload(
            bankdepositdate=kwargs.get("bankdepositdate"),
            departmentid=kwargs.get("departmentid"),
            externalrefid=kwargs.get("externalrefid"),
            fullrefund=kwargs.get("fullrefund"),
            ispaymentsettled=kwargs.get("ispaymentsettled"),
            patientid=kwargs.get("patientid"),
            paymentmethod=kwargs.get("paymentmethod"),
            postdate=kwargs.get("postdate"),
            vendorterminalid=kwargs.get("vendorterminalid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def record_patient_statements(self, practiceid, vendorcode, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_patient_statements"]["path"],
            practiceid=practiceid,
            vendorcode=vendorcode,
        )

        payload = self.build_payload(
            data=kwargs.get("data"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_closed(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["patient_closed"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "procedurecodes": kwargs.get("procedurecodes"),
                "departmentid": kwargs.get("departmentid"),
            },
        )

    def get_patient_outstanding(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["patient_outstanding"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "procedurecodes": kwargs.get("procedurecodes"),
                "departmentid": kwargs.get("departmentid"),
            },
        )

    def enter_patient_payment_information(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["enter_patient_payment_information"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            amount=kwargs.get("amount"),
            appointmentid=kwargs.get("appointmentid"),
            billingaddress=kwargs.get("billingaddress"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimpayment=kwargs.get("claimpayment"),
            copayamount=kwargs.get("copayamount"),
            departmentid=kwargs.get("departmentid"),
            ecommercemode=kwargs.get("ecommercemode"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            nameoncard=kwargs.get("nameoncard"),
            otheramount=kwargs.get("otheramount"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_one_year_contract(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["one_year_contract"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def submit_auth_one_year_contract(
        self, practiceid, patientid, appointmentid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["submit_auth_one_year_contract"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            appointmentid=appointmentid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            billingaddress=kwargs.get("billingaddress"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimpayment=kwargs.get("claimpayment"),
            departmentid=kwargs.get("departmentid"),
            ecommercemode=kwargs.get("ecommercemode"),
            email=kwargs.get("email"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            maxamount=kwargs.get("maxamount"),
            nameoncard=kwargs.get("nameoncard"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_view_auth_one_year_contract(
        self, practiceid, patientid, appointmentid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["view_auth_one_year_contract"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            appointmentid=appointmentid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def email_one_year_contract_agreement(
        self, practiceid, patientid, contractid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["email_one_year_contract_agreement"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            contractid=contractid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            email=kwargs.get("email"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_payment_plan(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_payment_plan"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            appointmentid=kwargs.get("appointmentid"),
            billingaddress=kwargs.get("billingaddress"),
            billingmethod=kwargs.get("billingmethod"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimids=kwargs.get("claimids"),
            cycleamount=kwargs.get("cycleamount"),
            departmentid=kwargs.get("departmentid"),
            downpaymentamount=kwargs.get("downpaymentamount"),
            ecommercemode=kwargs.get("ecommercemode"),
            email=kwargs.get("email"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            frequency=kwargs.get("frequency"),
            nameoncard=kwargs.get("nameoncard"),
            paymentplanname=kwargs.get("paymentplanname"),
            percentage=kwargs.get("percentage"),
            startdate=kwargs.get("startdate"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_view_payment_plan(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["view_payment_plan"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "departmentid": kwargs.get("departmentid"),
                "paymentplanids": kwargs.get("paymentplanids"),
            },
        )

    def get_single_appointment(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["single_appointment"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def enter_appointment(self, practiceid, patientid, appointmentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["enter_appointment"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            appointmentid=appointmentid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            billingaddress=kwargs.get("billingaddress"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimpayment=kwargs.get("claimpayment"),
            departmentid=kwargs.get("departmentid"),
            ecommercemode=kwargs.get("ecommercemode"),
            email=kwargs.get("email"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            maxamount=kwargs.get("maxamount"),
            nameoncard=kwargs.get("nameoncard"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def upload_credit_card_details(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["upload_credit_card_details"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            appointmentid=kwargs.get("appointmentid"),
            billingaddress=kwargs.get("billingaddress"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimpayment=kwargs.get("claimpayment"),
            departmentid=kwargs.get("departmentid"),
            ecommercemode=kwargs.get("ecommercemode"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            nameoncard=kwargs.get("nameoncard"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_credit_card_info(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["credit_card_info"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def create_specific_credit_card(
        self, practiceid, patientid, storedcardid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_specific_credit_card"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            storedcardid=storedcardid,
        )

        payload = self.build_payload(
            accountnumber=kwargs.get("accountnumber"),
            allowduplicatepayments=kwargs.get("allowduplicatepayments"),
            amount=kwargs.get("amount"),
            appointmentid=kwargs.get("appointmentid"),
            billingaddress=kwargs.get("billingaddress"),
            billingzip=kwargs.get("billingzip"),
            cardsecuritycode=kwargs.get("cardsecuritycode"),
            claimpayment=kwargs.get("claimpayment"),
            copayamount=kwargs.get("copayamount"),
            departmentid=kwargs.get("departmentid"),
            ecommercemode=kwargs.get("ecommercemode"),
            expirationmonthmm=kwargs.get("expirationmonthmm"),
            expirationyearyyyy=kwargs.get("expirationyearyyyy"),
            nameoncard=kwargs.get("nameoncard"),
            otheramount=kwargs.get("otheramount"),
            todayservice=kwargs.get("todayservice"),
            trackdata=kwargs.get("trackdata"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def update_specific_credit_card(
        self, practiceid, patientid, storedcardid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_specific_credit_card"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            storedcardid=storedcardid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            preferredcard=kwargs.get("preferredcard"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_specific_credit_card(
        self, practiceid, patientid, storedcardid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_specific_credit_card"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            storedcardid=storedcardid,
        )
        return self.delete(url, params={"departmentid": kwargs.get("departmentid")})

    def create_insurance_package(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_insurance_package"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            expirationdate=kwargs.get("expirationdate"),
            insuranceidnumber=kwargs.get("insuranceidnumber"),
            insurancepackageid=kwargs.get("insurancepackageid"),
            insurancephone=kwargs.get("insurancephone"),
            insurancepolicyholder=kwargs.get("insurancepolicyholder"),
            insurancepolicyholderaddress1=kwargs.get("insurancepolicyholderaddress1"),
            insurancepolicyholderaddress2=kwargs.get("insurancepolicyholderaddress2"),
            insurancepolicyholdercity=kwargs.get("insurancepolicyholdercity"),
            insurancepolicyholdercountrycode=kwargs.get(
                "insurancepolicyholdercountrycode"
            ),
            insurancepolicyholdercountryiso3166=kwargs.get(
                "insurancepolicyholdercountryiso3166"
            ),
            insurancepolicyholderdob=kwargs.get("insurancepolicyholderdob"),
            insurancepolicyholderfirstname=kwargs.get("insurancepolicyholderfirstname"),
            insurancepolicyholderlastname=kwargs.get("insurancepolicyholderlastname"),
            insurancepolicyholdermiddlename=kwargs.get(
                "insurancepolicyholdermiddlename"
            ),
            insurancepolicyholdersex=kwargs.get("insurancepolicyholdersex"),
            insurancepolicyholderssn=kwargs.get("insurancepolicyholderssn"),
            insurancepolicyholderstate=kwargs.get("insurancepolicyholderstate"),
            insurancepolicyholdersuffix=kwargs.get("insurancepolicyholdersuffix"),
            insurancepolicyholderzip=kwargs.get("insurancepolicyholderzip"),
            insuredentitytypeid=kwargs.get("insuredentitytypeid"),
            issuedate=kwargs.get("issuedate"),
            policynumber=kwargs.get("policynumber"),
            relationshiptoinsuredid=kwargs.get("relationshiptoinsuredid"),
            sequencenumber=kwargs.get("sequencenumber"),
            updateappointments=kwargs.get("updateappointments"),
            validateinsuranceidnumber=kwargs.get("validateinsuranceidnumber"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_patient_insurance(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["patient_insurance"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "showcancelled": kwargs.get("showcancelled"),
                "showfullssn": kwargs.get("showfullssn"),
                "departmentid": kwargs.get("departmentid"),
                "ignorerestrictions": kwargs.get("ignorerestrictions"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def update_patient_insurance(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_patient_insurance"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            expirationdate=kwargs.get("expirationdate"),
            insuranceidnumber=kwargs.get("insuranceidnumber"),
            insurancephone=kwargs.get("insurancephone"),
            insurancepolicyholder=kwargs.get("insurancepolicyholder"),
            insurancepolicyholderaddress1=kwargs.get("insurancepolicyholderaddress1"),
            insurancepolicyholderaddress2=kwargs.get("insurancepolicyholderaddress2"),
            insurancepolicyholdercity=kwargs.get("insurancepolicyholdercity"),
            insurancepolicyholdercountrycode=kwargs.get(
                "insurancepolicyholdercountrycode"
            ),
            insurancepolicyholdercountryiso3166=kwargs.get(
                "insurancepolicyholdercountryiso3166"
            ),
            insurancepolicyholderdob=kwargs.get("insurancepolicyholderdob"),
            insurancepolicyholderfirstname=kwargs.get("insurancepolicyholderfirstname"),
            insurancepolicyholderlastname=kwargs.get("insurancepolicyholderlastname"),
            insurancepolicyholdermiddlename=kwargs.get(
                "insurancepolicyholdermiddlename"
            ),
            insurancepolicyholdersex=kwargs.get("insurancepolicyholdersex"),
            insurancepolicyholderssn=kwargs.get("insurancepolicyholderssn"),
            insurancepolicyholderstate=kwargs.get("insurancepolicyholderstate"),
            insurancepolicyholdersuffix=kwargs.get("insurancepolicyholdersuffix"),
            insurancepolicyholderzip=kwargs.get("insurancepolicyholderzip"),
            insuredentitytypeid=kwargs.get("insuredentitytypeid"),
            issuedate=kwargs.get("issuedate"),
            newsequencenumber=kwargs.get("newsequencenumber"),
            policynumber=kwargs.get("policynumber"),
            relationshiptoinsuredid=kwargs.get("relationshiptoinsuredid"),
            sequencenumber=kwargs.get("sequencenumber"),
            validateinsuranceidnumber=kwargs.get("validateinsuranceidnumber"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_insurance_package(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_insurance_package"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.delete(
            url,
            params={
                "sequencenumber": kwargs.get("sequencenumber"),
                "departmentid": kwargs.get("departmentid"),
                "cancellationnote": kwargs.get("cancellationnote"),
            },
        )

    def update_specific_insurance_package(
        self, practiceid, patientid, insuranceid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_specific_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            adjusterfax=kwargs.get("adjusterfax"),
            adjusterfirstname=kwargs.get("adjusterfirstname"),
            adjusterlastname=kwargs.get("adjusterlastname"),
            adjusterphone=kwargs.get("adjusterphone"),
            anotherpartyresponsible=kwargs.get("anotherpartyresponsible"),
            autoaccidentstate=kwargs.get("autoaccidentstate"),
            caseinjurydate=kwargs.get("caseinjurydate"),
            departmentid=kwargs.get("departmentid"),
            descriptionofinjury=kwargs.get("descriptionofinjury"),
            expirationdate=kwargs.get("expirationdate"),
            icd10codes=kwargs.get("icd10codes"),
            icd9codes=kwargs.get("icd9codes"),
            injuredbodypart=kwargs.get("injuredbodypart"),
            insuranceclaimnumber=kwargs.get("insuranceclaimnumber"),
            insuranceidnumber=kwargs.get("insuranceidnumber"),
            insurancephone=kwargs.get("insurancephone"),
            insurancepolicyholder=kwargs.get("insurancepolicyholder"),
            insurancepolicyholderaddress1=kwargs.get("insurancepolicyholderaddress1"),
            insurancepolicyholderaddress2=kwargs.get("insurancepolicyholderaddress2"),
            insurancepolicyholdercity=kwargs.get("insurancepolicyholdercity"),
            insurancepolicyholdercountrycode=kwargs.get(
                "insurancepolicyholdercountrycode"
            ),
            insurancepolicyholdercountryiso3166=kwargs.get(
                "insurancepolicyholdercountryiso3166"
            ),
            insurancepolicyholderdob=kwargs.get("insurancepolicyholderdob"),
            insurancepolicyholderfirstname=kwargs.get("insurancepolicyholderfirstname"),
            insurancepolicyholderlastname=kwargs.get("insurancepolicyholderlastname"),
            insurancepolicyholdermiddlename=kwargs.get(
                "insurancepolicyholdermiddlename"
            ),
            insurancepolicyholdersex=kwargs.get("insurancepolicyholdersex"),
            insurancepolicyholderssn=kwargs.get("insurancepolicyholderssn"),
            insurancepolicyholderstate=kwargs.get("insurancepolicyholderstate"),
            insurancepolicyholdersuffix=kwargs.get("insurancepolicyholdersuffix"),
            insurancepolicyholderzip=kwargs.get("insurancepolicyholderzip"),
            insuredentitytypeid=kwargs.get("insuredentitytypeid"),
            issuedate=kwargs.get("issuedate"),
            newsequencenumber=kwargs.get("newsequencenumber"),
            policynumber=kwargs.get("policynumber"),
            realtedtoautoaccident=kwargs.get("realtedtoautoaccident"),
            relatedtoemployment=kwargs.get("relatedtoemployment"),
            relatedtootheraccident=kwargs.get("relatedtootheraccident"),
            relationshiptoinsuredid=kwargs.get("relationshiptoinsuredid"),
            repricername=kwargs.get("repricername"),
            repricerphone=kwargs.get("repricerphone"),
            stateofreportedinjury=kwargs.get("stateofreportedinjury"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def delete_specific_insurance_package(
        self, practiceid, patientid, insuranceid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_specific_insurance_package"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )
        return self.delete(
            url, params={"cancellationnote": kwargs.get("cancellationnote")}
        )

    def get_insurance_details(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["insurance_details"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )
        return self.get(
            url,
            params={
                "servicetypecode": kwargs.get("servicetypecode"),
                "dateofservice": kwargs.get("dateofservice"),
            },
        )

    def create_insurance_details(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_insurance_details"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            dateofservice=kwargs.get("dateofservice"),
            servicetypecode=kwargs.get("servicetypecode"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_ccm_enrollment_status(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["ccm_enrollment_status"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def update_ccm_enrollment_status(
        self, practiceid, patientid, insuranceid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_ccm_enrollment_status"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            effectivedate=kwargs.get("effectivedate"),
            expirationdate=kwargs.get("expirationdate"),
            status=kwargs.get("status"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def upload_insurance_card_image(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["upload_insurance_card_image"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            image=kwargs.get("image"),
        )
        return self.post(url, content_type="multipart/form-data", data=payload)

    def get_insurance_card_image(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["insurance_card_image"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )
        return self.get(url, params={"jpegoutput": kwargs.get("jpegoutput")})

    def update_insurance_card_image(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_insurance_card_image"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            departmentid=kwargs.get("departmentid"),
            image=kwargs.get("image"),
        )
        return self.put(url, content_type="multipart/form-data", data=payload)

    def delete_insurance_card_image(self, practiceid, patientid, insuranceid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_insurance_card_image"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )
        return self.delete(url, params={})

    def reactive_specific_insurance_package(
        self, practiceid, patientid, insuranceid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"][
                "reactive_specific_insurance_package"
            ]["path"],
            practiceid=practiceid,
            patientid=patientid,
            insuranceid=insuranceid,
        )

        payload = self.build_payload(
            expirationdate=kwargs.get("expirationdate"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def create_specific_case_policy(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["create_specific_case_policy"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            adjusterfax=kwargs.get("adjusterfax"),
            adjusterfirstname=kwargs.get("adjusterfirstname"),
            adjusterlastname=kwargs.get("adjusterlastname"),
            adjusterphone=kwargs.get("adjusterphone"),
            anotherpartyresponsible=kwargs.get("anotherpartyresponsible"),
            autoaccidentstate=kwargs.get("autoaccidentstate"),
            caseinjurydate=kwargs.get("caseinjurydate"),
            departmentid=kwargs.get("departmentid"),
            descriptionofinjury=kwargs.get("descriptionofinjury"),
            expirationdate=kwargs.get("expirationdate"),
            icd10codes=kwargs.get("icd10codes"),
            icd9codes=kwargs.get("icd9codes"),
            injuredbodypart=kwargs.get("injuredbodypart"),
            insuranceclaimnumber=kwargs.get("insuranceclaimnumber"),
            insuranceidnumber=kwargs.get("insuranceidnumber"),
            insurancepackageid=kwargs.get("insurancepackageid"),
            insurancephone=kwargs.get("insurancephone"),
            insurancepolicyholder=kwargs.get("insurancepolicyholder"),
            insurancepolicyholderaddress1=kwargs.get("insurancepolicyholderaddress1"),
            insurancepolicyholderaddress2=kwargs.get("insurancepolicyholderaddress2"),
            insurancepolicyholdercity=kwargs.get("insurancepolicyholdercity"),
            insurancepolicyholdercountrycode=kwargs.get(
                "insurancepolicyholdercountrycode"
            ),
            insurancepolicyholdercountryiso3166=kwargs.get(
                "insurancepolicyholdercountryiso3166"
            ),
            insurancepolicyholderdob=kwargs.get("insurancepolicyholderdob"),
            insurancepolicyholderfirstname=kwargs.get("insurancepolicyholderfirstname"),
            insurancepolicyholderlastname=kwargs.get("insurancepolicyholderlastname"),
            insurancepolicyholdermiddlename=kwargs.get(
                "insurancepolicyholdermiddlename"
            ),
            insurancepolicyholdersex=kwargs.get("insurancepolicyholdersex"),
            insurancepolicyholderssn=kwargs.get("insurancepolicyholderssn"),
            insurancepolicyholderstate=kwargs.get("insurancepolicyholderstate"),
            insurancepolicyholdersuffix=kwargs.get("insurancepolicyholdersuffix"),
            insurancepolicyholderzip=kwargs.get("insurancepolicyholderzip"),
            insuredentitytypeid=kwargs.get("insuredentitytypeid"),
            issuedate=kwargs.get("issuedate"),
            policynumber=kwargs.get("policynumber"),
            realtedtoautoaccident=kwargs.get("realtedtoautoaccident"),
            relatedtoemployment=kwargs.get("relatedtoemployment"),
            relatedtootheraccident=kwargs.get("relatedtootheraccident"),
            relationshiptoinsuredid=kwargs.get("relationshiptoinsuredid"),
            repricername=kwargs.get("repricername"),
            repricerphone=kwargs.get("repricerphone"),
            stateofreportedinjury=kwargs.get("stateofreportedinjury"),
            updateappointments=kwargs.get("updateappointments"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def add_prescription_card_image(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["add_prescription_card_image"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            image=kwargs.get("image"),
        )
        return self.post(url, content_type="multipart/form-data", data=payload)

    def get_prescription_card_image(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["prescription_card_image"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"jpegoutput": kwargs.get("jpegoutput")})

    def delete_prescription_card_image(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["delete_prescription_card_image"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.delete(url, params={})

    def get_payment_receipts(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["payment_receipts"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(url, params={"departmentid": kwargs.get("departmentid")})

    def get_e_payment_receipts(self, practiceid, patientid, epaymentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["e_payment_receipts"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )
        return self.get(url, params={"termsasjson": kwargs.get("termsasjson")})

    def get_e_payment_receipts_details(
        self, practiceid, patientid, epaymentid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["e_payment_receipts_details"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )
        return self.get(url, params={"termsasjson": kwargs.get("termsasjson")})

    def send_payment_receipts(self, practiceid, patientid, epaymentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["send_payment_receipts"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )

        payload = self.build_payload(
            email=kwargs.get("email"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_signed_e_payment_receipts(
        self, practiceid, patientid, epaymentid, **kwargs
    ):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["signed_e_payment_receipts"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )
        return self.get(url, params={})

    def submit_auth_payment_receipts(self, practiceid, patientid, epaymentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["submit_auth_payment_receipts"][
                "path"
            ],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )

        payload = self.build_payload(
            attachmentcontents=kwargs.get("attachmentcontents"),
        )
        return self.post(url, content_type="multipart/form-data", data=payload)

    def record_payment_details(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["record_payment_details"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            appointmentid=kwargs.get("appointmentid"),
            cardnumberlast4=kwargs.get("cardnumberlast4"),
            checknumber=kwargs.get("checknumber"),
            claimpayment=kwargs.get("claimpayment"),
            copayamount=kwargs.get("copayamount"),
            departmentid=kwargs.get("departmentid"),
            otheramount=kwargs.get("otheramount"),
            paymentmethod=kwargs.get("paymentmethod"),
            postdate=kwargs.get("postdate"),
            todayservice=kwargs.get("todayservice"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def submit_referral_auths(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["submit_referral_auths"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            appointmentids=kwargs.get("appointmentids"),
            departmentid=kwargs.get("departmentid"),
            expirationdate=kwargs.get("expirationdate"),
            icd10diagnosiscodes=kwargs.get("icd10diagnosiscodes"),
            icd9diagnosiscodes=kwargs.get("icd9diagnosiscodes"),
            insuranceid=kwargs.get("insuranceid"),
            noreferralrequired=kwargs.get("noreferralrequired"),
            note=kwargs.get("note"),
            notestoprovider=kwargs.get("notestoprovider"),
            procedurecodes=kwargs.get("procedurecodes"),
            referralauthnumber=kwargs.get("referralauthnumber"),
            referringproviderid=kwargs.get("referringproviderid"),
            specifiesvisits=kwargs.get("specifiesvisits"),
            startdate=kwargs.get("startdate"),
            visitsapproved=kwargs.get("visitsapproved"),
            visitsleft=kwargs.get("visitsleft"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def get_referral_auths(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["referral_auths"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )
        return self.get(
            url,
            params={
                "insuranceid": kwargs.get("insuranceid"),
                "showexpired": kwargs.get("showexpired"),
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
            },
        )

    def update_referral_auths(self, practiceid, patientid, referralauthid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["update_referral_auths"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            referralauthid=referralauthid,
        )

        payload = self.build_payload(
            appointmentids=kwargs.get("appointmentids"),
            departmentid=kwargs.get("departmentid"),
            expirationdate=kwargs.get("expirationdate"),
            icd10diagnosiscodes=kwargs.get("icd10diagnosiscodes"),
            icd9diagnosiscodes=kwargs.get("icd9diagnosiscodes"),
            insuranceid=kwargs.get("insuranceid"),
            noreferralrequired=kwargs.get("noreferralrequired"),
            notes=kwargs.get("notes"),
            notestoprovider=kwargs.get("notestoprovider"),
            procedurecodes=kwargs.get("procedurecodes"),
            referralauthnumber=kwargs.get("referralauthnumber"),
            referringproviderid=kwargs.get("referringproviderid"),
            startdate=kwargs.get("startdate"),
            visits=kwargs.get("visits"),
            visitsapproved=kwargs.get("visitsapproved"),
            visitsleft=kwargs.get("visitsleft"),
        )
        return self.put(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )

    def void_payment(self, practiceid, patientid, epaymentid, **kwargs):
        practiceid = practiceid if practiceid else self.practice_id

        url = self.build_url(
            ATHENA_URLS["Insurance_And_Financial"]["void_payment"]["path"],
            practiceid=practiceid,
            patientid=patientid,
            epaymentid=epaymentid,
        )

        payload = self.build_payload()
        return self.post(url, content_type="", data=payload)
