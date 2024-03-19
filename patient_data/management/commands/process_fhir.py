from django.core.management.base import BaseCommand, CommandError
from patient_data.service import store_fhir


class Command(BaseCommand):
    help = "Processes fhir JSON files and stores them in the Database. Add the file path as an argument"

    def add_arguments(self, parser):
        parser.add_argument("fhir_file_path", nargs="+", type=str)

    def handle(self, *args, **options):
        fhir_file_path = options["fhir_file_path"][0]
        print(f"processing fhir_file(s) at file path '{fhir_file_path}'")
        store_fhir(fhir_file_path)
        print("fhir files sucessfully stored")
