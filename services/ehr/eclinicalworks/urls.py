ECW_URLS = {
    "Chart": {
        "get_patient_demographics": {
            "method": "GET",
            "path": "/{practiceid}/Patient",
            "description": "Get patient's Demographics",
        },
        "get_patient_allergy": {
            "method": "GET",
            "path": "/{practiceid}/AllergyIntolerance",
            "description": "Get patient's allergies",
        },
        "get_patient_medication": {
            "method": "GET",
            "path": "/{practiceid}/MedicationAdministration",
            "description": "Get patient's medications",
        },
        "get_patient_problem": {
            "method": "GET",
            "path": "/{practiceid}/Condition",
            "description": "Get patient's problem-list-item",
        },
        "get_patient_encounter": {
            "method": "GET",
            "path": "/{practiceid}/Encounter",
            "description": "Get patient's Encounter",
        },
        "get_patient_vitals": {
            "method": "GET",
            "path": "/{practiceid}/Observation",
            "description": "Get patient's Vitals",
        },
        "get_patient_lab_result": {
            "method": "GET",
            "path": "/{practiceid}/Observation",
            "description": "Get patient's Lab Results",
        },
        "get_patient_insurance":{
            "method":"GET",
            "path":"/{practiceid}/Coverage",
            "description":"Get patient's insurance details"
        },
        "get_patient_relation":{
            "method":"GET",
            "path":"/{practiceid}/RelatedPerson",
            "description":"Get patient's relations"
        }
    },
    "Patient": {
        "specific_patient": {
            "method": "GET",
            "path": "/{practiceid}/Patient/{patientid}",
            "description": "Get specific patient record",
        },
        "search_criteria": {
            "method": "GET",
            "path": "/{practiceid}/Patient",
            "description": "Get list of patients - enhanced best matching search criteria",
        },
        "create_new_patient": {
            "description": "Create a new patient in ECW.",
            "method": "POST",
            "path": "/Patient",
        },
    },
    "Organization": {
        "get_organization": {
            "method": "GET",
            "path": "/{practiceid}/Organization",
            "description": "search for organization for given organization id",
        }
    },
    "Location": {
        "get_location": {
            "method": "GET",
            "path": "/{practiceid}/Location",
            "description": "Search for Location for a given location id",
        }
    },
    "Practitioner": {
        "get_practitioner": {
            "method": "GET",
            "path": "/{practiceid}/Practitioner",
            "description": "Search for Practitioner for a given practitioner id",
        },
        "search_practitioner": {
            "method": "GET",
            "path": "/{practiceid}/Practitioner",
            "description": "Search for Practitioner that meet given query parameters",
        },
        "get_practitioner_by_id": {
            "method": "GET",
            "path": "/{practiceid}/Practitioner",
            "description": "Search for Practitioner for a given practitioner id",
        },
    },
    "DiagnosticReport": {
        "get_diagnostic_report": {
            "method": "GET",
            "path": "/{practiceid}/DiagnosticReport",
            "description": "Search for Diagnostic Report for Lab results that meet supplied query parameters",
        }
    },
    "BulkData": {
        "get_job_id": {
            "method": "GET",
            "path": "/{practiceid}/Group/{group_id}/$export",
            "description": "Get List of Bulk Data",
        }
    },
    "MedicationRequest": {
        "get_patient_orders": {
            "method": "GET",
            "path": "/{practiceid}/MedicationRequest",
            "description": "Get List of Orders for a given patient",
        }
    },
    "DocumentReference": {
        "search_patient_documents": {
            "method": "GET",
            "path": "/{practiceid}/DocumentReference",
            "description": "Search for Document Reference that meet supplied query parameters",
        },
        "new_clinical_note": {
            "description": "Create a new document reference.",
            "method": "POST",
            "path": "/DocumentReference",
        },
    },
    "Binary": {
        "get_patient_ccda": {
            "method": "GET",
            "path": "/{practiceid}/Binary/{binaryid}",
            "description": "Get Patient CCDA Dat",
        }
    },
}
