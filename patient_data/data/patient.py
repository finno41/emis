from patient_data.models import Patient


def get_all_patients():
    return Patient.objects.all()


def get_patient_by_id(patient_id):
    return Patient.objects.get(id=patient_id)
