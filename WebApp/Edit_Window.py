import streamlit as st
import sqlite3
import keyboard
import os
#################################################################################

#Connecting DBs
st.set_page_config(page_title = "Edit Window")
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

#################################################################################

#Update Operations
def update_records(column_name,PID,info):
    cur.execute(f'UPDATE patient_db SET {column_name}=? WHERE patient_id=?',(info,PID))
    con.commit()

def update_test(column_name,PID,info):
    cur.execute(f'UPDATE test_db SET {column_name}=? WHERE patient_id=?',(info,PID))
    con.commit()
    
def search_ID(ID):
    cur.execute('SELECT * FROM patient_db WHERE patient_id=?', (ID,))
    id_final = cur.fetchall()
    return id_final

def check_close(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close

def update_comorbidity(column_name,PID,info):
    cur.execute(f'UPDATE comorbidity_db SET {column_name}=? WHERE patient_id=?',(info,PID))
    con.commit()

def update_tracing(column_name,PID,info):
    cur.execute(f'UPDATE tracing_db SET {column_name}=? WHERE patient_id=?',(info,PID))
    con.commit()

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("edit_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("This application will help you update Patient Records & Test Results.")
st.sidebar.write("")

st.sidebar.write("Please follow the steps given below to update Patient Records:")
st.sidebar.write("Case 1: Select 'Patient Details' from the select box followed by selecting the field of data you want to update in the Patient Records.")
st.sidebar.write("Case 2: Select 'Test Results' from the selectbox followed by entering the Conclusive Result of the test to update in Patient Records.") 
st.sidebar.markdown("""<div class ="sidebar">Direct To</div>""",True)
select_page = st.sidebar.selectbox("",['>>','Prediction Window','Search & View Records','Add Patient Test','Add Prescription','Drug Management'])

if(select_page == 'Prediction Window'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\UITesting.py"
    os.system(f"streamlit run {path}")
elif(select_page == 'Search & View Records'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\search_page.py"
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


st.markdown("""<div class="title">Edit Patient Records</div>""",True)
st.write("")

page = st.selectbox("",['Let me edit >>','Patient Details','Test Results','Comorbidity Information','Contact Tracing Information'])

if(page == 'Patient Details'):
    choice = st.selectbox("", ['Edit by >>','First Name','Last Name','Age','Gender','Marital Status','Phone Number','Secondary Phone Number','Address','Area','City','State','Pincode','Demographic Area','Occupation','Socio-Economic Status','HIV','Diabetic','Blood Pressure'])

    if (choice == 'First Name'):
        column_name = 'first_name'
        col_ID, col_FN = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_FN.header("First Name")
        name = col_FN.text_input(" ")

        update = st.button("UPDATE")
        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Last Name'):
        column_name = 'last_name'
        col_ID, col_LN = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_LN.header("Last Name")
        name = col_LN.text_input("  ")

        update = st.button("UPDATE")
        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                
    elif(choice == 'Age'):
        column_name = 'age'
        col_ID, col_age = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_age.header("Age")
        name = col_age.text_input("   ")

        update = st.button("UPDATE")
        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                
    elif(choice == 'Gender'):
        column_name = 'gender'
        col_ID, col_gender = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_gender.header("Gender")
        name = col_gender.selectbox("",['Male','Female','Transgender'])

        update = st.button("UPDATE")    

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                
    elif(choice == 'Marital Status'):
        column_name = 'marital'
        col_ID, col_ms = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_ms.header("Marital Status")
        name = col_ms.selectbox(" ",['Married','Unmarried'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Phone Number'):
        column_name = 'contact'
        col_ID, col_pn = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_pn.header("Phone Number")
        name = col_pn.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!") 
                
    elif(choice == 'Secondary Phone Number'):
        column_name = 'secondary_contact'
        col_ID, col_spn = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_spn.header("Secondary Phone Number")
        name = col_spn.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!") 
                
    elif(choice == 'Address'):
        column_name = 'address'
        col_ID, col_add = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_add.header("Address")
        name = col_add.text_input(" ")

        st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Area'):
        column_name = 'area'
        col_ID, col_area = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_area.header("Area")
        name = col_area.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                
    elif(choice == 'City'):
        column_name = 'city'
        col_ID, col_city = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_city.header("City")
        name = col_city.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'State'):
        column_name = 'state'
        col_ID, col_state = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_state.header("State")
        name = col_state.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Pincode'):
        column_name = 'pincode'
        col_ID, col_code = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_code.header("Pincode")
        name = col_code.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
    
    elif(choice == 'Demographic Area'):
        column_name = 'demographic_area'
        col_ID, col_darea = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_darea.header("City")
        name = col_darea.selectbox("  ",["Tribal","Rural","Urban","Sub-Urban","Urban Slum","Unknown"])
        
        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Occupation'):
        column_name = 'occupation'
        col_ID, col_occ = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_occ.header("Occupation")
        name = col_occ.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Socio-Economic Status'):
        column_name = 'status'
        col_ID, col_status = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_status.header("Socio-Economic Status")
        name = col_status.selectbox("  ",['APL','BPL'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'HIV'):
        column_name = 'hiv'
        col_ID, col_hiv = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_hiv.header("HIV")
        name = col_hiv.selectbox("    ",['Reactive','Non-Reactive','Unknown'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Diabetic'):
        column_name = 'diabetic'
        col_ID, col_diabetic = st.beta_columns(2)
        col_ID.header("Patient-ID")
        PID = col_ID.text_input("",type = 'password')

        col_diabetic.header("Diabetic")
        name = col_diabetic.selectbox("      ",['Yes','No'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

    elif(choice == 'Blood Pressure'):
        column_name = 'bp'
        col_ID, col_bp = st.beta_columns(2)
        col_ID.header("Blood Pressure")
        PID = col_ID.text_input("",type = 'password')

        col_bp.header("Blood Pressure")
        name = col_bp.selectbox("       ",["Normal","High Blood Pressure","Low Blood Pressure"])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_records(column_name,PID,name)
                    st.success("Records updated successfully!")
                else:
                    st.error(f"Patient with ID = {PID} does not exist!")
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

elif(page == 'Test Results'):
    column_name = 'result'
    col_ID, col_result = st.beta_columns(2)
    col_ID.header("Patient-ID")
    PID = col_ID.text_input("",type = 'password')

    col_result.header("Conclusive Result")
    name = col_result.text_input(" ")

    update = st.button("UPDATE")

    if(update):
        check_close_data = check_close(PID)
        if(check_close_data == []):
            data = search_ID(PID)
            if(data):
                update_test(column_name,PID,name)
                st.success("Records updated successfully!")
            else:
                st.error(f"Patient with ID = {PID} does not exist!")
        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")

elif(page == 'Comorbidity Information'):
    choice = st.selectbox(" ", ['Edit by >>','Random Blood Sugar','Fasting Blood Sugar','Current Tobacco User','Alcohol Intake'])
    if(choice == 'Random Blood Sugar'):
        column_name = 'rbs'
        col_ID, col_rbs = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_rbs.header("Random Blood Sugar")
        col_rbs.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_rbs.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_comorbidity(column_name,PID,info)

    elif(choice == 'Fasting Blood Sugar'):
        column_name = 'fbs'
        col_ID, col_fbs = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_fbs.header("Fasting Blood Sugar")
        col_fbs.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_fbs.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_comorbidity(column_name,PID,info)

    elif(choice == 'Current Tobacco User'):
        column_name = 'tobacco_user'
        col_ID, col_tu = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_tu.header("Current Tobaco User")
        col_tu.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_tu.selectbox("",['Positive','Negative'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_comorbidity(column_name,PID,info)

    elif(choice == 'Alcohol Intake'):
        column_name = 'alcohol_intake'
        col_ID, col_ai = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_ai.header("Alcohol Intake")
        col_ai.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_ai.selectbox("    ",['Yes','No','N/A'])

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_comorbidity(column_name,PID,info)

elif(page == 'Contact Tracing Information'):
    choice = st.selectbox(" ",['Edit by >>','Household Contacts Screened','Contacts with Symptoms','Contacts Diagnosed','Contacts on Treatment'])
    if(choice == 'Household Contacts Screened'):
        column_name = 'number_screened'
        col_ID, col_ns = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_ns.header("Contacts Screened")
        col_ns.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_ns.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_tracing(column_name,PID,info)

    elif(choice == 'Contacts with Symptoms'):
        column_name = 'number_symptoms'
        col_ID, col_cs = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_cs.header("Contacts with Symptoms")
        col_cs.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_cs.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_tracing(column_name,PID,info)

    elif(choice == 'Contacts Diagnosed'):
        column_name = 'number_diagnosed'
        col_ID, col_cd = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_cd.header("Contacts Diagnosed")
        col_cd.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_cd.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_tracing(column_name,PID,info)

    elif(choice == 'Contacts on Treatment'):
        column_name = 'number_treatment'
        col_ID, col_ct = st.beta_columns(2)
        col_ID.header("Patient-ID")
        col_ID.markdown('<div class = "divide">_____________________________________</div>',True)
        PID = col_ID.text_input("  ",type='password')

        col_ct.header("Contacts on Treatment")
        col_ct.markdown('<div class = "divide">_____________________________________</div>',True)
        info = col_ct.text_input(" ")

        update = st.button("UPDATE")

        if(update):
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_ID(PID)
                if(data):
                    update_tracing(column_name,PID,info)
