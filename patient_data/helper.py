from patient_data.models import Patient
from patient_data.data.patient import get_patient_by_id
import uuid


def store_fhir_files(data: list):
    existing_patients = Patient.objects.all()
    existing_patient_ids = list(existing_patients.values_list("id", flat=True))
    bulk_create_patients = []
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
            """
            Assuming this would run multiple times in practice
            I wanted to ensure that we didn't add multiple entries per patient
            """
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
            if patient_exists:
                patient.save()
            else:
                bulk_create_patients.append(patient)
    Patient.objects.bulk_create(bulk_create_patients)
