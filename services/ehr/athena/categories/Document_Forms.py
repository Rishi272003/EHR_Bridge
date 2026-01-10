from services.ehr.athena.client import AthenaHealthClient
from services.ehr.athena.urls import ATHENA_URLS

class DocumentsAndForms(AthenaHealthClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def add_patient_clinical_doc(self, practiceid, patientid, **kwargs):
        practiceid = practiceid if practiceid else self.practiceid

        url = self.build_url(
            ATHENA_URLS["Document_And_Forms"]["add_patient_clinical_doc"]["path"],
            practiceid=practiceid,
            patientid=patientid,
        )

        payload = self.build_payload(
            attachmentcontents=kwargs.get("attachmentcontents"),
            attachmenttype=kwargs.get("attachmenttype"),
            autoclose=kwargs.get("autoclose"),
            clinicalproviderid=kwargs.get("clinicalproviderid"),
            departmentid=kwargs.get("departmentid"),
            documentdata=kwargs.get("documentdata"),
            documentsubclass=kwargs.get("documentsubclass"),
            documenttypeid=kwargs.get("documenttypeid"),
            entityid=kwargs.get("entityid"),
            entitytype=kwargs.get("entitytype"),
            internalnote=kwargs.get("internalnote"),
            observationdate=kwargs.get("observationdate"),
            observationtime=kwargs.get("observationtime"),
            originalfilename=kwargs.get("originalfilename"),
            priority=kwargs.get("priority"),
            providerid=kwargs.get("providerid"),
        )
        return self.post(
            url, content_type="application/x-www-form-urlencoded", data=payload
        )
    def get_documents_by_id(self, patient_id, **kwargs):
        url = self.build_url(
            ATHENA_URLS["Documents"]["get_documents_by_id"]["path"],
            patientid=patient_id,
        )
        payload = {"departmentid": kwargs.get("departmentid")}
        return self.get(url, payload=payload)
