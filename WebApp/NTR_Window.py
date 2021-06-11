import streamlit as st
import os
import keyboard
import sqlite3
import pandas as pd 
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from fpdf import FPDF

#################################################################################

st.set_page_config(page_title = "Data Analysis Window")
sns.set_style('whitegrid')

#################################################################################

#SQL importing to pandas
cnx = create_engine('sqlite:///TB_5.db').connect()
df_docs = pd.read_sql_table('TB_dcs', cnx)
df_patients = pd.read_sql_table('patient_db',cnx)

#################################################################################

#Connecting DBs
con = sqlite3.connect('TB_5.db')
cur = con.cursor()

#################################################################################

#Styling via CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("data_analysis_style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#################################################################################

def sec_key(secret_key):
    cur.execute('SELECT * FROM TB_dcs WHERE secret_key=?', (secret_key,))
    res = cur.fetchone()
    return res
    
#################################################################################

st.markdown("""<div class="title">NATIONAL TUBERCULOSIS REPORT</div>""",True)
st.write("")
st.write("")

col_pres, col_PID = st.beta_columns(2)
col_pres.header("Private Key")
col_pres.markdown('<div class = "divide">_____________________________________</div>',True)
PK = col_pres.text_input("   ", type='password')

download = st.button("DOWNLOAD REPORT")

if(download):
    verify = sec_key(PK)
    if(verify == []):
        st.error(f"Doctor with the given Private Key does not exist!")
    else:
        #TB Distribution Based on Gender
        df_gender_ratio = df_patients.gender.value_counts()
        df_gender = pd.DataFrame(df_gender_ratio).reset_index()
        df_gender.rename(columns = {'index':'Gender','gender':'Count'}, inplace=True)

        plt.figure(figsize=(10,5))
        gender_graph = sns.barplot(x=df_gender.Gender,y=df_gender.Count,ci=None).set_title('TB distribution based on Gender')
        gender_graph.figure.savefig('Reports/graphs/gender_graph.png')

        #TB Distribution Based on Age Intervals
        df_age = df_patients['age']
        df_age_gap = list(df_age)
        
        sns.set_style('whitegrid')
        sns.set(color_codes=True)
        bins = [0,20,40,60,80,100]

        fig, ax = plt.subplots(figsize =(10, 5))
        age_graph = sns.distplot(df_age_gap, bins = bins)
           
        plt.xlabel("Age Interval")
        plt.ylabel("Cases")
        plt.title('TB distribution based on Age Intervals')

        age_graph.figure.savefig('Reports/graphs/age_graph.png')

        #TB Distribution Based on Occupation
        df_occupation_ratio = df_patients.occupation.value_counts()
        df_occupation = pd.DataFrame(df_occupation_ratio).reset_index()
        df_occupation.rename(columns = {'index':'Occupation','occupation':'Count'}, inplace=True)

        plt.figure(figsize=(10,5))
        plt.rcParams['font.sans-serif'] = 'Arial'
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.size']=12
        plt.rcParams['axes.labelcolor']= 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.rcParams['text.color'] = 'black'

        occupation_graph = df_occupation.plot.pie(y='Count',labels = ['Health Care Worker','Transportation Sector','Sanitation Worker','Daily Wage Worker','Jailor','Student','Miner'], figsize=(7, 7))
        occupation_graph.figure.savefig('Reports/graphs/occupation_graph.png')

        #TB Distribution Based on State
        df_state_ratio = df_patients['state'].value_counts()
        df_state = pd.DataFrame(df_state_ratio).reset_index()
        df_state.rename(columns = {'index':'State','state':'Count'}, inplace=True)
        
        plt.figure(figsize=(10,5))
        plt.rcParams['axes.labelcolor']= 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        state_graph = sns.barplot(x=df_state.State,y=df_state.Count,ci=None).set_title('TB distribution based on State')
        state_graph.figure.savefig('Reports/graphs/state_graph.png')

        #TB Distribution Based on Demographies
        df_area_ratio = df_patients['demographic_area'].value_counts()
        df_area = pd.DataFrame(df_area_ratio).reset_index()
        df_area.rename(columns = {'index':'Demographic Area','demographic_area':'Count'}, inplace=True)

        plt.figure(figsize=(10,5))
        plt.rcParams['axes.labelcolor']= 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        demographies_graph = sns.barplot(df_area['Demographic Area'],df_area.Count,ci=None).set_title('TB distribution based on Demographic Areas')
        demographies_graph.figure.savefig('Reports/graphs/demographies_graph.png')

        #TB Distribution Based on Economic Status
        df_status_ratio = df_patients['status'].value_counts()
        df_status = pd.DataFrame(df_status_ratio).reset_index()
        df_status.rename(columns={'index':'Economic Status','status':'Count'},inplace=True)

        plt.figure(figsize=(10,5))
        plt.rcParams['axes.labelcolor']= 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'

        status_graph = sns.barplot(df_status['Economic Status'],df_status.Count,ci=None).set_title('TB distribution based on Economic Status')
        status_graph.figure.savefig('Reports/graphs/status_graph.png')

        #TB Distribution Based on HIV/Diabetes/Blood Pressure
        plt.figure(figsize=(10,5))
        plt.rcParams['axes.labelcolor']= 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        
        df_hiv_ratio = df_patients['hiv'].value_counts()
        df_hiv = pd.DataFrame(df_hiv_ratio).reset_index()
        df_hiv.rename(columns = {'index':'HIV Status','hiv':'Count'},inplace=True)
        hiv_graph = sns.barplot(df_hiv['HIV Status'],df_hiv.Count,ci=None).set_title('TB distribution based on HIV') 
        hiv_graph.figure.savefig('Reports/graphs/hiv_graph.png')
        
        df_diabetic_ratio = df_patients['diabetic'].value_counts()
        df_diabetic = pd.DataFrame(df_diabetic_ratio).reset_index()
        df_diabetic.rename(columns = {'index':'Diabetes Status','diabetic':'Count'},inplace=True)
        diabetes_graph = sns.barplot(df_diabetic['Diabetes Status'],df_diabetic.Count,ci=None).set_title('TB distribution based on Diabetes')
        diabetes_graph.figure.savefig('Reports/graphs/diabetes_graph.png')
        
        df_bp_ratio = df_patients['bp'].value_counts()
        df_bp = pd.DataFrame(df_bp_ratio).reset_index()
        df_bp.rename(columns = {'index':'Blood Pressure','bp':'Count'},inplace=True)
        bp_graph = sns.barplot(df_bp['Blood Pressure'],df_bp.Count,ci=None).set_title('TB distribution based on Blood Pressure')
        bp_graph.figure.savefig('Reports/graphs/bp_graph.png')

        WIDTH = 210
        HEIGHT  = 297

        pdf = FPDF('P', 'mm', 'A4')
        pdf.set_font('Arial', 'B', 16)

        pdf.add_page()
        pdf.image('Reports/graphs/Cover_Page.jpg', x = 0, y = 0, w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/Contents_Page.jpg', x = 0, y = 0, w=WIDTH,h=HEIGHT)

        pdf.add_page()
        pdf.image('Reports/graphs/Message_Page.jpg', x = 0, y = 0, w=WIDTH,h=HEIGHT)

        pdf.add_page()
        pdf.image('Reports/graphs/stats.jpg', x = 0, y = 0, w=WIDTH)
        pdf.image('Reports/graphs/gender_graph.png', x = 0, y = 55,w=WIDTH)
        pdf.image('Reports/graphs/age_graph.png', x = 0, y = 175,w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/stats.jpg', x = 0, y = 0, w=WIDTH)
        pdf.image('Reports/graphs/occupation_graph.png', x = 0, y = 65,w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/stats.jpg', x = 0, y = 0, w=WIDTH)
        pdf.image('Reports/graphs/state_graph.png', x = 0, y = 55,w=WIDTH)
        pdf.image('Reports/graphs/demographies_graph.png', x = 0, y = 175,w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/stats.jpg', x = 0, y = 0, w=WIDTH)
        pdf.image('Reports/graphs/status_graph.png', x = 0, y = 55,w=WIDTH)
        pdf.image('Reports/graphs/hiv_graph.png', x = 0, y = 175,w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/stats.jpg', x = 0, y = 0, w=WIDTH)
        pdf.image('Reports/graphs/diabetes_graph.png', x = 0, y = 55,w=WIDTH)
        pdf.image('Reports/graphs/bp_graph.png', x = 0, y = 175,w=WIDTH)

        pdf.add_page()
        pdf.image('Reports/graphs/Conclusion_Page.jpg', x = 0, y = 0, w=WIDTH,h=HEIGHT)

        pdf.output('Reports/NTR_2021.pdf','F')

        st.success("Data Analysed & Inference Downloaded Successfully!")
