from patient_data.service import export_data as export_data_service
from django.http import HttpResponse


def export_data(request):
    export_data_service()
    return HttpResponse("working test")
