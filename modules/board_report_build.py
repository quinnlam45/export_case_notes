import pandas as pd
from excel_module import *

from report_builder import *
from get_data import get_cases
from openpyxl import Workbook


file_name = 'board_report_v1.xlsx'

service_groups = {
     'Accommodation' : '1',
     'Children' : '2',
     'DV community' : '3',
     #'Modern Slavery' : '4',
     #'Rape and SV' : '5',
     #'Stalking' : '6',
     #'Therapeutic' : '7',
     #"Women’s Justice" : '8',
    }

report_sections = {
    "cases_opened" : ["Service area", "Referrer", "Gender", "Age group"], #, "Ethnicity", "Caring status"
    "cases_closed" :  {"Engagement outcome": ["Advice and guidance", "One to one support"]}
    }

start_range = '1 apr 2022'
end_range = '30 apr 2022'

def write_to_excel_multiple_sheets(file_obj):
    wb = Workbook()
    ws = wb.active
    with pd.ExcelWriter(file_obj) as writer:
        writer.book = wb

        for service_group, groupID in service_groups.items(): # run each query
            df = get_cases(start_range, end_range, '', groupID)
            cols = 'Service'
            rows_to_pivot = report_sections['cases_opened']

            pivoted_df_list = return_pivoted_dfs(df, rows_to_pivot, cols)

            closed_df = get_cases(start_range, end_range, '', groupID, case_typ='Closed')
            # closed summary
            closed_summary = return_pivoted_dfs(closed_df, ['Support type'], cols)
            for closed_pivot_tbl in closed_summary:
                pivoted_df_list.append(closed_pivot_tbl)

            # AG summary
            advice_summary = return_pivoted_dfs(closed_df[closed_df['Support type'] == 'Advice and guidance'], ['Engagement outcome'], cols)
            for advice_pivot_tbl in advice_summary:
                advice_pivot_tbl.rename_axis("Advice and guidance", axis='index', inplace=True)
                pivoted_df_list.append(advice_pivot_tbl)

            # one to one summary
            one_to_one_summary = return_pivoted_dfs(closed_df[closed_df['Support type'] == 'One to one support'], ['Engagement outcome'], cols)
            for one_to_one_pivot_tbl in one_to_one_summary:
                one_to_one_pivot_tbl.rename_axis("One to one support", axis='index', inplace=True)
                pivoted_df_list.append(one_to_one_pivot_tbl)


            sh_name = service_group.replace(' ', '_')

            current_row = 0

            for df in pivoted_df_list:
                no_of_cols_in_df = len(df.columns) + 1
                no_of_rows_in_df = len(df.index) + 1
                current_row += 1
                df.to_excel(writer, startrow=current_row, sheet_name=sh_name, na_rep=0)                
                
                ws = wb[sh_name]
                apply_table_styling(ws, current_row, no_of_rows_in_df, no_of_cols_in_df)
                
                current_row += no_of_rows_in_df

        writer.save()

write_to_excel_multiple_sheets(file_name)