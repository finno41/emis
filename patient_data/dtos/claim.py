import pandas as pd
from patient_data.data.patient import get_patients_by_ids


class ClaimDTOCollection:
    def __init__(self, data_collection):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        patient_ids = [data["patient_id"] for data in data_collection]
        patients = get_patients_by_ids(patient_ids)
        self.data_df = pd.DataFrame(data_collection)

    def output(self):
        return self.data_collection

    def output_dataframe(self):
        return self.data_df
