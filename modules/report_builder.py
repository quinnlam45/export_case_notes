from asyncore import write
from cgi import test
from fileinput import filename
import io
from json import load
from tempfile import NamedTemporaryFile
from turtle import mode

from numpy import byte
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.styles import Font
import pandas as pd
from excel_module import *

from pivot_table import PivotTable, make_pivot_table, pivot_df


def build_report(excel_writer):

    current_row = 0
    buffer = io.BytesIO()

    with NamedTemporaryFile(suffix='.xlsx') as tmp:

        #implement different excelwriter/to excel methods here
        excel_writer(tmp)

        tmp.seek(0)
        stream = tmp.read()
        buffer.write(stream)

    return buffer

def read_file_obj_to_bytes(file_obj):

    file_bytes = io.BytesIO()

    file_obj.seek(0)
    stream = file_obj.read()
    file_bytes.write(stream)

    return file_bytes


def bytes_to_file(stream, filename):
    with open(filename, 'wb') as ex_file:
        stream.seek(0)
        ex_file.write(stream.read())

def return_no_of_df_rows(df):
    no_of_dimensions = df.ndim
    no_of_indexes = df.shape[0] # dataframe rows
    no_rows_in_df = no_of_dimensions + no_of_indexes

    return no_rows_in_df

def return_pivoted_dfs(df, df_rows, df_cols):
    dfs_list = []
    
    for df_row in df_rows:

        if df_row == 'Age group':
            pivoted_df = pivot_df(df, df_row, df_cols)
            age_groups = ['12 and under',
                            '13-18 years',
                            '19-24 years',
                            '25-34 years',
                            '35-44 years',
                            '45-54 years',
                            '55-64 years',
                            '65-74 years',
                            '75+ years'
                            ]
            age_template_df = pd.DataFrame(None, index = age_groups)
            pivoted_df = pd.concat([age_template_df, pivoted_df], axis=1).rename_axis("Age group", axis='index')
        else:
            pivoted_df = pivot_df(df, df_row, df_cols)
        transformed_pivot_df = make_pivot_table(pivoted_df)
        dfs_list.append(transformed_pivot_df)
    
    return dfs_list

#def write_to_excel_multiple_sheets(file_obj):
#    with pd.ExcelWriter(file_obj) as writer:
#        wb = writer.book

#        for f in filenames: # run each query
#            data = read_excel_file(f) # get data method
#            df = pd.DataFrame(data[1:], columns=data[0])

#            pivoted_df_list = return_pivoted_dfs(df, rows_to_pivot, cols)

#            sh_name = f[:-5]

#            current_row = 0

#            for df in pivoted_df_list:
#                no_of_cols_in_df = len(df.columns) + 1
#                no_of_rows_in_df = len(df.index) + 1
#                current_row += 1
#                df.to_excel(writer, startrow=current_row, sheet_name=sh_name, na_rep=0)                
                
#                ws = wb[sh_name]
#                apply_table_styling(ws, current_row, no_of_rows_in_df, no_of_cols_in_df)
                
#                current_row += no_of_rows_in_df

#        writer.save()