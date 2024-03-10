import streamlit as st
import pandas as pd
import plotly_express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, timezone, timedelta, date
from google.cloud import firestore
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid import GridOptionsBuilder

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Function to read data from Google Sheet
def read_google_sheet(sheet_url):
    
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

def app():

    st.write("Historial")

    concat = ""
    unique_clients_code = []
    unique_clients_code.append(" ")

    unique_clients_name = []
    unique_clients_name.append(" ")

    selected_codi = ""
    ambit = ""

    df_reserves = db.collection("Reserves")

    #query = db.collection('Reserves').where('Material', '==', "")
    #docs = query.stream()
    # Delete the documents
    #deleted_count = 0
    #for doc in docs:
    #    doc.reference.delete()
    #    deleted_count += 1
    #st.write(deleted_count)

    #query = collection_ref.where("field1", "==", condition1).where("field2", "==", condition2)
    query = db.collection('Reserves').where('Estat_entrega', '==', "pendent")
    reserva_id = []
    reserva_material = []
    reserva_descripcio = []
    reserva_client = []
    reserva_nom = []
    reserva_inicial = []
    reserva_inicial_date = []
    reserva_final_date = []
    reserva_final = []
    reserva_estat = []
    reserva_issue = []

    # Personal docent que fa la recepció

    for doc in query.stream():
        document = doc.id
        document2 = doc.reference
        for field, value in doc.to_dict().items():
            if field == 'Client':
                client = value
            if field == 'Material':
                material = value
            if field == 'Descripció':
                descripció = value
            if field == 'Data_inici':
                inici = value
            if field == 'Data_fi':
                final = value
            if field == 'Nom':
                nom = value
            if field == 'Estat_entrega':
                estat = value
        if estat == "pendent" :
            mat = material + " - "+ descripció
            cli = str(client) + " - " + nom
            reserva_id.append(document)
            reserva_material.append(mat)
            reserva_client.append(cli)
            reserva_inicial.append(inici)
            reserva_inicial_date.append(datetime.strptime(inici, "%d/%m/%Y"))
            reserva_final_date.append(datetime.strptime(final, "%d/%m/%Y"))
            reserva_final.append(final)
            reserva_estat.append(estat)
            reserva_issue.append("Incidència")

    new_data = {
    'key': reserva_id,
    'Material': reserva_material,
    'Client': reserva_client,
    'Inici': reserva_inicial,
    'Final': reserva_final,
    }

    new_data2 = {
    'key': reserva_id,
    'Material': reserva_material,
    'Client': reserva_client,
    'Inici_date' : reserva_inicial_date,
    'Final_date' : reserva_final_date,
    }

    # AGGRID PART -------------------------------------------------------------            
    # df2 = pd.DataFrame(new_data)
    # AgGrid(df2)
    data2 = new_data
    df = pd.DataFrame(data2)
    #grid_return = AgGrid(df, editable=True)
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(
        flex=1,
        minWidth=100,
        maxWidth=500,
        resizable=True,
    )
    gd.configure_column('Material', editable=True)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    #gd.configure_auto_height(autoHeight=: True)

    gridoptions = gd.build()

    grid_table = AgGrid(df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    #df2 = pd.DataFrame(new_data2)

    fig = px.timeline(df2, x_start="Inici_date", x_end="Final_date", y="key")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    fig.show()
