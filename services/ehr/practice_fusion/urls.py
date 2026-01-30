PRACTICE_FUSION_URLS = {
    "Patient": {
        "search_patients": {
            "method": "GET",
            "path": "/Patient",
            "description": "Search for patients that meet supplied query parameters",
        },
        "get_patient": {
            "method": "GET",
            "path": "/Patient/{patient_id}",
            "description": "Get specific patient by ID",
        },
        "create_patient": {
            "method": "POST",
            "path": "/Patient",
            "description": "Create a new patient",
        },
        "update_patient": {
            "method": "PUT",
            "path": "/Patient/{patient_id}",
            "description": "Update an existing patient",
        },
    },
    "Chart": {
        "get_patient_demographics": {
            "method": "GET",
            "path": "/Patient",
            "description": "Get patient's Demographics",
        },
        "get_patient_allergy": {
            "method": "GET",
            "path": "/AllergyIntolerance",
            "description": "Get patient's allergies",
        },
        "get_patient_medication": {
            "method": "GET",
            "path": "/MedicationStatement",
            "description": "Get patient's medications",
        },
        "get_patient_problem": {
            "method": "GET",
            "path": "/Condition",
            "description": "Get patient's problem-list-item",
        },
        "get_patient_encounter": {
            "method": "GET",
            "path": "/Encounter",
            "description": "Get patient's Encounter",
        },
        "get_patient_vitals": {
            "method": "GET",
            "path": "/Observation",
            "description": "Get patient's Vitals",
        },
        "get_patient_lab_result": {
            "method": "GET",
            "path": "/Observation",
            "description": "Get patient's Lab Results",
        },
        "get_patient_insurance": {
            "method": "GET",
            "path": "/Coverage",
            "description": "Get patient's insurance details",
        },
    },
    "Practitioner": {
        "get_practitioner": {
            "method": "GET",
            "path": "/Practitioner",
            "description": "Search for Practitioner - returns all practitioners if no params",
        },
        "get_practitioner_by_id": {
            "method": "GET",
            "path": "/Practitioner/{practitioner_id}",
            "description": "Get specific Practitioner by ID",
        },
    },
    "Organization": {
        "get_organization": {
            "method": "GET",
            "path": "/Organization",
            "description": "Search for organization for given organization_id/name/type",
        },
    },
    "Encounter": {
        "get_encounter": {
            "method": "GET",
            "path": "/Encounter",
            "description": "Search for Encounter that meet supplied query parameters",
        },
        "get_encounter_by_id": {
            "method": "GET",
            "path": "/Encounter/{encounter_id}",
            "description": "Get specific Encounter by ID",
        },
    },
    "DocumentReference": {
        "search_patient_documents": {
            "method": "GET",
            "path": "/DocumentReference",
            "description": "Search for Document Reference that meet supplied query parameters",
        },
        "get_document_by_id": {
            "method": "GET",
            "path": "/DocumentReference/{document_id}",
            "description": "Get specific Document Reference by ID",
        },
    },
    "Coverage": {
        "search_coverage": {
            "method": "GET",
            "path": "/Coverage",
            "description": "Search for Coverage that meet supplied query parameters",
        },
        "get_coverage_by_id": {
            "method": "GET",
            "path": "/Coverage/{coverage_id}",
            "description": "Get specific Coverage by ID",
        },
    },
}
