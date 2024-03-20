from patient_data.service import export_data as export_data_service
from django.http import HttpResponse


def export_data(request):
    export_data = export_data_service()
    patients = export_data["patients"]
    claims = export_data["claims"]
    conditions = export_data["conditions"]
    encounters = export_data["encounters"]
    return HttpResponse("working test")
