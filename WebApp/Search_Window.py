import streamlit as st
import pandas as pd
import sqlite3
import SessionState
import keyboard
import os

#################################################################################
st.set_page_config(page_title = "Search Page")
#################################################################################

#Database Management System
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

def search_ID(ID):
    cur.execute('SELECT * FROM patient_db WHERE patient_id=?', (ID,))
    id_final = cur.fetchall()
    return id_final

def search_number(number):
    cur.execute('SELECT * FROM patient_db WHERE contact=?', (number,))
    name_final = cur.fetchall()
    return name_final

def test_details_id(PID):
    cur.execute('SELECT patient_id, test_reason, test_type, test_status, result FROM test_db WHERE patient_id=?',(PID,))
    test_final = cur.fetchall()
    return test_final

def test_details_number(number):
    cur.execute('SELECT patient_id, test_reason, test_type, test_status, result FROM test_db WHERE patient_id=?',(number,))
    test_final = cur.fetchall()
    return test_final

def check_close_ID(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close

def check_close_contact(number):
    cur.execute('SELECT * FROM closed_db WHERE contact=?',(number,))
    data_close = cur.fetchall()
    return data_close

def treatment_details(ID):
    cur.execute('SELECT patient_id, patient_type, site_of_disease, basis_of_diagnosis, drug_resistance FROM treatment_db WHERE patient_id=?',(ID,))
    data_treatment = cur.fetchall()
    return data_treatment

def tracing_details(ID):
    cur.execute('SELECT patient_id, number_contacts, number_screened, number_symptoms, number_diagnosed, number_treatment FROM tracing_db WHERE patient_id=?',(ID,))
    data_tracing = cur.fetchall()
    return data_tracing
  
#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("search_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("This application will help you out in searching & viewing Patient Records, either by Patient-ID or by Contact Number")
st.sidebar.write("Please follow the steps given below to search & view Patient Records accordingly:")
st.sidebar.write("Case 1: Select 'Search by Patient-ID' in the select box to get access to a text input field where the correct Patient-ID can be entered to fetch the relevant Patient Data.")
st.sidebar.write("Case 2: Select 'Search by Contact Number' in the select box to get access to a text input field where the correct Conatct Number can be entered to fetch the relevant Patient Data.")

st.sidebar.markdown("""<div class ="sidebar">Direct To</div>""",True)
select_page = st.sidebar.selectbox("",['>>','Prediction Window','Edit Patient Records','Add Patient Test','Add Prescription','Drug Management'])

if(select_page == 'Prediction Window'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\UITesting.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Edit Patient Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Add Patient Test'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\PMS_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Add Prescription'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\prescription_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Drug Management'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\prescription_page.py"
    os.system(f"streamlit run {path}")

    
st.markdown("""<div class="title">Search & View Patients</div>""",True)
st.write("")

choice = st.selectbox("",['Let me >>','Search by Patient ID','Search by Contact Number'])

if (choice == 'Search by Patient ID'):
    col_1, col_2 = st.beta_columns(2)
    col_1.header("Patient-ID")
    col_1.markdown('<div class = "divide">_____________________________________</div>',True)
    ID = col_1.text_input("                ", type='password')
    session_state = SessionState.get(name="", button_sent=True)
    button_sent = st.button("Search")

    if button_sent:
        session_state.button_sent = True

    if session_state.button_sent:
        if(ID == ""):
            st.write(" ")
        else:
            check_close_data = check_close_ID(ID)
            if(check_close_data == []):
                data = search_ID(ID)
                data_test = test_details_id(ID)
                data_treatment = treatment_details(ID)
                data_tracing = tracing_details(ID)
                if(data == []):
                    st.error(f"Patient with ID = {ID} does not exist!")
                else:
                    st.write("")
                    st.header("Registration Details")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                    database_basic = pd.DataFrame(data, columns = ['Patient-ID','First Name','Last Name','Age','Gender','Marital Status','Phone Number','Secondary Phone Number','Address','Area','City','State','Pincode','Area','Occupation','Socio-Economic Status','HIV','Diabetic','Blood Pressure','Private Key','Prescription-ID'])
                    st.dataframe(database_basic)
                    st.write("")
                    st.header("Test Details")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                    database_test = pd.DataFrame(data_test, columns = ['Patient-ID','Test Reason','Type of Test','Result Status','Conclusive Result'])
                    st.dataframe(database_test)
                    st.header("Treatment Details")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                    database_treatment = pd.DataFrame(data_treatment, columns = ['Patient-ID','Type of Patient','Site of Disease','Basis of Diagnosis','Drug Resistance'])
                    st.dataframe(database_treatment)
                    st.header("Contact Tracing Details")
                    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                    database_tracing = pd.DataFrame(data_tracing, columns = ['Patient-ID','Household Contacts','Contacts Screened','Contacts with Symptoms','Contacts Diagnosed','Contacts on Treatment'])
                    st.dataframe(database_tracing)
                    session_state.edit_button = st.button("Edit Details")
                    
                    if (session_state.edit_button):
                        keyboard.press_and_release('ctrl + w')
                        path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
                        os.system(f"streamlit run {path}")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")                    
                    
elif(choice == 'Search by Contact Number'):
    col_1, col_2 = st.beta_columns(2)
    col_1.header("Contact Number")
    col_1.markdown('<div class = "divide">_____________________________________</div>',True)
    number = col_1.text_input("                ", type='password')
    session_state = SessionState.get(name="", button_sent=True)
    button_sent = st.button("Search")

    if button_sent:
        session_state.button_sent = True
        
    if(session_state.button_sent):
        if(number == ""):
            st.write(" ")
        else:
            #check_close_data = check_close_contact(number)
            #if(check_close_data == []):
            data = search_number(number)
            data_test = test_details_number(data[0][0])
            
            if(data==[]):
                st.error(f"Patient with Contact Number +91 {number} does not exist!")
            else:
                st.write("")
                st.header("Registration Details")
                st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                database_basic = pd.DataFrame(data, columns = ['Patient-ID','First Name','Last Name','Age','Gender','Marital Status','Phone Number','Secondary Phone Number','Address','Area','City','State','Pincode','Area','Occupation','Socio-Economic Status','HIV','Diabetic','Blood Pressure','Private Key','Prescription-ID'])
                st.dataframe(database_basic)
                st.write("")
                st.header("Tests")
                st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
                database_test = pd.DataFrame(data_test, columns = ['Patient-ID','Test Reason','Type of Test','Result Status','Conclusive Result'])
                st.dataframe(database_test)
                session_state.edit_button = st.button("Edit Details")
                
                if (session_state.edit_button):
                    keyboard.press_and_release('ctrl + w')
                    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
                    os.system(f"streamlit run {path}")
    else:
        st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!") 

else:
    st.write("")
