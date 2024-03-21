import json
import os
from patient_data.helper import store_fhir_files, convert_json_files
from patient_data.data.patient import get_all_patients
from patient_data.data.claim import get_all_claims
from patient_data.data.condition import get_all_conditions
from patient_data.data.encounter import get_all_encounters


def store_fhir(relative_file_path):
    fhir_files = convert_json_files(relative_file_path)
    store_fhir_files(fhir_files)
    return True


def export_data():
    patients = get_all_patients()
    claims = get_all_claims()
    conditions = get_all_conditions()
    encounters = get_all_encounters()
    return {
        "patients": patients,
        "claims": claims,
        "conditions": conditions,
        "encounters": encounters,
    }
