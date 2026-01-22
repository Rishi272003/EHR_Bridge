from services.ehr.transformer import Transformer
from rest_framework import status
from rest_framework.response import Response
class OrganizationQueryTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Organization",
                "EventType": "Query",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            },
            "Organization": {
                "Identifiers": [],
                "Name": None,
                "Type": None,
                "Address": None,
                "Telecom": [],
            },
        }

    def transform(self):
        self.destination_response.update({"detail": "Not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)
        return self.destination_response

class OrganizationCreateTransformer(Transformer):
    def __init__(self, connection_obj,source_data):
        self.connection = connection_obj
        self.source_json = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Organization",
                "EventType": "Create",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            },
        }

    def transform(self):
        self.destination_response.update({"detail": "Not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)
        return self.destination_response
