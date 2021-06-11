import streamlit as st
import sqlite3
import datetime
import pandas as pd
import pyqrcode
import png
from pyqrcode import QRCode
import keyboard
import os
#################################################################################

#Connecting DBs
st.set_page_config(page_title = "AMS Window")
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("prescription_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

#Database Management System
def create_pres_table():
    cur.execute('CREATE TABLE IF NOT EXISTS prescription_db(prescription_ID INT, product_type TEXT, age_factor TEXT, product_name TEXT, weight_band TEXT, number_of_days INT, number_of_blisters INT, date_issue TEXT)')

def add_data(pres_ID, product_type, aging, product_name, weight_band, number_of_days, number_of_blisters, date_issue):
    cur.execute('INSERT INTO prescription_db(prescription_ID, product_type, age_factor, product_name, weight_band, number_of_days, number_of_blisters, date_issue) VALUES (?,?,?,?,?,?,?,?)',(pres_ID, product_type, aging, product_name, weight_band, number_of_days, number_of_blisters, date_issue))
    con.commit()

def pres_db(pres_ID):
    data = cur.execute(f'SELECT * FROM patient_db WHERE prescription_key={pres_ID}')
    return data

def dose_db():
    cur.execute('CREATE TABLE IF NOT EXISTS dose_tab(pres_ID INT, product_name TEXT, weight_band TEXT,  morning TEXT, afternoon TEXT, night TEXT, purchased TEXT)')

def add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased):
    cur.execute('INSERT INTO dose_tab(pres_ID, product_name, weight_band, morning, afternoon, night, purchased) VALUES(?,?,?,?,?,?,?)',(pres_ID, product_name, weight_band, morning, afternoon, night, purchased))
    con.commit()

def data_pres(pres_ID):
    cur.execute(f'SELECT * FROM dose_tab WHERE pres_ID={pres_ID}')    
    data = cur.fetchall()
    return data

def extract_name(pres_ID):
    name = cur.execute(f'SELECT first_name FROM patient_db WHERE prescription_key={pres_ID}')
    return name

def check_close(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close

#################################################################################

#QR_Code Functions
def convert_to_csv(pres_ID):
    info = data_pres(pres_ID)
    database = pd.DataFrame(info, columns = ['Prescription-ID','Drug Name','Weight Band','Morning','Afternoon','Night','Purchased'])
    database.to_csv(r'C:\Users\Admin\Desktop\UI_Phase2\prescriptions\{}.csv'.format(pres_ID))

def createQRCode(pres_ID):
    df = pd.read_csv(r'C:\Users\Admin\Desktop\UI_Phase2\prescriptions\{}.csv'.format(pres_ID))
    for index, values in df.iterrows():
        prescription_ID = values['Prescription-ID']
        product_name = values['Drug Name']
        weight_band = values['Weight Band']
        morning_dose = values['Morning']
        afternoon_dose = values['Afternoon']
        night_dose = values['Night']
        purchased_status = values['Purchased']
        data = f'''
Dear concerned,\n
please find the details of your medicines below, along with the dose intake information.\n
Prescription-ID: {prescription_ID}\n
Medicine Name: {product_name}\n
Weight Band: {weight_band}\n
Morning Dose: {morning_dose}\n
Afternoon Dose: {afternoon_dose}\n
Night Dose: {night_dose}\n
Purchased: {purchased_status}\n\n
Here,\n
1 --> Medicine intake compulsory\n
0 --> Medicine intake not required\n
Please take your medicines on time & we promise, you'll get well soon <3
'''
        image = pyqrcode.create(data)
        image.png(r"C:\Users\Admin\Desktop\UI_Phase2\QR_Codes\{}.png".format(pres_ID), scale = '6')        
    
#################################################################################

#Prescription Page
def prescription_page():
    st.markdown("""<div class = "header">Product Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")
    
    col_type, col_aging = st.beta_columns(2)

    col_type.header("Product Type")
    col_type.markdown('<div class = "divide">_____________________________________</div>',True)
    product_type = col_type.selectbox("",['Private','RNTCP'])
    
    col_aging.header("Adult/Pediatric")
    col_aging.markdown('<div class = "divide">_____________________________________</div>',True)
    aging = col_aging.selectbox("",['Adult','Pediatric'])

    st.write("")
    st.write("")

    col_name, col_weight = st.beta_columns(2)
    col_name.header("Product Name")
    col_name.markdown('<div class = "divide">_____________________________________</div>',True)
    product_name = col_name.text_input(" ")
    
    col_weight.header("Weight Band")
    col_weight.markdown('<div class = "divide">_____________________________________</div>',True)
    weight_band = col_weight.text_input("  ")

    st.write("")
    st.write("")
    
    col_days, col_blisters = st.beta_columns(2)
    col_days.header("Number of Days")
    col_days.markdown('<div class = "divide">_____________________________________</div>',True)
    number_of_days = col_days.text_input("   ")
    
    col_blisters.header("Number of Blisters")
    col_blisters.markdown('<div class = "divide">_____________________________________</div>',True)
    number_of_blisters = col_blisters.text_input("    ")

    st.write("")
    st.write("")

    st.markdown("""<div class = "header">Dose Break-Up</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")
    
    dose = st.radio("",['0 - 0 - 1','0 - 1 - 0','1 - 0 - 0','0 - 1 - 1','1 - 0 - 1','1 - 1 - 0','1 - 1 - 1'])

    st.write("")
    st.write("")   
        
    st.markdown("""<div class = "header">Validation</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_pres_ID, col_PID = st.beta_columns(2)
    col_pres_ID.header("Prescription-ID")
    col_pres_ID.markdown('<div class = "divide">_____________________________________</div>',True)
    pres_ID = col_pres_ID.text_input("                      ", type = 'password')

    col_PID.header("Patient-ID")
    col_PID.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_PID.text_input("                           ",type='password')

    col_date, col_y = st.beta_columns(2)
    col_date.header("Date of Issue")
    col_date.markdown('<div class = "divide">_____________________________________</div>',True)
    date_issue = col_date.date_input("",  datetime.date(2011,1,1))

    st.write("")
    add_pres = st.button("Add Prescription")
    
    if(add_pres):
        create_pres_table()
        dose_db()
        check_close_data = check_close(PID)
        if(check_close_data == []):
            feedback = pres_db(pres_ID)
            if(feedback):
                add_data(pres_ID, product_type, aging, product_name, weight_band, number_of_days, number_of_blisters, date_issue)
                if(dose == '0 - 0 - 1'):
                    morning = '0'
                    afternoon = '0'
                    night = '1'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
                elif(dose == '0 - 1 - 0'):
                    morning = '0'
                    afternoon = '1'
                    night = '0'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added! & QR Code Generated")
                elif(dose == '1 - 0 - 0'):
                    morning = '1'
                    afternoon = '0'
                    night = '0'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
                elif(dose == '0 - 1 - 1'):
                    morning = '0'
                    afternoon = '1'
                    night = '1'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
                elif(dose == '1 - 0 - 1'):
                    morning = '1'
                    afternoon = '0'
                    night = '1'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
                elif(dose == '1 - 1 - 0'):
                    morning = '1'
                    afternoon = '1'
                    night = '0'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
                elif(dose == '1 - 1 - 1'):
                    morning = '1'
                    afternoon = '1'
                    night = '1'
                    purchased = 'Pending'
                    add_dose(pres_ID, product_name, weight_band, morning, afternoon, night, purchased)
                    convert_to_csv(pres_ID)
                    createQRCode(pres_ID)
                    st.success("Prescription Added & QR Code Generated!")
            elif(feedback == []):
                st.info(f'Patient with Prescription-ID: {pres_ID} does not exist!')
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

#Drug Page
def drug_page():
    pat_ID, pre_ID = st.beta_columns(2)

    pat_ID.header("Patient-ID")
    pat_ID.markdown('<div class = "divide">_____________________________________</div>',True)
    pt_ID = pat_ID.text_input("", type = 'password')

    pre_ID.header("Prescription-ID")
    pre_ID.markdown('<div class = "divide">_____________________________________</div>',True)
    pres_ID = pre_ID.text_input(" ",type = 'password')

    access = st.button("Access")

    if(access):
        check_close_data = check_close(pt_ID)
        if(check_close_data == []):
            info = data_pres(pres_ID)
            database = pd.DataFrame(info, columns = ['Prescription-ID','Drug Name','Weight Band','Morning','Afternoon','Night','Purchased'])
            st.dataframe(database)
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
    
#################################################################################

st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("This application will help you in adding a precription & altering the same whenever needed.")
st.sidebar.write("Please follow the steps given below to add & alter prescriptions:")
st.sidebar.write("Case 1: Select 'Add Prescription' from the selectbox to add a new prescription for a concerned patient")
st.sidebar.write("Case 2: Select 'Drug Management' from the selectbox to view and alter prescriptions accordingly")

st.sidebar.markdown("""<div class ="sidebar">Direct To</div>""",True)
select_page = st.sidebar.selectbox("",['>>','Prediction Window','Search & View Records','Edit Patient Records','Add Patient Test'])

if(select_page == 'Prediction Window'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\UITesting.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Search & View Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Edit Patient Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Add Patient Test'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\PMS_page.py"
    os.system(f"streamlit run {path}")

st.markdown("""<div class="title">Adherence Management System</div>""",True)
st.write("")
st.write("")

choice = st.selectbox("",['>>','Add Prescription','Drug Management'])

if (choice == 'Add Prescription'):
    prescription_page()
elif(choice == 'Drug Management'):
    drug_page()
