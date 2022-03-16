from http.client import HTTPResponse
from django.shortcuts import render
from django.db import Error
from django.http import HttpResponse
import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Create your views here.
def index(request):
    try:
        # build excel report here
        if request.method == "POST":
            wb = Workbook()
            ws = wb.active
            ws["A1"] = "Test!"

            # saves workbook in memory as string
            excel_data = save_virtual_workbook(wb)

            ws["B1"] = "Second test!"
            excel_data = save_virtual_workbook(wb)

            response = HttpResponse(excel_data, headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                'Content_Disposition': 'attachment; filename="Test_file.xlsx"',})
            return response
        return render(request, 'performance_reports/index.html')
    except Error as err:
        return HttpResponse(f"Error: {err}")