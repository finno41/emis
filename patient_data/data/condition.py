from patient_data.models import Condition


def get_all_conditions():
    return Condition.objects.all()
