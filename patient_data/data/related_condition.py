from patient_data.models import RelatedCondition


def get_related_condition_by_type(resource_type):
    return RelatedCondition.objects.filter(resource_type=resource_type)


def get_related_condition_by_ids(resource_type, resource_ids):
    return RelatedCondition.objects.filter(
        resource_type=resource_type, resource_id__in=resource_ids
    )
