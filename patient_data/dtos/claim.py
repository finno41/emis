import pandas as pd
from patient_data.data.patient import get_patients_by_ids
from patient_data.data.related_condition import get_related_condition_by_ids
from patient_data.models import Claim


class ClaimDTOCollection:
    def __init__(self, data_collection):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        patient_ids = [data["patient_id"] for data in data_collection]
        patients = get_patients_by_ids(patient_ids)
        self.data_df = pd.DataFrame(data_collection)
        date_fields = Claim.get_timezone_fields()
        for date_field in date_fields:
            self.data_df[date_field] = self.data_df[date_field].dt.tz_convert(None)

    def output(self):
        return self.data_collection

    def output_df_data(self):
        return {"df": self.data_df, "title": "claims"}
