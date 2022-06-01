import requests
from http.client import HTTPResponse
from django.shortcuts import render
from django.db import Error
from django.http import HttpResponse, JsonResponse
import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import Font

from modules.get_data import get_cases
from modules.excel_module import *
from modules.case_note_func import transform_case_note_data
from modules.export_case_notes import *
from modules.pd_user import *

# Create your views here.
def index(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            pwd = request.POST['pwd']
            login_msg = verify_pd_user(username, pwd)
        
            return render(request, 'performance_reports/index.html', {'message': login_msg})
        else:
            return render(request, 'performance_reports/index.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")


def export_report(request):
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
        if request.method == 'POST':

            clientID = request.POST['clientID']
            pw_str = request.POST['random-str']
            srv_str = ''
            grp_str = ''

            excel_data = create_case_notes(clientID, pw_str)

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Case_notes.xlsx"',})

            return response

        else:
            return render(request, 'performance_reports/export_notes.html')

    except Error as err:
        return HttpResponse(f"Error: {err}")

def get_random_string(request):
    pw_str = create_random_pw_string()
    return HttpResponse(pw_str)

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd_str = request.POST['pwd']
        add_user_result = add_pd_user(username, pwd_str)

        return render(request, 'performance_reports/add_user.html', {'message': add_user_result})
    
    else:
        return render(request, 'performance_reports/add_user.html')