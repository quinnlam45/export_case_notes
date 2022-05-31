from django.conf import settings
from modules.excel_module import *
from modules.case_note_func import *
from modules.get_data import get_case_notes

temp_path = settings.TEMP_DIR

def create_case_notes(clientID, pw_str, srv_str='', grp_str=''):
    case_note_data = get_case_notes(clientID, srv_str, grp_str)

    temp_file_name = create_temp_file_name()

    filename = temp_path + '\\' + temp_file_name + '.xlsx'

    string_length_limit = 1000

    transformed_rows = transform_case_note_data(case_note_data, string_length_limit = string_length_limit)
    
    client_initials = case_note_data[1][0]
    print(client_initials)
    #print(transformed_rows)

    excel_file_data = create_case_notes_excel_file(transformed_rows, clientID, filename, pw_str)

    return excel_file_data

