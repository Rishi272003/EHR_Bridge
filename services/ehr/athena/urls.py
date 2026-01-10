ATHENA_URLS = {
    "Patient":{
        "get_by_id":{
            "method":"GET",
            "path":"patients/{id}",
            "description":"Get the patient details using it's EHR id."
        },
        "get_by_name":{
            "method":"GET",
            "path":"patients/search",
            "description":"Get the patient details using it's name."
        }
    },
    "Chart":{
        "get_patient_allergies":{
            "method":"GET",
            "path":"chart/{patientId}/allergies",
            "description":"Get the patients allergies details"
        },
        "get_patient_problems":{
            "method":"GET",
            "path":"chart/{patientId}/problems",
            "description":"Get the patients problems/conditions details"
        },
        "get_patient_medications":{
            "method":"GET",
            "path":"chart/{patientId}/medications",
            "description":"Get the patients problems/conditions details"
        },
        "get_patient_vitals":{
            "method":"GET",
            "path":"chart/{patientId}/vitals",
            "description":"Get the patients problems/conditions details"
        },
    },
    "Appointment":{
        "get_appointments_by_dates":{
            "method":"GET",
            "path":"appointments/booked",
            "description":"Get the patients appointments"
        },
        "get_appointments_by_id":{
            "method":"GET",
            "path":"appointments/{appointmentId}",
            "description":"Get the patients appointments"
        },
        "cancel_appointment":{
            "method":"PUT",
            "path":"appointments/{appointmentId}/cancel",
            "description":"Cancel the patients appointments"
        },
        "reschedule_appointment":{
            "method":"PUT",
            "path":"appointments/{appointmentId}/reschedule",
            "description":"Reschedule the patients appointments"
        },
    },
    "Documents":{
        "get_documents_by_id":{
            "method":"GET",
            "path":"patients/{patientid}/documents",
            "description":"Get the documents details"
        },
    },
    "Providers":{
        "get_all_providers":{
            "method":"GET",
            "path":"providers",
            "description":"Get all providers"
        },
        "get_provider_by_id":{
            "method":"GET",
            "path":"providers/{providerid}",
            "description":"Get the provider details by id"
        },
        "create_provider":{
            "method":"POST",
            "path":"providers",
            "description":"Create a new provider"
        },
    },
}
