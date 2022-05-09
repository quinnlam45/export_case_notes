import pandas as pd

class PivotTable:

    def __init__(self, pivoted_dataframe):
        self.df = pd.DataFrame(pivoted_dataframe)
        self.no_of_rows = self.df.ndim + self.df.shape[0]

    #row totals
    def add_totals_col(self):
        self.df['Total'] = self.df.sum(axis=1)

    #calculate %
    def add_percent_col(self):
        for df_col in self.df.columns:
            self.df[df_col + ' %'] = (self.df[df_col]/self.df[df_col].sum()).round(2).map('{:03.2f}'.format).astype(float)    

    #col totals

    #sort functions
    def sort_pivot_table(self, sort_on='columns', asc=True):
        axis = 1
        if sort_on == 'rows':
            axis = 0

        self.df.sort_index(axis=axis, ascending=asc, inplace=True)


def make_pivot_table(pivoted_df):
    pivot_table = PivotTable(pivoted_df)
    pivot_table.add_totals_col()
    pivot_table.add_percent_col()

    return pivot_table.df

def pivot_df(df, rows, cols, count_value = "CaseID"):
    df_pivot = pd.pivot_table(df, values=count_value, index=rows, columns=cols, aggfunc=lambda x: x.value_counts().count(), fill_value=0)
    
    return df_pivot
