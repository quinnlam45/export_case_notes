import unittest
import pandas as pd
from openpyxl import Workbook

from modules.excel_module import df_to_IO

class TestExcelModule(unittest.TestCase):
    def test_df_to_IO(self):
        df_columns = {'High': [2, 5, 6], 'Medium': [7, 3, 2], 'Standard': [0, 3, 2]}
        df_index = ['Sandwell', 'Dudley', 'Walsall']
        df = pd.DataFrame(df_columns, index=df_index).rename_axis(index="Area", columns="Risk")

        io_output = df_to_IO(df)
        print(io_output)
