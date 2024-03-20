from patient_data.service import export_data as export_data_service
from patient_data.excel_logic import create_excel_from_df_data
from patient_data.dtos.claim import ClaimDTOCollection
from patient_data.dtos.condition import ConditionDTOCollection
from patient_data.dtos.encounter import EncounterDTOCollection
from patient_data.dtos.patients import PatientDTOCollection
from django.http import HttpResponse


def export_data(request):
    export_data = export_data_service()
    patients = export_data["patients"]
    claims = export_data["claims"]
    conditions = export_data["conditions"]
    encounters = export_data["encounters"]
    claim_df_data = ClaimDTOCollection(claims).output_df_data()
    condition_df_data = ConditionDTOCollection(conditions).output_df_data()
    encounter_df_data = EncounterDTOCollection(encounters).output_df_data()
    patient_df_data = PatientDTOCollection(patients).output_df_data()
    excel_response = create_excel_from_df_data(
        [claim_df_data, condition_df_data, encounter_df_data, patient_df_data]
    )
    return excel_response
