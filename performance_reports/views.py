from http.client import HTTPResponse
from django.shortcuts import render
from django.db import Error
from django.http import HttpResponse
import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import Font

from modules.get_data import get_cases
from modules.excel_module import *
from modules.case_note_func import transform_case_note_data

# Create your views here.
def index(request):
    try:
        #data_output = get_cases('1 Jan 2019', '23 mar 2022', '89,16,5,30', '')
        #print(data_output)
        # build excel report here
        if request.method == "POST":
            df_columns = {'High': [2, 5, 6], 'Medium': [7, 3, 2], 'Standard': [0, 3, 2]}
            df_index = ['Sandwell', 'Dudley', 'Walsall']
            df = pd.DataFrame(df_columns, index=df_index).rename_axis(index="Area", columns="Risk")

            excel_data = io.BytesIO()

            with pd.ExcelWriter(excel_data) as writer:
                df.to_excel(writer, sheet_name='Sheet')
                df.to_excel(writer, sheet_name='Sheet', startrow=7) 

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Test_file.xlsx"',})
            return response
        return render(request, 'performance_reports/index.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")

def export_notes(request):
    try:

        if request.method == "POST":
            clientID = 33575
            srv_str = ''
            grp_str = ''

            #case_note_data = gd.get_case_notes(clientID, srv_str, grp_str)
            filename = "test_case_notes_v1.xlsx"
            case_note_data = read_excel_file(filename)

            transformed_case_notes = transform_case_note_data(case_note_data)

            excel_data = create_case_notes_file(transformed_case_notes, clientID)

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Test_file.xlsx"',})
            
            return response
        return render(request, 'performance_reports/export_notes.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")