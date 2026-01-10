from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Observation(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_LDA_W(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["create_new_LDA_W"]["path"]
        )
        payload = self.build_payload(962, **kwargs)
        return self.post(url, data=payload)

    def create_new_vitals(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["create_new_vitals"]["path"]
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def get_activities_of_daily_living(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_activities_of_daily_living"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_core_characteristics(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_core_characteristics"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_labs(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_labs"]["path"], ID=ID
        )

        return self.get(url)

    def get_LDA_W(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_LDA_W"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_obstetric_details(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_specific_obstetric_details"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_periodontal(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_specific_periodontal"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_smart_data_elements(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_smart_data_elements"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_social_history(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_social_history"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_vatals(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["get_specific_vatals"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_activities_of_daily_living(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"][
                "search_activities_of_daily_living"
            ]["path"],
            **kwargs
        )

        return self.get(url)

    def search_core_characteristics(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_core_characteristics"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_labs(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_labs"]["path"],
            patient=kwargs.get("patientid"),
            category=kwargs.get("category")
        )
        params = {

        }
        return self.get(url,params)

    def search_LDA_W(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_LDA_W"]["path"], **kwargs
        )

        return self.get(url)

    def search_obstetric_details(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_obstetric_details"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_periodontal(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_periodontal"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_smart_data_elements(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_smart_data_elements"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_social_history(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_social_history"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_vitals(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["search_vitals"]["path"]
        )
        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "vital-signs",
                # "date": [
                #     "ge" + kwargs.get("start_date"),
                #     "le" + kwargs.get("end_date"),
                # ],
            },
        )

    def update_LDA_W(self, ID, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Observation"]["update_LDA_W"]["path"], ID=ID
        )
        payload = self.build_payload(974, **kwargs)
        return self.put(url, data=payload)


class DiagnosticReport(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_results(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DiagnosticReport"]["get_results"]["path"], ID=ID
        )

        return self.get(url)

    def search_results(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DiagnosticReport"]["search_results"]["path"],
            **kwargs
        )

        return self.get(url)


class ServiceRequest(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_community_resource(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"][
                "get_specific_community_resource"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_dental_procedure(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["get_dental_procedure"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_order_template(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["get_specific_order_template"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_orders(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["get_orders"]["path"], ID=ID
        )

        return self.get(url)

    def get_speciffic_refferal(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["get_speciffic_refferal"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_community_resource(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["search_community_resource"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_dental_procedure(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["search_dental_procedure"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_order_template(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["search_order_template"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_orders(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ServiceRequest"]["search_orders"]["path"],
            **kwargs
        )

        return self.get(url)


class BodyStructure(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_tooth(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["BodyStructure"]["get_specific_tooth"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_tooth(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["BodyStructure"]["search_tooth"]["path"],
            **kwargs
        )

        return self.get(url)


class Specimen(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_specimen(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Specimen"]["get_specific_specimen"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_specimen(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Specimen"]["search_specimen"]["path"], **kwargs
        )

        return self.get(url)


class ResearchStudy(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_research_study(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ResearchStudy"]["get_specific_research_study"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_research_study(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ResearchStudy"]["search_research_study"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class ResearchSubject(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_research_subject(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ResearchSubject"][
                "get_specific_research_subject"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_research_subject(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ResearchSubject"]["search_research_subject"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def create_new_research_subject(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["ResearchSubject"][
                "create_new_research_subject"
            ]["path"]
        )

        return self.get(url)


class DocumentReference(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_clinical_notes(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "create_new_clinical_notes"
            ]["path"]
        )
        payload = self.build_payload(1046, **kwargs)
        return self.post(url, data=payload)

    def create_new_document_information(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "create_new_document_information"
            ]["path"]
        )
        payload = self.build_payload(10050, **kwargs)
        return self.post(url, data=payload)

    def get_specific_clinical_notes(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "get_specific_clinical_notes"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_correspondences(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "get_specific_correspondences"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_document_information(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "get_specific_document_information"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_external_CCDA_document(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "get_external_CCDA_document"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_handoff(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["get_specific_handoff"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_HIS(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["get_specific_HIS"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_labs(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["get_labs"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_OASIS(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["get_specific_OASIS"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_radiology_results(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["get_radiology_results"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_clinical_notes(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_clinical_notes"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_correspondences(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_correspondences"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_document_information(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "search_document_information"
            ]["path"],
            **kwargs
        )

        return self.get(url)

    def search_external_CCDA_document(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "search_external_CCDA_document"
            ]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_external_CCDA_document(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "create_new_external_CCDA_document"
            ]["path"]
        )
        payload = self.build_payload(10135, **kwargs)
        return self.post(url, data=payload)

    def search_handoff(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_handoff"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_handoff(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["create_new_handoff"][
                "path"
            ]
        )
        payload = self.build_payload(10131, **kwargs)
        return self.post(url, data=payload)

    def search_HIS(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_HIS"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_HIS(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["create_new_HIS"]["path"]
        )

        return self.get(url)

    def search_labs(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_labs"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_labs(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["create_labs"]["path"]
        )
        payload = self.build_payload(10133, **kwargs)
        return self.post(url, data=payload)

    def search_OASIS(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_OASIS"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_OASIS(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["create_new_OASIS"]["path"]
        )
        payload = self.build_payload(10127, **kwargs)
        return self.post(url, data=payload)

    def search_radiology_results(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"]["search_radiology_results"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def update_document_information(self, ID, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["DocumentReference"][
                "update_document_information"
            ]["path"],
            ID=ID,
        )
        payload = self.build_payload(10051, **kwargs)
        return self.put(url, data=payload)


class Binary(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_clinical_notes(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_clinical_notes"]["path"], ID=ID
        )

        return self.get(url)

    def get_correspondences(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_correspondences"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_document_information(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_document_information"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_external_CCDA_document(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_external_CCDA_document"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_handoff(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_handoff"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_HIS(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_HIS"]["path"], ID=ID
        )

        return self.get(url)

    def get_labs(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_labs"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_OASIS(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_OASIS"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_practitioner_photo(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_specific_practitioner_photo"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_radiology_results(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Diagnostic"]["Binary"]["get_radiology_results"]["path"], ID=ID
        )

        return self.get(url)
