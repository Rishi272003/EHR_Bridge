from datetime import datetime

from rest_framework import status

from services.ehr.transformer import Transformer
from services.ehr.eclinicalworks.categories.Task import Task


class TaskCreateTransformer(Transformer):
    def __init__(self, connection_obj, source_data):
        self.connection = connection_obj
        self.source_data = source_data
        self.destination_response = {
            "Meta": {
                "DataModel": "Task",
                "EventType": "CreateResponse",
                "Source": {"ID": self.connection.uuid, "Name": "connectionid"},
                "Raw": [],
            },
        }

    def transform(self):
        try:
            task_client = Task(self.connection)
            auth_status = task_client.authenticate()
            if auth_status is None:
                self.destination_response.update({
                    "Error": "Authentication failed - unable to obtain valid access token",
                    "statuscode": 401,
                })
                return self.destination_response

            task_data = self.source_data.get("Task", {})

            # Required fields
            intent = task_data.get("Intent", "order")
            task_status = task_data.get("Status", "ready")

            # Optional fields
            priority = task_data.get("Priority", "routine")
            focus_display = task_data.get("Focus")
            patient_id = task_data.get("Patient", {}).get("ID")
            patient_name = task_data.get("Patient", {}).get("Name")
            requester_id = task_data.get("Requester", {}).get("ID")
            requester_name = task_data.get("Requester", {}).get("Name")
            owner_id = task_data.get("Owner", {}).get("ID")
            owner_name = task_data.get("Owner", {}).get("Name")
            location_id = task_data.get("Location", {}).get("ID")
            execution_start = task_data.get("ExecutionPeriod", {}).get("Start")
            execution_end = task_data.get("ExecutionPeriod", {}).get("End")
            note_text = task_data.get("Note")

            # Build FHIR Task resource
            task_resource = {
                "resourceType": "Task",
                "meta": {
                    "lastUpdated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "profile": "http://hl7.org/fhir/StructureDefinition/Task",
                },
                "status": task_status,
                "intent": intent,
                "priority": priority,
                "authoredOn": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "lastModified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            }

            if focus_display:
                task_resource["focus"] = {"display": focus_display}

            if patient_id:
                task_resource["for"] = {"reference": f"Patient/{patient_id}"}
                if patient_name:
                    task_resource["for"]["display"] = patient_name

            if requester_id:
                task_resource["requester"] = {"reference": f"Practitioner/{requester_id}"}
                if requester_name:
                    task_resource["requester"]["display"] = requester_name

            if owner_id:
                task_resource["owner"] = {"reference": f"Practitioner/{owner_id}"}
                if owner_name:
                    task_resource["owner"]["display"] = owner_name

            if location_id:
                task_resource["location"] = {"reference": f"Location/{location_id}"}

            if execution_start or execution_end:
                task_resource["executionPeriod"] = {}
                if execution_start:
                    task_resource["executionPeriod"]["start"] = execution_start
                if execution_end:
                    task_resource["executionPeriod"]["end"] = execution_end

            if note_text:
                task_resource["note"] = [{"text": note_text}]

            # Wrap in FHIR Bundle
            bundle = {
                "resourceType": "Bundle",
                "id": "bundle-transaction",
                "meta": {
                    "lastUpdated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                "type": "transaction",
                "entry": [
                    {
                        "resource": task_resource,
                        "request": {
                            "method": "POST",
                            "url": "Task",
                        },
                    }
                ],
            }

            # Send to ECW
            response_data, status_code = task_client.create_task(bundle)

            if self.source_data.get("Meta", {}).get("Test"):
                self.destination_response["Meta"]["Raw"].append(response_data)

            if status_code in [200, 201]:
                # Extract task location from response
                entries = response_data.get("entry", [])
                task_location = None
                task_id = None
                if entries:
                    resp = entries[0].get("response", {})
                    task_location = resp.get("location", "")
                    task_id = task_location.split("/")[-1] if task_location else None

                self.destination_response.update({
                    "Task": {
                        "ID": task_id,
                        "Location": task_location,
                        "Status": task_status,
                    },
                    "statuscode": status_code,
                })
            else:
                self.destination_response.update(response_data)
                self.destination_response.update({"statuscode": status_code})

        except Exception as e:
            self.destination_response.update({"Error": str(e)})
            self.destination_response.update({"statuscode": status.HTTP_400_BAD_REQUEST})

        return self.destination_response
