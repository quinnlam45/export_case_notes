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
from modules.export_case_notes import create_case_notes

# Create your views here.
def index(request):
    try:
        data_output = get_cases('1 Jan 2022', '23 mar 2022', '89,16,5,30', '')
        print(data_output)
        # build excel report here
        if request.method == "POST":

            excel_data = io.BytesIO()

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
            # validate clientID is int
            clientID = request.POST['clientID']
            srv_str = ''
            grp_str = ''
            #print(clientID)

            pw, excel_data = create_case_notes(clientID)
            print(pw)

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Case_notes.xlsx"',})
            
            return response
        return render(request, 'performance_reports/export_notes.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")