import streamlit as st
import numpy as np
import pandas as pd
import os
from twilio.rest import Client
import math, random
import keyboard
import SessionState
import re

#################################################################################
st.set_page_config(page_title = "Chemist Management Window")
#################################################################################

#Database Management System
import sqlite3
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

def verification(pres_ID, PID):
    status = cur.execute(f'SELECT patient_id from patient_db WHERE prescription_key = {pres_ID}')
    data = cur.fetchall()
    if (data == []):
        return False
    else:
        ID = data[0][0]
        if(str(ID) == str(PID)):
            return True
        else:
            return False

def data_access(pres_ID):
    cur.execute(f'SELECT * FROM dose_tab WHERE pres_ID={pres_ID} AND purchased="Pending"')    
    data = cur.fetchall()
    return data

def update_purchase(PID,drug_name):
    cur.execute('UPDATE dose_tab SET purchased="Issued" WHERE product_name=? AND pres_ID=?',(drug_name,PID))
    con.commit()

def check_close(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f: 
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
local_css("chemist_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

st.markdown("""<div class="title">Drug Administration & Control</div>""",True)
st.write("")
st.write("")

col_pat_ID, col_pres_ID = st.beta_columns(2)

col_pat_ID.header("Patient-ID")
col_pat_ID.markdown('<div class = "divide">_____________________________________</div>',True)
PA_ID = col_pat_ID.text_input("", type = 'password')

col_pres_ID.header("Prescription-ID")
col_pres_ID.markdown('<div class = "divide">_____________________________________</div>',True)
PR_ID = col_pres_ID.text_input(" ", type='password')

session_state = SessionState.get(name="", button_sent=False)
button_access = st.button("Access Prescription")

if button_access:
    session_state.button_sent = True

if session_state.button_sent:
    if((PA_ID and PR_ID) == ""):
        st.write("")
    else:
        check_close_data = check_close(PA_ID)
        if(check_close_data == []): 
            status_check = verification(PR_ID,PA_ID)
            if(status_check):
                database = data_access(PR_ID)
                if(database == []):
                    st.info("No pending medicines to be purchased!")
                else:
                    database_pd = pd.DataFrame(database, columns = ['Prescription-ID','Drug Name','Weight Band','Morning','Afternoon','Night','Purchased'])
                    
                    st.write("")
                    st.write("")

                    st.header("Prescription Details")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

                    st.write("")
                    st.write("")

                    st.dataframe(database_pd)
                    
                    st.write("")
                    st.write("")

                    st.header("Purchase Status")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

                    st.write("")
                    st.write("")

                    ind = 1
                    drug = []
                    weight = []
                    for index, row in database_pd.iterrows():
                        drug.append(row['Drug Name'])
                        weight.append(row['Weight Band'])

                    if(len(database_pd.index) == 1):
                        med1 = st.checkbox(drug[0] + " " + weight[0], value = False)
                        st.write("")
                        session_state.button_update = st.button("UPDATE")

                        if(session_state.button_update):
                            if(med1):
                                update_purchase(PR_ID,drug[0])
                                st.success("Purchase Status Updated!")
                    elif(len(database_pd.index) == 2):
                        med1 = st.checkbox(drug[0] + " " + weight[0], value = False)
                        med2 = st.checkbox(drug[1] + " " + weight[1], value = False)
                        st.write("")
                        session_state.button_update = st.button("UPDATE")

                        if(session_state.button_update):
                            if((med1 == True) and (med2 == False)):
                                update_purchase(PR_ID,drug[0])
                                st.success("Purchase Status Updated!")
                            elif((med1 == False) and (med2 == True)):
                                update_purchase(PR_ID,drug[1])
                                st.success("Purchase Status Updated!")
                            elif((med1 == True) and (med2 == True)):
                                update_purchase(PR_ID,drug[0])
                                update_purchase(PR_ID,drug[1])
                                st.success("Purchase Status Updated!")
            else:
                st.error("Prescription-ID does not match the relevant Patient-ID")
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
