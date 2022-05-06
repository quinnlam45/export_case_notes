import unittest
import pandas as pd
from dataframe_func import pivot_df

class TestDataframeFunc(unittest.TestCase):
    dataframe_columns = ['CaseID', 'Referrer', 'Area', 'Risk']
    dataframe_data = [(1, 'MASH', 'Sandwell', 'High'), (2, 'School', 'Dudley', 'Medium'), (3, 'MARAC', 'Sandwell','High')]

    df = pd.DataFrame(dataframe_data, columns=dataframe_columns)
    
    def test_pivot_df(self):
        pivoted_df = pivot_df(self.df, "Area", "Risk")
        self.assertEqual(2, pivoted_df["High"].loc["Sandwell"])
