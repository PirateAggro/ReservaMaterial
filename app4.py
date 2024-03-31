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

Assigned_product = []


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
            sheet.update_cell(last_row,8, row['Data Inici'].strftime('%d/%m/%Y'))  #data inici
            print(row['Data inici'])
            sheet.update_cell(last_row,9, row['Data Final'].strftime('%d/%m/%Y') )    #data fi
            sheet.update_cell(last_row,10, 'pendent' )  #estat
            sheet.update_cell(last_row,11, row['Docent'])  #rebut per
            # sheet.update_cell(last_row,12, )  #estat
            # sheet.update_cell(last_row,13, )  #comentari
            last_row = last_row+1
            st.warning('Reserva efectuada amb èxit', icon="👋")

def check_reserva(product_code_selected,quantitat, start_date2, end_date2, df_products):

    # Recuperar full reserves actualitzat
    df_reserves = []
    #print(f'df_reserves entrant check_reserva {df_reserves}')
    #df_reserves = df_reserves.drop(df_reserves.index)
    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit?pli=1#gid=1859943936"
    if 'df_reserves' not in st.session_state:
        st.session_state.df_reserves = None
    df_reserves = read_google_sheet_x(sheet_url)
    #print(f'df_reserves despres google read {df_reserves}')

    Assigned_flag = " "
    filtered_df_productes_0 = []
    filtered_df_productes_1 = []
    Assigned_product = []

    # Recuperar tots els productes del tipus seleccionat
    #filtered_df_reserves_1 = df_reserves[df_reserves['estat']=="pendent"]
    #filtered_df_reserves = filtered_df_reserves_1[filtered_df_reserves_1['TIPUS']==product_code_selected]
    filtered_df_productes_0 = df_products[df_products['Producte']==product_code_selected]
    filtered_df_productes_1 = filtered_df_productes_0[filtered_df_productes_0['estat']=="disponible"]
    #st.write(filtered_df_productes_1)
  
    # si algun producte no te reserva, s'assigna

    for _ in range(1,quantitat+1):
        next_loop = False
        Assigned_flag = " "

        for index, row in filtered_df_productes_1.iterrows(): 
            next_loop = False
            producte = row['Codi']

            #if producte in Assigned_product:   # el producte ja ha estat prèviament assignat
            #    next_loop = True
            #    st.write(producte, "ja assignat prèviament")
            #st.write(row['Codi'], " - ", Assigned_product)
            for row in Assigned_product:
                if row[1] == producte:
                    next_loop = True
                    #st.write(producte, "ja assignat prèviament")

            if next_loop == False:
                filtered_df_reserves_1 = df_reserves[df_reserves['estat']=="pendent"]
                filtered_df_reserves = filtered_df_reserves_1[filtered_df_reserves_1['material']==producte]
                #st.write(filtered_df_reserves)     
                if filtered_df_reserves.empty and Assigned_flag == " ":
                    new_row = [product_code_selected, producte]
                    Assigned_product.append(new_row)
                    Assigned_flag = "x"
                    #st.write(Assigned_product)


            if Assigned_flag == " " and next_loop == False:  # tots els codis tenen alguna reserva --> mirar dates

                flag_check_data = ""
                flag_validesa_reserva = False
                product_assigned = ""
                # reserves pendents d'aquell tipus de codi
                filtered_df_reserves_1 = df_reserves[df_reserves['estat']=="pendent"]
                #filtered_df_reserves = filtered_df_reserves_1[filtered_df_reserves_1['TIPUS']==product_code_selected]
                filtered_df_reserves = filtered_df_reserves_1[filtered_df_reserves_1['material']==producte]

                #query_check = db.collection('Reserves').where('Material', '==', product_code_selected).where('Estat_entrega', '==', 'pendent')
                flag_check_data = ""
                for index, row in filtered_df_reserves.iterrows(): 
                #for doc in query_check.stream():

                    Data_Inici = row['data_inici']
                    Data_Inici2 = pd.to_datetime(Data_Inici, format='%d/%m/%Y')
                    #st.write(Data_Inici2)
                    Data_Final = row['data_fi']
                    Data_Final2 = pd.to_datetime(Data_Final, format='%d/%m/%Y')

                    if Data_Inici2.date() <= start_date2 <= Data_Final2.date() or Data_Inici2.date() <= end_date2 <= Data_Final2.date():
                        #st.write("La reserva no és possible.")
                        flag_validesa_reserva = False
                        flag_check_data = "X"
                    elif start_date2 <= Data_Inici2.date() and end_date2 >= Data_Final2.date():
                        #st.write("La reserva no és possible.")
                        flag_validesa_reserva = False
                        flag_check_data = "X"
                        #Assigned_product = " "
                    else:
                        if flag_check_data == "":
                            flag_validesa_reserva = True 
                            #st.write("La reserva sí és possible.")
                    
                if flag_validesa_reserva == True:    
                    new_row = [product_code_selected, row['material']]
                    Assigned_product.append(new_row)
                    Assigned_flag = "X"



    return Assigned_product


def app():

    # st.set_page_config(
    #     page_title="Reserva Material",
    #     layout="wide"
    # )


    # LECTURA RESERVES a df_reserves
    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
    if 'df_reserves' not in st.session_state:
        st.session_state.df_reserves = None
        st.session_state.df_reserves = read_google_sheet_x(sheet_url)
    st.write("Reserves loaded")

    # LECTURA CLIENTS A df_clients

    sheet_url = "https://docs.google.com/spreadsheets/d/1uMANAvFf14030QZHner0incZyE2Tj9ex04Uiu1H-ldE/edit#gid=0"
    if 'df_clients' not in st.session_state:
        st.session_state.df_clients = None
        st.session_state.df_clients = read_google_sheet_x(sheet_url)
    st.write("Clients loaded")

    # LECTURA PRODUCTES A df_products

    sheet_url = "https://docs.google.com/spreadsheets/d/10OJjKforD1t0VSG1ynpa5QlQ2WbvmXDCGz8R4yxkoXM/edit#gid=0"

    if 'df_products' not in st.session_state:
        st.session_state.df_products = None
        st.session_state.df_products = read_google_sheet_x(sheet_url)

    st.write("Products loaded") 

    if 'count' not in st.session_state:
        st.session_state.count = 0

    # VARIABLES DEFINITION

    unique_clients_code = []
    unique_clients_code.append(" ")
    unique_docents_code = []
    unique_docents_code.append(" ")
    unique_clients_name = []
    unique_clients_name.append(" ")
    unique_products_code = []
    unique_products_code.append(" ")
    unique_products_type = []
    unique_products_type.append(" ")
    unique_products_docents_type = []
    unique_products_docents_type.append(" ")
    reserves_check = ""
    ambit = " "
    data = []

    # LAYOUT DEFINITION 

    esquerra, dreta = st.columns(2)

    # STYLE OF TABLE CLIENTS

    # style
    # th_props = [
    # ('font-size', '14px'),
    # ('text-align', 'center'),
    # ('font-weight', 'bold'),
    # ('color', '#6d6d6d'),
    # ('background-color', '#c4ffff')
    # ]
                                
    # td_props = [
        
    # ('font-size', '12px'),
    # ('background-color', '#f0f0f0')
    # ]

    # td_props_senar = [
    # ('font-size', '12px'),
    # ('background-color', '#000000')
    # ]
                                    
    # styles = [
    # dict(selector="th", props=th_props),
    # dict(selector="td", props=td_props)
    # ]

    # END STYLE CLIENTS TABLE

    # -------------------------------------------------------
    # GENERATE SELECTBOX PER RESERVADOR I DOCENT

    for index, row in st.session_state.df_clients.iterrows():
        for column in st.session_state.df_clients.columns:            
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

        if str(alumne) != "":
            concat = str(alumne) + " - "+ nom
            if ambit == "P":
                concatp = str(alumne) + " - "+ nom
                unique_docents_code.append(concatp)
            unique_clients_code.append(concat)



        
    with esquerra:
        selected_codi = st.selectbox('Reserva a nom de:', unique_clients_code)
        if selected_codi:
            #parts = selected_codi.split('-')
            position = selected_codi.find('-')
            if position != -1:
                substring = selected_codi[:position]    
                # st.write(substring)
                subint = int(substring.strip())
                # st.write(substring)
                filtered_df = st.session_state.df_clients[st.session_state.df_clients['Alumne']==subint]
                nom_codi = filtered_df['Nom']
                ambit_a = filtered_df['AP']
                ambit_1 = ambit_a.iloc[0]
                for idx in filtered_df.index:
                    nom_codi_index = idx
                
                #filtered_df_prod = df_products[df_products['Tipus']==ambit_a]
                #st.write(filtered_df_prod)


    # for row in df_clients.itertuples(index=False):
    #     for value in row:

    with dreta:       
            selected_docent = st.selectbox('Docent que autoritza:', unique_docents_code)
            #button_clicked_docent = st.button("Seleccionat")
            if selected_docent != " ":
                position_d = selected_docent.find('-')
                if position != -1:
                    substring_d = selected_docent[:position_d]    
                    #st.write(substring_d)
                    subint_d = int(substring_d.strip())
                    #st.write(substring_d)
                    filtered_df_d = st.session_state.df_clients[st.session_state.df_clients['Alumne']==subint_d]
                    nom_codi_d = filtered_df_d['Nom']
                    #st.write("nom_codi_d :", nom_codi_d)
                    for idx_d in filtered_df_d.index:
                        nom_codi_d_index = idx_d

    if selected_codi != "" and selected_codi != " " and selected_docent != " ":
        if ambit_1 == "A":
            filtered_df_prod = st.session_state.df_products[st.session_state.df_products['TIPUS']==ambit_1]
        else:
            filtered_df_prod = st.session_state.df_products

        # FILTERED_DF_PROD CONTE TOTS TIPUS (SI PROFE) O NOMÉS ELS D'ALUMNES
        filtered_df_prod.sort_values(by='TIPUS')

        # NO DUPLICATS
        unique_products_list = filtered_df_prod['Producte'].unique()

        # ES DEFINEIX COM A DATAFRAME I S'AFEGEIXEN VALORS PER DEFEECTE (QTY, DATA INICIAL / FINAL I STATUS)
        unique_df = pd.DataFrame(unique_products_list)
        for index, row in unique_df.iterrows(): 
            unique_df['Quantitat'] = 1
            unique_df['Data Inici'] = datetime.now().date()
            unique_df['Data Final'] = datetime.now().date() + timedelta(days=7) 
            unique_df['Reserva'] = False

        # USUARI SELECCIONA TIPUS MATERIAL, QUANTITAT A RESERVAR I DATES
        edited_df = st.data_editor(unique_df,
                        column_config={
                        "Reserva": st.column_config.CheckboxColumn(
                            "Selecciona Material",
                            help="Select your **favorite** widgets",
                            default=False,
                        )
                    },
                    disabled=["widgets"],
                    hide_index=True,
                    num_rows="dynamic",
                    )  
           
        # DATAFRAME EDITAT PER L'USUARI
        reserva_df = edited_df[edited_df['Reserva']==True]
        codi_assignat = []

        # ASSIGNACIÓ DE PRODUCTES  --------------------------------------------------- boto generar proposta
        List_codis_assignats = []

        if st.button("Generar proposta"):
            st.session_state.count += 1
            codi_assignat = []
            for index, row in reserva_df.iterrows(): 
                index_original = index
                product_code_selected = row['0']
                quantitat = row['Quantitat']
                inici = row['Data Inici']
                final = row['Data Final']

                # CHECK RESERVA I ASSIGNACIÓ DE CODI DE PRODUCTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                codi_assignat =  check_reserva(product_code_selected, quantitat, inici, final, st.session_state.df_products)


                if len(codi_assignat) == 0:
                    st.write('RESERVA NO DISPONIBLE')
                else:
                    st.write(codi_assignat)
                    List_codis_assignats.append(codi_assignat)

                    # CODI ASSIGNAT ES 0: TIPUS 1: CODI

            # Create an empty list to store duplicated rows
            expanded_rows = []

            # Iterate over each row in the DataFrame
            for index, row in reserva_df.iterrows():
                item = row['0']
                quantity = row['Quantitat']
                DataInici = row['Data Inici']
                DataFinal = row['Data Final']
                Reserva = False 
                Assignat = False
                # Duplicate the row based on the quantity and append to the list
                for _ in range(quantity):
                    expanded_rows.append({'0': item, 'Quantitat': 1,'Data inici': DataInici, 'Data Final': DataFinal, 'Reserva':  Reserva, 'Assignat': Assignat, 'Codi Material': "", 'Reservat per': "", 'Docent': ""})
            
            expanded_df = pd.DataFrame(expanded_rows)
            st.write(expanded_df)


            codi_ass = ""
            index_1 = 90
            data_ini = datetime.now().date()
            data_fini = datetime.now().date()
            st.write("-------------------------")
            st.warning("Marqueu el flag de Reserva per confirmar els materials entregats")
            st.warning("i modifiqueu el codi de material assignat en cas necessari.")
            st.warning("Després premeu el Botó 'Confirmar Reserva'")
            print(f"---- List_codis_assignats {List_codis_assignats}")
            tipus = ""
            tipus_old = ""
            codi = ""
            flag_first = "X"
            control_quantitat = 0
            for index_ca, row_as in enumerate(List_codis_assignats):
                # print(f"List at index_ca {index_ca}")
                # print(f"First field value at index {index_ca}: {row_as[0][0]}")
                # print(f"First field value at index {index_ca}: {row_as[0][1]}")
                print(f"List at index {index_ca}: {row_as}")
                tipus_old = ""
                for inner_list in row_as: 
                    print(f"Inner list:")

                    for element in enumerate(inner_list):
                        print(f"- {element}" )
                        if element[0]==0:
                            tipus = element[1]
                            print(f"tipus - {tipus}" )     
                            # loop a reserves df i comparar TIPUS.                       
                        if element[0]==1:
                            codi = element[1]
                            print(f"codi - {codi}" )     
                            flag_first = "X"        
                            codi_old = ""             
                            for index, row in expanded_df.iterrows():  # index 0 i 1    
                                if tipus_old == tipus:
                                    index = index + 0
                                #if row['0'] == tipus and flag_first == "X":     
                                if row['0'] == tipus and row['Assignat'] == False and flag_first == "X":     
                                    print(f"Assignat - {Assignat} codi - {codi} index - {index}")                             
                                    expanded_df.loc[index,'Codi Material'] = codi
                                    expanded_df.loc[index,'Reservat per'] = selected_codi               
                                    expanded_df.loc[index,'Docent'] = selected_docent 
                                    expanded_df.loc[index,'Assignat'] = True

                                    flag_first = ""
                                    tipus_old = tipus

            st.write('--------------------')
            st.write(expanded_df)
            # un cop construit LOOP AL DATAFRAME quan Reserva = True ---> codis que no tenen
            # assignació i per tant no es pot fer reserva
            for index, row in expanded_df.iterrows():  # index 0 i 1       
                if row['Assignat'] == False:
                    expanded_df.loc[index, 'Codi Material'] = "No Material Disponible"
                    expanded_df.loc[index, 'Reserva'] = False
                    expanded_df.loc[index, 'Data inici'] = ""
                    expanded_df.loc[index, 'Data Final'] = ""


            pd.set_option('display.max_columns', None)  # Display all columns


            expanded_df_sorted = []
            #st.data_editor

            if 'expanded_df_sorted' not in st.session_state:
                st.session_state.expanded_df_sorted = None
            st.session_state.expanded_df_sorted = expanded_df.sort_values(by='0')


            st.switch_page("pages/your_app.py")


            # if st.button('Confirmar Reserva'):  

            #     print(f'Linia 490: {expanded_df_sorted}')
            #     expanded_df_sorted_filtered = expanded_df_sorted[expanded_df_sorted['Codi Material'] != ""]
            #     #print(f'Linia 492: {reserva_df_sorted_filtered}')
            #     write_google_sheet_x(expanded_df_sorted_filtered)




app()          