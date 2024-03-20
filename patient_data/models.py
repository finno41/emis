from django.db import models
from patient_data.model_options.language import LANGUAGE_OPTIONS
from patient_data.model_options.currency import CURRENCY_OPTIONS
import uuid


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    GENDER_CODES = {
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "unknown": "Unknown",
    }
    gender = models.CharField(max_length=7, choices=GENDER_CODES)
    birth_date = models.DateField()
    deceased_date_time = models.DateTimeField(blank=True, null=True)
    MARITAL_STATUS_OPTIONS = {
        "A": "Annulled",
        "D": "Divorced",
        "I": "Interlocutory",
        "L": "Legally Separated",
        "M": "Married",
        "C": "Common Law",
        "P": "Polygamous",
        "T": "Domestic partner",
        "U": "unmarried",
        "S": "Never Married",
        "W": "Widowed",
        "UNK": "unknown",
    }
    marital_status = models.CharField(max_length=3, choices=MARITAL_STATUS_OPTIONS)
    language = models.CharField(max_length=5, choices=LANGUAGE_OPTIONS)


class Encounter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    STATUS_OPTIONS = {
        "planned": "Planned",
        "in-progress": "In Progress",
        "on-hold": "On Hold",
        "discharged": "Discharged",
        "completed": "Completed",
        "cancelled": "Cancelled",
        "discontinued": "Discontinued",
        "entered-in-error": "Entered in Error",
        "unknown": "Unknown",
    }
    status = models.CharField(max_length=16, choices=STATUS_OPTIONS)
    CLASS_OPTIONS = {
        "IMP": "inpatient encounter",
        "AMB": "ambulatory",
        "OBSENC": "observation encounter",
        "EMER": "emergency",
        "VR": "virtual",
        "HH": "home health",
    }
    encounter_class = models.CharField(max_length=6, choices=CLASS_OPTIONS)
    coding_system = models.CharField(max_length=80, choices=CLASS_OPTIONS)
    code = models.CharField(max_length=40)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Condition(models.Model):
    # some of the fields here should have had choices but in the interest of time I've skipped them
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinical_status = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    onset_date_time = models.DateTimeField()
    recorded_date = models.DateTimeField()


# the assumption here is that multiple patient actions could relate to conditions
class RelatedCondition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    resource_id = models.UUIDField()
    resource_type = models.CharField(max_length=50)


class Claim(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created = models.DateTimeField()
    PRIORITY_OPTIONS = {"stat": "Immediate", "normal": "Normal", "deferred": "Deferred"}
    priority = models.CharField(max_length=8, choices=PRIORITY_OPTIONS)
    value_total = models.FloatField()
    value_currency = models.CharField(max_length=3, choices=CURRENCY_OPTIONS)
