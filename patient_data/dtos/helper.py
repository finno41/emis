import pandas as pd
from django.db.models.query import QuerySet


def join_patients_to_df(
    patients_df: pd.DataFrame,
    df: pd.DataFrame,
    patients_join_key="id",
    df_join_key="patient_id",
):
    patients_df = patients_df.rename(columns={patients_join_key: df_join_key})
    df = pd.merge(
        df,
        patients_df,
        on=df_join_key,
        how="left",
    )
    return df
