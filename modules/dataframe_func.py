
import pandas as pd
import numpy as np

# Tranforms SQL data to col labelled dict for DataFrames
def transform_data(sql_data):
    dataframe_dict = {}

    col_names = sql_data[0]
    data_rows = sql_data[1:]

    for x, col in enumerate(col_names):
        column_values = []
        # loop through all data_rows and append item at position x
        for item in data_rows:
            column_values.append(item[x])
        dataframe_dict[col] = column_values
    
    # Set order of categories
    for col in col_names:
        if col == "Month":
            dataframe_dict["Month"] = pd.Categorical(dataframe_dict["Month"], categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
        elif col == "Service risk level":
            dataframe_dict["Service risk level"] = pd.Categorical(dataframe_dict["Service risk level"], categories=["Standard Risk", "Medium Risk", "High Risk", "NULL"], ordered=True)
        
    return dataframe_dict

def filter_df(df, field, filter_value):
    if field and filter_value:
        filtered_df = df[df[field] == filter_value]
        return filtered_df
    else:
        return df

# Pivot dataframe using specified rows and cols
# def pivot_df(df, rows, cols, count_value = "CaseID"):
#     df_pivot = pd.pivot_table(df, values=count_value, index=rows, columns=cols, aggfunc=lambda x: x.value_counts().count(), fill_value=0)
    
#     return df_pivot

def add_percent_col(df):
    for column in df:
        df["%"] = (df[column]/df[column].sum()).round(2).map('{:03.2f}'.format).astype(float)
        # df[column] = df[column].replace([1.0], "100%")
    return df