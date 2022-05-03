from asyncore import read
import unittest
from case_note_func import *
from excel_module import read_excel_file

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

    def test_transform_case_note_data(self):
        filename = r"C:\Users\quinn\Documents\Programming\performance_dashboard\performance_dashboard\test_case_notes_v1.xlsx"
        fake_SQL_data = read_excel_file(filename)
        transformed_data = transform_case_note_data(fake_SQL_data)
        self.assertEqual("TS/TEST", transformed_data[1][0])