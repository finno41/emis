from patient_data.models import Encounter, Claim, Condition, RelatedCondition

RESOURCE_CONFIG = {
    "Encounter": {
        "model": Encounter,
        "key": "encounter",
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
    "Condition": {
        "model": Condition,
        "key": "condition",
        "fields": [
            {"field_name": "id", "fhir_keys": ["resource", "id"]},
            {
                "field_name": "clinical_status",
                "fhir_keys": ["resource", "clinicalStatus", "coding", 0, "code"],
            },
            {
                "field_name": "category",
                "fhir_keys": ["resource", "category", 0, "coding", 0, "code"],
            },
            {
                "field_name": "code",
                "fhir_keys": ["resource", "code", "coding", 0, "code"],
            },
            {
                "field_name": "onset_date_time",
                "fhir_keys": ["resource", "onsetDateTime"],
            },
            {
                "field_name": "recorded_date",
                "fhir_keys": ["resource", "recordedDate"],
            },
        ],
    },
    "Claim": {
        "model": Claim,
        "key": "claim",
        "fields": [
            {"field_name": "id", "fhir_keys": ["resource", "id"]},
            {"field_name": "created", "fhir_keys": ["resource", "created"]},
            {
                "field_name": "priority",
                "fhir_keys": ["resource", "priority", "coding", 0, "code"],
            },
            {
                "field_name": "diagnosis",
                "fhir_keys": [
                    "resource",
                    "diagnosis",
                ],
                "optional": True,
                "multiple": {"loop_keys": ["diagnosisReference", "reference"]},
                "join_table": {
                    "model_data": {"model": Condition, "name": "condition"},
                    "join_model_data": {
                        "model": RelatedCondition,
                        "name": "related_condition",
                    },
                    "own_id_attr": "resource_id",
                    "attributes": {"resource_type": "claim"},
                },
                "regex": "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            },
            {
                "field_name": "value_total",
                "fhir_keys": [
                    "resource",
                    "total",
                    "value",
                ],
            },
            {
                "field_name": "value_currency",
                "fhir_keys": [
                    "resource",
                    "total",
                    "currency",
                ],
            },
        ],
    },
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
