import django
from django.db import Error #,connection
import pyodbc
import pandas as pd
import numpy as np

# returns DataFrame
def get_cases(start_range, end_range, srv_str, grp_str, case_typ="Opened"):

    try:
        #connection = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER={DESKTOP-TC8EDHO\SQLEXPRESS};DATABASE=4site;Trusted_connection=yes'
        conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=4site-2019;DATABASE=4site;Trusted_Connection=yes;"
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        params = (start_range, end_range, srv_str, grp_str)
        case_type = str(case_typ)
        #if case_type == "Opened":
        #    sql = "EXEC spQLGetCasesOpened @StartRange=%s, @EndRange=%s, @strServiceString=%s, @groupString=%s"
        #elif case_type == "Closed":
        #    sql = "EXEC spQLGetCasesClosed @StartRange=%s, @EndRange=%s, @strServiceString=%s, @groupString=%s"
        #elif case_type == "Outcomes":
        #    sql = "EXEC spQLGetClosureOutcomes @StartRange=%s, @EndRange=%s, @strServiceString=%s, @groupString=%s"
        if case_type == "Opened":
            sql = "EXEC spQLGetCasesOpened @StartRange=?, @EndRange=?, @strServiceString=?, @groupString=?"
        elif case_type == "Closed":
            sql = "EXEC spQLGetCasesClosed @StartRange=?, @EndRange=?, @strServiceString=?, @groupString=?"
        elif case_type == "Outcomes":
            sql = "EXEC spQLGetClosureOutcomes @StartRange=?, @EndRange=?, @strServiceString=?, @groupString=?"
        
        cursor.execute(sql, params)

        #fetch col names from cursor desc
        fieldDesc = cursor.description
    
        field_names = []
        for fieldName in fieldDesc:
            field_names.append(fieldName[0])

        sql_data_rows = []

        # retrieve data and add to sql_data dict
        row = cursor.fetchone()

        while row:
            sql_data_rows.append(list(row))
            row = cursor.fetchone()

        df = pd.DataFrame(sql_data_rows, columns=field_names)
        #print(field_names)
        #print(sql_data_rows)

        return df

    except Error as err:
        print(err)
    finally:
        connection.close()