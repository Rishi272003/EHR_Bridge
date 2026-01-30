import logging

from services.ehr.transformer import Transformer
from services.ehr.practice_fusion.categories.Chart import Chart

logger = logging.getLogger(__name__)


class PatientQueryTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.source_json = source_data
        self.connection = connection_obj
        self.patient_id = None
        self.destination_response = {
            "Meta": {
                "DataModel": "PatientQuery",
                "EventType": "Query",
                "Source": {"ID": str(self.connection.uuid), "Name": "connectionid"},
                "Raw": [],
            },
        }

    def transform(self, events):
        """
        Transform patient query request and fetch data from Practice Fusion.

        Args:
            events: List of events to fetch (e.g., ["demographics", "allergies", "medications"])
        """
        try:
            idtype = self.source_json.get("Patient").get("Identifiers")[0].get("IDType")
            if idtype == "EHRID":
                self.patient_id = self.source_json.get("Patient").get("Identifiers")[0].get("ID")
            else:
                return {"error": "Invalid ID Type"}, 400

            patients_chart = Chart(self.connection)
            patients_chart.authenticate()

            for event in events:
                event = event.lower()
                # TODO: Implement event handlers
                # Demographics Data
                if event == "demographics" or event == "patient" or event == "all":
                    # TODO: Implement demographics transformation
                    pass

                # Allergies Data
                if event == "allergies" or event == "all":
                    # TODO: Implement allergies transformation
                    pass

                # Medications Data
                if event == "medications" or event == "all":
                    # TODO: Implement medications transformation
                    pass

                # Conditions/Problems Data
                if event == "conditions" or event == "problems" or event == "diagnoses" or event == "all":
                    # TODO: Implement conditions transformation
                    pass

                # Vitals Data
                if event == "vitals" or event == "all":
                    # TODO: Implement vitals transformation
                    pass

                # Lab Results Data
                if event == "labresults" or event == "results" or event == "all":
                    # TODO: Implement lab results transformation
                    pass

                # Coverage Data
                if event == "coverage" or event == "insurance" or event == "all":
                    # TODO: Implement coverage transformation
                    pass

        except Exception as e:
            logger.exception("PatientQueryTransformer failed for patient %s", self.patient_id)
            self.destination_response["Meta"]["Error"] = str(e)
            return self.destination_response

        return self.destination_response
