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
        data_output = get_cases('1 Jan 2019', '23 mar 2022', '89,16,5,30', '')
        print(data_output)
        # build excel report here
        if request.method == "POST":
            wb = Workbook()
            ws = wb.active
            ws["A1"] = "Test!"

            # saves workbook in memory as string
            excel_data = save_virtual_workbook(wb)

            ws["B1"] = "Second test!"
            ws["B1"].font = Font(bold="true")
            excel_data = save_virtual_workbook(wb)

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