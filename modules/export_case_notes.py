from modules.excel_module import *
from modules.case_note_func import *
from modules.get_data import get_case_notes

#clientID = 34607
#srv_str = ''
#grp_str = ''

def create_case_notes(clientID, srv_str='', grp_str=''):
    case_note_data = get_case_notes(clientID, srv_str, grp_str)
    #filename = "test_case_notes_v1.xlsx"
    #case_note_data = read_excel_file(filename)

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
    
    client_initials = case_note_data[1][0]
    print(client_initials)
    print(transformed_rows)
    excel_file_data = create_case_notes_file(transformed_rows, clientID)

    return excel_file_data