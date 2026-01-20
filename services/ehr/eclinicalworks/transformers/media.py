from services.ehr.transformer import Transformer
from rest_framework.response import Response
from rest_framework import status

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
        return Response({"detail":"Not have apporpriate access to get media"},status=status.HTTP_403_FORBIDDEN)
