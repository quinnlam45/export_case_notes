from asyncore import read
import unittest
import datetime
from case_note_func import *
from export_case_notes import *
from excel_module import read_excel_file
from fixture_transform_case_note_func import expected_transformed_case_notes

class CaseNoteFuncTest(unittest.TestCase):

    test_string = "A test string, to test if this can be sliced appropriately. Let's test this!"
    
    def test_return_slice_length(self):
        slice_length = return_slice_length(self.test_string, 11)
        self.assertEqual(14, slice_length)

    def test_return_slice_length_if_char_not_found(self):
        slice_length = return_slice_length(self.test_string, 73)
        self.assertEqual(75, slice_length)

    def test_add_contd_to_sliced_str_list(self):
        str_list = ["First line", "second line", "third line"]
        appended_sliced_str_list = add_contd_to_sliced_str_list_items(str_list)
        self.assertEqual("First line ...", appended_sliced_str_list[0])
        self.assertEqual("[cont'd] second line ...", appended_sliced_str_list[1])
        self.assertEqual("[cont'd] third line", appended_sliced_str_list[2])

    def test_slice_str(self):
        sliced_str_list = slice_str(self.test_string, 11)
        self.assertEqual("A test string, ...", sliced_str_list[0])
        self.assertEqual("[cont'd]  to test if ...", sliced_str_list[1])

    def test_return_copied_rows_for_sliced_str(self):
        current_row = ['TS/TEST', 63108, 1, 2020, datetime.datetime(2020, 6, 23, 0, 0), datetime.time(10, 14), 'One to one support']
        sliced_str_list = ["First line ...", "[cont'd] second line ...", "... last line"]
        expected_result = [
            ['TS/TEST', 63108, 1, 2020, datetime.datetime(2020, 6, 23, 0, 0), datetime.time(10, 14), 'One to one support', "First line ..."],
            ['TS/TEST', 63108, 1, 2020, datetime.datetime(2020, 6, 23, 0, 0), datetime.time(10, 14), 'One to one support', "[cont'd] second line ..."],
            ['TS/TEST', 63108, 1, 2020, datetime.datetime(2020, 6, 23, 0, 0), datetime.time(10, 14), 'One to one support', "... last line"]
        ]
        transformed_rows = return_copied_rows_for_sliced_str(current_row, sliced_str_list)
        self.assertEqual(expected_result, transformed_rows)
    
    def test_transform_case_note_data(self):
        # replace fake SQL data
        pass
        #filename = r"C:\Users\quinn\Documents\Programming\performance_dashboard\performance_dashboard\test_case_notes_transform_data_v1.xlsx"
        #fake_SQL_data = read_excel_file(filename)
        #transformed_data = transform_case_note_data(fake_SQL_data)
        #self.assertEqual(expected_transformed_case_notes, transformed_data)
        #self.assertListEqual(expected_transformed_case_notes, transformed_data)

