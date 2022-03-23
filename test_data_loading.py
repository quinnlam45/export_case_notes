import unittest
from modules.excel_module import read_excel_file

filename = "initial_test_data.xlsx"
data_output = read_excel_file(filename)

class LoadDataTest(unittest.TestCase):
    def test_read_excel_file(self):        
        print(data_output)
        self.assertEqual(data_output[0][0], "CaseID")
        self.assertEqual(data_output[1][0], 19)
    
if __name__ == "__main__":
    unittest.main()