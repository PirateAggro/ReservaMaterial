import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import gspread
from google.cloud import firestore
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import  retorn, historial, dadesmestres, materials, reserva_fb_Boot, reserva, app3

st.set_page_config(
    page_title="Gestió Reserves",
    page_icon="👋",
    layout="wide",
    
)

# FUNCTIONS DEFINITION

# # Function to read data from Google Sheet
# def read_google_sheet_x(sheet_url):
    
#     # Use credentials to create a client to interact with Google Drive API
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
#     gc = gspread.authorize(credentials)

#     # Open the Google Sheet using its URL
#     worksheet = gc.open_by_url(sheet_url).sheet1

#     # Get the data as a Pandas DataFrame
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)

#     return df

# MULTIPAGE MENU DEFINITION

class Multiapp:
    def __ini__(self):
        self.apps = []
    def add_app(self,title,funcion):
        self.apps.append({
            "title": title,
            "function": function
        })

    # CHAT
    def run():  

        # Initialization
        if 'key' not in st.session_state:
            st.session_state['flag_fixed'] = ""
        with st.sidebar:
            app = option_menu(
                menu_title='Menu',
                options=["Title","Reserva", "Retorn", "Historial"],
                menu_icon="cast",
                default_index=0
            )

        if app == 'Title':
            st.image('sunrise.jpeg', caption='Sunrise by the mountains')

        if app == 'Reserva':
            app3.app()

        if app == 'Retorn':
            retorn.app()

        if app == 'Historial':
            reserva.app()


    '''
    NOSTRA
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Menu',
                options=["Title","Reserva", "Retorn", "Historial"],
                menu_icon="cast",
                default_index=0
            )
        ##my_expander = st.expander(label='Expand me')
        ##my_expander.write('Hello there!')
        ##clicked = my_expander.button('Click me!')
        if app=='Title':
                    st.image('sunrise.jpeg', caption='Sunrise by the mountains')


                    # LOAD PRODUCTS FROM GOOGLE SHEET
                    #sheet_url = "https://docs.google.com/spreadsheets/d/10OJjKforD1t0VSG1ynpa5QlQ2WbvmXDCGz8R4yxkoXM/edit#gid=0"

                    # if 'df_products' not in st.session_state:
                    #     st.session_state.df_products = None
                    # df_products = read_google_sheet_x(sheet_url)
                    # st.session_state.df_products = df_products
                    # st.write("Products loaded")



                    # # LOAD CLIENTS FROM GOOGLE SHEET
                    # sheet_url = "https://docs.google.com/spreadsheets/d/1uMANAvFf14030QZHner0incZyE2Tj9ex04Uiu1H-ldE/edit#gid=0"
                    # if 'df_clients' not in st.session_state:
                    #     st.session_state.df_clients = None
                    # df_clients = read_google_sheet_x(sheet_url)
                    # st.session_state.df_clients = df_clients
                    # st.write("Clients loaded")


                    # # LOAD BOOKINGS FROM GOOGLE SHEET
                    # sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
                    # if 'df_bookings' not in st.session_state:
                    #     st.session_state.df_bookings = None

                    # df_bookings = read_google_sheet_x(sheet_url)
                    # st.session_state.df_bookings = df_bookings
                    # #st.dataframe(df_bookings)
                    # st.write("Bookings loaded")

        if app=='Reserva':
            app3.app()
        if app=='Retorn':
            retorn.app()
        if app=='Historial':
            reserva.app()
    run()
    '''
    run()