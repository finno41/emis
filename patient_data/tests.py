from django.test import TestCase
from patient_data.models import Patient, Encounter, Condition, Claim, RelatedCondition
from django.db.utils import IntegrityError
from patient_data.helper import convert_json_files, store_fhir_files
from django.db import transaction
from patient_data.test_helper import get_optional_fields_test_data
from parameterized import parameterized

# Create your tests here.


class HfirTests(TestCase):
    def setUp(self):
        self.correct_json_data = {
            "file": convert_json_files(
                "patient_data/fhir_data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json"
            ),
            "patient_count": 1,
            "encounter_count": 25,
            "condition_count": 26,
            "claim_count": 28,
            "rel_condition_count": 26,
        }

    # to test more models this list can be expanded
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
    def test_data_storage(self):
        """
        Unfortunately I ran out of time, but to test the correct data is stored I would mock up some JSON files which I would
        generate in setUp. I would then grab the objects from the DB and use assertEqual to check them against the expected values.
        As a basic test I have initially tested that the correct amount of objects are being stored
        """
        json_data = self.correct_json_data
        store_fhir_files(json_data["file"])
        patients_stored = Patient.objects.count()
        encounter_stored = Encounter.objects.count()
        condition_stored = Condition.objects.count()
        claim_stored = Claim.objects.count()
        rel_condition_stored = RelatedCondition.objects.count()
        self.assertEqual(patients_stored, json_data["patient_count"])
        self.assertEqual(encounter_stored, json_data["encounter_count"])
        self.assertEqual(condition_stored, json_data["condition_count"])
        self.assertEqual(claim_stored, json_data["claim_count"])
        self.assertEqual(rel_condition_stored, json_data["rel_condition_count"])

    # test export is generated
    """
    Initially I would check that an excel file is generated in the API response. I would mock up a request using
    request factory. For more comprehensive testing I would convert each excel sheet into a data frame and check it
    against the expected variables in setUp
    """
