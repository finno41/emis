import json
import os
from patient_data.helper import store_fhir_files
from patient_data.data.patient import get_all_patients
from patient_data.data.claim import get_all_claims
from patient_data.data.condition import get_all_conditions
from patient_data.data.encounter import get_all_encounters


def store_fhir(relative_file_path):

    if relative_file_path:
        file_path = os.path.abspath(relative_file_path)

    if os.path.isdir(file_path):
        file_paths = [
            f"{file_path}/{f}" for f in os.listdir(file_path) if not os.path.isdir(f)
        ]
    else:
        file_paths = [file_path]
    fhir_files = []
    for file_path in file_paths:
        with open(file_path, "r") as json_file:
            fhir_files.append(json.load(json_file))
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
