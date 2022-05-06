import unittest

from excel_module import read_excel_file
from case_note_func import transform_case_note_data

class CreateCaseNoteExcelFileTest(unittest.TestCase):
    filename = r"C:\Users\quinn\Documents\Programming\performance_dashboard\performance_dashboard\test_case_notes_transform_data_v1.xlsx"
    fake_SQL_data = read_excel_file(filename)
    transformed_data = transform_case_note_data(fake_SQL_data)