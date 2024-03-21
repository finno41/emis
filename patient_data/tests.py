from django.test import TestCase
from patient_data.models import Patient, Encounter, Condition, Claim
from django.db.utils import IntegrityError
from patient_data.helper import create_patient
from django.db import transaction
from patient_data.test_helper import get_optional_fields_test_data
from parameterized import parameterized

# Create your tests here.


class HfirTests(TestCase):
    def setUp(self):
        self.patient = create_patient(
            "2024-01-01", "New York", "NYC", "US", "male", "A", "da"
        )

    optional_fields = [
        {
            "model": Patient,
            "key": "patient",
            "correct_data": {
                "city": "New York",
                "birth_date": "2024-01-01",
                "state": "NYC",
                "country": "US",
                "gender": "male",
                "marital_status": "A",
                "language": "da",
            },
            "incorrect_fields": [
                {"field": "gender", "inputs": ["dsgkal", "ikgnaj"]},
                {"field": "marital_status", "inputs": ["SOS", "DNF", "B"]},
                {"field": "language", "inputs": ["aa", "ab", "ac"]},
            ],
        }
    ]
    optional_test_data = get_optional_fields_test_data(optional_fields)

    # test optional DB fields reject incorrect values
    """
    parameterized.expand splits iterables allowing you to run them as separate tests. In this
    example, were we to add more model data to the optional_fields variable above it would run as a
    separate test.
    """

    @parameterized.expand(optional_test_data)
    def test_database_validation(self, optional_fields):
        for i, optional_field_data in enumerate(optional_fields):
            with self.subTest(test_number=i + 1):
                model = optional_field_data["model"]
                model_instance = model()
                correct_data = optional_field_data["correct_data"]
                for attribute, value in correct_data.items():
                    setattr(model_instance, attribute, value)
                for field_data in optional_field_data["incorrect_fields"]:
                    setattr(model_instance, field_data["field"], field_data["input"])
                with self.assertRaises(IntegrityError) as context:
                    with transaction.atomic():
                        model_instance.save()

    # test correct data is stored
    """
    Unfortunately I ran out of time, but to test the correct data is stored I would mock up some JSON files which I would
    generate in setUp. I would then grab the objects from the DB and use assertEqual to check
    them against the expected values
    """
    # test export is generated
    """
    Initially I would check that an excel file is generated in the API response. I would mock up a request using
    request factory. For more comprehensive testing I would convert each excel sheet into a data frame and check it
    against the expected variables in setUp
    """
