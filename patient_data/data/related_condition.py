from patient_data.models import RelatedCondition


def get_related_condition_by_type(resource_type):
    return RelatedCondition.objects.filter(resource_type=RelatedCondition)
