from ecaremd.ehr_integrations.ehr_services.eclinicalworks.client import ECWFHIRClient
from ecaremd.ehr_integrations.ehr_services.eclinicalworks.urls import ECW_URLS


class DiagnosticReport(ECWFHIRClient):
    def __init__(self, customer_id, tenant_name,source_json) -> None:
        super().__init__(customer_id, tenant_name,source_json)

    def get_diagnostic_report(self, practiceid, **kwargs):
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
            practiceid=practiceid,
        )

        return self.get(
            url,
            params={
                "category": kwargs.get("category"),
                "patient": kwargs.get("patient"),
            },
        )
