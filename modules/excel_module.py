import io
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo, TableColumn
from openpyxl.styles import Font, Alignment, Border, Side, NamedStyle, PatternFill, Color
from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties
from openpyxl.worksheet.page import PrintPageSetup, PageMargins
from openpyxl.worksheet.header_footer import HeaderFooter, HeaderFooterItem
from openpyxl.writer.excel import save_virtual_workbook

import pandas as pd

# reads excel file and returns python data object/fake SQL data
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

def df_to_IO(df):
    stream = io.BytesIO()
    with pd.ExcelWriter(stream) as writer:
        df.to_excel(writer)
    
    return stream

def create_case_notes_file(data, clientID):
    sql_data = data
    wb = Workbook()

    ws1 = wb.active
    ws1["A1"] = "Client ref"
    ws1["A1"].font = Font(bold=True)
    bd = Side(border_style="thin")
    ws1["A1"].border = Border(top=bd, bottom=bd)
    ws1["A2"] = int(clientID)    
    ws1["A2"].fill = PatternFill("solid", fgColor=Color(indexed=22))
    
    max_col_width = 10
    
    # add data
    start_row = ws1.max_row + 1
    for row_no, datarow in enumerate(sql_data, start=1):
        for col_no, value in enumerate(datarow, start=1):
            #print(row)
            #print(value)
            ws1.cell(row=start_row+row_no, column=col_no, value=value)
            # update max col width
            if col_no == 1 and len(value) > max_col_width:
                max_col_width = len(value)

    max_row = ws1.max_row
    start_row += 1
    max_col_letter = ws1.cell(column=ws1.max_column, row=1).column_letter
    
    # set width of last col
    ws1.column_dimensions[max_col_letter].width = 80
    
    # convert data range into table
    datarange = f"A{start_row}:{max_col_letter}{max_row}"
    tab = Table(displayName="Table1", ref=datarange)

    style = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws1.add_table(tab)

    # adjust other col width
    ft = Font(b=True)
    for col in ws1.iter_cols(min_row=4, max_col=ws1.max_column-1, max_row=max_row):
        col_width = 9
        for cell in col:
            cell.alignment = Alignment(vertical="top")
            if isinstance(cell.value, str) and len(cell.value) > col_width:
                col_width = len(cell.value)
        ws1.column_dimensions[cell.column_letter].width = col_width

    for row in ws1.iter_rows(min_row=start_row, min_col=ws1.max_column, max_col=ws1.max_column, max_row=max_row):
        for row_cell in row:
            row_cell.alignment = Alignment(wrap_text=True, vertical="top")
    
    # page and print setup
    ws1.page_setup = PrintPageSetup(orientation = "landscape", scale=70, paperSize=9)
    ws1.page_margins = PageMargins(left=0.6, right=0.6, top=0.7, bottom=0.7)
    ws1.oddFooter.right.text = "&[Page]"
    ws1.evenFooter.left.text = "&[Page]"

    excel_data = save_virtual_workbook(wb)
    return excel_data

def reset_formatting(ws, start_row_no, max_row_no, max_col_no):
    ft = Font(bold=False)
    bd_style = Side(border_style=None)
    border_setting = Border(top=bd_style, left=bd_style, right=bd_style, bottom=bd_style)

    row_counter = 0
    for row in ws.iter_rows(min_row=start_row_no, max_row=start_row_no+max_row_no, min_col=1, max_col=max_col_no):
        for row_cell in row:
            row_cell.font = ft
            row_cell.border = border_setting
        row_counter += 1

def add_row_banding(ws, start_row_no, max_row_no, max_col_no):
    row_counter = 0
    for row in ws.iter_rows(min_row=start_row_no, max_row=start_row_no+max_row_no, min_col=1, max_col=max_col_no):
        for row_cell in row:
            if row_counter % 2:
                row_cell.style = "20 % - Accent1"
                row_cell.font = Font(size=11)
        row_counter += 1

def set_column_header_style(ws, start_row_no, max_col_no):
    for row in ws.iter_rows(min_row=start_row_no, max_row=start_row_no, min_col=1, max_col=max_col_no):
        for row_cell in row:
            row_cell.style = "Total"
            row_cell.font = Font(size=11, bold=True)
            row_cell.alignment = Alignment(wrap_text=True, vertical="top")


def find_max_str_length(max_value, str_val):
    max_str_len = max_value
    
    if len(str_val) > max_value:
        max_str_len = len(str_val)

    return max_str_len

def set_row_header_style(ws, ws_max_row, ws_max_col, ws_min_row=4):
    for column in ws.iter_cols(min_row=ws_min_row, max_col=ws_max_col, max_row=ws_max_row):
        for column_cell in column:
            column_cell.alignment = Alignment(horizontal='left', vertical="top")

def set_max_column_width(ws, max_col_width_setting, ws_max_row, ws_max_col, ws_min_row=4):
    #iterate through col cells
    max_width = max_col_width_setting
    for column in ws.iter_cols(min_row=ws_min_row, max_col=ws_max_col, max_row=ws_max_row):
        for column_cell in column:
            if column_cell != None and isinstance(column_cell.value, str):
                max_width = find_max_str_length(max_width, column_cell.value)
    
    # set col width
        ws.column_dimensions[column_cell.column_letter].width = max_width

def apply_default_style(ws, start_row_no, max_row_no, max_col_no):
    reset_formatting(ws, start_row_no, max_row_no, max_col_no)
    add_row_banding(ws, start_row_no, max_row_no, max_col_no)
    set_column_header_style(ws, start_row_no, max_col_no)
    set_row_header_style(ws, max_row_no, max_col_no)
    set_max_column_width(ws, 80, max_row_no, max_col_no)
