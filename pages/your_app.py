import streamlit as st
import pandas as pd
import numpy as np
import time
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, timezone, timedelta, date
#from google.cloud import firestore
import gspread

def write_google_sheet_x(dt):

    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit?pli=1#gid=1859943936"
    
    # Google Sheets credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
    gc = gspread.authorize(credentials)

    sheet = gc.open_by_url(sheet_url).sheet1
    last_row = len(sheet.get_all_values())+1
    #st.write(dt)

    for i, row in dt.iterrows():  
        if row['Codi Material'] != "":
            words = row['Reservat per'].split("-")
            # Access each word separately
            word1 = words[0]
            word2 = words[1]

            sheet.update_cell(last_row,1, words[0])  #codi client
            sheet.update_cell(last_row,2, words[1])  #nom client
            sheet.update_cell(last_row,3, row['0'])  #TIPUS
            sheet.update_cell(last_row,4, row['Codi Material'])  #codi material
            # sheet.update_cell(last_row,5,  )  #descripcio material
            sheet.update_cell(last_row,6, row['Quantitat'])  #quantitat
            sheet.update_cell(last_row,7, datetime.now().strftime('%d/%m/%Y'))  #data reserva
            print(row['Data inici'])
            sheet.update_cell(last_row,8, row['Data inici'].strftime('%d/%m/%Y'))  #data inici
            sheet.update_cell(last_row,9, row['Data Final'].strftime('%d/%m/%Y') )    #data fi
            sheet.update_cell(last_row,10, 'pendent' )  #estat
            sheet.update_cell(last_row,11, row['Docent'])  #rebut per
            # sheet.update_cell(last_row,12, )  #estat
            # sheet.update_cell(last_row,13, )  #comentari
            last_row = last_row+1
            st.warning('Reserva efectuada amb èxit', icon="👋")


edited_reserva_df_sorted = st.data_editor(st.session_state.expanded_df_sorted,                                                      
                column_config={
                "favorite": st.column_config.CheckboxColumn(
                    "Your favorite?",
                    help="Select your **favorite** widgets",
                    default=False,
                )
            },
            disabled=["widgets"],
            hide_index=True,
            num_rows="dynamic"
            )    

if st.button('Confirmar Reserva'):  
    reserva_df_sorted_filtered = edited_reserva_df_sorted[edited_reserva_df_sorted['Codi Material'] != "RESERVA NO DISPONIBLE"]
    reserva_df_sorted_filtered2 = reserva_df_sorted_filtered[reserva_df_sorted_filtered['Reserva'] == True]
    write_google_sheet_x(reserva_df_sorted_filtered2)

if st.button('Tornar Menu'):
    st.switch_page("main.py")