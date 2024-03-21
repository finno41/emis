import pandas as pd
from patient_data.models import Condition
from patient_data.dtos.patients import PatientDTOCollection
from patient_data.dtos.helper import join_patients_to_df
from patient_data.data.patient import get_patients_by_ids


class ConditionDTOCollection:
    def __init__(self, data_collection, merge_patient_data=True):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        patient_ids = [data["patient_id"] for data in data_collection]
        patients = get_patients_by_ids(patient_ids)
        patients_df = PatientDTOCollection(patients).output_df_data()["df"]
        self.data_df = pd.DataFrame(data_collection)
        if merge_patient_data:
            self.data_df = join_patients_to_df(patients_df, self.data_df)
        date_fields = Condition.get_timezone_fields()
        for date_field in date_fields:
            self.data_df[date_field] = self.data_df[date_field].dt.tz_convert(None)

    def output(self):
        return self.data_collection

    def output_df_data(self):
        return {"df": self.data_df, "title": "conditions"}
