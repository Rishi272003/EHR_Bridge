from services.ehr.transformer import Transformer
from rest_framework.response import Response
from rest_framework import status
from services.ehr.eclinicalworks.categories.DocumentReference import DocumentReference
class MediaNewTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        super().__init__(connection_obj, source_data)
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {}

    def transform(self):
        return Response({"detail":"Not have apporpriate access to create media"},status=status.HTTP_403_FORBIDDEN)

class MediaGetTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        super().__init__(connection_obj, source_data)
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {}

    def transform(self):
        patient_documents = DocumentReference(self.connection)
        patient_documents.authenticate()
        patient_id = self.source_json.get("Meta",{}).get("Source",{}).get("ID")
        if not patient_id:
            self.destination_response.update({"detail":"Patient ID is required"})
            return self.destination_response
        patient_documents = patient_documents.search_by_patient(patient_id)

        if patient_documents.get("status") == 200:
            self.destination_response.update({"data": patient_documents.get("data")})
        else:
            self.destination_response.update({"detail": patient_documents.get("detail")})
        return self.destination_response
