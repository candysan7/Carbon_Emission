import streamlit as st
import pandas as pd
from gsheetsdb import connect

def app():
### Sidebar Stuff 
   
    st.sidebar.title("Feedback")
    st.sidebar.info(
        "This an open source project completed for KPMG and we are very open to any **feedback** you have. You are more than welcome welcome to **contribute** your "
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
        You can learn more about instiution at [www.usc.edu](https://www.usc.edu/).
    """)


### Title

    st.title("Calculate my Carbon Emission Trip")
    gsheet_url = "https://docs.google.com/spreadsheets/d/19Stp_EFjRXvWFzaLuG1f8qsfZCbzt9oDuCV3NGRE1sM/edit#gid=532282035"
    conn = connect()
    rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
    df = pd.DataFrame(rows)

    # st.write(df)
    # with st.form(key='bkey'):
    car_make = list(sorted(df['Make'].unique()))
    car_make_select = st.selectbox('Car Manufacturer',car_make) #1ST SELECT BOX 
    # car_make_select = str(car_make_select)
    #     
    car_model_df = df.loc[(df['Make']==car_make_select)] 
    
    car_model = list(sorted(car_model_df['Model'].unique()))
    car_model_select = st.selectbox('Car Model',car_model)

    model_make_df = car_model_df.loc[car_model_df["Model"]==car_model_select]

    miles_drive = st.number_input('Miles Driven', min_value=0.0, max_value=500.0, step=1e-6,format="%.2f")

    carbon_usage = list(model_make_df['_12'])[0] ### conversion for df to column name is not right

    # st.write(carbon_usage)

    if st.button('Calculate My Carbon Emission!'): 

        average_carbon = 160 ### not sure of this value 
    # if st.form_submit_button('Calculate My Carbon Emission!'):
        carbon_emission = round(miles_drive*carbon_usage,2)
        lb_to_gram = (1/453.592) ####(lbs/grams)
        carbon_emission = carbon_emission * lb_to_gram # convert from grams to lbs 
        carbon_emission = str(round(carbon_emission,2))
        display_emission = "Your trip added " + carbon_emission + " pounds(lbs) of C02 to the atmosphere"
        st.subheader(display_emission)

        if miles_drive: 
            percent_diff = (average_carbon - carbon_usage) / average_carbon
            percent_diff = round((percent_diff*100),2)
    

            if percent_diff >=0: 
                percent_diff= str(percent_diff)
                st.success(percent_diff+'%'+ ' lower than U.S. average')
            else: 
                percent_diff= str(percent_diff)
                st.error(percent_diff+'%' + ' higher than U.S. average')