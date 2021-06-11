import streamlit as st
import sqlite3
import pandas as pd
import SessionState
import datetime
import math
import random
import keyboard
import os
from twilio.rest import Client
#################################################################################

#Connecting DBs
st.set_page_config(page_title = "PMS Window")
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("PMS_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

#Enrollment_Form    
def create_pftable():
    cur.execute('CREATE TABLE IF NOT EXISTS patient_db(patient_id TEXT, first_name TEXT, last_name TEXT, age INT, gender TEXT,  marital TEXT, contact INT, secondary_contact INT, address TEXT, area TEXT, city TEXT, state TEXT, pincode INT, demographic_area TEXT, occupation TEXT, status TEXT, hiv TEXT, diabetic TEXT, bp TEXT, private_key TEXT, prescription_key INT)')

def add_pfdata(pid, fname, lname, age, gender, marital, contact, scontact, address, area, city, state, pincode, darea, occupation, status, hiv, diabetic, bp, private_key,pres_key):
    cur.execute('INSERT INTO patient_db(patient_id, first_name, last_name, age, gender, marital, contact, secondary_contact, address, area, city, state, pincode, demographic_area, occupation, status, hiv, diabetic, bp, private_key, prescription_key) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(pid, fname, lname, age, gender, marital, contact, scontact, address, area, city, state, pincode, darea, occupation, status, hiv, diabetic, bp, private_key,pres_key))
    con.commit()

def view_all_users():
    cur.execute('SELECT * FROM patient_db')
    data = cur.fetchall()
    return data

def sec_key(secret_key):
    cur.execute('SELECT * FROM TB_dcs WHERE secret_key=?', (secret_key,))
    res = cur.fetchone()
    return res

def deduplication(PID,fname,lname):
    cur.execute('SELECT * FROM patient_db WHERE patient_id=? AND first_name=? AND last_name=?', (PID,fname,lname))
    dup = cur.fetchall()
    return dup

def PresKey(PID, fname, contact):
    key = '0123456789'
    prescription_key = ""
    length = len(key)

    for i in range(6):
        prescription_key += key[math.floor(random.random() * length)]

    account_sid = 'ACe959e17c5ee1f9d5e816fecefb93ae13'
    auth_token = '68ee317bbfc44ab7da11ab1bf009e880'
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=f'Dear {fname}, Greetings from TESTUBE.ai! Your Patient-ID: {PID} has been allotted the Prescription ID: {prescription_key}. Please keep it safe for purchasing your medicines. Get Well Soon <3',from_='+19728290536',to=f'+91{contact}')
    return prescription_key

def check_close(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close

def delete_case(PID):
    cur.execute('DELETE FROM closed_db WHERE patient_id=?',(PID,))

def delete_record(PID,pres_ID):
    cur.execute('DELETE FROM patient_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM test_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM treatment_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM closed_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM comorbidity_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM tracing_db WHERE patient_id=?',(PID,))
    cur.execute('DELETE FROM prescription_db WHERE prescription_id=?',(pres_ID,))
    cur.execute('DELETE FROM dose_tab WHERE pres_ID=?',(pres_ID,))

#################################################################################

#Test_Page
def create_test_table():
    cur.execute('CREATE TABLE IF NOT EXISTS test_db(patient_id TEXT, test_reason TEXT, test_type TEXT, test_requested_from TEXT, test_status TEXT, date_reported TEXT, date_tested TEXT, reported_by TEXT, specimen_type_tested TEXT, visual_sputum TEXT, number_samples INT, sample_result TEXT, result TEXT)')
    
def add_data(PID,test_reason,test_type,test_requested,test_status,date_reported,date_tested,reported_by,specimen_type,visual_appearance,no_samples,sample_result,result):
    cur.execute('INSERT INTO test_db(patient_id, test_reason, test_type, test_requested_from, test_status, date_reported, date_tested, reported_by, specimen_type_tested, visual_sputum, number_samples, sample_result, result) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(PID,test_reason,test_type,test_requested,test_status,date_reported,date_tested,reported_by,specimen_type,visual_appearance,no_samples,sample_result,result))
    con.commit()

def search_ID(ID):
    cur.execute('SELECT * FROM patient_db WHERE patient_id=?', (ID,))
    id_final = cur.fetchall()
    return id_final
    
def obtain_basic(PID):
    cur.execute(f'SELECT patient_id, first_name, last_name, age, gender, contact FROM patient_db WHERE patient_id = {PID}')
    obtain_data = cur.fetchall()
    return obtain_data

def obtain_medical(PID):
    cur.execute(f'SELECT  hiv, diabetic, bp FROM patient_db WHERE patient_id = {PID}')
    obtain_data = cur.fetchall()
    return obtain_data

def obtain_info(PID):
    cur.execute(f'SELECT first_name, contact FROM patient_db WHERE patient_id="{PID}"')
    data_basic = cur.fetchall()
    name = data_basic[0][0]
    contact = data_basic[0][1]
    
    cur.execute(f'SELECT date_reported, test_type FROM test_db WHERE patient_ID = "{PID}"')
    data_test = cur.fetchall()
    date = data_test[0][0]
    test = data_test[0][1]

    account_sid = '#####'
    auth_token = '#####'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(body=f'Dear {name}, Greetings from TESTUBE.ai! Your {test} has been scheduled on {date}. Please visit your nearest diagnostic center ASAP & report soon. We wish you a pleasing result <3',from_='+19728290536',to=f'+91{contact}')
    
def create_treatment_table():
    cur.execute('CREATE TABLE IF NOT EXISTS treatment_db(patient_id TEXT, patient_type TEXT, date_of_diagnosis TEXT, site_of_disease TEXT, basis_of_diagnosis TEXT, drug_resistance TEXT, height INT, date_of_initiation TEXT)')

def add_treatment_data(PID,type_patient,date_diagnosis,site_of_disease,basis_of_diagnosis,drug_resistance,height,date_of_initiation):
    cur.execute('INSERT INTO treatment_db(patient_id, patient_type, date_of_diagnosis, site_of_disease, basis_of_diagnosis, drug_resistance, height, date_of_initiation) VALUES(?,?,?,?,?,?,?,?)', (PID,type_patient,date_diagnosis,site_of_disease,basis_of_diagnosis,drug_resistance,height,date_of_initiation))
    con.commit()
    
def search_doc(PK):
    cur.execute('SELECT * FROM TB_dcs WHERE secret_key=?', (PK,))
    doc_data = cur.fetchall()
    return doc_data

def create_close_case():
    cur.execute('CREATE TABLE IF NOT EXISTS closed_db(patient_id TEXT, private_key TEXT, reason TEXT, date TEXT)')

def add_close_data(PID,PK,reason,date_of_closure):
        cur.execute('INSERT INTO closed_db(patient_id, private_key, reason, date) VALUES(?,?,?,?)', (PID,PK,reason,date_of_closure))
        con.commit()

#################################################################################

#Tracing Form
def create_tracing_table():
    cur.execute('CREATE TABLE IF NOT EXISTS tracing_db(patient_id TEXT, age TEXT, number_contacts TEXT, number_screened TEXT, number_symptoms TEXT, number_diagnosed TEXT, number_treatment TEXT, bcg_status TEXT)')

def add_tracing_data(PID,age,contacts,number_screened,number_symptoms,number_diagnosed,number_treatment,bcg):
    cur.execute('INSERT INTO tracing_db(patient_id, age, number_contacts, number_screened, number_symptoms, number_diagnosed, number_treatment, bcg_status) VALUES(?,?,?,?,?,?,?,?)', (PID,age,contacts,number_screened,number_symptoms,number_diagnosed,number_treatment,bcg))
    con.commit()

#################################################################################

#Patient Admission
def case_page():

    st.markdown("""<div class ='header'>Basic Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    colID, col1, col2 = st.beta_columns(3)
    colID.markdown('<div class="styling">Patient-ID</div>', True)
    PID = colID.text_input("            ")
    col1.markdown('<div class="styling">First Name</div>', True)
    fname = col1.text_input("")
    col2.markdown('<div class="styling">Last Name</div>', True)
    lname = col2.text_input(" ")

    col3, col4, col5 = st.beta_columns(3)
    col3.markdown('<div class="styling">Age</div>', True)
    age = col3.text_input("  ")
    col4.markdown('<div class="styling">Gender</div>', True)
    gender = col4.selectbox("", ["Male","Female","Other"])
    col5.markdown('<div class="styling">Marital Status</div>', True)
    marital = col5.selectbox("", ["Married","Unmarried"])

    col6, col7 = st.beta_columns(2)
    col6.markdown('<div class="styling">Phone Number</div>', True)
    contact = col6.text_input("   ")
    col7.markdown('<div class="styling">Secondary Phone Number</div>', True)
    scontact = col7.text_input("    ")

    st.markdown("""<div class ='header'>Residential Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")
    
    st.markdown('<div class="styling">Address</div>', True)
    address = st.text_input("     ")

    col8, col9 = st.beta_columns(2)
    col8.markdown('<div class="styling">Area</div>', True)
    area = col8.text_input("      ")
    col9.markdown('<div class="styling">City</div>', True)
    city = col9.text_input("       ")

    col10, col11 = st.beta_columns(2)
    col10.markdown('<div class="styling">State</div>', True)
    state = col10.text_input("        ")
    col11.markdown('<div class="styling">Pincode</div>', True)
    pincode = col11.text_input("         ")

    st.markdown("""<div class ='header'>Demographic Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col12, col13 = st.beta_columns(2)
    col12.markdown('<div class="styling">Area</div>', True)
    darea = col12.radio("",["Tribal","Rural","Urban","Sub-Urban","Urban Slum","Unknown"])
    col13.markdown('<div class="styling">Occupation</div>', True)
    occupation = col13.text_input("           ")
    col13.markdown('<div class="styling">Socio-economic Status</div>', True)
    status = col13.selectbox(" ",["APL","BPL"])

    st.markdown("""<div class ='header'>Medical History</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col14, col15, col16 = st.beta_columns(3)
    col14.markdown('<div class="styling">HIV</div>', True)
    hiv = col14.radio(" ",["Reactive","Non-Reactive","Unknown"])
    col15.markdown('<div class="styling">Diabetic</div>', True)
    diabetic = col15.radio("  ", ["Yes","No"])
    col16.markdown('<div class="styling">Blood Pressure</div>', True)
    bp = col16.radio("   ", ["Normal","High Blood Pressure","Low Blood Pressure"])

    st.markdown("""<div class ='header'>Authentication</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col17, col18 = st.beta_columns(2)
    col17.subheader("Private Key")
    private_key = col17.text_input("            ",type='password')

    submit = st.button("Confirm & Submit")

    if(submit):
        if(PID == ""):
            st.write("")
        else:
            create_pftable()
            check_close_data = check_close(PID)
            if(check_close_data == []):
                duplication = deduplication(PID,fname,lname)
                if (duplication == []):
                    if ((PID or fname or lname or age or gender or marital or contact or scontact or address or area or city or state or pincode or darea or occupation or status or hiv or diabetic or bp or private_key) == ' '):
                        st.error("Please enter all the details!")
                    elif ((PID and fname and lname and age and gender and marital and contact and scontact and address and area and city and state and pincode and darea and occupation and status and hiv and diabetic and bp and private_key) != ''):
                        if ((len(private_key) < 6)):
                            st.error("Length of the Private Key should be 6 characters!")
                        elif ((len(private_key) > 6)):
                            st.error("Length of the Private Key should not exceed 6 characters!")
                        else:
                            final = sec_key(private_key)
                            pres_key = PresKey(PID, fname, contact)
                            if (final):
                                create_pftable()
                                add_pfdata(PID, fname, lname, age, gender, marital, contact, scontact, address, area, city, state, pincode, darea, occupation, status, hiv, diabetic, bp, private_key,pres_key)
                                st.success("Registration Successful!")
                            else:
                                st.error("Private Key doesn't exist!")
                else:
                    st.error("Patient already exists!")
                    st.subheader("Following patient(s) with the same name & mobile number are already registered on TESTUBE.ai")

                    database = pd.DataFrame(duplication, columns = ['Patient-ID','First Name','Last Name','Age','Gender','Marital Status','Phone Number','Secondary Phone Number','Address','Area','City','State','Pincode','Area','Occupation','Socio-Economic Status','HIV','Diabetic','Blood Pressure','Private Key','Prescription Key'])
                    st.dataframe(database)
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
        
#################################################################################

#Add Test Details
def test_page():
    
    st.markdown("""<div class ='header'>Add Test Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")
    
    col_1, col_2 = st.beta_columns(2)
    col_1.header("Test Reason")
    col_1.markdown('<div class = "divide">_____________________________________</div>',True)
    test_reason = col_1.selectbox("",['Diagnosis of DSTB','Follow-up of DSTB (Smear)','Diagnosis of DRTB','Follow-up of DRTB (Smear & Culture)'])

    st.write("")
    st.write("")
    
    col_2.header("Test Type")
    col_2.markdown('<div class = "divide">_____________________________________</div>',True)
    test_type = col_2.text_input(" ")

    col_3, col_4 = st.beta_columns(2)
    col_3.header("Test Requested From")
    col_3.markdown('<div class = "divide">_____________________________________</div>',True)
    test_requested = col_3.text_input("  ")

    col_4.header("Test Status")
    col_4.markdown('<div class = "divide">_____________________________________</div>',True)
    test_status = col_4.radio("",['Result Pending','Result Available'])
    
    st.write("")
    st.write("")

    col_5, col_6 = st.beta_columns(2)
    col_5.header("Test Details")
    col_5.markdown('<div class = "divide">_____________________________________</div>',True)
    col_5.write("")
    date_reported = col_5.date_input("Date Reported", datetime.date(2011,1,1))
    date_tested = col_5.date_input("Date Tested", datetime.date(2011,1,1))
    reported_by = col_5.text_input("Reported by")

    col_6.header("Medical History")
    col_6.markdown('<div class = "divide">_____________________________________</div>',True)
    col_6.write("")
    specimen_type = col_6.radio("Specimen Type Tested",['Sputum','Other'])
    visual_appearance = col_6.text_input("Visual Appearance of Sputum")

    st.write("")
    st.write("")
    
    col_7, col_8 = st.beta_columns(2)
    col_7.header("Microscopy Result")
    col_7.markdown('<div class = "divide">_____________________________________</div>',True)
    col_7.write("")
    no_samples = col_7.radio("Number of samples tested",['1','2'])
    sample_result = col_7.radio("Sample a Result",['Negative/Not Seen','1+','2+','3+','Scanty'])

    col_8.header("Conclusive Result")
    col_8.markdown('<div class = "divide">_____________________________________</div>',True)
    col_8.write("")
    result = col_8.text_input("    ")

    st.write("")
    st.write("")
    
    col_9, col_10 = st.beta_columns(2)
    col_9.header("Patient-ID")
    col_9.markdown('<div class = "divide">_____________________________________</div>',True)
    col_9.write("")
    PID = col_9.text_input("     ",type = 'password')
    
    st.write("")
    st.write("")

    submit_button = st.button("Confirm & Submit")
    if(submit_button):
        check_close_data = check_close(PID)
        if(check_close_data == []):
            if((PID or test_reason or test_type or test_requested or test_status or date_reported or date_tested or reported_by or specimen_type or visual_appearance or no_samples or sample_result or result) == ""):
                st.error("Please enter all the details!")
            else:
                data = search_ID(PID)
                if (data):
                    create_test_table()
                    add_data(PID,test_reason,test_type,test_requested,test_status,date_reported,date_tested,reported_by,specimen_type,visual_appearance,no_samples,sample_result,result)
                    obtain_info(PID)
                    st.success(f"{test_type} has been initiated & notified!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

#################################################################################

#Initiate Patient Treatment
def treatment_page():
    
    st.markdown("""<div class ='header'>Treatment Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_ID, col_type = st.beta_columns(2)

    col_ID.header("Patient-ID")
    col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
    col_ID.write("")
    PID = col_ID.text_input("",type = 'password')

    col_type.header("Type of Patient")
    col_type.markdown('<div class = "divide">_____________________________________</div>',True)
    col_type.write("")
    type_patient = col_type.selectbox("",['New','Retreatment: Recurrent','Retreatment: Treatment after failure','Retreatment: After lost to follow up','Retreatment: Others','PMDT'])

    st.markdown("""<div class ='header'>Diagnosis</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")
    
    col_date, col_site = st.beta_columns(2)

    col_date.header("Date of Diagnosis")
    col_date.markdown('<div class = "divide">_____________________________________</div>',True)
    date_diagnosis = col_date.date_input("", datetime.date(2011,1,1))

    col_site.header("Site of Disease")
    col_site.markdown('<div class = "divide">_____________________________________</div>',True)
    site_of_disease = col_site.radio("",['Pulmonary','Extra Pulmonary'])

    col_basis, col_drug = st.beta_columns(2)
    col_basis.header("Basis of Diagnosis")
    col_basis.markdown('<div class = "divide">_____________________________________</div>',True)
    basis_of_diagnosis = col_basis.text_input("  ")

    col_drug.header("Drug Resistance")
    col_drug.markdown('<div class = "divide">_____________________________________</div>',True)
    drug_resistance = col_drug.selectbox("",['Yes','No','Unknown'])

    col_height, col_TB_start = st.beta_columns(2)
    col_height.header("Height in (cms)")
    col_height.markdown('<div class = "divide">_____________________________________</div>',True)
    height = col_height.text_input("   ")

    col_TB_start.header("Date of Initiation")
    col_TB_start.markdown('<div class = "divide">_____________________________________</div>',True)
    date_of_initiation = col_TB_start.date_input(" ",datetime.date(2011,1,1))

    st.write("")
    st.write("")

    start_treatment = st.button("START TREATMENT")

    if(start_treatment):
        check_close_data = check_close(PID)
        if(check_close_data == []):
            if((PID or type_patient or date_diagnosis or site_of_disease or basis_of_diagnosis or drug_resistance or height or date_of_initiation) == ""):
                st.error("Please enter all the details!")
            else:
                data = search_ID(PID)
                if(data):
                    create_treatment_table()
                    add_treatment_data(PID,type_patient,date_diagnosis,site_of_disease,basis_of_diagnosis,drug_resistance,height,date_of_initiation)
                    st.success("Treatment Started!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

#################################################################################

#Contact Tracing
def tracing_page():

    st.markdown("""<div class ='header'>Contact Tracing Details</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)
    
    col_contacts, col_screened = st.beta_columns(2)
    col_contacts.header("Number of household contacts")
    col_contacts.markdown('<div class = "divide">_____________________________________</div>',True)
    contacts = col_contacts.text_input("")

    col_screened.header("Number of household contacts screened")
    col_screened.markdown('<div class = "divide">_____________________________________</div>',True)
    number_screened = col_screened.text_input(" ")

    col_symptoms, col_evaluated = st.beta_columns(2)
    col_symptoms.header("Contacts with Symptoms")
    col_symptoms.markdown('<div class = "divide">_____________________________________</div>',True)
    number_symptoms = col_symptoms.text_input("  ")
    
    col_evaluated.header("Contacts Diagnosed")
    col_evaluated.markdown('<div class = "divide">_____________________________________</div>',True)
    number_diagnosed = col_evaluated.text_input("   ")

    col_treatment, col_age = st.beta_columns(2)
    col_treatment.header("Contacts on Treatment")
    col_treatment.markdown('<div class = "divide">_____________________________________</div>',True)
    number_treatment = col_treatment.text_input("     ")
    
    col_age.header("Age is")
    col_age.markdown('<div class = "divide">_____________________________________</div>',True)
    choice_age = col_age.selectbox("",[">>",'< 6 years','> 6 years'])

    col_1, col_2 = st.beta_columns(2)
    if(choice_age == '< 6 years'):
        col_1.header("Age")
        col_1.markdown('<div class = "divide">_____________________________________</div>',True)
        age = col_1.text_input("          ")

        col_2.header("BCG Vaccine Status")
        col_2.markdown('<div class = "divide">_____________________________________</div>',True)
        bcg = col_2.selectbox("  ",['>>','Shot Taken','Shot Pending'])
    elif(choice_age == '> 6 years'):
        col_1.header("Age")
        col_1.markdown('<div class = "divide">_____________________________________</div>',True)
        age = col_1.text_input("          ")

        col_2.header("BCG Vaccine Status")
        col_2.markdown('<div class = "divide">_____________________________________</div>',True)
        bcg = col_2.selectbox("  ",['>>','Shot Taken','Shot Pending'])

    st.markdown("""<div class ='header'>Authentication</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    col_3, col_4 = st.beta_columns(2)
    col_3.header("Patient-ID")
    col_3.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_3.text_input("                ", type='password')

    submit = st.button("UPDATE")

    if (submit):
        check_close_data = check_close(PID)
        if(check_close_data == []):        
            if((contacts or number_screened or number_symptoms or number_diagnosed or number_treatment or age or bcg or PID) == ""):
                st.error("Please enter all the details!")
            elif((contacts and number_screened and number_symptoms and number_diagnosed and number_treatment and age and bcg and PID) != ""):
                data = search_ID(PID)
                if(data):
                    create_tracing_table()
                    add_tracing_data(PID,age,contacts,number_screened,number_symptoms,number_diagnosed,number_treatment,bcg)
                    st.success("Tracing Data Updated!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
        
################################################################################

#Case Closure
def close_page():
    st.write("")
    st.write("")

    col_reason, col_endDate = st.beta_columns(2)
    col_reason.header("Reason for Closing Case")
    col_reason.markdown('<div class = "divide">_____________________________________</div>',True)
    reason = col_reason.selectbox("    ",['Patient Recovered','Died','Untraceable (Incomplete/Wrong Address)','Untraceable (Migrated)','Duplicate Record (Repeat Diagnosis/Already on Treatment)','Wrongly diagnosed as TB','Patient Refused Treatment'])

    col_endDate.header("Date of Closing Case")
    col_endDate.markdown('<div class = "divide">_____________________________________</div>',True)
    date_of_closure = col_endDate.date_input("  ",datetime.date(2011,1,1))
    
    col_privateKey, col_PID = st.beta_columns(2)
    col_privateKey.header("Private Key")
    col_privateKey.markdown('<div class = "divide">_____________________________________</div>',True)
    PK = col_privateKey.text_input("  ", type='password')
    
    col_PID.header("Patient-ID")
    col_PID.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_PID.text_input("   ", type='password')

    st.write("")
    
    submit = st.button("CLOSE CASE")

    if(submit):
        if((PK or PID) == ""):
            st.error("Please enter all the details!")
        else:
            check_ID = search_ID(PID)
            check_doc = search_doc(PK)
            if((check_ID or check_doc) == []):
                st.error("Authorisation denied!")
            else:
                create_close_case()
                add_close_data(PID,PK,reason,date_of_closure)
                st.success(f"Patient Case with ID: {PID} successfully closed!")
    
#################################################################################

#Patient Re-initiate Page
def initiate_page():
    
    st.write("")
    st.write("")

    col_privateKey, col_PID = st.beta_columns(2)
    col_privateKey.header("Private Key")
    col_privateKey.markdown('<div class = "divide">_____________________________________</div>',True)
    PK = col_privateKey.text_input("  ", type='password')
    
    col_PID.header("Patient-ID")
    col_PID.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_PID.text_input("   ", type='password')

    st.write("")
    
    submit = st.button("Re-Initiate Case")

    if(submit):
        doc_info = search_doc(PK)
        patient_info = check_close(PID)

        if((doc_info or patient_info) == []):
            st.error("Authorisation denied!")
        else:
            delete_case(PID)
            st.success(f"Patient Case with ID: {PID} Re-Initiated Successfully!")

#################################################################################

#Delete Case
def delete_page():
    
    st.write("")
    st.write("")

    col_privateKey, col_null= st.beta_columns(2)
    col_privateKey.header("Private Key")
    col_privateKey.markdown('<div class = "divide">_____________________________________</div>',True)
    PK = col_privateKey.text_input("  ", type='password')

    col_pres, col_PID = st.beta_columns(2)
    col_pres.header("Patient-ID")
    col_pres.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_pres.text_input("   ", type='password')

    col_PID.header("Prescription-ID")
    col_PID.markdown('<div class = "divide">_____________________________________</div>',True)
    pres_id = col_PID.text_input("      ", type='password')

    st.write("")
    
    submit = st.button("DELETE CASE")

    if(submit):
        doc_info = search_doc(PK)
        #patient_info = check_close(PID)
        
        if((doc_info or patient_info) == []):
            st.error("Authorisation denied!")
        else:
            delete_record(PID,pres_id)
            st.success(f"Patient Case with ID: {PID} deleted successfully!")
            

#################################################################################

st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("This application serves as a Patient Management System which can help you with Adding a Patient Case, Adding Tests, Initiating Treatments & Closing a case.")
st.sidebar.write("Please follow the steps given below to perform the diverse operations as needed:")
st.sidebar.write("Case 1: Select 'Add Patient Case' to add a new Patient Record to the Database")
st.sidebar.write("Case 2: Select 'Add Patient Test' to add a new Patient Test when needed")
st.sidebar.write("Case 3: Select 'Add Initiate Treatment' to commence TB Treatment if the tests indicate the occurance of Tuberculosis")
st.sidebar.write("Case 4: Select 'Close Case' to end an existing case due to any reason such as recovery of a patient or death")

st.sidebar.markdown("""<div class ="sidebar">Direct To</div>""",True)
select_page = st.sidebar.selectbox("",['>>','Prediction Window','Search & View Records','Edit Patient Records','Add Prescription','Drug Management'])

if(select_page == 'Prediction Window'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\UITesting.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Search & View Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\search_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Edit Patient Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Add Prescription'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\prescription_page.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Drug Management'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\prescription_page.py"
    os.system(f"streamlit run {path}")

st.markdown("""<div class="title">Patient Management System</div>""",True)
st.write("")
st.write("")
    
choice = st.selectbox("", ['Let me >>','Add Patient Case','Add Patient Test','Initiate Treatment','Contact Tracing','Close Case','Delete Case','Re-Initiate Case'])

if(choice == 'Add Patient Case'):
    case_page()
elif(choice == 'Add Patient Test'):
    test_page()
elif(choice == 'Initiate Treatment'):
    treatment_page()
elif(choice == 'Contact Tracing'):
    tracing_page()
elif(choice == 'Close Case'):
    close_page()
elif(choice == 'Delete Case'):
    delete_page()
elif(choice == 'Re-Initiate Case'):
    initiate_page()
