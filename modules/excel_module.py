from openpyxl import load_workbook
import pandas as pd

# reads excel file and returns python data object
def read_excel_file(filename):
    wb = load_workbook(filename)
    ws = wb.active

    data_rows = []

    for row in ws.iter_rows(min_row=1, max_row=1):
        row_list = []
        for cell in row:
            row_list.append(cell.value)
        data_rows.append(row_list)

    for row in ws.iter_rows(min_row=2):
        row_list = []
        for cell in row:
            row_list.append(cell.value)
        data_rows.append(tuple(row_list))
    return data_rows

def df_to_excel(df, sh_name, dest_filename):
    wb = load_workbook(dest_filename)
    ws = wb.active
    row = ws.max_row + 1

    with pd.ExcelWriter(dest_filename, mode='a', if_sheet_exists="overlay") as writer:
        df.to_excel(writer, startrow=row, sheet_name=sh_name)
        writer.save()