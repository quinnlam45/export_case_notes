import django
from django.db import connection, Error
import pandas as pd
from modules.dataframe_func import transform_data

# returns DataFrame
def get_cases(start_range, end_range, srv_str, grp_str, case_typ="Opened"):

    try:
        #connection = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER={DESKTOP-TC8EDHO\SQLEXPRESS};DATABASE=4site;Trusted_connection=yes'
        cursor = connection.cursor()

        params = (start_range, end_range, srv_str, grp_str)
        case_type = str(case_typ)
        if case_type == "Opened":
            sql = "EXEC spQLGetCasesOpened @StartRange=%s, @EndRange=%s, @strServiceString=%s, @grpStr=%s"
        elif case_type == "Closed":
            sql = "EXEC spQLGetCasesClosed @StartRange=%s, @EndRange=%s, @strServiceString=%s, @grpStr=%s"
        elif case_type == "Outcomes":
            sql = "EXEC spQLGetClosureOutcomes @StartRange=%s, @EndRange=%s, @strServiceString=%s, @grpStr=%s"
        
        cursor.execute(sql, params)

        #fetch col names from cursor desc
        fieldDesc = cursor.description
    
        field_names = []
        for fieldName in fieldDesc:
            field_names.append(fieldName[0])

        sql_data = []
        sql_data.append(field_names)

        # retrieve data and add to sql_data dict
        row = cursor.fetchone()

        while row:
            sql_data.append(row)
            row = cursor.fetchone()

        data_to_dict = transform_data(sql_data)
        df = pd.DataFrame(data_to_dict)

        return df

    except Error as err:
        print(err)
    finally:
        connection.close()