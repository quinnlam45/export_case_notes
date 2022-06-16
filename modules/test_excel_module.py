import unittest
from django.conf import settings
import pandas as pd
from openpyxl import Workbook

from excel_module import *

class TestExcelModule(unittest.TestCase):
    temp_dir = settings.TEMP_DIR
    filename = temp_dir + r'\Test.xlsx'
    test_data = [['Heading 1'], ['Case note text']]

    def test_create_case_notes_files(self):
        pw_str, excel_data = create_case_notes_file(self.test_data, 12345, self.filename)
        print(pw_str)
        print(excel_data.read())
    
    def test_read_file_return_bytes(self):
        file_bytes = read_file_return_bytes(self.filename)
        print(file_bytes.read())

    def test_create_random_pw_string(self):
        pw = create_random_pw_string()
        print(pw)
    
    def test_create_temp_file_name(self):
        temp_name = create_temp_file_name()
        print(temp_name)

    def test_remove_file_if_exists(self):
        #remove_file_if_exists(self.filename)
        pass