import unittest
import pandas as pd
from pandas.testing import assert_frame_equal 
from dataframe_func import pivot_df

class TestDataframeFunc(unittest.TestCase):
    dataframe_columns = ['CaseID', 'Referrer', 'Area', 'Risk']
    dataframe_data = [(1, 'MASH', 'Sandwell', 'High'), (2, 'School', 'Dudley', 'Medium'), (3, 'MARAC', 'Sandwell','High')]

    raw_data_df = pd.DataFrame(dataframe_data, columns=dataframe_columns)

    expected_df_columns = {'High': [0, 2], 'Medium': [1, 0],}
    expected_df_index = ['Dudley', 'Sandwell']
    expected_pivoted_df = pd.DataFrame(expected_df_columns, index=expected_df_index).rename_axis(index="Area", columns="Risk")
    
    def test_pivot_df(self):
        pivoted_df = pivot_df(self.raw_data_df, "Area", "Risk")
        assert_frame_equal(self.expected_pivoted_df, pivoted_df)