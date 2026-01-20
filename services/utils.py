from services.ehr.athena.transformers.clinical_summary import PatientQueryTransformer as AthenaPatientQueryTransformer
from services.ehr.athena.transformers.patient_search import PatientSearchTransformer as AthenaPatientSearchTransformer
from services.ehr.athena.transformers.visit_query import VisitQueryTransformer
from services.ehr.athena.transformers.transformer import ProvidersTransformer
from services.ehr.eclinicalworks.transformers.patient_search import QueryTransformer as ECWPatientSearchTransformer
from services.ehr.eclinicalworks.transformers.clinical_summary import PatientQueryTransformer as ECWPatientQueryTransformer
from services.ehr.eclinicalworks.transformers.encounter import VisitQuerTransformer as ECWVisitQueryTransformer
from services.ehr.eclinicalworks.transformers.patient_admin import NewPatientTransformer as ECWNewPatientTransformer
from services.ehr.eclinicalworks.transformers.clinical_summary import ClinicalsPushTransformer as ECWClinicalsPushTransformer
from services.ehr.eclinicalworks.transformers.clinical_summary import MedicationNewTransformer as ECWMedicationNewTransformer
from services.ehr.eclinicalworks.transformers.media import MediaNewTransformer as ECWMediaNewTransformer
from services.ehr.eclinicalworks.transformers.media import MediaGetTransformer as ECWMediaGetTransformer
def get_query_transformer(connection_obj,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    events = source_data.get("Meta",{}).get("Events",[])
    match ehr_name:
        case "athena":
            patientQ_obj = AthenaPatientQueryTransformer(connection_obj,events,source_data)
            response = patientQ_obj.transform()
        case "eclinicalworks":
            patientQ_obj = ECWPatientQueryTransformer(connection_obj,source_data)
            response = patientQ_obj.transform(events)
    return response

def get_search_transformer(connection_obj,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "athena":
            patientSearch_obj = AthenaPatientSearchTransformer(connection_obj,source_data)
            response = patientSearch_obj.transform()
        case "eclinicalworks":
            patientSearch_obj = ECWPatientSearchTransformer(connection_obj,source_data)
            response = patientSearch_obj.transform()
    return response

def get_visit_transformer(connection_obj, source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "athena":
            visitQ_obj = VisitQueryTransformer(connection_obj, source_data)
            response = visitQ_obj.transform()
        case "eclinicalworks":
            visitQ_obj = ECWVisitQueryTransformer(connection_obj, source_data)
            response = visitQ_obj.transform()
    return response

def get_providers_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    if ehr_name=="athena":
        providers_obj = ProvidersTransformer(connection_obj,connection_data,source_data)
        response = providers_obj.transform()
    return response

def get_patient_admin_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "eclinicalworks":
            patientAdmin_obj = ECWNewPatientTransformer(connection_obj,source_data)
            response = patientAdmin_obj.transform()
    return response

def get_medication_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "eclinicalworks":
            medication_obj = ECWMedicationNewTransformer(connection_obj,source_data)
            response = medication_obj.transform()
    return response

def get_media_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "eclinicalworks":
            media_obj = ECWMediaNewTransformer(connection_obj,source_data)
            response = media_obj.transform()
    return response

def get_media_get_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "eclinicalworks":
            media_obj = ECWMediaGetTransformer(connection_obj,source_data)
            response = media_obj.transform()
    return response

def clinicals_push_transformer(connection_obj,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    match ehr_name:
        case "eclinicalworks":
            clinicals_push_obj = ECWClinicalsPushTransformer(connection_obj,source_data)
            response = clinicals_push_obj.transform()
    return response
