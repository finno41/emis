from patient_data.models import Claim


def get_all_claims():
    return Claim.objects.all()
