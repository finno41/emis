from patient_data.models import Encounter

RESOURCE_CONFIG = {
    "Encounter": {
        "model": Encounter,
        "fields": [
            {"field_name": "id", "fhir_keys": ["resource", "id"]},
            {"field_name": "status", "fhir_keys": ["resource", "status"]},
            {
                "field_name": "encounter_class",
                "fhir_keys": ["resource", "class", "code"],
            },
            {
                "field_name": "coding_system",
                "fhir_keys": ["resource", "type", 0, "coding", 0, "system"],
            },
            {
                "field_name": "code",
                "fhir_keys": ["resource", "type", 0, "coding", 0, "code"],
            },
            {
                "field_name": "start_time",
                "fhir_keys": ["resource", "period", "start"],
            },
            {
                "field_name": "end_time",
                "fhir_keys": ["resource", "period", "end"],
            },
        ],
    },
    # "Claim": {"fields": [{"field_name": "id", "fhir_keys": ["id"]}]},
    # "Medication": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "DocumentReference": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "MedicationRequest": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Condition": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Device": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "ExplanationOfBenefit": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Immunization": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "CarePlan": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "CareTeam": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Provenance": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Procedure": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "ImagingStudy": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "Observation": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "MedicationAdministration": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "DiagnosticReport": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "AllergyIntolerance": {"fields": [{"field_name": "", "fhir_keys": []}]},
    # "SupplyDelivery": {"fields": [{"field_name": "", "fhir_keys": []}]},
}
