EPIC_R4_URLS = {
    "Administration": {
        "Patient": {
            "create_new_patient": {
                "category": "Patient",
                "description": "Patient.Create (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Patient",
            },
            "get_specific_patient": {
                "category": "Patient",
                "description": "Patient.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Patient/{ID}",
            },
            "search_patient": {
                "category": "Patient",
                "description": "Patient.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Patient",
            },
        },
        "RelatedPerson": {
            "get_specific_related_person": {
                "category": "RelatedPerson",
                "description": "RelatedPerson.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/RelatedPerson/{ID}",
            }
        },
        "Practitioner": {
            "get_specific_practitioner": {
                "category": "Practitioner",
                "description": "Practitioner.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Practitioner/{ID}",
            },
            "search_practitioner": {
                "category": "Practitioner",
                "description": "Practitioner.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Practitioner?address={address}&address-city={address-city}&address-postalcode=\
                    {address-postalcode}&address-state={address-state}&family={family}&given={given}&identifier={identifier}\
                        &name={name}&_id={_id}",
            },
        },
        "PractitionerRole": {
            "get_specific_practitioner_role": {
                "category": "PractitionerRole",
                "description": "PractitionerRole.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/PractitionerRole/{ID}",
            },
            "search_practitioner_role": {
                "category": "PractitionerRole",
                "description": "PractitionerRole.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/PractitionerRole",
            },
        },
        "Organization": {
            "get_specific_organization": {
                "category": "Organization",
                "description": "Organization.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Organization/{ID}",
            },
            "search_organization": {
                "category": "Organization",
                "description": "Organization.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Organization?_id={_id}",
            },
        },
        "Location": {
            "get_specific_location": {
                "category": "Location",
                "description": "Location.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Location/{locationid}",
            },
            "search_location": {
                "category": "Location",
                "description": "Location.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Location?_id={_id}",
            },
        },
        "Endpoint": {
            "get_specific_endpoint": {
                "category": "Endpoint",
                "description": "Endpoint.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Endpoint/{ID}",
            }
        },
        "Schedule": {},
        "Slot": {},
        "EpisodeOfCare": {
            "get_specific_episode_of_care": {
                "category": "EpisodeOfCare",
                "description": "EpisodeOfCare.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/EpisodeOfCare/{ID}",
            },
            "search_episode_of_care": {
                "category": "EpisodeOfCare",
                "description": "EpisodeOfCare.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/EpisodeOfCare?patient={patient}&status={status}&type={type}",
            },
            "create_new_episode_of_care": {
                "category": "EpisodeOfCare",
                "description": "EpisodeOfCare.Search (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/EpisodeOfCare?patient={patient}&status={status}&type={type}",
            },
        },
        "Encounter": {
            "get_specific_encounter": {
                "category": "Encounter",
                "description": "Encounter.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Encounter/{ID}",
            },
            "search_encounter": {
                "category": "Encounter",
                "description": "Encounter.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Encounter",
            },
        },
        "Appointment": {
            "search_appointments": {
                "category": "Appointment",
                "description": "Appointment.Search (Appointments) (R4",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag/{ID}",
            },
            "get_appointment": {
                "category": "Appointment",
                "description": "Appointment.Read (Appointments) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Appointment/{ID}",
            },
            "get_open_appointment": {
                "category": "Appointment",
                "description": "Appointment $find (STU3)",
                "method": "POST",
                "path": "/api/FHIR/STU3/Appointment/$find",
            },
            "new_appointment": {
                "category": "Appointment",
                "description": "Appointment $find (STU3)",
                "method": "POST",
                "path": "/api/FHIR/STU3/Appointment/$book",
            },
        },
        "Flag": {
            "get_specific_health_concern_flag": {
                "category": "Flag",
                "description": "Flag.Read (Health Concern) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag/{ID}",
            },
            "get_infection_flag": {
                "category": "Flag",
                "description": "Flag.Read (Infection) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag/{ID}",
            },
            "get_specific_isolation_flag": {
                "category": "Flag",
                "description": "Flag.Read (Isolation) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag/{ID}",
            },
            "get_specific_patient_FYI_flag": {
                "category": "Flag",
                "description": "Flag.Read (Patient FYI) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag/{ID}",
            },
            "search_health_concern_flag": {
                "category": "Flag",
                "description": "Flag.Search (Health Concern) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag?category={category}&patient={patient}&status={status}\
                    &subject={subject}",
            },
            "search_infection_flag": {
                "category": "Flag",
                "description": "Flag.Search (Infection) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag?category={category}&patient={patient}&status={status}\
                    &subject={subject}",
            },
            "search_isolation_flag": {
                "category": "Flag",
                "description": "Flag.Search (Isolation) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag?category={category}&encounter={encounter}&patient={patient}\
                    &status={status}&subject={subject}",
            },
            "search_patient_FYI_flag": {
                "category": "Flag",
                "description": "Flag.Search (Patient FYI) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Flag?category={category}&patient={patient}&status={status}&subject=\
                    {subject}&_id={_id}",
            },
            "create_patient_FYI_flag": {
                "category": "Flag",
                "description": "Flag.Search (Patient FYI) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Flag?category={category}&patient={patient}&status={status}&subject=\
                    {subject}&_id={_id}",
            },
        },
        "Device": {
            "get_specific_device": {
                "category": "Device",
                "description": "Device.Read (External Devices) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Device/{ID}",
            },
            "get_specific_implants_device": {
                "category": "Device",
                "description": "Device.Read (Implants) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Device/{ID}",
            },
            "search_implants_device": {
                "category": "Device",
                "description": "Device.Search (Implants) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Device?_id={_id}&device-name={device-name}&manufacturer=\
                    {manufacturer}&model={model}&patient={patient}&udi-carrier=\
                        {udi-carrier}&udi-di={udi-di}",
            },
        },
        "Substance": {
            "get_specific_substance": {
                "category": "Substance",
                "description": "Substance.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Substance/{ID}",
            },
            "search_substance": {
                "category": "Substance",
                "description": "Substance.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Substance?_id={ID}",
            },
        },
        "RequestGroup": {
            "get_specific_dental_visit": {
                "category": "RequestGroup",
                "description": "RequestGroup.Read (Dental Visit) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/RequestGroup/{ID}",
            },
            "get_specific_oncology_plan_day": {
                "category": "RequestGroup",
                "description": "RequestGroup.Read (Oncology Plan Day) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/RequestGroup/{ID}",
            },
            "search_dental_visit": {
                "category": "RequestGroup",
                "description": "RequestGroup.Search (Dental Visit) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/RequestGroup?_id={_id}",
            },
            "search_oncology_plan_day": {
                "category": "RequestGroup",
                "description": "RequestGroup.Search (Oncology Plan Day) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/RequestGroup?_id={_id}",
            },
        },
        "Consent": {
            "get_specific_code_status": {
                "category": "Consent",
                "description": "Consent.Read (Code Status) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Consent/{ID}",
            },
            "get_specific_document": {
                "category": "Consent",
                "description": "Consent.Read (Document) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Consent/{ID}",
            },
            "search_code_status": {
                "category": "Consent",
                "description": "Consent.Search (Code Status) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Consent?category={category}&patient={patient}&status={status}\
                    &subject={subject}",
            },
            "search_document": {
                "category": "Consent",
                "description": "Consent.Search (Document) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Consent?_id={_id}&patient={patient}&status={status}&category={category}\
                    &identifier={identifier}&scope={scope}&dateTime={dateTime}&provision={provision}",
            },
            "create_new_document": {
                "category": "Consent",
                "description": "Consent.Search (Document) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Consent?_id={_id}&patient={patient}&status={status}&category={category}\
                    &identifier={identifier}&scope={scope}&dateTime={dateTime}&provision={provision}",
            },
        },
        "Questionnaire": {
            "get_specific_questionnaire": {
                "category": "Questionnaire",
                "description": "Questionnaire.Read (Patient-Entered Questionnaires) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Questionnaire/{ID}",
            },
            "search_questionnaire": {
                "category": "Questionnaire",
                "description": "Questionnaire.Search (Patient-Entered Questionnaires) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Questionnaire?_count={_count}&_id={_id}",
            },
        },
        "QuestionnaireResponse": {
            "create_new_questionnaire_response": {
                "category": "QuestionnaireResponse",
                "description": "QuestionnaireResponse.Create (Patient-Entered Questionnaires) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/QuestionnaireResponse",
            },
            "get_specific_code_status": {
                "category": "QuestionnaireResponse",
                "description": "QuestionnaireResponse.Read (Code Status) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/QuestionnaireResponse/{ID}",
            },
            "get_specific_patient_entered": {
                "category": "QuestionnaireResponse",
                "description": "QuestionnaireResponse.Read (Patient-Entered Questionnaires) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/QuestionnaireResponse/{ID}",
            },
            "search_patient_entered": {
                "category": "QuestionnaireResponse",
                "description": "QuestionnaireResponse.Search (Patient-Entered Questionnaires) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/QuestionnaireResponse?_id={_id}",
            },
        },
        "List": {
            "get_specific_allergies": {
                "category": "List",
                "description": "List.Read (Allergies) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "get_specific_family_history": {
                "category": "List",
                "description": "List.Read (Family History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "get_specific_hospital_problems": {
                "category": "List",
                "description": "List.Read (Hospital Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "get_specific_immunizations": {
                "category": "List",
                "description": "List.Read (Immunizations) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "get_specific_medications": {
                "category": "List",
                "description": "List.Read (Medications) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "get_specific_problems": {
                "category": "List",
                "description": "List.Read (Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List/{ID}",
            },
            "search_allergies": {
                "category": "List",
                "description": "List.Search (Allergies) (R4)",
                "method": "GET;POST",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}&subject={subject}",
            },
            "create_new_allergies": {
                "category": "List",
                "description": "List.Search (Allergies) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}&subject={subject}",
            },
            "search_family_history": {
                "category": "List",
                "description": "List.Search (Family History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}",
            },
            "search_hospital_problems": {
                "category": "List",
                "description": "List.Search (Hospital Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List?code={code}&encounter={encounter}&patient={patient}\
                    &subject={subject}",
            },
            "create_new_hospital_problems": {
                "category": "List",
                "description": "List.Search (Hospital Problems) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/List?code={code}&encounter={encounter}&patient={patient}\
                    &subject={subject}",
            },
            "search_immunizations": {
                "category": "List",
                "description": "List.Search (Immunizations) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}",
            },
            "create_new_immunizations": {
                "category": "List",
                "description": "List.Search (Immunizations) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}",
            },
            "search_medications": {
                "category": "List",
                "description": "List.Search (Medications) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List?patient={patient}&code={code}",
            },
            "search_problems": {
                "category": "List",
                "description": "List.Search (Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}&subject={subject}",
            },
            "create_new_problems": {
                "category": "List",
                "description": "List.Search (Problems) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/List?code={code}&patient={patient}&subject={subject}",
            },
        },
        "ValueSet": {
            "get_value_set": {
                "category": "ValueSet",
                "description": "ValueSet.$expand (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ValueSet/$expand?context={context}&contextDirection={contextDirection}\
                    &filter={filter}",
            }
        },
    },
    "Clinic": {
        "AllergyIntolerance": {
            "create_new_allergy_intolerance": {
                "category": "AllergyIntolerance",
                "description": "AllergyIntolerance.Create (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/AllergyIntolerance",
            },
            "get_specific_allergy_intolerance": {
                "category": "AllergyIntolerance",
                "description": "AllergyIntolerance.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/AllergyIntolerance/{ID}",
            },
            "search_allergy_intolerance": {
                "category": "AllergyIntolerance",
                "description": "AllergyIntolerance.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/AllergyIntolerance",
            },
        },
        "Condition": {
            "create_new_problems": {
                "category": "Condition",
                "description": "Condition.Create (Problems) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Condition",
            },
            "get_specific_care_plan_problem": {
                "category": "Condition",
                "description": "Condition.Read (Care Plan Problem) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_dental_finding": {
                "category": "Condition",
                "description": "Condition.Read (Dental Finding) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_encounter_diagnosis": {
                "category": "Condition",
                "description": "Condition.Read (Encounter Diagnosis) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_genomics": {
                "category": "Condition",
                "description": "Condition.Read (Genomics) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_health_concern": {
                "category": "Condition",
                "description": "Condition.Read (Health Concern) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_infection": {
                "category": "Condition",
                "description": "Condition.Read (Infection) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_problems": {
                "category": "Condition",
                "description": "Condition.Read (Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "get_specific_reason_for_visit": {
                "category": "Condition",
                "description": "Condition.Read (Reason for Visit) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition/{ID}",
            },
            "search_care_plan_problem": {
                "category": "Condition",
                "description": "Condition.Search (Care Plan Problem) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?category={category}&clinical-status={clinical-status}\
                    &encounter={encounter}&patient={patient}&subject={subject}&_id={_id}",
            },
            "search_dental_finding": {
                "category": "Condition",
                "description": "Condition.Search (Dental Finding) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?abatement-date={abatement-date}&category={category}\
                    &clinical-status={clinical-status}&code={code}&encounter={encounter}&onset-date={onset-date}\
                        &patient={patient}&recorded-date={recorded-date}&subject={subject}&_id={_id}",
            },
            "search_encounter_diagnosis": {
                "category": "Condition",
                "description": "Condition.Search (Encounter Diagnosis) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition",
            },
            "search_genomics": {
                "category": "Condition",
                "description": "Condition.Search (Genomics) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition",
            },
            "search_health_concern": {
                "category": "Condition",
                "description": "Condition.Search (Health Concern) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?patient={patient}&subject={subject}&category=\
                    {category}&clinical-status={clinical-status}&_id={_id}",
            },
            "search_infection": {
                "category": "Condition",
                "description": "Condition.Search (Infection) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?abatement-date={abatement-date}&category={category}\
                    &clinical-status={clinical-status}&code={code}&encounter={encounter}&onset-date=\
                        {onset-date}&patient={patient}&recorded-date={recorded-date}&subject={subject}\
                            &_id={_id}",
            },
            "create_new_infection": {
                "category": "Condition",
                "description": "Condition.Search (Infection) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Condition?abatement-date={abatement-date}&category={category}\
                    &clinical-status={clinical-status}&code={code}&encounter={encounter}&onset-date=\
                        {onset-date}&patient={patient}&recorded-date={recorded-date}&subject={subject}\
                            &_id={_id}",
            },
            "search_problems": {
                "category": "Condition",
                "description": "Condition.Search (Problems) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?patient={patient}&category={category}&clinical-status=active",
            },
            "search_reason_for_visit": {
                "category": "Condition",
                "description": "Condition.Search (Reason for Visit) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Condition?category={category}&encounter={encounter}&patient=\
                    {patient}&subject={subject}",
            },
        },
        "Procedure": {
            "get_specific_orders": {
                "category": "Procedure",
                "description": "Procedure.Read (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure/{ID}",
            },
            "get_specific_surgeries": {
                "category": "Procedure",
                "description": "Procedure.Read (Surgeries) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure/{ID}",
            },
            "get_specific_surgical_history": {
                "category": "Procedure",
                "description": "Procedure.Read (Surgical History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure/{ID}",
            },
            "search_orders": {
                "category": "Procedure",
                "description": "Procedure.Search (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure",
            },
            "search_surgeries": {
                "category": "Procedure",
                "description": "Procedure.Search (Surgeries) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure?date={date}&patient={patient}&subject={subject}\
                    &_id={_id}",
            },
            "search_surgical_history": {
                "category": "Procedure",
                "description": "Procedure.Search (Surgical History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Procedure?category=387713003&patient={patient}&subject={subject}\
                    &_id={_id}",
            },
        },
        "FamilyMemberHistory": {
            "get_specific_family_member_history": {
                "category": "FamilyMemberHistory",
                "description": "FamilyMemberHistory.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/FamilyMemberHistory/{ID}",
            },
            "search_family_member_history": {
                "category": "FamilyMemberHistory",
                "description": "FamilyMemberHistory.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/FamilyMemberHistory?patient={patient}",
            },
            "create_family_member_history": {
                "category": "FamilyMemberHistory",
                "description": "FamilyMemberHistory.Search (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/FamilyMemberHistory?patient={patient}",
            },
        },
        "CarePlan": {
            "get_specific_dental": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Dental) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_encounter_level": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Encounter-Level) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_specific_inpatient_pathway": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Inpatient Pathway) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_specific_inpatient": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Inpatient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_longitudinal": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Longitudinal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_specific_oncology": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Oncology) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_specific_outpatient": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Outpatient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "get_specific_questionnaires_due": {
                "category": "CarePlan",
                "description": "CarePlan.Read (Questionnaires Due) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan/{ID}",
            },
            "search_dental": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Dental) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient}&subject=\
                    {subject}",
            },
            "search_encounter_level": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Encounter-Level) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient}&subject=\
                    {subject}&encounter={encounter}",
            },
            "search_inpatient_pathway": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Inpatient Pathway) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?activity-date={activity-date}&category={category}\
                    &encounter={encounter}&patient={patient}&status={status}&subject={subject}&_id=\
                        {_id}",
            },
            "search_inpatient": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Inpatient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient}&status=\
                    {status}&subject={subject}",
            },
            "search_longitudinal": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Longitudinal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient}\
                    &subject={subject}",
            },
            "search_oncology": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Oncology) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient\
                    }&status={status}",
            },
            "search_outpatient": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Outpatient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?category={category}&patient={patient}&status=\
                    {status}&subject={subject}",
            },
            "search_questionnaires_due": {
                "category": "CarePlan",
                "description": "CarePlan.Search (Questionnaires Due) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CarePlan?activity-date={activity-date}&category=\
                    {category}&patient={patient}",
            },
        },
        "Goal": {
            "get_specific_care_plan": {
                "category": "Goal",
                "description": "Goal.Read (Care Plan) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal/{ID}",
            },
            "get_specific_pathway_step": {
                "category": "Goal",
                "description": "Goal.Read (Pathway Step) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal/{ID}",
            },
            "get_specific_patient": {
                "category": "Goal",
                "description": "Goal.Read (Patient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal/{ID}",
            },
            "search_care_plan": {
                "category": "Goal",
                "description": "Goal.Search (Care Plan) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal?category={category}&lifecycle-status={lifecycle-status}\
                    &patient={patient}&subject={subject}&_count={_count}&_id={_id}&_include={_include}",
            },
            "search_pathway_step": {
                "category": "Goal",
                "description": "Goal.Search (Pathway Step) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal?category={category}&lifecycle-status={lifecycle-status}\
                    &patient={patient}&subject={subject}&_count={_count}&_id={_id}&_include={_include}",
            },
            "search_patient": {
                "category": "Goal",
                "description": "Goal.Search (Patient) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Goal?category={category}&lifecycle-status={lifecycle-status}\
                    &patient={patient}&subject={subject}&_count={_count}&_id={_id}&_include={_include}",
            },
        },
        "CareTeam": {
            "get_specific_episode": {
                "category": "CareTeam",
                "description": "CareTeam.Read (Episode) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CareTeam/{ID}",
            },
            "get_longitudinal": {
                "category": "CareTeam",
                "description": "CareTeam.Read (Longitudinal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CareTeam/{ID}",
            },
            "search_episode": {
                "category": "CareTeam",
                "description": "CareTeam.Search (Episode) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CareTeam?patient={patient}&status={status}&subject={subject}\
                    &_id={_id}",
            },
            "create_new_episode": {
                "category": "CareTeam",
                "description": "CareTeam.Search (Episode) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/CareTeam?patient={patient}&status={status}&subject={subject}\
                    &_id={_id}",
            },
            "search_longitudinal": {
                "category": "CareTeam",
                "description": "CareTeam.Search (Longitudinal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/CareTeam?patient={patient}&subject={subject}&status={status}",
            },
        },
        "AdverseEvent": {
            "get_specific_adverse_event": {
                "category": "AdverseEvent",
                "description": "AdverseEvent.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/AdverseEvent/{ID}",
            },
            "search_adverse_event": {
                "category": "AdverseEvent",
                "description": "AdverseEvent.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/AdverseEvent?seriousness={seriousness}&subject={subject}\
                    &study={study}&_id={_id}",
            },
        },
        "Communication": {
            "create_new_community_resource": {
                "category": "Communication",
                "description": "Communication.Create (Community Resource) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Communication",
            },
            "get_specific_community_resource": {
                "category": "Communication",
                "description": "Communication.Read (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Communication/{ID}",
            },
            "search_community_resource": {
                "category": "Communication",
                "description": "Communication.Search (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Communication?part-of={part-of}&patient={patient}\
                    &subject={subject}&_id={_id}",
            },
        },
    },
    "Diagnostic": {
        "Observation": {
            "create_new_LDA_W": {
                "category": "Observation",
                "description": "Observation.Create (LDA-W) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Observation",
            },
            "create_new_vitals": {
                "category": "Observation",
                "description": "Observation.Create (Vitals) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/Observation",
            },
            "get_activities_of_daily_living": {
                "category": "Observation",
                "description": "Observation.Read (Activities of Daily Living) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_core_characteristics": {
                "category": "Observation",
                "description": "Observation.Read (Core Characteristics) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_labs": {
                "category": "Observation",
                "description": "Observation.Read (Labs) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_LDA_W": {
                "category": "Observation",
                "description": "Observation.Read (LDA-W) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_specific_obstetric_details": {
                "category": "Observation",
                "description": "Observation.Read (Obstetric Details) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_specific_periodontal": {
                "category": "Observation",
                "description": "Observation.Read (Periodontal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_smart_data_elements": {
                "category": "Observation",
                "description": "Observation.Read (SmartData Elements) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_social_history": {
                "category": "Observation",
                "description": "Observation.Read (Social History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "get_specific_vatals": {
                "category": "Observation",
                "description": "Observation.Read (Vitals) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
            "search_activities_of_daily_living": {
                "category": "Observation",
                "description": "Observation.Search (Activities of Daily Living) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?based-on={based-on}&category={category}\
                    &code={code}&date={date}&focus={focus}&issued={issued}&patient={patient}\
                        &subject={subject}&_count={_count}&_id={_id}",
            },
            "search_core_characteristics": {
                "category": "Observation",
                "description": "Observation.Search (Core Characteristics) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?category={category}&code={code}&date={date}\
                    &issued={issued}&patient={patient}&subject={subject}&_count={_count}&_id=\
                        {_id}",
            },
            "search_labs": {
                "category": "Observation",
                "description": "Observation.Search (Labs) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?patient={patient}&category={category}",
            },
            "search_LDA_W": {
                "category": "Observation",
                "description": "Observation.Search (LDA-W) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?category={category}&code={code}&date={date}\
                    &issued={issued}&patient={patient}&subject={subject}&_count={_count}&_id=\
                        {_id}",
            },
            "search_obstetric_details": {
                "category": "Observation",
                "description": "Observation.Search (Obstetric Details) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?patient={patient}&subject={subject}&category=\
                    {category}&_id={_id}&code={code}&date={date}",
            },
            "search_periodontal": {
                "category": "Observation",
                "description": "Observation.Search (Periodontal) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?based-on={based-on}&category={category}&code=\
                    {code}&date={date}&focus={focus}&issued={issued}&patient={patient}&subject=\
                        {subject}&_count={_count}&_id={_id}",
            },
            "search_smart_data_elements": {
                "category": "Observation",
                "description": "Observation.Search (SmartData Elements) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?category={category}&code={code}&focus={focus}\
                    &patient={patient}",
            },
            "search_social_history": {
                "category": "Observation",
                "description": "Observation.Search (Social History) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation?patient={patient}&subject={subject}&category=\
                    {category}&_id={_id}&code={code}&issued={issued}",
            },
            "search_vitals": {
                "category": "Observation",
                "description": "Observation.Search (Vitals) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Observation",
            },
            "update_LDA_W": {
                "category": "Observation",
                "description": "Observation.Update (LDA-W) (R4)",
                "method": "PUT",
                "path": "/api/FHIR/R4/Observation/{ID}",
            },
        },
        "DiagnosticReport": {
            "get_results": {
                "category": "DiagnosticReport",
                "description": "DiagnosticReport.Read (Results) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DiagnosticReport/{ID}",
            },
            "search_results": {
                "category": "DiagnosticReport",
                "description": "DiagnosticReport.Search (Results) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DiagnosticReport?patient={patient}&subject={subject}\
                    &identifier={identifier}&_id={_id}&code={code}&date={date}",
            },
        },
        "ServiceRequest": {
            "get_specific_community_resource": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Read (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            },
            "get_dental_procedure": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Read (Dental Procedure) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            },
            "get_specific_order_template": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Read (Order Template) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            },
            "get_orders": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Read (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            },
            "get_speciffic_refferal": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Read (Referral) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            },
            "search_community_resource": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Search (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest?category={category}&encounter={encounter}\
                    &onlyscannable={onlyscannable}&patient={patient}&requester={requester}\
                        &status={status}&subject={subject}&_id={_id}",
            },
            "search_dental_procedure": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Search (Dental Procedure) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest?category={category}&encounter={encounter}\
                    &onlyscannable={onlyscannable}&patient={patient}&requester={requester}\
                        &status={status}&subject={subject}&_id={_id}",
            },
            "search_order_template": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Search (Order Template) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest?_id={_id}",
            },
            "search_orders": {
                "category": "ServiceRequest",
                "description": "ServiceRequest.Search (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest?encounter={encounter}&onlyscannable=\
                    {onlyscannable}&patient={patient}&requester={requester}&status={status}\
                        &subject={subject}&category={category}",
            },
        },
        "BodyStructure": {
            "get_specific_tooth": {
                "category": "BodyStructure",
                "description": "BodyStructure.Read (Tooth) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/BodyStructure/{ID}",
            },
            "search_tooth": {
                "category": "BodyStructure",
                "description": "BodyStructure.Search (Tooth) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/BodyStructure?location={location}&morphology={morphology}\
                    &patient={patient}&subject={subject}&_id={_id}",
            },
        },
        "Specimen": {
            "get_specific_specimen": {
                "category": "Specimen",
                "description": "Specimen.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Specimen/{ID}",
            },
            "search_specimen": {
                "category": "Specimen",
                "description": "Specimen.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Specimen?_id={_id}",
            },
        },
        "ResearchStudy": {
            "get_specific_research_study": {
                "category": "ResearchStudy",
                "description": "ResearchStudy.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ResearchStudy/{ID}",
            },
            "search_research_study": {
                "category": "ResearchStudy",
                "description": "ResearchStudy.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ResearchStudy?identifier={identifier}",
            },
        },
        "ResearchSubject": {
            "get_specific_research_subject": {
                "category": "ResearchSubject",
                "description": "ResearchSubject.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ResearchSubject/{ID}",
            },
            "search_research_subject": {
                "category": "ResearchSubject",
                "description": "ResearchSubject.Search (R4)",
                "method": "GET;POST",
                "path": "/api/FHIR/R4/ResearchSubject?patient={patient}&status={status}\
                    &study={study}",
            },
            "create_new_research_subject": {
                "category": "ResearchSubject",
                "description": "ResearchSubject.Search (R4)",
                "method": "GET;POST",
                "path": "/api/FHIR/R4/ResearchSubject?patient={patient}&status={status}\
                    &study={study}",
            },
        },
        "DocumentReference": {
            "create_new_clinical_notes": {
                "category": "DocumentReference",
                "description": "DocumentReference.Create (Clinical Notes) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference",
            },
            "create_new_document_information": {
                "category": "DocumentReference",
                "description": "DocumentReference.Create (Document Information) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference/",
            },
            "get_specific_clinical_notes": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Clinical Notes) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_specific_correspondences": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Correspondences) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_specific_document_information": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Document Information) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_external_CCDA_document": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (External CCDA Document) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_specific_handoff": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Handoff) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_specific_HIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (HIS) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_labs": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Labs) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_specific_OASIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (OASIS) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "get_radiology_results": {
                "category": "DocumentReference",
                "description": "DocumentReference.Read (Radiology Results) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
            "search_clinical_notes": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Clinical Notes) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference",
            },
            "search_correspondences": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Correspondences) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?author={author}&category={category}\
                    &date={date}&patient={patient}&period={period}&type={type}",
            },
            "search_document_information": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Document Information) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?author={author}&category={category}\
                    &date={date}&docstatus={docstatus}&encounter={encounter}&patient={patient}\
                        &period={period}&subject={subject}&type={type}&_id={_id}&_include=\
                            {_include}&_lastupdated={_lastupdated}",
            },
            "search_external_CCDA_document": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (External CCDA Document) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference",
            },
            "create_new_external_CCDA_document": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (External CCDA Document) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}\
                    &patient={patient}&period={period}",
            },
            "search_handoff": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Handoff) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}\
                    &docstatus={docstatus}&encounter={encounter}&patient={patient}\
                        &period={period}&subject={subject}&type={type}&_id={_id}&_include=\
                            {_include}&_lastupdated={_lastupdated}",
            },
            "create_new_handoff": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Handoff) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}\
                    &docstatus={docstatus}&encounter={encounter}&patient={patient}&period=\
                        {period}&subject={subject}&type={type}&_id={_id}&_include={_include}\
                            &_lastupdated={_lastupdated}",
            },
            "search_HIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (HIS) (R4)",
                "method": "GET;POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}&docstatus=\
                    {docstatus}&encounter={encounter}&patient={patient}&period={period}&subject={\
                        subject}&type={type}&_id={_id}&_include={_include}&_lastupdated={_lastupdated}",
            },
            "create_new_HIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (HIS) (R4)",
                "method": "GET;POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}&docstatus=\
                    {docstatus}&encounter={encounter}&patient={patient}&period={period}&subject=\
                        {subject}&type={type}&_id={_id}&_include={_include}&_lastupdated=\
                            {_lastupdated}",
            },
            "search_labs": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Labs) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}&patient=\
                    {patient}&subject={subject}&type={type}",
            },
            "create_labs": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Labs) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&date={date}&patient=\
                    {patient}&subject={subject}&type={type}",
            },
            "search_OASIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (OASIS) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&patient={patient}\
                    &period={period}&subject={subject}",
            },
            "create_new_OASIS": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (OASIS) (R4)",
                "method": "POST",
                "path": "/api/FHIR/R4/DocumentReference?category={category}&patient={patient}\
                    &period={period}&subject={subject}",
            },
            "search_radiology_results": {
                "category": "DocumentReference",
                "description": "DocumentReference.Search (Radiology Results) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DocumentReference?author={author}&category={category}\
                    &date={date}&patient={patient}&period={period}&subject={subject}&type={type}",
            },
            "update_document_information": {
                "category": "DocumentReference",
                "description": "DocumentReference.Update (Document Information) (R4)",
                "method": "PUT",
                "path": "/api/FHIR/R4/DocumentReference/{ID}",
            },
        },
        "Binary": {
            "get_clinical_notes": {
                "category": "Binary",
                "description": "Binary.Read (Clinical Notes) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_correspondences": {
                "category": "Binary",
                "description": "Binary.Read (Correspondences) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_document_information": {
                "category": "Binary",
                "description": "Binary.Read (Document Information) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_external_CCDA_document": {
                "category": "Binary",
                "description": "Binary.Read (External CCDA Document) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_handoff": {
                "category": "Binary",
                "description": "Binary.Read (Handoff) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_HIS": {
                "category": "Binary",
                "description": "Binary.Read (HIS) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_labs": {
                "category": "Binary",
                "description": "Binary.Read (Labs) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_OASIS": {
                "category": "Binary",
                "description": "Binary.Read (OASIS) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_specific_practitioner_photo": {
                "category": "Binary",
                "description": "Binary.Read (Practitioner Photo) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
            "get_radiology_results": {
                "category": "Binary",
                "description": "Binary.Read (Radiology Results) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Binary/{ID}",
            },
        },
    },
    "Medication": {
        "MedicationRequest": {
            "get_specific_order_template": {
                "category": "MedicationRequest",
                "description": "MedicationRequest.Read (Order Template) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationRequest/{ID}",
            },
            "get_orders": {
                "category": "MedicationRequest",
                "description": "MedicationRequest.Read (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationRequest/{ID}",
            },
            "search_order_template": {
                "category": "MedicationRequest",
                "description": "MedicationRequest.Search (Order Template) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationRequest?authoredon={authoredon}&category=\
                    {category}&date={date}&intent={intent}&patient={patient}&status={status}\
                        &subject={subject}&_id={_id}",
            },
            "search_orders": {
                "category": "MedicationRequest",
                "description": "MedicationRequest.Search (Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationRequest",
            },
        },
        "MedicationDispense": {
            "get_verified_orders": {
                "category": "MedicationDispense",
                "description": "MedicationDispense.Read (Verified Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationDispense/{ID}",
            },
            "search_verified_orders": {
                "category": "MedicationDispense",
                "description": "MedicationDispense.Search (Verified Orders) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationDispense?patient={patient}&subject={subject}\
                    &_count={_count}&_id={_id}",
            },
        },
        "Medication": {
            "get_specific_medication": {
                "category": "Medication",
                "description": "Medication.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Medication/{ID}",
            },
            "search_medications": {
                "category": "Medication",
                "description": "Medication.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Medication?_id={_id}",
            },
        },
        "Immunization": {
            "get_specific_immunization": {
                "category": "Immunization",
                "description": "Immunization.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Immunization/{ID}",
            },
            "search_immunization": {
                "category": "Immunization",
                "description": "Immunization.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Immunization",
            },
        },
        "ImmunizationRecommendation": {
            "get_specific_immunization_recommendation": {
                "category": "ImmunizationRecommendation",
                "description": "ImmunizationRecommendation.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ImmunizationRecommendation/{ID}",
            },
            "search_immunization_recommendation": {
                "category": "ImmunizationRecommendation",
                "description": "ImmunizationRecommendation.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ImmunizationRecommendation?patient={patient}",
            },
        },
    },
    "Workflow": {
        "Task": {
            "get_community_resource": {
                "category": "Task",
                "description": "Task.Read (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Task/{ID}",
            },
            "search_community_resource": {
                "category": "Task",
                "description": "Task.Search (Community Resource) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Task?code={code}&encounter={encounter}&patient=\
                    {patient}&subject={subject}&_id={_id}",
            },
            "update_community_resource": {
                "category": "Task",
                "description": "Task.Update (Community Resource) (R4)",
                "method": "PUT",
                "path": "/api/FHIR/R4/Task/{ID}",
            },
        },
        "NutritionOrder": {
            "get_nutrition_order": {
                "category": "NutritionOrder",
                "description": "NutritionOrder.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/NutritionOrder/{ID}",
            },
            "search_nutrition_order": {
                "category": "NutritionOrder",
                "description": "NutritionOrder.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/NutritionOrder?patient={patient}",
            },
        },
        "DeviceRequest": {
            "get_specific_device_request": {
                "category": "DeviceRequest",
                "description": "DeviceRequest.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceRequest/{ID}",
            },
            "search_device_request": {
                "category": "DeviceRequest",
                "description": "DeviceRequest.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceRequest?patient={patient}&status={status}",
            },
        },
        "DeviceUseStatement": {
            "get_external_devices": {
                "category": "DeviceUseStatement",
                "description": "DeviceUseStatement.Read (External Devices) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceUseStatement/{ID}",
            },
            "get_specific_implants": {
                "category": "DeviceUseStatement",
                "description": "DeviceUseStatement.Read (Implants) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceUseStatement/{ID}",
            },
            "search_external_devices": {
                "category": "DeviceUseStatement",
                "description": "DeviceUseStatement.Search (External Devices) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceUseStatement?patient={patient}",
            },
            "search_implants": {
                "category": "DeviceUseStatement",
                "description": "DeviceUseStatement.Search (Implants) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/DeviceUseStatement?patient={patient}",
            },
        },
        "Provenance": {
            "get_specific_provenance": {
                "category": "Provenance",
                "description": "Provenance.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Provenance/{ID}",
            }
        },
    },
    "Financial": {
        "Coverage": {
            "get_specific_coverage": {
                "category": "Coverage",
                "description": "Coverage.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Coverage/{ID}",
            },
            "search_coverage": {
                "category": "Coverage",
                "description": "Coverage.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/Coverage?patient={patient}",
            },
        },
        "ExplanationOfBenefit": {
            "get_explanation_of_benefit": {
                "category": "ExplanationOfBenefit",
                "description": "ExplanationOfBenefit.Read (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ExplanationOfBenefit/{ID}",
            },
            "search_explanation_of_benefit": {
                "category": "ExplanationOfBenefit",
                "description": "ExplanationOfBenefit.Search (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ExplanationOfBenefit?patient={patient}&created={created}",
            },
        },
    },
    "ClinicalReasoning": {
        "CDS Hooks ServiceRequest": {
            "get_unsigned_order": {
                "category": "CDS Hooks ServiceRequest",
                "description": "CDS Hooks ServiceRequest.Read (Unsigned Order) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/ServiceRequest/{ID}",
            }
        },
        "CDS Hooks MedicationRequest": {
            "get_unsigned_order": {
                "category": "CDS Hooks MedicationRequest",
                "description": "CDS Hooks MedicationRequest.Read (Unsigned Order) (R4)",
                "method": "GET",
                "path": "/api/FHIR/R4/MedicationRequest/{ID}",
            }
        },
    },
}
