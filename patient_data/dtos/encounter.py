import pandas as pd
from patient_data.models import Encounter


class EncounterDTOCollection:
    def __init__(self, data_collection):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        self.data_df = pd.DataFrame(data_collection)
        date_fields = Encounter.get_timezone_fields()
        for date_field in date_fields:
            self.data_df[date_field] = self.data_df[date_field].dt.tz_convert(None)

    def output(self):
        return self.data_collection

    def output_df_data(self):
        return {"df": self.data_df, "title": "encounters"}
