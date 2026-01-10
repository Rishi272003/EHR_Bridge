from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class AllergyIntolerance(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_allergy_intolerance(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["AllergyIntolerance"][
                "create_new_allergy_intolerance"
            ]["path"]
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def get_specific_allergy_intolerance(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["AllergyIntolerance"][
                "get_specific_allergy_intolerance"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_allergy_intolerance(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["AllergyIntolerance"]["search_allergy_intolerance"][
                "path"
            ],
            **kwargs
        )
        return self.get(url, params=kwargs)


class Condition(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["create_new_problems"]["path"]
        )
        payload = self.build_payload(**kwargs)
        return self.post(url, data=payload)

    def get_specific_care_plan_problem(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_care_plan_problem"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_dental_finding(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_dental_finding"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_encounter_diagnosis(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_encounter_diagnosis"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_genomics(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_genomics"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_health_concern(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_health_concern"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_infection(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_infection"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_problems(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_problems"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_reason_for_visit(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["get_specific_reason_for_visit"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_care_plan_problem(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_care_plan_problem"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_dental_finding(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_dental_finding"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_encounter_diagnosis(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_encounter_diagnosis"]["path"]
        )

        return self.get(
            url,
            params={
                "patient": kwargs.get("patientid"),
                "category": "encounter-diagnosis",
            },
        )

    def search_genomics(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_genomics"]["path"], **kwargs
        )

        return self.get(url)

    def search_health_concern(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_health_concern"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_infection(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_infection"]["path"], **kwargs
        )

        return self.get(url)

    def create_new_infection(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["create_new_infection"]["path"]
        )
        payload = self.build_payload(10141, **kwargs)
        return self.post(url, data=payload)

    def search_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_problems"]["path"],
            patient=kwargs.get("patientid"),
            category="problem-list-item",
        )
        return self.get(url)

    def search_reason_for_visit(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Condition"]["search_reason_for_visit"]["path"],
            **kwargs
        )

        return self.get(url)


class Procedure(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_orders(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["get_specific_orders"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_surgeries(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["get_specific_surgeries"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_surgical_history(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["get_specific_surgical_history"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_orders(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["search_orders"]["path"],
        )

        return self.get(url, params={"patient": kwargs.get("patientid")})

    def search_surgeries(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["search_surgeries"]["path"], **kwargs
        )

        return self.get(url)

    def search_surgical_history(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Procedure"]["search_surgical_history"]["path"],
            **kwargs
        )

        return self.get(url)


class FamilyMemberHistory(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_family_member_history(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["FamilyMemberHistory"][
                "get_specific_family_member_history"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_family_member_history(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["FamilyMemberHistory"][
                "search_family_member_history"
            ]["path"],
            **kwargs
        )

        return self.get(url)

    def create_family_member_history(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["FamilyMemberHistory"][
                "create_family_member_history"
            ]["path"]
        )
        payload = self.build_payload(10159, **kwargs)
        return self.post(url, data=payload)


class CarePlan(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_dental(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_dental"]["path"], ID=ID
        )

        return self.get(url)

    def get_encounter_level(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_encounter_level"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_inpatient_pathway(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_inpatient_pathway"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_inpatient(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_inpatient"]["path"], ID=ID
        )

        return self.get(url)

    def get_longitudinal(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_longitudinal"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_oncology(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_oncology"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_outpatient(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_outpatient"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_questionnaires_due(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["get_specific_questionnaires_due"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_dental(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_dental"]["path"], **kwargs
        )

        return self.get(url)

    def search_encounter_level(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_encounter_level"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_inpatient_pathway(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_inpatient_pathway"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_inpatient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_inpatient"]["path"], **kwargs
        )

        return self.get(url)

    def search_longitudinal(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_longitudinal"]["path"], **kwargs
        )

        return self.get(url)

    def search_oncology(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_oncology"]["path"], **kwargs
        )

        return self.get(url)

    def search_outpatient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_outpatient"]["path"], **kwargs
        )

        return self.get(url)

    def search_questionnaires_due(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CarePlan"]["search_questionnaires_due"]["path"],
            **kwargs
        )

        return self.get(url)


class Goal(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_care_plan(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["get_specific_care_plan"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_pathway_step(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["get_specific_pathway_step"]["path"], ID=ID
        )

        return self.get(url)

    def get_specific_patient(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["get_specific_patient"]["path"], ID=ID
        )

        return self.get(url)

    def search_care_plan(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["search_care_plan"]["path"], **kwargs
        )

        return self.get(url)

    def search_pathway_step(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["search_pathway_step"]["path"], **kwargs
        )

        return self.get(url)

    def search_patient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Goal"]["search_patient"]["path"], **kwargs
        )

        return self.get(url)


class CareTeam(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_episode(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CareTeam"]["get_specific_episode"]["path"], ID=ID
        )

        return self.get(url)

    def get_longitudinal(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CareTeam"]["get_longitudinal"]["path"], ID=ID
        )

        return self.get(url)

    def search_episode(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CareTeam"]["search_episode"]["path"], **kwargs
        )

        return self.get(url)

    def create_new_episode(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CareTeam"]["create_new_episode"]["path"]
        )
        payload = self.build_payload(10155, **kwargs)
        return self.post(url, data=payload)

    def search_longitudinal(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["CareTeam"]["search_longitudinal"]["path"], **kwargs
        )

        return self.get(url)


class AdverseEvent(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_adverse_event(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["AdverseEvent"]["get_specific_adverse_event"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_adverse_event(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["AdverseEvent"]["search_adverse_event"]["path"],
            **kwargs
        )

        return self.get(url)


class Communication(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_community_resource(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Communication"]["create_new_community_resource"][
                "path"
            ]
        )
        payload = self.build_payload(10090, **kwargs)
        return self.post(url, data=payload)

    def get_specific_community_resource(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Communication"]["get_specific_community_resource"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_community_resource(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Clinic"]["Communication"]["search_community_resource"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)
