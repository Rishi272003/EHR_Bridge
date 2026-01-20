from services.ehr.eclinicalworks.client import ECWClient
from services.ehr.eclinicalworks.urls import ECW_URLS

class DiagnosticReport(ECWClient):
    def __init__(self, connection_obj) -> None:
        super().__init__(connection_obj)

    def get_diagnostic_report_by_id(self, report_id):
        """
        Search for Diagnostic Report by specific ID.
        GET [base]/DiagnosticReport/[id] or GET [base]/DiagnosticReport?_id=[id]

        Args:
            report_id: DiagnosticReport ID

        Returns:
            DiagnosticReport resource for the specific id
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        return self.get(url, params={"_id": report_id})

    def search_by_patient(self, patient_reference):
        """
        Search for Diagnostic Report by patient.
        GET [base]/DiagnosticReport?patient=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])

        Returns:
            DiagnosticReport resources associated with the specific patient
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(url, params={"patient": patient_reference})

    def search_by_patient_and_category(self, patient_reference, category):
        """
        Search for Diagnostic Report by patient and category.
        GET [base]/DiagnosticReport?patient=[reference]&category=[code]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            category: Category code (e.g., 'LAB' for laboratory)

        Returns:
            DiagnosticReport resources associated with the specific patient and category
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "category": category,
            },
        )

    def search_by_patient_category_and_date(
        self, patient_reference, category, date_params=None
    ):
        """
        Search for Diagnostic Report by patient, category and date range.
        GET [base]/DiagnosticReport?patient=[reference]&category=[code]&date=ge[date]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            category: Category code (e.g., 'LAB' for laboratory)
            date_params: Dictionary with date search parameters. Can include:
                - 'ge': greater than or equal to date
                - 'gt': greater than date
                - 'le': less than or equal to date
                - 'lt': less than date
                - 'eq': equal to date
                Example: {'ge': '2019-01-01', 'le': '2019-12-31'}

        Returns:
            DiagnosticReport resources associated with the specific patient, category and date range
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        params = {
            "patient": patient_reference,
            "category": category,
        }

        # Add date parameters with appropriate prefixes
        if date_params:
            date_list = []
            for operator, date_value in date_params.items():
                if operator in ["ge", "gt", "le", "lt", "eq"]:
                    date_list.append(f"{operator}{date_value}")
            if date_list:
                params["date"] = date_list

        return self.get(url, params=params)

    def search_by_patient_and_code(self, patient_reference, code):
        """
        Search for Diagnostic Report by patient and code (test/panel code).
        GET [base]/DiagnosticReport?patient=[reference]&code=[code]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            code: Test/panel code (e.g., LOINC code)

        Returns:
            DiagnosticReport resources associated with the specific patient and code
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "code": code,
            },
        )

    def search_by_patient_and_status(self, patient_reference, status):
        """
        Search for Diagnostic Report by patient and status.
        GET [base]/DiagnosticReport?patient=[reference]&status=[status]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            status: Report status (e.g., 'final', 'preliminary', 'amended', 'cancelled', 'entered-in-error')

        Returns:
            DiagnosticReport resources associated with the specific patient and status
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "status": status,
            },
        )

    def search_by_patient_and_encounter(self, patient_reference, encounter_id):
        """
        Search for Diagnostic Report by patient and encounter.
        GET [base]/DiagnosticReport?patient=[reference]&encounter=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            encounter_id: Encounter ID

        Returns:
            DiagnosticReport resources associated with the specific patient and encounter
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        # Remove 'Encounter/' prefix if present
        if encounter_id and encounter_id.startswith("Encounter/"):
            encounter_id = encounter_id.replace("Encounter/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "encounter": encounter_id,
            },
        )

    def search_by_patient_and_performer(self, patient_reference, performer_reference):
        """
        Search for Diagnostic Report by patient and performer (lab/organization).
        GET [base]/DiagnosticReport?patient=[reference]&performer=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            performer_reference: Performer reference (Organization or Practitioner)

        Returns:
            DiagnosticReport resources associated with the specific patient and performer
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        # Remove prefix from performer reference if present
        if performer_reference and "/" in performer_reference:
            performer_reference = performer_reference.split("/")[-1]

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "performer": performer_reference,
            },
        )

    def search_by_patient_and_specimen(self, patient_reference, specimen_id):
        """
        Search for Diagnostic Report by patient and specimen.
        GET [base]/DiagnosticReport?patient=[reference]&specimen=[reference]

        Args:
            patient_reference: Patient reference (can be patient ID or Patient/[id])
            specimen_id: Specimen ID

        Returns:
            DiagnosticReport resources associated with the specific patient and specimen
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )
        # Remove 'Patient/' prefix if present
        if patient_reference and patient_reference.startswith("Patient/"):
            patient_reference = patient_reference.replace("Patient/", "")

        # Remove 'Specimen/' prefix if present
        if specimen_id and specimen_id.startswith("Specimen/"):
            specimen_id = specimen_id.replace("Specimen/", "")

        return self.get(
            url,
            params={
                "patient": patient_reference,
                "specimen": specimen_id,
            },
        )

    def search_diagnostic_reports(self, **kwargs):
        """
        Generic search method that supports all search parameters.
        This method can handle any combination of search parameters.

        Args:
            **kwargs: Search parameters including:
                - _id: DiagnosticReport ID
                - patient: Patient reference
                - category: Category code (e.g., 'LAB')
                - code: Test/panel code
                - status: Report status
                - date: Date search parameter (can be string like 'ge2019' or dict with operators)
                - encounter: Encounter ID
                - performer: Performer reference
                - specimen: Specimen ID
                - result: Observation reference

        Returns:
            DiagnosticReport resources matching the search criteria
        """
        url = self.build_url(
            ECW_URLS["DiagnosticReport"]["get_diagnostic_report"]["path"],
        )

        params = {}

        # Handle _id parameter
        if kwargs.get("_id"):
            params["_id"] = kwargs.get("_id")

        # Handle patient parameter
        if kwargs.get("patient") or kwargs.get("patientid"):
            patient_ref = kwargs.get("patient") or kwargs.get("patientid")
            if patient_ref and patient_ref.startswith("Patient/"):
                patient_ref = patient_ref.replace("Patient/", "")
            params["patient"] = patient_ref

        # Handle category parameter
        if kwargs.get("category"):
            params["category"] = kwargs.get("category")

        # Handle code parameter
        if kwargs.get("code"):
            params["code"] = kwargs.get("code")

        # Handle status parameter
        if kwargs.get("status"):
            params["status"] = kwargs.get("status")

        # Handle encounter parameter
        if kwargs.get("encounter"):
            encounter_ref = kwargs.get("encounter")
            if encounter_ref and encounter_ref.startswith("Encounter/"):
                encounter_ref = encounter_ref.replace("Encounter/", "")
            params["encounter"] = encounter_ref

        # Handle performer parameter
        if kwargs.get("performer"):
            performer_ref = kwargs.get("performer")
            if performer_ref and "/" in performer_ref:
                performer_ref = performer_ref.split("/")[-1]
            params["performer"] = performer_ref

        # Handle specimen parameter
        if kwargs.get("specimen"):
            specimen_ref = kwargs.get("specimen")
            if specimen_ref and specimen_ref.startswith("Specimen/"):
                specimen_ref = specimen_ref.replace("Specimen/", "")
            params["specimen"] = specimen_ref

        # Handle result parameter
        if kwargs.get("result"):
            result_ref = kwargs.get("result")
            if result_ref and result_ref.startswith("Observation/"):
                result_ref = result_ref.replace("Observation/", "")
            params["result"] = result_ref

        # Handle date parameter
        if kwargs.get("date"):
            date_param = kwargs.get("date")
            if isinstance(date_param, dict):
                # Multiple date operators
                date_values = []
                for operator, date_value in date_param.items():
                    if operator in ["ge", "gt", "le", "lt", "eq"]:
                        date_values.append(f"{operator}{date_value}")
                if date_values:
                    params["date"] = date_values
            elif isinstance(date_param, str):
                # Single date string (e.g., 'ge2019-01-01')
                params["date"] = date_param

        return self.get(url, params=params)
