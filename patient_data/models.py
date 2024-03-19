from django.db import models
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
    language = models.CharField(max_length=20)
