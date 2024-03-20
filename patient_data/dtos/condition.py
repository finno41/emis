import pandas as pd


class ConditionDTOCollection:
    def __init__(self, data_collection):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        self.data_df = pd.DataFrame(data_collection)

    def output(self):
        return self.data_collection

    def output_dataframe(self):
        return self.data_df
