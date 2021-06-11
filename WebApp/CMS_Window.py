import streamlit as st
import sqlite3
import datetime
import pandas as pd
#################################################################################

#Connecting DBs
st.set_page_config(page_title = "CMS Window")
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("comorbidity_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

#Database Management System
def create_com_table():
    cur.execute('CREATE TABLE IF NOT EXISTS comorbidity_db(patient_id TEXT, hiv_status TEXT, date_of_testing TEXT, pid_number TEXT, date_cpt TEXT, dor_art TEXT, art_initiated TEXT, date_initiated TEXT, cd_count TEXT, pre_art_number TEXT, art_number TEXT, diabetes_status TEXT, rbs TEXT, fbs TEXT, end_ip TEXT, end_treatment TEXT, anti_diabetic_treatment TEXT, date_anti_diabetic TEXT, other_comorbidity TEXT, tobacco_user TEXT, alcohol_intake TEXT)')

def add_com_data(hiv_status,hiv_date,pid_number,cpt_date,date_art,art_status,date_initiation,cd_count,pre_art_number,art_number,diabetes_status,rbs,fbs,ip,end_treatment,anti_status,date_started,other_comorbidity,tobacco,alcohol,PID):
    cur.execute('INSERT INTO patient_db(patient_id, hiv_status, date_of_testing, pid_number, date_cpt, dor_art, art_initiated, date_initiated, cd_count, pre_art_number, art_number, diabetes_status, rbs, fbs, end_ip, end_treatment, anti_diabetic_treatment, date_anti_diabetic, other_comorbidity, tobacco_user, alcohol_intake) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(PID,hiv_status,hiv_date,pid_number,cpt_date,date_art,art_status,date_initiation,cd_count,pre_art_number,art_number,diabetes_status,rbs,fbs,ip,end_treatment,anti_status,date_started,other_comorbidity,tobacco,alcohol))
    con.commit()

def view_hiv_data(ID):
    cur.execute('SELECT hiv_status, date_of_testing, art_initiated, cd_count  FROM comorbidity_db WHERE patient_id=?',(ID,))
    data_hiv = cur.fetchall()
    return data_hiv

def view_diabetes_data(ID):
    cur.execute('SELECT diabetes_status, rbs, fbs, anti_diabetic_treatment  FROM comorbidity_db WHERE patient_id=?',(ID,))
    data_diabetes = cur.fetchall()
    return data_diabetes

def view_add_data(ID):
    cur.execute('SELECT tobacco_user, alcohol_intake  FROM comorbidity_db WHERE patient_id=?',(ID,))
    data_add = cur.fetchall()
    return data_add

def search_ID(ID):
    cur.execute('SELECT * FROM patient_db WHERE patient_id=?', (ID,))
    id_final = cur.fetchall()
    return id_final

def check_close(PID):
    cur.execute('SELECT * FROM closed_db WHERE patient_id=?',(PID,))
    data_close = cur.fetchall()
    return data_close
    
#################################################################################

def add_info():
    st.write("")
    st.write("")

    st.markdown("""<div class ='header'>HIV Information</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_status, col_date = st.beta_columns(2)
    col_status.header("HIV Status")
    col_status.markdown('<div class = "divide">_____________________________________</div>',True)
    hiv_status = col_status.selectbox("",['Reactive','Non-Reactive','Unknown'])
    col_date.header("Date of Testing")
    col_date.markdown('<div class = "divide">_____________________________________</div>',True)
    hiv_date = col_date.date_input("", datetime.date(2011,1,1))

    col_pid, col_date_cpt = st.beta_columns(2)
    col_pid.header("PID Number")
    col_pid.markdown('<div class = "divide">_____________________________________</div>',True)
    pid_number = col_pid.text_input("")
    col_date_cpt.header("Date of CPT Delivered")
    col_date_cpt.markdown('<div class = "divide">_____________________________________</div>',True)
    cpt_date = col_date_cpt.date_input(" ", datetime.date(2011,1,1))

    col_date_art, col_art_status = st.beta_columns(2)
    col_date_art.header("DoR to ART Center")
    col_date_art.markdown('<div class = "divide">_____________________________________</div>',True)
    date_art = col_date_art.date_input("  ", datetime.date(2011,1,1))
    col_art_status.header("Intiated to ART")
    col_art_status.markdown('<div class = "divide">_____________________________________</div>',True)
    art_status = col_art_status.radio("", ['Yes','No'])

    col_initiation, col_cd_count = st.beta_columns(2)
    col_initiation.header("Date of Initiation")
    col_initiation.markdown('<div class = "divide">_____________________________________</div>',True)
    date_initiation = col_initiation.date_input("   ", datetime.date(2011,1,1))
    col_cd_count.header("CD4 Count")
    col_cd_count.markdown('<div class = "divide">_____________________________________</div>',True)
    cd_count = col_cd_count.text_input("    ")

    col_pre_art, col_art = st.beta_columns(2)
    col_pre_art.header("Pre ART Number")
    col_pre_art.markdown('<div class = "divide">_____________________________________</div>',True)
    pre_art_number = col_pre_art.text_input("       ")
    col_art.header("ART Number")
    col_art.markdown('<div class = "divide">_____________________________________</div>',True)
    art_number = col_art.text_input("        ")

    st.write("")
    st.write("")

    st.markdown("""<div class ='header'>Diabetes Information</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_d_status,col_rbs = st.beta_columns(2)
    col_d_status.header("Diabetes Status")
    col_d_status.markdown('<div class = "divide">_____________________________________</div>',True)
    diabetes_status = col_d_status.selectbox("",['Diabetic','Non-Diabetic','Unknown'])
    col_rbs.header("Random Blood Sugar")
    col_rbs.markdown('<div class = "divide">_____________________________________</div>',True)
    rbs = col_rbs.text_input("            ")

    col_fbs,col_IP = st.beta_columns(2)
    col_fbs.header("Fasting Blood Sugar")
    col_fbs.markdown('<div class = "divide">_____________________________________</div>',True)
    fbs = col_fbs.text_input("               ")
    col_IP.header("End of IP")
    col_IP.markdown('<div class = "divide">_____________________________________</div>',True)
    ip = col_IP.text_input("                ")

    col_end, col_anti = st.beta_columns(2)
    col_end.header("End of Treatment")
    col_end.markdown('<div class = "divide">_____________________________________</div>',True)
    end_treatment = col_end.text_input("                  ")
    col_anti.header("Anti-Diabetic Treatment")
    col_anti.markdown('<div class = "divide">_____________________________________</div>',True)
    anti_status = col_anti.selectbox(" ",['Initiated','Pending'])

    col_date_initiated, other_comorbidity = st.beta_columns(2)
    col_date_initiated.header("Date of Initiation")
    col_date_initiated.markdown('<div class = "divide">_____________________________________</div>',True)
    date_started = col_date_initiated.date_input("    ", datetime.date(2011,1,1))
    other_comorbidity.header("Other Comorbidity (If any)")
    other_comorbidity.markdown('<div class = "divide">_____________________________________</div>',True)
    other_comorbidity = other_comorbidity.text_input("                 ")

    st.write("")
    st.write("")

    st.markdown("""<div class ='header'>Additional Information</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_tobacco,col_alcohol = st.beta_columns(2)
    col_tobacco.header("Current Tobaco User")
    col_tobacco.markdown('<div class = "divide">_____________________________________</div>',True)
    tobacco = col_tobacco.selectbox("     ",['Positive','Negative'])
    col_alcohol.header("Alcohol Intake")
    col_alcohol.markdown('<div class = "divide">_____________________________________</div>',True)
    alcohol = col_alcohol.selectbox("   ",['Yes','No','N/A'])

    st.write("")
    st.write("")

    st.markdown("""<div class ='header'>Authentication</div>""",True)
    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    st.write("")
    st.write("")

    col_1, col_2 = st.beta_columns(2)
    col_1.header("Patient-ID")
    col_1.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_1.text_input("",type='password')
    final_submit = st.button("UPLOAD DETAILS")

    if(final_submit):
        check_close_data = check_close(PID)
        if(check_close_data == []):
            if((hiv_status or hiv_date or pid_number or cpt_date or date_art or art_status or date_initiation or cd_count or pre_art_number or art_number or diabetes_status or rbs or fbs or ip or end_treatment or anti_status or date_started or other_comorbidity or tobacco or alcohol or PID) == ""):
                st.error("Please enter all the details!")
            elif((hiv_status and hiv_date and pid_number and cpt_date and date_art and art_status and date_initiation and cd_count and pre_art_number and art_number and diabetes_status and rbs and fbs and ip and end_treatment and anti_status and date_started and other_comorbidity and tobacco and alcohol and PID) != ""):
                create_com_table()
                db = search_id(PID)
                if(db == []):
                    st.error(f"Patient with Patient-ID: {PID} does not exist!")
                else:
                    add_com_data(hiv_status,hiv_date,pid_number,cpt_date,date_art,art_status,date_initiation,cd_count,pre_art_number,art_number,diabetes_status,rbs,fbs,ip,end_treatment,anti_status,date_started,other_comorbidity,tobacco,alcohol,PID)
                    st.success("Comorbidity details uploaded!")

        else:
            st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                   
#################################################################################

def view_info():
    
    st.write("")

    col_PID, col_waste = st.beta_columns(2)
    col_PID.header("Patient-ID")
    col_PID.markdown('<div class = "divide">_____________________________________</div>',True)
    PID = col_PID.text_input("", type='password')
    access = st.button("ACCESS")

    if(access):
        if(PID == ""):
            st.error("Please enter the Patient-ID!")
        else:
            check_close_data = check_close(PID)
            if(check_close_data == []):
                data = search_id(PID)
                if (data == []):
                    st.error(f"Patient with Patient-ID: {PID} does not exist!")
                else:
                    db_hiv = view_hiv_data(PID)
                    db_diabetes = view_diabetes_data(PID)
                    db_add = view_add_data(PID)

                    hiv_table = pd.DataFrame(db_hiv, columns = ['HIV Status','Date of Testing','ART Status','CD Count'])
                    diabetes_table = pd.DataFrame(db_diabetes, columns = ['Diabetes Status','Random Blood Sugar','Fasting Blood Sugar','Anti-Diabetic Treatment Status'])
                    add_table = pd.DataFrame(db_add, columns = ['Current Tobbaco User','Alcohol Intake'])

                    st.dataframe(hiv_table)
                    st.write("")
                    st.write("")
                    
                    st.dataframe(diabetes_table)
                    st.write("")
                    st.write("")
                    
                    st.dataframe(add_table)
            else:
                st.error(f"Authorisation denied as Patient Case with ID {PID} is closed!")
                
#################################################################################

st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("This application serves as a Comorbidity Management System which can help you with adding information (HIV/Diabetes/Alcohol Intake/Tobacco Usage) of a particular patient.")
st.sidebar.write("Please follow the steps given below to perform the diverse operations as needed:")
st.sidebar.write("Case 1: Select 'Add Comorbidity Information' to add the comorbidity information to the Database")
st.sidebar.write("Case 2: Select 'Search & View Comorbidity Information' to view Patient Comorbidity Information")

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

                
st.markdown("""<div class="title">Comorbidity Management System</div>""",True)
st.write("")
st.write("")

choice = st.selectbox("",['Let me >>','Add Comorbidity Information','Search & View Comorbidity Information'])

if(choice == 'Add Comorbidity Information'):
    add_info()
elif(choice == 'Search & View Comorbidity Information'):
    view_info()
