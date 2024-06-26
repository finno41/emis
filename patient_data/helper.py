from patient_data.models import Patient
from patient_data.data.patient import get_patient_by_id
from patient_data.data_structure_config import RESOURCE_CONFIG, PATIENT_CONFIG
import json
import os
import re
import uuid


def store_fhir_files(fhir_files: list):
    patients_with_error = []
    for fhir_file in fhir_files:
        if fhir_file["resourceType"] == "Bundle":
            entries = fhir_file["entry"]
            patient_data = next(
                entry
                for entry in entries
                if entry["resource"]["resourceType"] == "Patient"
            )
            patient_id = patient_data["resource"]["id"]
            print(f"Storing data for patient '{patient_id}'")
            try:
                patient = store_resource(
                    patient_data,
                    False,
                    resource=PATIENT_CONFIG,
                    resource_type_check=False,
                )
            except:
                patients_with_error.append(patient.id)
            else:
                for entry in entries:
                    store_resource(entry, patient)
    print(
        f"The following patients were not saved due to incorrect data: '{patients_with_error}'"
    )


def store_resource(
    entry,
    patient,
    resource=False,
    resource_type_check=True,
):
    processable_resource_types = list(RESOURCE_CONFIG.keys())
    resource_type = entry["resource"]["resourceType"]
    if resource_type in processable_resource_types or not resource_type_check:
        if not resource:
            resource = RESOURCE_CONFIG[resource_type]
        entry_id = get_id_from_fhir_resource(resource, entry)
        model = resource["model"]
        model_exists = model.objects.filter(id=entry_id).exists()
        model_instance = model.objects.get(id=entry_id) if model_exists else model()
        if patient:
            model_instance.patient = patient
        for field_data in resource["fields"]:
            multiple = field_data.get("multiple", False)
            field_value = get_value_from_keys(field_data, entry, resource, multiple)
            join_table_data = field_data.get("join_table")
            if join_table_data:
                join_table_data = create_join_model(
                    model_instance, field_data, field_value, entry_id
                )
            else:
                setattr(
                    model_instance,
                    field_data["field_name"],
                    field_value,
                )
        model_instance.save()
        return model_instance


def get_value_from_keys(field_data, fhir_resource_data, resource, multiple):
    keys = field_data["fhir_keys"]
    optional = field_data.get("optional", False)
    regex = field_data.get("regex", False)
    value = find_from_keys(keys, fhir_resource_data, optional, field_data, resource)
    if multiple:
        value_list = value
        values = []
        if value_list:
            for value in value_list:
                list_value = find_from_keys(
                    multiple["loop_keys"], value, optional, field_data, resource
                )
                if regex and list_value:
                    list_value = re.search(regex, list_value)[0]
                values.append(list_value)
            return values
        else:
            return None
    elif regex:
        value = re.search(regex, value)[0]
    return value


def create_join_model(model_instance, field_data, field_value, entry_id):
    if field_value is not None:
        join_table_data = field_data.get("join_table")
        model_data = join_table_data["model_data"]
        join_model_data = join_table_data["join_model_data"]
        if isinstance(field_value, list):
            models = [
                model_data["model"].objects.get(id=value)
                for value in field_value
                if value
            ]
        else:
            models = [model_data["model"].objects.get(id=field_value)]

        model_attribute_name = model_data["name"]
        join_model = join_model_data["model"]
        for model in models:
            # to avoid duplicate join tables when re-processing data
            if not join_model.objects.filter(
                **{
                    model_attribute_name: model,
                    join_table_data["own_id_attr"]: entry_id,
                }
            ).exists():
                join_model_instance = join_model()
                setattr(join_model_instance, model_attribute_name, model)
                setattr(join_model_instance, join_table_data["own_id_attr"], entry_id)
                for attribute, value in join_table_data["attributes"].items():
                    setattr(join_model_instance, attribute, value)
                join_model_instance.save()


def get_id_from_fhir_resource(resource_config, fhir_entry):
    id_field_data = next(
        field for field in resource_config["fields"] if field["field_name"] == "id"
    )
    return get_value_from_keys(id_field_data, fhir_entry, resource_config, False)


def find_from_keys(keys, fhir_resource_data, optional, field_data, resource):
    value = fhir_resource_data
    for key in keys:
        try:
            value = value[key]
        except:
            if optional:
                return None
            else:
                raise KeyError(
                    f"fhir keys '{keys}' are incorrect for field '{field_data['field_name']}' for resource '{resource['key']}'"
                )
    return value


def create_patient(
    birth_date,
    city,
    state,
    country,
    gender,
    marital_status,
    language,
    deceased_date_time=False,
    patient_id=False,
):
    patient = Patient()
    if patient_id:
        patient.id = patient_id
    patient.gender = gender
    patient.birth_date = birth_date
    if deceased_date_time:
        patient.deceased_date_time = deceased_date_time
    patient.city = city
    patient.state = state
    patient.country = country
    patient.marital_status = marital_status
    patient.language = language
    patient.save()


def convert_json_files(relative_file_path):
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
    return fhir_files
