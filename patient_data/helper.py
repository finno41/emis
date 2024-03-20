from patient_data.models import Patient
from patient_data.data.patient import get_patient_by_id
from patient_data.data_structure_config import RESOURCE_CONFIG
import re
import uuid


def store_fhir_files(data: list):
    processable_resource_types = list(RESOURCE_CONFIG.keys())
    existing_patients = Patient.objects.all()
    existing_patient_ids = list(existing_patients.values_list("id", flat=True))
    # bulk_create_models = {}
    # bulk_create_patients = []
    # bulk_create_join_tables = {}
    for fhir_file in data:
        if fhir_file["resourceType"] == "Bundle":
            entries = fhir_file["entry"]
            patient_data = next(
                entry
                for entry in entries
                if entry["resource"]["resourceType"] == "Patient"
            )
            main_patient_data = patient_data["resource"]
            patient_id = main_patient_data["id"]
            patient_exists = uuid.UUID(patient_id) in existing_patient_ids
            patient = get_patient_by_id(patient_id) if patient_exists else Patient()
            patient.id = patient_id
            patient.gender = main_patient_data["gender"]
            patient.birth_date = main_patient_data["birthDate"]
            # the documentation suggests we should treat the absence of a deceases time as the user being alive
            patient.deceased_date_time = main_patient_data.get("deceasedDateTime")
            address_data = main_patient_data["address"][0]
            patient.city = address_data["city"]
            patient.state = address_data["state"]
            patient.country = address_data["country"]
            patient.marital_status = main_patient_data["maritalStatus"]["coding"][0][
                "code"
            ]
            patient.language = main_patient_data["communication"][0]["language"][
                "coding"
            ][0]["code"]
            if len(patient.marital_status) > 3:
                print(patient.marital_status)
            # if patient_exists:
            patient.save()
            # else:
            #     bulk_create_patients.append(patient)
            for entry in entries:
                resource_type = entry["resource"]["resourceType"]
                if resource_type in processable_resource_types:
                    resource = RESOURCE_CONFIG[resource_type]
                    entry_id = get_id_from_fhir_resource(resource, entry)
                    model = resource["model"]
                    model_exists = model.objects.filter(id=entry_id).exists()
                    model_instance = (
                        model.objects.get(id=entry_id) if model_exists else model()
                    )
                    model_instance.patient = patient
                    for field_data in resource["fields"]:
                        field_value = get_value_from_keys(field_data, entry, resource)
                        join_table_data = field_data.get("join_table")
                        if join_table_data:
                            join_table_data = create_join_model(
                                model_instance, field_data, field_value, entry_id
                            )
                            # join_table_model = join_table_data["model"]
                            # join_model_instance = join_table_model["model_instance"]
                            # if join_table_model in bulk_create_join_tables:
                            #     bulk_create_models[join_table_model].append(
                            #         join_model_instance
                            #     )
                            # else:
                            #     bulk_create_models[join_table_model] = (
                            #         join_model_instance
                            #     )
                        else:
                            setattr(
                                model_instance,
                                field_data["field_name"],
                                field_value,
                            )
                    model_instance.save()
                    # if model in bulk_create_models:
                    #     bulk_create_models[model].append(model_instance)
                    # else:
                    #     bulk_create_models[model] = [model_instance]
    # Patient.objects.bulk_create(bulk_create_patients)
    # for model, model_instances in bulk_create_models.items():
    #     model.objects.bulk_create(model_instances)
    # for model, model_instances in bulk_create_join_tables.items():
    #     model.objects.bulk_create(model_instances)


def get_value_from_keys(field_data, fhir_resource_data, resource):
    keys = field_data["fhir_keys"]
    optional = field_data.get("optional", False)
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
    regex = field_data.get("regex", False)
    if regex:
        value = re.search(regex, value)[0]
    return value


def create_join_model(model_instance, field_data, field_value, entry_id):
    if not field_value is None:
        join_table_data = field_data.get("join_table")
        model_data = join_table_data["model_data"]
        join_model_data = join_table_data["join_model_data"]
        model = model_data["model"].objects.get(id=field_value)
        model_attribute_name = model_data["name"]
        join_model = join_model_data["model"]
        join_model_instance = join_model()
        setattr(join_model_instance, model_attribute_name, model)
        setattr(join_model_instance, join_table_data["own_id_attr"], entry_id)
        for attribute, value in join_table_data["attributes"].items():
            setattr(join_model_instance, attribute, value)
        join_model_instance.save()
        # return {"model_instance": join_model_instance, "model": join_model}


def get_id_from_fhir_resource(resource_config, fhir_entry):
    id_field_data = next(
        field for field in resource_config["fields"] if field["field_name"] == "id"
    )
    return get_value_from_keys(id_field_data, fhir_entry, resource_config)
