
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, timezone, timedelta, date
from google.cloud import firestore


# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Function to read data from Google Sheet
def read_google_sheet_x(sheet_url):
    
    # Use credentials to create a client to interact with Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
    gc = gspread.authorize(credentials)

    # Open the Google Sheet using its URL
    worksheet = gc.open_by_url(sheet_url).sheet1

    # Get the data as a Pandas DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df

def write_google_sheet_x(index, docent, comentari, flag_reserva):

    #print(f'index a write: {index}')
    if flag_reserva == True:
        sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit?pli=1#gid=1859943936"

        # Google Sheets credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url(sheet_url).sheet1
        
        last_row = len(sheet.get_all_values())+1
        #st.write(dt)
        # Example datetime object
        dt = datetime.now().strftime('%a %d %b %Y, %I:%M%p')
        

        for i in range(last_row):
            if i == index :
                sheet.update_cell(index,10, 'retornat' )  #estat       
                sheet.update_cell(index,13, docent  )  #docent rep producte
                sheet.update_cell(index,12, comentari )  #docent rep producte
                sheet.update_cell(index,14, dt )  #docent rep producte
                st.warning('Reserva retornada amb èxit', icon="👋")
    else:
        st.warning('Marqueu la reserva que voleu confirmar i premeu Confirmar Reserva')
        
def app():

    concat = ""
    unique_clients_code = []
    unique_clients_code.append(" ")

    unique_docents_code = []
    unique_docents_code.append(" ")

    unique_clients_name = []
    unique_clients_name.append(" ")

    selected_codi = ""
    ambit = ""

    # LOAD CLIENTS FROM GOOGLE SHEET
    sheet_url = "https://docs.google.com/spreadsheets/d/1uMANAvFf14030QZHner0incZyE2Tj9ex04Uiu1H-ldE/edit#gid=0"
    if 'df_clients' not in st.session_state:
        st.session_state.df_clients = None
    df_clients = read_google_sheet_x(sheet_url)
    #st.session_state.df_clients = df_clients
    #st.write("Clients loaded")
    
    for index, row in df_clients.iterrows():
        for column in df_clients.columns:
            
            if column == "Nom":
                nom = row[column]
                #st.write(f"Element at index {index} and column {column}: {row[column]}")
                #st.write(nom)
            if column == "Alumne":
                alumne = row[column]
                #st.write(f"Element at index {index} and column {column}: {row[column]}")
                #st.write(alumne)
            if column == "AP":
                ambit =row[column]
                
        concat = str(alumne) + " - "+ nom
        if ambit == "P":
            concatp = str(alumne) + " - "+ nom
            unique_docents_code.append(concatp)
        #st.write(concat)
        unique_clients_code.append(concat)

    unique_docents_code.sort
    selected_codi_docent = st.selectbox('Personal Docent que recepciona material:', unique_docents_code)
    if selected_codi_docent != " ":
        docent = selected_codi_docent
        # st.write("Escollit", selected_codi_docent)   
        # if selected_codi > 0:
        separator = " - "
        part = selected_codi_docent.split(separator)
        # st.write(" Part: ", part)
        # st.write(part[0])
        selected_codi_docent = int(part [0])        
        # st.write("Escollit codi", selected_codi_docent)  


    unique_clients_code.sort
    selected_codi_reservador = st.selectbox('Persona que retorna material:', unique_clients_code)
    if selected_codi_reservador != " ":
        # st.write("Escollit", selected_codi_reservador)
        # if selected_codi > 0:
        separator = " - "
        part = selected_codi_reservador.split(separator)
        # st.write(" Part: ", part)
        # st.write(part[0])
        selected_codi_reservador = int(part [0])        
        # st.write("Escollit codi", selected_codi_reservador)  


            #df_reserves = db.collection("Reserves")
            #query = db.collection('Reserves').where('Client', '==', selected_codi_reservador)

            # LOAD RESERVES FROM GOOGLE SHEET

    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
    #if 'df_reserves' not in st.session_state:
    #    st.session_state.df_reserves = None

    df_reserves = read_google_sheet_x(sheet_url)
    #st.write(df_reserves)

    filtered_df_prod_0 = df_reserves[df_reserves['client']==selected_codi_reservador]
    filtered_df_prod = filtered_df_prod_0[filtered_df_prod_0['estat']=="pendent"]


    for row in filtered_df_prod:
        filtered_df_prod['producte retornat'] = False
        filtered_df_prod['estat retorn'] = " "
    edited_filtered_df_prod = st.data_editor(filtered_df_prod, column_order=("producte retornat","estat retorn", "client", "nom","material", "data_inici", "data_fi"))
    
    if st.button('RETORN'):
        for index, row in edited_filtered_df_prod.iterrows():  # index 0 i 1  
            if row['producte retornat'] == True:
                if row['estat retorn'] == " ":
                    st.warning("Indica l'estat del material retornat i prem 'RETORN'")
                else:
                    #print(f'index : {index}')
                    #print(f'Line 405: edited df: {reserva_df}')
                    write_google_sheet_x(index+2, docent, row['estat retorn'], row['Reserva'])
      
    
