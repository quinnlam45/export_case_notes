from cgi import test
import io
from tempfile import NamedTemporaryFile

from numpy import byte
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook, save_workbook, ExcelWriter
from openpyxl.styles import Font
import pandas as pd

from pivot_table import PivotTable, make_pivot_table, pivot_df


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

def return_pivoted_dfs(df, df_rows, df_cols):
    dfs_list = []
    
    for df_row in df_rows:
        pivoted_df = pivot_df(df, df_row, df_cols)
        transformed_pivot_df = make_pivot_table(pivoted_df)
        dfs_list.append(transformed_pivot_df)
    
    return dfs_list


def build_report(df_list):

    current_row = 0
    buffer = io.BytesIO()

    with NamedTemporaryFile(suffix='.xlsx') as tmp:

        # func in excel module?
        with pd.ExcelWriter(tmp) as writer:
            for df in df_list:
                df.to_excel(writer, startrow=current_row+1, sheet_name='sheet', na_rep = 0)
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

# file_bytes = build_report(pivoted_df_list)

# bytes_to_file(file_bytes, 'Test.xlsx')
exp_df_columns = {'High': [0, 2], 'Medium': [1, 0],}
exp_df_index = ['Dudley', 'Sandwell']
expected_pivoted_df = pd.DataFrame(exp_df_columns, index=exp_df_index).rename_axis(index="Area", columns="Risk")
expected_totals_series = pd.Series([1,2], index=['Dudley', 'Sandwell'])
cols1 = expected_pivoted_df['High']
print(expected_totals_series)
print(cols1)
print('test')