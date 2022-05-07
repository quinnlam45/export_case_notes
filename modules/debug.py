import io
from tempfile import NamedTemporaryFile

from numpy import byte
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook, save_workbook, ExcelWriter
from openpyxl.styles import Font
import pandas as pd

from dataframe_func import *
from pivot_table import PivotTable, make_pivot_table


dataframe_columns = ['CaseID', 'Referrer', 'Area', 'Risk']
dataframe_data = [(1, 'MASH', 'Sandwell', 'High'), (2, 'School', 'Dudley', 'Medium'), (3, 'MARAC', 'Sandwell','High')]
df = pd.DataFrame(dataframe_data, columns=dataframe_columns)


df_columns = {'High': [2, 5, 6], 'Medium': [7, 3, 2], 'Standard': [0, 3, 2]}
df_index = ['Sandwell', 'Dudley', 'Walsall']
df_dummy_pivot = pd.DataFrame(df_columns, index=df_index).rename_axis(index="Area", columns="Risk")



def return_no_of_df_rows(df):
    no_of_dimensions = df.ndim
    no_of_indexes = df.shape[0] # dataframe rows
    no_rows_in_df = no_of_dimensions + no_of_indexes

    return no_rows_in_df

def add_empty_percent_col(df):
    for df_col in df.columns:
        df[df_col + ' %'] = np.nan
    return df

def return_pivoted_dfs(df, df_rows, df_cols):
    dfs_list = []
    
    for df_row in df_rows:
        pivoted_df = pivot_df(df, df_row, df_cols)

        dfs_list.append(pivoted_df)
    
    return dfs_list


def build_report(df_list):

    current_row = 0
    buffer = io.BytesIO()

    with NamedTemporaryFile(suffix='.xlsx') as tmp:

        with pd.ExcelWriter(tmp) as writer:
            for df in df_list:
                df.to_excel(writer, startrow=current_row+1, sheet_name='sheet')
                no_rows_in_df = return_no_of_df_rows(df)
                current_row += no_rows_in_df
            writer.save()

        tmp.seek(0)
        stream = tmp.read()
        buffer.write(stream)

    return buffer

def bytes_to_file(stream, filename):
    with open(filename, 'wb') as ex_file:
        stream.seek(0)
        ex_file.write(stream.read())


cols = 'Risk'
rows_to_pivot = ['Area', 'Referrer']
pivoted_df_list = return_pivoted_dfs(df, rows_to_pivot, cols)

transformed_pivot_dfs = []

for pivoted_df in pivoted_df_list:
    transformed_pivot_df = make_pivot_table(pivoted_df)
    transformed_pivot_dfs.append(transformed_pivot_df)

del pivoted_df_list

file_bytes = build_report(transformed_pivot_dfs)

bytes_to_file(file_bytes, 'Test.xlsx')