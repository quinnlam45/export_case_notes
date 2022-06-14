import io
from django.conf import settings
from django.shortcuts import render, redirect
from django.db import Error
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

from modules.get_data import get_cases
from modules.excel_module import *
from modules.case_note_func import transform_case_note_data
from modules.export_case_notes import *
from modules.pd_user import *

# Create your views here.
@login_required
def index(request):
    try:
        #print(request.user.is_authenticated)
        return render(request, 'performance_reports/index.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")

@login_required
def export_report(request):
    try:
        data_output = get_cases('1 Jan 2022', '23 mar 2022', '89,16,5,30', '')
        print(data_output)

        if request.method == "POST":

            excel_data = io.BytesIO()

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Test_file.xlsx"',})
            return response
        return render(request, 'performance_reports/index.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")

@login_required
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
            return render(request, 'performance_reports/export-notes.html')

    except Error as err:
        return HttpResponse(f"Error: {err}")

def get_random_string(request):
    pw_str = create_random_pw_string()
    return HttpResponse(pw_str)

def add_user(request):
    user_message = {'message': ''}
    if request.method == 'POST':
        username = request.POST['username']
        pwd_str = request.POST['pwd']
        add_user_result = add_pd_user(username, pwd_str)
        user_message['message'] = add_user_result

    return render(request, 'performance_reports/add-user.html', user_message)

def user_login(request):
    user_message = {'message': ''}
    try:
        if request.method == 'POST':
            username = request.POST['username']
            pwd = request.POST['pwd']
            user = authenticate(request, username=username, password=pwd)
            print(f'view func:{user}')
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                user_message['message'] = 'Invalid login'
        return render(request, 'performance_reports/login.html', user_message)

    except Error as err:
        return HttpResponse(f"Error: {err}")

def user_logout(request):
    logout(request)
    return redirect('/')