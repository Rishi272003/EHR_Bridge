import logging

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
from services.ehr.eclinicalworks.transformers.organization import OrganizationQueryTransformer as ECWOrganizationQueryTransformer
from services.ehr.eclinicalworks.transformers.organization import OrganizationCreateTransformer as ECWOrganizationCreateTransformer
from services.ehr.eclinicalworks.transformers.practitioner import PractitionerQueryTransformer as ECWPractitionerQueryTransformer
from services.ehr.eclinicalworks.transformers.document_reference import DocumentReferenceQueryTransformer as ECWDocumentReferenceQueryTransformer

logger = logging.getLogger(__name__)

# Supported EHR types for each transformer
SUPPORTED_QUERY_EHRS = {"athena", "eclinicalworks"}
SUPPORTED_SEARCH_EHRS = {"athena", "eclinicalworks"}
SUPPORTED_VISIT_EHRS = {"athena", "eclinicalworks"}
SUPPORTED_PROVIDERS_EHRS = {"athena", "eclinicalworks"}
SUPPORTED_PATIENT_ADMIN_EHRS = {"eclinicalworks"}
SUPPORTED_MEDICATION_EHRS = {"eclinicalworks"}
SUPPORTED_MEDIA_EHRS = {"eclinicalworks"}
SUPPORTED_CLINICALS_PUSH_EHRS = {"eclinicalworks"}
SUPPORTED_ORGANIZATION_EHRS = {"eclinicalworks"}
SUPPORTED_DOCUMENT_REF_EHRS = {"eclinicalworks"}


def _get_ehr_name(connection_obj):
    """
    Safely extract EHR name from connection object.
    Returns None if connection_obj is invalid.
    """
    if not connection_obj or not hasattr(connection_obj, "ehr_name"):
        return None
    return connection_obj.ehr_name


def _unsupported_ehr_response(ehr_name, operation, supported_ehrs):
    """
    Generate a standardized error response for unsupported EHR types.
    """
    logger.warning(
        "Unsupported EHR type '%s' for operation '%s'. Supported: %s",
        ehr_name, operation, supported_ehrs
    )
    return {
        "error": f"EHR type '{ehr_name}' is not supported for {operation}",
        "supported_ehrs": list(supported_ehrs)
    }


def get_query_transformer(connection_obj, source_data):
    """
    Get the appropriate patient query transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for query transformer")
        return {"error": "Invalid connection object"}

    events = source_data.get("Meta", {}).get("Events", [])

    match ehr_name:
        case "athena":
            transformer = AthenaPatientQueryTransformer(connection_obj, events, source_data)
            return transformer.transform()
        case "eclinicalworks":
            transformer = ECWPatientQueryTransformer(connection_obj, source_data)
            return transformer.transform(events)
        case _:
            return _unsupported_ehr_response(ehr_name, "patient query", SUPPORTED_QUERY_EHRS)


def get_search_transformer(connection_obj, source_data):
    """
    Get the appropriate patient search transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for search transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "athena":
            transformer = AthenaPatientSearchTransformer(connection_obj, source_data)
            return transformer.transform()
        case "eclinicalworks":
            transformer = ECWPatientSearchTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "patient search", SUPPORTED_SEARCH_EHRS)


def get_visit_transformer(connection_obj, source_data):
    """
    Get the appropriate visit query transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for visit transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "athena":
            transformer = VisitQueryTransformer(connection_obj, source_data)
            return transformer.transform()
        case "eclinicalworks":
            transformer = ECWVisitQueryTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "visit query", SUPPORTED_VISIT_EHRS)


def get_providers_transformer(connection_obj, source_data):
    """
    Get the appropriate providers/practitioners transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for providers transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "athena":
            transformer = ProvidersTransformer(connection_obj, {}, source_data)
            return transformer.transform()
        case "eclinicalworks":
            transformer = ECWPractitionerQueryTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "providers query", SUPPORTED_PROVIDERS_EHRS)


def get_patient_admin_transformer(connection_obj, connection_data, source_data):
    """
    Get the appropriate patient admin transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for patient admin transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWNewPatientTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "patient admin", SUPPORTED_PATIENT_ADMIN_EHRS)


def get_medication_transformer(connection_obj, connection_data, source_data):
    """
    Get the appropriate medication transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for medication transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWMedicationNewTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "medication", SUPPORTED_MEDICATION_EHRS)


def get_media_transformer(connection_obj, connection_data, source_data):
    """
    Get the appropriate media transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for media transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWMediaNewTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "media", SUPPORTED_MEDIA_EHRS)


def clinicals_push_transformer(connection_obj, source_data, event):
    """
    Get the appropriate clinicals push transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for clinicals push transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWClinicalsPushTransformer(connection_obj, source_data)
            return transformer.transform(event)
        case _:
            return _unsupported_ehr_response(ehr_name, "clinicals push", SUPPORTED_CLINICALS_PUSH_EHRS)


def get_organization_transformer(connection_obj, source_data):
    """
    Get the appropriate organization query transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for organization transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWOrganizationQueryTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "organization query", SUPPORTED_ORGANIZATION_EHRS)


def create_organization_transformer(connection_obj, source_data):
    """
    Get the appropriate organization create transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for organization create transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWOrganizationCreateTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "organization create", SUPPORTED_ORGANIZATION_EHRS)


def get_document_reference_transformer(connection_obj, source_data):
    """
    Get the appropriate document reference transformer for the EHR type.
    """
    ehr_name = _get_ehr_name(connection_obj)
    if not ehr_name:
        logger.error("Invalid connection object for document reference transformer")
        return {"error": "Invalid connection object"}

    match ehr_name:
        case "eclinicalworks":
            transformer = ECWDocumentReferenceQueryTransformer(connection_obj, source_data)
            return transformer.transform()
        case _:
            return _unsupported_ehr_response(ehr_name, "document reference", SUPPORTED_DOCUMENT_REF_EHRS)
