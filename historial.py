import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import numpy as np
import time
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, timezone, timedelta, date
#from google.cloud import firestore
import gspread


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

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

def app():

    from streamlit_calendar import calendar

    # LECTURA RESERVES a df_reserves
    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
    if 'df_reserves' not in st.session_state:
        st.session_state.df_reserves = None
        st.session_state.df_reserves = read_google_sheet_x(sheet_url)
        st.write("Reserves loaded")

    filtered_df_reserves_1 = st.session_state.df_reserves[st.session_state.df_reserves['estat']=="pendent"]

    st.write(filtered_df_reserves_1)
    resources = []
    calendar_events = []
    resource = ["id","building"]
    calendar_event = ["title","start","end","resourceID","display"]
    for index, row in st.session_state.df_reserves.iterrows(): 
        # product_code_selected = row['0']
        # quantitat = row['Quantitat']
        # inici = row['Data Inici']
        # final = row['Data Final']
        # reserva_df.loc[index, 'Codi Material'] = row_as[0][1]
        # reserva_df.loc[index, 'Reservat per'] = selected_codi
        # reserva_df.loc[index, 'Docent'] = selected_docent
        # reserva_df.loc[index, 'Reserva'] = False
        if row[9] == "pendent":
            #st.write(row)
            resource = {
                #"id": f"{row[0]} - {row[1]}",  # f"Element at index {index} and column {column}: {row[column]}"
                #"building": f"{row[2]}"  # row[2] = TIPUS
                "id": f"{row[2]} - {row[3]} - {row[0]}",  # f"Element at index {index} and column {column}: {row[column]}"
                "building": f"{row[0]} - {row[1]}"  # row[2] = TIPUS

            }
            resources.append(resource)
            formatted_ini1= row[7].replace( "/", "-")
            formatted_ini = formatted_ini1[-4:] + "-" + formatted_ini1[3:5] + "-" + formatted_ini1[:2]

            formatted_end1 = row[8].replace( "/", "-")
            formatted_end = formatted_end1[-4:] + "-" + formatted_end1[3:5] + "-" + formatted_end1[:2]
            calendar_event = {
                "title": f"Reserva - {row[3]}",
                "start": formatted_ini,
                "end": formatted_end,
                "resourceId": f"{row[2]} - {row[3]} - {row[0]}",
                "display": 'block'
            }
            calendar_events.append(calendar_event)

    #st.write(resource)
    #st.write(calendar_events)

    calendar_options = {
        "editable": "true",
        "selectable": "true",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            #"right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            "right": "resourceTimelineMonth",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        "initialView": "resourceTimelineMonth",
        "resourceGroupField": "building",
        "resources": resources,
        # "resources": [
        #     {"id": "a", "building": "Building AA", "title": "Building A"},
        #     {"id": "b", "building": "Building A", "title": "Building B"},
        #     {"id": "c", "building": "Building B", "title": "Building C"},
        #     {"id": "d", "building": "Building B", "title": "Building D"},
        #     {"id": "e", "building": "Building C", "title": "Building E"},
        #     {"id": "f", "building": "Building C", "title": "Building F"},
        # ],
    }
    # calendar_events = [
    #     {
    #         "title": "Event 1",
    #         "start": "2024-03-01T08:30:00",
    #         "end": "2024-03-05T10:30:00",
    #         "resourceId": "a",
    #     },
    #     {
    #         "title": "Event 2",
    #         "start": "2024-03-10T07:30:00",
    #         "end": "2024-03-16T10:30:00",
    #         "resourceId": "b",
    #     },
    #     {
    #         "title": "Event 3",
    #         "start": "2024-03-08T10:40:00",
    #         "end": "2024-03-1931T12:30:00",
    #         "resourceId": "a",
    #     }
    # ]
    custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """

    st.write("--------------------------")
    calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
    #st.write(calendar)

app()