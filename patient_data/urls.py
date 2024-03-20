from django.urls import path
from patient_data.api import export_data

urlpatterns = [
    path("export", export_data, name="index"),
]
