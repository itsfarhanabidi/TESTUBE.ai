import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img
import numpy as np
from cv2 import cv2
from keras.preprocessing import image
from model import predictor
import os
import keyboard
import SessionState

#################################################################################
st.set_page_config(page_title = "Prediction Window")
#################################################################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Styling via CSS
local_css("pred_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

name = open("usernames.txt","r")
user = name.read()
st.sidebar.markdown(f"""<div class ="username">Dr. {user}</div>""",True)
name.close()
st.write("")
st.write("")
st.markdown("""<style> body {background-color: #fc9d9a;}</style>""",True)
st.sidebar.markdown("""<div class ="sidebar">Navigation Window</div>""",True)
st.sidebar.write("")
st.sidebar.info("The application serves to depict how a trained Convolutional Neural Network makes predictions on unseen data.")
st.sidebar.write("Please follow the steps given below to predict a CXR as either TB Positive or TB Negative:")
st.sidebar.markdown("""<ol><li>Upload the Chest X-ray in JPEG format</li><li>Click on    the Predict Button below the uploaded X-ray</li><li>Observe the predicted output on the Main Window</li><li>If positive, you can proceed towards the Patient Intake Window(PIW) else predcit another CXR.</li></ol>""",True)
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.markdown("""<div class ="sidebar">Direct To</div>""",True)
select_page = st.sidebar.selectbox("",['>>','Search & View Patients','Edit Patient Records','Add Patient Test','Add Prescription','Drug Management'])

if(select_page == 'Search & View Patients'):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\search_page.py"
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

st.markdown("""<div class="title">Hello Doctor, it's diagnosis time!</div>""",True)
st.write("")
st.image("images\lungs2.png")
st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

st.header("Upload a Chest X-ray & Predict")
imageselect = st.file_uploader("")
st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

if (imageselect is not None):
    
    byte = np.asarray(bytearray(imageselect.read()),dtype=np.uint8)
    cv_img = cv2.imdecode(byte,1)
    st.write("")
    st.header("Uploaded X-ray")
    st.image(cv_img, use_column_width=True,width=500,height=500)

    st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

    session_state = SessionState.get(name="", button_sent=False)
        
    test_image = cv2.resize(cv_img, (224,224))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result     = predictor.predict(test_image)
    
    if (result[0][0] == 1):
        st.header("Impression")
        st.markdown("""<i class="result">Tuberculosis Positive</i>""",True)
        st.markdown('<div class = "divide">_____________________________________________________________________________</div>',True)

        
        st.header("Proceed to Patient Intake Window")
        session_state.adm_button = st.button("Admission Button")
        
        if session_state.adm_button:
            keyboard.press_and_release('ctrl + w')
            path = r'C:\Users\Admin\Desktop\UI_Phase2\PMS_page.py'
            os.system(f"streamlit run {path}")
    else:
        st.header("Impression")
        st.markdown("""<i class = "result">Tuberculosis Negative</i>""",True)
        
else:
    st.write("")
