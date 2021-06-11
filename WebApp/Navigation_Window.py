import streamlit as st
import os
import keyboard

#################################################################################
st.set_page_config(page_title = "Navigation Window")
#################################################################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("navigation_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

st.markdown("""<div class="title">Navigation Window</div>""",True)
st.write("")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

col_1, col_2, col_3, col_4, col_5 = st.beta_columns(5)
predict = col_1.button("Predict a Chest X-ray")
search = col_3.button("Search & View Patients")
edit = col_5.button("Edit Patient Records")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

col_1, col_2, col_3, col_4, col_5 = st.beta_columns(5)
add_test = col_1.button("Add Patient Test")
add_pres = col_3.button("Add Prescription")
data_analysis = col_5.button("Data Analysis Report")

if (predict):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\UITesting.py"
    os.system(f"streamlit run {path}")
elif (search):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\search_page.py"
    os.system(f"streamlit run {path}")
elif (edit):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\edit_page.py"
    os.system(f"streamlit run {path}")
elif(add_test):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\PMS_page.py"
    os.system(f"streamlit run {path}")
elif(add_pres):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\prescription_page.py"
    os.system(f"streamlit run {path}")
elif(data_analysis):
    keyboard.press_and_release('ctrl + w')
    path = r"C:\Users\Admin\Desktop\UI_Phase2\data_analysis_page.py"
    os.system(f"streamlit run {path}")
