CH_URLS = {
    "AllergyIntolerance": {
        "get_patient_allergy": {
            "method": "GET",
            "path": "/patients/{patient_id}/allergies",
            "description": "Get patient's allergies",
        },
    },
    "Appointment": {
        "get_patient_appointment": {
            "method": "GET",
            "path": "/Appointment",
            "description": "Get patient's Appointment",
        },
    },
    "CarePlan": {
        "get_patient_careplan": {
            "method": "GET",
            "path": "/Appointment",
            "description": "Get patient's careplan(fetch the CarePlan data (Assessment Notes and Treatment Notes))",
        },
    },
    "Problems": {
        "get_patient_condition": {
            "method": "GET",
            "path": "/patients/{patient_id}/problems",
            "description": "Get patient's condition",
        },
    },
    "Device": {
        "get_patient_device": {
            "method": "GET",
            "path": "/Device",
            "description": "Get patient's Device",
        },
    },
    "LabResults": {
        "get_patient_lab_report": {
            "method": "GET",
            "path": "/patients/{patient_id}/labresults",
            "description": "Get patient's Lab reports",
        },
    },
    "DocumentReference": {
        "get_patient_documents": {
            "method": "GET",
            "path": "/DocumentReference",
            "description": "Get patient's documents(Diet Notes, Lifestyle Notes and Instructions)",
        },
    },
    "MedicationRequest": {
        "get_patient_medication_orders": {
            "method": "GET",
            "path": "/patients/{patient_id}/medications",
            "description": "Get patient's medication orders",
        },
    },
    "Medications": {
        "get_patient_medications": {
            "method": "GET",
            "path": "/patients/{patient_id}/medications",
            "description": "Get patient's medications",
        },
    },
    "Vitals": {
        "get_patient_vitals": {
            "method": "GET",
            "path": "/patients/{patient_id}/vitals",
            "description": "Get patient's vitals",
        },
    },
    "Patient": {
        "get_specific_patient": {
            "method": "GET",
            "path": "/patients/id",
            "description": "Get patient's data(Demographics)",
        },
        "get_patient_demographics": {
            "method": "GET",
            "path": "/patients/{patientid}",
            "description": "Get patient's demographics",
        },
    },
    "Practitioner": {
        "get_practitioner": {
            "method": "GET",
            "path": "/Practitioner",
            "description": "Get the Practitioner data.",
        },
    },
    "CCDA": {
        "get_patients_ccda": {
            "method": "GET",
            "path": "/patients/{patient_id}/ccda",
            "description": "Fetches the entire patients' data in the Clinical Document Architecture (CDA) style.",
        }
    },
}
