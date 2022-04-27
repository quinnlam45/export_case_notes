from excel_module import *
from case_note_func import *

clientID = 35959
srv_str = ''
grp_str = ''

#case_note_data = gd.get_case_notes(clientID, srv_str, grp_str)
filename = "test_case_notes_v1.xlsx"
case_note_data = read_excel_file(filename)

transformed_rows = []

string_length_limit = 1000

for datarow in case_note_data:
    row = []
    for item in datarow[5:]:
        if isinstance(item, str) and len(item) > string_length_limit:
            current_row = row
            sliced_str_list = slice_str(item, string_length_limit)
            for sliced_str in sliced_str_list:
                sliced_row = current_row.copy()
                sliced_row.append(sliced_str)
                transformed_rows.append(sliced_row)

            row = []
        else:
            row.append(item)
    if row:
        transformed_rows.append(row)

print(transformed_rows)
#ex.create_excel(transformed_rows, f"CN{clientID}.xlsx", str(clientID))