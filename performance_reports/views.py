import io
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.db import Error
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
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
        return render(request, 'performance_reports/reports.html')
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

@login_required
def get_random_string(request):
    pw_str = create_random_pw_string()
    return HttpResponse(pw_str)

@login_required
def add_user(request):
    user_message = {'message': ''}
    if request.method == 'POST':
        username = request.POST['username']
        pwd_str = request.POST['pwd']
        pwd_confirm_str = request.POST['pwd-confirm']

        if pwd_str == pwd_confirm_str:
            add_user_result = add_pd_user(username, pwd_str)
            user_message['message'] = add_user_result
        else:
            user_message['message'] = 'Passwords did not match'
            user_message['username'] = username

    return render(request, 'performance_reports/add-user.html', user_message)

def admin_check(user):
    # check if user is admin
    username = user.username
    admin_check = check_user_is_admin(username)
    return admin_check

def user_login(request):
    user_message = {'message': ''}
    try:
        if request.method == 'POST':
            username = request.POST['username']
            pwd = request.POST['pwd']
            user = authenticate(request, username=username, password=pwd)

            if user is not None:
                login(request, user)
                record_login_time(username)
                admin_check_result = admin_check(user)
                if admin_check_result:
                    request.session['user_type'] = 1
                return redirect('/')
            else:
                user_message['message'] = 'Invalid login'
        return render(request, 'performance_reports/login.html', user_message)

    except Error as err:
        return HttpResponse(f"Error: {err}")

def user_logout(request):
    logout(request)
    return redirect('/')



@user_passes_test(admin_check, login_url='/admin-only')
def user_admin(request):
    try:
        user_dict = get_all_users()
        return render(request, 'performance_reports/user-admin.html', user_dict)
    except Error as err:
        return HttpResponse(f"Error: {err}")

@user_passes_test(admin_check, login_url='/admin-only')
def user_admin_delete_user(request, username):
    try:
        delete_user(username)
        return redirect('performance_reports:user-admin')
    except Error as err:
        return HttpResponse(f"Error: {err}")

@user_passes_test(admin_check, login_url='/admin-only')
def user_admin_update_user_pwd(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            user_id = request.POST['user-id']
            pwd_str = request.POST['pwd']
            pwd_confirm_str = request.POST['pwd-confirm']

            if pwd_str == pwd_confirm_str:
                update_result = update_user_pwd(username, pwd_str)
                print(update_result)
                return redirect('performance_reports:user-admin')
            else:
                base_url = reverse('performance_reports:user-admin')
                query_str = urlencode({'user-id': user_id})
                url = f'{base_url}?{query_str}'
                return redirect(url)

    except Error as err:
        return HttpResponse(f"Error: {err}")

@login_required
def admin_only(request):
    try:
        return render(request, 'performance_reports/admin-only.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")

@login_required
def user_update_pwd(request):
    user_message = {'message': ''}
    try:
        if request.method == 'POST':
            username = request.POST['username']
            current_pwd_str = request.POST['pwd-current']
            pwd_str = request.POST['pwd']
            pwd_confirm_str = request.POST['pwd-confirm']
            user = authenticate(request, username=username, password=current_pwd_str)

            if user and username == user.username:
                if pwd_str == pwd_confirm_str:
                    update_result = update_user_pwd(username, pwd_str)
                    # log out then redirect to login
                    logout(request)
                    base_url = reverse('performance_reports:login')
                    query_str = urlencode({'user_updated': 'True'})
                    url = f'{base_url}?{query_str}'
                    return redirect(url)
                else:
                    user_message['message'] = 'Passwords do not match'
            else:
                user_message['message'] = 'Could not verify user'
        return render(request, 'performance_reports/change-pwd.html', user_message)

    except Error as err:
        return HttpResponse(f"Error: {err}")