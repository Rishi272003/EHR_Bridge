ADVANCEMD_URLS = {
    "Patient": {
        "get_patient_demographics": {
            "method": "GET",
            "path": "/Patient",
            "description": "Retrieve get patient",
        },
    },
    "AllergyIntolerance": {
        "search_patient_allergies": {
            "method": "GET",
            "path": "/AllergyIntolerance",
            "description": "Searches for allergy intolerances for a single patient",
        }
    },
    "Condition": {
        "search_patient_diagnoses": {
            "method": "GET",
            "path": "/Condition",
            "description": "Searches for diagnoses for a single patient",
        }
    },
    "Observation": {
        "search_patient_vitals": {
            "method": "GET",
            "path": "/Observation",
            "description": "Searches for vitals and lab_result for a single patient",
        }
    },
    "Organization": {
        "get_organization": {
            "method": "GET",
            "path": "/Organization/{organizationid}",
            "description": "Searches for diagnoses for a single patient",
        }
    },
    "Practitioner": {
        "search_practitioner": {
            "path": "/Practitioner/{id}",
            "method": "GET",
            "description": "Searches for all based on the given search criteria.",
        }
    },
    "DiagnosticReport": {
        "search_patient_reports": {
            "path": "/DiagnosticReport",
            "method": "GET",
            "description": "Search for Diagnostic Report for Lab results that meet supplied query parameters",
        }
    },
    "MedicationRequest": {
        "search_medication_request": {
            "path": "/MedicationRequest",
            "method": "GET",
            "description": "Returns MedicationRequest resources by parameters.",
        }
    },
    "DocumentReference": {
        "get_documents": {
            "path": "/DocumentReference",
            "method": "GET",
            "description": "Get List of all CCDA per patients.",
        }
    },
    "Device": {
        "get_patient_devices": {
            "method": "GET",
            "path": "/Device",
            "description": "Get the device reading of the patient",
        }
    },
    "Encounter": {
        "get_encounter_by_id": {
            "method": "GET",
            "path": "/Encounter/{id}",
            "description": "Get the encounter details of the patient by encounter id",
        }
    },
}
