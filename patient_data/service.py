import json
import os
from patient_data.helper import store_fhir_files


def store_fhir(relative_file_path):

    if relative_file_path:
        file_path = os.path.abspath(relative_file_path)

    if os.path.isdir(file_path):
        file_paths = [
            f"{file_path}/{f}" for f in os.listdir(file_path) if not os.path.isdir(f)
        ]
    else:
        file_paths = [file_path]
    resource_types = []
    for file_path in file_paths:
        with open(file_path, "r") as json_file:
            resource_types.append(json.loads(json_file))
    store_fhir_files(resource_types)
    return True
