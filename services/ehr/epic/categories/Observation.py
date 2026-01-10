from ecaremd.ehr_integrations.ehr_services.epic.client import EpicFHIRClient


class Observation(EpicFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def create_new_LDA_W(self, **kwargs):
        return self.client.resource("Observation", **kwargs).save()

    def create_new_vitals(self, **kwargs):
        return self.client.resource("Observation", **kwargs).save()

    def get_activities_of_daily_living(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_core_characteristics(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_labs(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_LDA_W(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_specific_obstetric_details(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_specific_periodontal(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_smart_data_elements(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_social_history(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def get_specific_vatals(self, ID):
        return self.client.reference("Observation", ID).to_resource().serialize()

    def search_activities_of_daily_living(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_core_characteristics(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_labs(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_LDA_W(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_obstetric_details(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_periodontal(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_smart_data_elements(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_social_history(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list

    def search_vitals(self, **kwargs):
        response_list = [
            response.serialize()
            for response in self.client.resources("Observation")
            .search(**kwargs)
            .fetch()
        ]
        return response_list
