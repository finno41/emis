from django.http import HttpResponse
import io
import xlsxwriter
import pandas as pd


def create_excel_from_df_data(df_data_list: list):
    excel_file = io.BytesIO()
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    for df_data in df_data_list:
        df = df_data["df"]
        df.to_excel(writer, sheet_name=df_data["title"], index=False)
    writer.close()
    excel_file.seek(0)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="patients_upload.xlsx"'
    response.write(excel_file.read())
    return response
