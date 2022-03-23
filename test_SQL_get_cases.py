import unittest
from modules.get_data import get_cases

data_output = get_cases('1 Jan 2019', '23 mar 2022', '89,16,5,30', '')

class SQLTest(unittest.TestCase):
    def test_get_cases_opened(self):        
        print(data_output)
        self.assertEqual(data_output.columns[0], "CaseID")
        self.assertEqual(data_output.index[0], 19)
    
if __name__ == "__main__":
    unittest.main()