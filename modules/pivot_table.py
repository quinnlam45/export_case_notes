


class Pivot_table:
    #init method
    def __init__(self, dataframe, name = None):
        self.name = name
        self.df = dataframe

    #add % cols
    def add_empty_percent_col(self):
        for df_col in self.df.columns:
            self.df[df_col + ' %'] = np.nan

    #calculate %

    #row totals

    #col totals

    #sort functions

