from patient_data.models import Encounter


def get_all_encounters():
    return Encounter.objects.all()
