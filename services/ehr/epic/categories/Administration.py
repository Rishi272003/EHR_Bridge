from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient
from ecaremd.ehr_integrations.ehr_services.epic.urls import EPIC_R4_URLS


class Patient(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_patient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["create_new_patient"]["path"],
            **kwargs
        )
        payload = self.build_payload(930, **kwargs)
        return self.post(url, data=payload)

    def get_specific_patient(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["get_specific_patient"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_patient(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Patient"]["search_patient"]["path"],
            **kwargs
        )

        return self.get(url)


class RelatedPerson(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_related_person(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["RelatedPerson"][
                "get_specific_related_person"
            ]["path"],
            ID=ID,
        )

        return self.get(url)


class Practitioner(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name) -> None:
        super().__init__(customer_id, tenant_name)

    def get_specific_practitioner(self, providerid, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Practitioner"]["get_specific_practitioner"][
                "path"
            ],
            ID=providerid,
        )

        return self.get(url)

    def search_practitioner(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Practitioner"]["search_practitioner"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class PractitionerRole(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_practitioner_role(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["PractitionerRole"][
                "get_specific_practitioner_role"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_practitioner_role(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["PractitionerRole"][
                "search_practitioner_role"
            ]["path"]
        )

        return self.get(url, params={"location": kwargs.get("departmentid")})


class Organization(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_organization(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Organization"]["get_specific_organization"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_organization(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Organization"]["search_organization"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class Location(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_location(self, departmentid, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Location"]["get_specific_location"]["path"],
            locationid=departmentid,
        )

        return self.get(url)

    def search_location(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Location"]["search_location"]["path"],
            **kwargs
        )

        return self.get(url)


class Endpoint(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_endpoint(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Endpoint"]["get_specific_endpoint"]["path"],
            ID=ID,
        )

        return self.get(url)


class EpisodeOfCare(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_episode_of_care(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["EpisodeOfCare"][
                "get_specific_episode_of_care"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_episode_of_care(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["EpisodeOfCare"]["search_episode_of_care"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def create_new_episode_of_care(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["EpisodeOfCare"][
                "create_new_episode_of_care"
            ]["path"]
        )
        payload = self.build_payload(10157, **kwargs)
        return self.post(url, data=payload)


class Encounter(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_encounter(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Encounter"]["get_specific_encounter"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_encounter(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Encounter"]["search_encounter"]["path"],
            **kwargs
        )

        return self.get(url)


class Flag(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_health_concern_flag(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["get_specific_health_concern_flag"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_infection_flag(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["search_infection_flag"]["path"],
            **kwargs
        )

        return self.get(url)

    def get_specific_isolation_flag(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["get_specific_isolation_flag"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_patient_FYI_flag(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["get_specific_patient_FYI_flag"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_health_concern_flag(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["search_health_concern_flag"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_isolation_flag(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["search_isolation_flag"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_patient_FYI_flag(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["search_patient_FYI_flag"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_patient_FYI_flag(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Flag"]["create_patient_FYI_flag"]["path"]
        )
        payload = self.build_payload(10166, **kwargs)
        return self.post(url, data=payload)


class Device(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_device(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Device"]["get_specific_device"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_implants_device(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Device"]["get_specific_implants_device"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_implants_device(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Device"]["search_implants_device"]["path"],
            **kwargs
        )

        return self.get(url)


class Substance(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_substance(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Substance"]["get_specific_substance"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def search_substance(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Substance"]["search_substance"]["path"],
            **kwargs
        )

        return self.get(url)


class RequestGroup(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_dental_visit(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["RequestGroup"]["get_specific_dental_visit"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_oncology_plan_day(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["RequestGroup"][
                "get_specific_oncology_plan_day"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_dental_visit(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["RequestGroup"]["search_dental_visit"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)

    def search_oncology_plan_day(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["RequestGroup"]["search_oncology_plan_day"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class Consent(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_code_status(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Consent"]["get_specific_code_status"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_document(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Consent"]["get_specific_document"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_code_status(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Consent"]["search_code_status"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_document(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Consent"]["search_document"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_document(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Consent"]["create_new_document"]["path"]
        )
        payload = self.build_payload(987, **kwargs)
        return self.post(url, data=payload)


class Questionnaire(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_questionnaire(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Questionnaire"][
                "get_specific_questionnaire"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_questionnaire(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["Questionnaire"]["search_questionnaire"][
                "path"
            ],
            **kwargs
        )

        return self.get(url)


class QuestionnaireResponse(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_questionnaire_response(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["QuestionnaireResponse"][
                "create_new_questionnaire_response"
            ]["path"]
        )
        payload = self.build_payload(10023, **kwargs)
        return self.post(url, data=payload)

    def get_specific_code_status(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["QuestionnaireResponse"][
                "get_specific_code_status"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_patient_entered(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["QuestionnaireResponse"][
                "get_specific_patient_entered"
            ]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_patient_entered(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["QuestionnaireResponse"][
                "search_patient_entered"
            ]["path"],
            **kwargs
        )

        return self.get(url)


class List(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_specific_allergies(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_allergies"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_family_history(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_family_history"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_hospital_problems(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_hospital_problems"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_immunizations(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_immunizations"][
                "path"
            ],
            ID=ID,
        )

        return self.get(url)

    def get_specific_medications(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_medications"]["path"],
            ID=ID,
        )

        return self.get(url)

    def get_specific_problems(self, ID):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["get_specific_problems"]["path"],
            ID=ID,
        )

        return self.get(url)

    def search_allergies(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_allergies"]["path"], **kwargs
        )

        return self.get(url)

    def create_new_allergies(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["create_new_allergies"]["path"]
        )
        payload = self.build_payload(10147, **kwargs)
        return self.post(url, data=payload)

    def search_family_history(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_family_history"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_hospital_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_hospital_problems"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_hospital_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["create_new_hospital_problems"][
                "path"
            ]
        )
        payload = self.build_payload(10149, **kwargs)
        return self.post(url, data=payload)

    def search_immunizations(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_immunizations"]["path"],
            **kwargs
        )

        return self.get(url)

    def create_new_immunizations(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["create_new_immunizations"]["path"]
        )
        payload = self.build_payload(10153, **kwargs)
        return self.post(url, data=payload)

    def search_medications(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_medications"]["path"],
            **kwargs
        )

        return self.get(url)

    def search_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["search_problems"]["path"], **kwargs
        )

        return self.get(url)

    def create_new_problems(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["List"]["create_new_problems"]["path"]
        )
        payload = self.build_payload(10145, **kwargs)
        return self.post(url, data=payload)


class ValueSet(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_value_set(self, **kwargs):
        url = self.build_url(
            EPIC_R4_URLS["Administration"]["ValueSet"]["get_value_set"]["path"],
            **kwargs
        )

        return self.get(url)
