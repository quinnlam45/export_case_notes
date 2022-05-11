import unittest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from pivot_table import pivot_df, PivotTable

class TestPivotTable(unittest.TestCase):
    dataframe_columns = ['CaseID', 'Referrer', 'Area', 'Risk']
    dataframe_data = [(1, 'MASH', 'Sandwell', 'High'), (2, 'School', 'Dudley', 'Medium'), (3, 'MARAC', 'Sandwell','High')]

    raw_data_df = pd.DataFrame(dataframe_data, columns=dataframe_columns)

    expected_df_columns = {'High': [0, 2], 'Medium': [1, 0]}
    expected_df_index = ['Dudley', 'Sandwell']
    expected_pivoted_df = pd.DataFrame(expected_df_columns, index=expected_df_index).rename_axis(index="Area", columns="Risk")
    
    def test_pivot_df(self):
        pivoted_df = pivot_df(self.raw_data_df, "Area", "Risk")
        assert_frame_equal(self.expected_pivoted_df, pivoted_df)

    def test_pivot_table_add_totals_col(self):
        expected_totals_series = pd.Series([1,2], name='Total')
        pivot_table = PivotTable(self.expected_pivoted_df)
        pivot_table.add_totals_col()
        # raise exception if total cols does not exist
        total_col_added = pivot_table.df['Total']
        # print(pivot_table.df)
        # check name and values only
        assert_series_equal(expected_totals_series, total_col_added, check_index=False)

    def test_pivot_table_add_percent_col(self):
        pivoted_df_with_totals = self.expected_pivoted_df.copy()
        pivoted_df_with_totals['Total'] = [1, 2]

        pivot_table_add_percent = PivotTable(pivoted_df_with_totals)
        pivot_table_add_percent.add_percent_col()

        #raise exception if does not exist
        high_percent_col = pivot_table_add_percent.df['High %']
        expected_high_percent_col = pd.Series([0.0, 1.0], dtype='float64', name='High %')
        assert_series_equal(expected_high_percent_col, high_percent_col, check_index=False)

        totals_percent_col = pivot_table_add_percent.df['Total %']
        expected_totals_percent_col = pd.Series([0.33, 0.67], dtype='float64', name='Total %')
        assert_series_equal(expected_totals_percent_col, totals_percent_col, check_index=False)

    def test_sort_pivot_table(self):
        expected_sorted_df = pd.DataFrame({'a': [1, 2], 'b': [1, 2], 'c': [1, 2]}, index=self.expected_df_index)

        test_df_for_sorting = pd.DataFrame({'b': [1, 2], 'a': [1, 2], 'c': [1, 2]}, index=self.expected_df_index)
        pivot_table_for_sorting = PivotTable(test_df_for_sorting)
        pivot_table_for_sorting.sort_pivot_table()
        sorting_result = pivot_table_for_sorting.df

        assert_frame_equal(expected_sorted_df, sorting_result)
