from patient_data.models import Patient
from patient_data.data.patient import get_patient_by_id
from patient_data.data_structure_config import RESOURCE_CONFIG
import uuid


def store_fhir_files(data: list):
    processable_resource_types = list(RESOURCE_CONFIG.keys())
    existing_patients = Patient.objects.all()
    existing_patient_ids = list(existing_patients.values_list("id", flat=True))
    bulk_create_patients = []
    bulk_create_models = {}
    # grab the patient from the entry first and either save the patient or look up the patient (use same uuids)
    # for each entry check that the resource type is in the keys, if not skip
    # if it is, iterate through each of the fields items from the config and use this to grab the data
    # use the inbuilt uuid to check if the item already exists, if it does overwrite if not create new
    # store the data
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
            # In a real life scenario I would find out why address is stored as a list, it's unclear in the
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
            if patient_exists:
                patient.save()
            else:
                bulk_create_patients.append(patient)
            for entry in entries:
                resource_type = entry["resource"]["resourceType"]
                if resource_type in processable_resource_types:
                    resource = RESOURCE_CONFIG[resource_type]
                    model = resource["model"]
                    model_instance = model()
                    model_instance.patient = patient
                    for field_data in resource["fields"]:
                        field_value = get_value_from_keys(
                            field_data["fhir_keys"], entry
                        )
                        setattr(
                            model_instance,
                            field_data["field_name"],
                            field_value,
                        )
                    if model in bulk_create_models:
                        bulk_create_models[model].append(model_instance)
                    else:
                        bulk_create_models[model] = [model_instance]
    Patient.objects.bulk_create(bulk_create_patients)
    for model, model_instances in bulk_create_models.items():
        model.objects.bulk_create(model_instances)


def get_value_from_keys(keys, fhir_resource_data):
    value = fhir_resource_data
    for key in keys:
        value = value[key]
    return value
