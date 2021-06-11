import streamlit as st
import numpy as np
import pandas as pd
import os
from twilio.rest import Client
import math, random
import keyboard
from PIL import Image

#################################################################################
st.set_page_config(page_title = "TESTUBE.ai")
#################################################################################

#Database Management
import sqlite3
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

def create_drtable():
    cur.execute('CREATE TABLE IF NOT EXISTS TB_dcs(first_name TEXT, email TEXT, contact INT, rid TEXT, password TEXT,secret_key TEXT)')

def create_chemist_table():
    cur.execute('CREATE TABLE IF NOT EXISTS TB_chemists(pharmacist_name TEXT, pharmacy_name TEXT, license_number TEXT, contact_number INT)')

def login_doctor(username,pwd):
    cur.execute('SELECT * FROM TB_dcs WHERE email=? AND password=?',(username,pwd))
    data = cur.fetchall()
    return data

def add_drdata(name,email,contact,rid,password,secret_key):
    cur.execute('INSERT INTO TB_dcs(first_name, email, contact, rid, password,secret_key) VALUES(?,?,?,?,?,?)',(name,email,contact,rid,password,secret_key))
    con.commit()

def add_chemist_data(pharmacist_name,pharmacy_name,license_number,number):
    cur.execute('INSERT INTO TB_chemists(pharmacist_name,pharmacy_name,license_number,contact_number) VALUES(?,?,?,?)',(pharmacist_name,pharmacy_name,license_number,number))
    con.commit()

def check_existence(lic_number):
    cur.execute(f'SELECT * FROM TB_chemists WHERE license_number="{lic_number}"')
    data = cur.fetchall()
    return data
    
def local_css(file_name):
    with open(file_name) as f: 
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
#################################################################################

#Styling via CSS
local_css("main_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

def generateKey():
    key = '0123456789abcdefghijklmnopqrstuvwxyz'
    PrivateKey = ""
    length = len(key)

    for i in range(6):
        PrivateKey += key[math.floor(random.random() * length)]

    return PrivateKey    

#################################################################################

#UI/UX Code
st.markdown('<div class="header1">Welcome Doctor!</div>', unsafe_allow_html=True)
st.write("")
st.image("images\logo3.jpg")
st.write("")
st.markdown('<i class="about">"TESTUBE.ai is a domain created by a group of engineers who are working towards mitigating Tuberculosis in India which is considered to be the TB capital of the world using Artificial Intelligence. "</i>',True)
st.write("")
st.write("")
st.markdown("""<div class = "header3">OVERVIEW</div>""",True)
st.write("")
st.markdown("""<i class="overview">Tuberculosis or TB is caused by the bacteria Mycobacterium tuberculosis, most often affecting the lungs. It can also spread to other parts of your body like the brain and spine. When a person with TB coughs, spits or sneezes, tiny droplets are released containing the germs. A person in the vicinity who inhales these droplets can be infected with TB. TB can be classified into Active and Latent Tuberculosis.</i>""",True)
st.markdown("""<i class="overview">In Latent TB, the germs persist in the body but the immune system prevents the spread of germs. The person shows no symptoms and the disease remains dormant but can activate at any given time. In Active TB, the person shows clear symptoms and the germs in the body multipy, weakening the immune system. A latent or Active TB infection can also be drug resistant meaning that certain medicines do not work against the bacteria.</i>""",True)
st.write("")
st.markdown("""<div class = "header3">SYMPTOMS & PREVENTION</div>""",True)
st.write("")
st.video("https://www.youtube.com/watch?v=H_R_b7VGMFw")
st.markdown("""<i class = "intro">For more information on Tuberculosis, visit [Tuberculosis - WHO](https://www.who.int/health-topics/tuberculosis)</i>""",True)
st.write("")
st.markdown("""<div class = "header3">NUMERICAL FIGURES</div>""",True)
st.write("")

select = st.select_slider("Slide to view statistics", options=['India','Indonesia','China','Philippines','Pakistan'])
data = {
    'India':[2640000],
    'Indonesia':[1020000],
    'China':[776000],
    'Philippines':[573000],
    'Pakistan':[518000]
}

df = pd.DataFrame.from_dict(data)
if select == "India":
    st.bar_chart(df["India"])
elif select == "Indonesia":
    st.bar_chart(df["Indonesia"])
elif select == "China":
    st.bar_chart(df["China"])
elif select == "Philippines":
    st.bar_chart(df["Philippines"])
else:
    st.bar_chart(df["Pakistan"])

check = st.checkbox("Visualise the countries with maximum TB cases")
if check:
    st.image("images\World_Map_TB.jpg")


#Login/SignUp Code -- Sidebar
st.sidebar.markdown('<div class = "register">Login/Sign-Up</div>', True)
selection = st.sidebar.selectbox("",['Let me >>',"Login","Register"])
if(selection == 'Login'):
    who = st.sidebar.selectbox(" ",['Login as >>','Doctor','Chemist'])
    if (who == 'Doctor'):
        st.sidebar.write("")
        st.sidebar.write("")
        if selection == "Login":
            st.sidebar.markdown('<div class = "login">Username</div>', True)
            username = st.sidebar.text_input("")
            st.sidebar.markdown('<div class = "login">Password</div>', True)
            pwd = st.sidebar.text_input(" ", type='password')
            login = st.sidebar.button("Login")

            if (login):
                if ((username or pwd) == ""):
                    st.sidebar.warning("Please enter the credentials!")
                else:
                    create_drtable()
                    result = login_doctor(username,pwd)

                    if result:
                        selection = "Pred_Page"
                        cur.execute('SELECT first_name FROM TB_dcs WHERE email=?',[username])
                        data = cur.fetchone()
                        data = str(data)
                        unwanted_chars = ['(',"'",",",")"]
                        for char in unwanted_chars:
                            data = data.replace(char,'')
                        file = open("usernames.txt","a")
                        file.write(data)
                        file.close()
                        keyboard.press_and_release('ctrl + w')
                        path = r"C:\Users\Admin\Desktop\UI_Phase2\navigation_window.py"
                        os.system(f"streamlit run {path}")
                    else:
                        st.sidebar.info("Invalid credentials!")
    elif(who == 'Chemist'):
        st.sidebar.write("")
        st.sidebar.markdown('<div class = "login">License Number</div>', True)
        lic_number = st.sidebar.text_input(" ", type = 'password')
        lic_submit = st.sidebar.button("Login")

        if(lic_submit):
            if(lic_number == ""):
                st.sidebar.warning("Please enter the License Number!")
            elif(lic_number != ""):
                chemist_data = check_existence(lic_number)
                if(chemist_data):
                    keyboard.press_and_release('ctrl + w')
                    path = r"C:\Users\Admin\Desktop\UI_Phase2\chemist_page.py"
                    os.system(f"streamlit run {path}")
                else:
                    st.sidebar.warning(f"Chemist with License Number: {lic_number} is not registered!")

elif(selection == 'Register'):
    signup_who = st.sidebar.selectbox("",['Register as >>','Doctor','Chemist'])
    if (signup_who == 'Doctor'):
        st.sidebar.write("")
        st.sidebar.markdown('<div class = "login">Name</div>', True)
        name = st.sidebar.text_input("")
        st.sidebar.markdown('<div class = "login">Email</div>', True)
        email = st.sidebar.text_input(" ")
        st.sidebar.markdown('<div class = "login">Contact Number</div>', True)
        contact = st.sidebar.text_input("  ")
        st.sidebar.markdown('<div class = "login">Registration ID</div>', True)
        rid = st.sidebar.text_input("   ")
        st.sidebar.markdown('<div class = "login">Password</div>', True)
        password = st.sidebar.text_input("    ", type='password')
        st.sidebar.markdown('<div class = "login">Confirm Password</div>', True)
        Cpassword = st.sidebar.text_input("     ", type='password')
        submit = st.sidebar.button("Submit")

        if (submit):
            if ((name or email or contact or rid or password or Cpassword) == ""):
                st.sidebar.warning("Please enter all the details!")
            elif (((name and email and contact and rid and password and Cpassword) != "") and (password == Cpassword)):
                final = generateKey()
                create_drtable()
                add_drdata(name,email,contact,rid,password,final)
                st.sidebar.success("Registration Successful!")
                account_sid = '#####'
                auth_token = '#####'
                client = Client(account_sid, auth_token)

                message = client.messages.create(body=f'Welcome Dr. {name}! Here is your Private Key to administer operations on TESTUBE.ai: {final}. Thank you for joining a community which strives to make India TB Free! ',from_='+19728290536',to=f'+91{contact}')
                st.sidebar.info("Your private key has been sent to your registered mobile number!")
                
            elif (password != Cpassword):
                st.sidebar.warning("Passwords don't match!")

    elif(signup_who == 'Chemist'):
        st.sidebar.write("")
        st.sidebar.markdown('<div class = "login">Pharmacist Name</div>', True)
        pharmacist_name = st.sidebar.text_input("")        
        st.sidebar.markdown('<div class = "login">Pharmacy Name</div>', True)
        pharmacy_name = st.sidebar.text_input(" ")
        st.sidebar.markdown('<div class = "login">License Number</div>', True)
        license_number = st.sidebar.text_input("  ", type = 'password')
        st.sidebar.markdown('<div class = "login">Contact Number</div>', True)
        number = st.sidebar.text_input("   ")
        submit_signup = st.sidebar.button("Submit")

        if(submit_signup):
            if((pharmacist_name or pharmacy_name or license_number or number) == ""):
                st.sidebar.warning("Please enter all the details!")
            elif(((pharmacist_name and pharmacy_name and license_number and number) != "")):
                create_chemist_table()
                data = check_existence(license_number)
                if(data == []):
                    add_chemist_data(pharmacist_name,pharmacy_name,license_number,number)
                    st.sidebar.success("Registration Successful!")
                else:
                    st.sidebar.warning(f"Chemist with License Number: {license_number} already exists!")
