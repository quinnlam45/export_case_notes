from case_note_func import return_slice_length
from excel_module import read_excel_file
# slice_len = return_slice_length("Test data here. this is a string", 30)
# print(slice_len)

filename = r"C:\Users\quinn\Documents\Programming\performance_dashboard\performance_dashboard\test_case_notes_v1.xlsx"
fake_SQL_data = read_excel_file(filename)
print(fake_SQL_data)