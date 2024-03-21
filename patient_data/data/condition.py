from patient_data.models import Condition


def get_all_conditions():
    return Condition.objects.all()


def get_conditions_by_ids(condition_ids):
    return Condition.objects.filter(id__in=condition_ids)
