import pandas as pd
from patient_data.dtos.patients import PatientDTOCollection
from patient_data.dtos.condition import ConditionDTOCollection
from patient_data.data.patient import get_patients_by_ids
from patient_data.dtos.helper import join_patients_to_df
from patient_data.data.related_condition import get_related_condition_by_resource_ids
from patient_data.data.condition import get_conditions_by_ids
from patient_data.models import Claim


class ClaimDTOCollection:
    def __init__(self, data_collection):
        if not isinstance(data_collection, list):
            data_collection = list(data_collection.values())
        claim_ids = [data["id"] for data in data_collection]
        patient_ids = [data["patient_id"] for data in data_collection]
        patients = get_patients_by_ids(patient_ids)
        patients_df = PatientDTOCollection(patients).output_df_data()["df"]
        data_df = pd.DataFrame(data_collection)
        related_conditions = get_related_condition_by_resource_ids("claim", claim_ids)
        related_conditions_df = pd.DataFrame(
            related_conditions.values("resource_id", "condition_id")
        )
        condition_ids = list(related_conditions_df["condition_id"])
        conditions = get_conditions_by_ids(condition_ids)
        conditions_df = ConditionDTOCollection(
            conditions, merge_patient_data=False
        ).output_df_data()["df"]
        conditions_df.drop(columns=["patient_id"], inplace=True)
        conditions_df.columns = [f"condition_{col}" for col in conditions_df.columns]
        data_df = join_patients_to_df(patients_df, data_df)
        related_conditions_df = related_conditions_df.rename(
            columns={"resource_id": "id"}
        )
        data_df = pd.merge(
            data_df,
            related_conditions_df,
            on="id",
            how="left",
        )
        data_df = pd.merge(
            data_df,
            conditions_df,
            on="condition_id",
            how="left",
        )
        self.data_df = data_df
        date_fields = Claim.get_timezone_fields()
        for date_field in date_fields:
            self.data_df[date_field] = self.data_df[date_field].dt.tz_convert(None)

    def output(self):
        return self.data_collection

    def output_df_data(self):
        return {"df": self.data_df, "title": "claims"}
