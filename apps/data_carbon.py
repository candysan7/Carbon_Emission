import streamlit as st
import pandas as pd
from gsheetsdb import connect
import pandas as pd
import numpy as np
import time 
import pymysql
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def app():

    st.sidebar.title("Feedback")
    st.sidebar.info(
        "This an open source project completed for KPMG and we are very open to any **feedback** you have. You are more than welcome to **contribute** your "
        "questions, concerns, and suggestions at "
        "[email](andyxian@usc.edu) or at our "
        "[github](https://github.com/candysan7). "
        # REFERENCE ----- (https://github.com/MarcSkovMadsen/awesome-streamlit). "
    )
    st.sidebar.title("About Us")
    st.sidebar.info(
        """
        This app is maintained by [Andy Xiang](https://www.linkedin.com/in/andy-xiang/). 
        Please feel free to reach out to us if you have any questions. 
        You can learn more about our institution at [www.usc.edu](https://www.usc.edu/).
    """)

    st.title("Data")
    gsheet_url = "https://docs.google.com/spreadsheets/d/19Stp_EFjRXvWFzaLuG1f8qsfZCbzt9oDuCV3NGRE1sM/edit#gid=532282035"
    conn = connect()
    rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
    # df = pd.DataFrame(rows)
    
    column_names = ["id","University_name","Average_SAT","Average_ACT","Weighted_GPA","Admision_rate","Type","Early_Action","Regular_Deadline","Average_Cost","Average_Cost_after_aid","Graduation_rate"]
    # full_resultdf = pd.DataFrame(rows ,columns=column_names) ### need column names 
    full_resultdf = pd.DataFrame(rows)

    # full_resultdf = full_resultdf.drop(['id'],axis=1)
    # full_resultdf = full_resultdf.drop(['Index'],axis=1)
    
    # full_resultdf = full_resultdf.drop(['Index'],axis=1)
    # st.table(full_resultdf)
    # AgGrid(full_resultdf)

    ####SOURCE: https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
    gb = GridOptionsBuilder.from_dataframe(full_resultdf)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gridOptions = gb.build()

    grid_response = AgGrid(
        full_resultdf,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True,
        height=650, 
        width='100%',
        reload_data=True)
