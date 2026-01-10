from services.ehr.athena.transformers.clinical_summary import PatientQueryTransformer
from services.ehr.athena.transformers.patient_search import PatientSearchTransformer
from services.ehr.athena.transformers.visit_query import VisitQueryTransformer
from services.ehr.athena.transformers.transformer import ProvidersTransformer
def get_query_transformer(connection_obj,patient_id,events,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    if ehr_name=="athena":
        patientQ_obj = PatientQueryTransformer(connection_obj,patient_id,source_data)
        response = patientQ_obj.transform(events)
    return response

def get_search_transformer(connection_obj,source_data,connection_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    if ehr_name=="athena":
        patientSearch_obj = PatientSearchTransformer(connection_obj,source_data,connection_data)
        response = patientSearch_obj.transform()
    return response

def get_visit_transformer(connection_obj, visit_data, connection_data, meta_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    if ehr_name=="athena":
        visitQ_obj = VisitQueryTransformer(connection_obj, visit_data, connection_data, meta_data)
        response = visitQ_obj.transform()
    return response

def get_providers_transformer(connection_obj,connection_data,source_data):
    response = None
    ehr_name = connection_obj.ehr_name if hasattr(connection_obj,"ehr_name") else None
    if ehr_name=="athena":
        providers_obj = ProvidersTransformer(connection_obj,connection_data,source_data)
        response = providers_obj.transform()
    return response
