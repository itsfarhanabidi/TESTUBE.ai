This is a web application created by TESTUBE.ai for doctors and chemists. The application helps doctors handle the patient treatment cycle effectively and helps the chemist with drug administration and control. The entire application is built using Streamlit which is an open source framework written in Python. A Sqlite3 database is used to store the information of patient records.

The Web application comprises of the following pages in the specified order:
1) Home page: This is the inception of the entire web application. The page has the following details present:
    - Overview on TESTUBE.ai
    - A brief introduction to Tuberculosis
    - A video that provides information on the symptoms and prevention of Tuberculosis
    - Provision for Data visualization of the top 5 countries infected with TB along with a world map highlighting the countries with the most number of TB cases.
    - Provision for a doctor or a chemist to register/login into the web application. Once a doctor is successfully registered, they shall receive a private key on their mobile       phone which will help with future operations in the web application.

2) Navigation window: Once the Doctor has logged in succesfully, they are redirected to the Navigation Window where six operations can be carried out:
    - Diagnosis window: A doctor can upload Chest X-Ray images and predict whether the patient has Tuberculosis or not. A deep ConvNet model built from scratch helps with this         prediciton. The model achieved an accuracy of 100% and functions in the backend.
    - Search & View Patients: The Doctor is given an opportunity to search and view any patient who is registered to obtain brief information by using his/her unique Patient-ID       which is provided during the registration process.
    - Edit Patient Records: - If any Patient’s details have to be edited at any course of time, an option is provided to do the needful.
    - Add Patient Test: The doctor can add all types of patient tests prescribed to them to help with further analayis of the disease.
    - Add prescription: For effective treatment, a patient under the treatment cycle is given medications for a specific duration. The doctor can add the prescription in this         window and also facilitate follow ups.
    - Data Analysis Report: Helps with the generation of the **NATIONAL TUBERCULOSIS REPORT** which gives insights on different factors that infleunce Tuberculosis. The report         is generated using libraries such as Pandas, Matplotlib, Seaborne and Fpdf.

3) Diagnosis Window:  
    - This is where a doctor can predict Tuberculosis from Chest X-Ray images using the deep Convolutional Neural Network model running in the backend.
    - There is also a sidebar where the doctor can shift to any other page of operation like: Search & View Patients Window, Edit Patient Records Window, Patient Management           System Window (PMS) & Adherence Management System Window (AMS).
    - If a patient is tested positive for Tuberculosis, the doctor can admit the patient and begin the patient treatment cycle.
   
4) Patient Management System : This is where the onset of patient treatment cycle happens where a doctor can admit a patient and enter their details in the portal. There are six    different pages under this:
   - Add Patient Case: Here, the Doctor has the opportunity to admit a new Patient to the portal for further treatment initiation.
   - Add Patient Test: All the tests prescribed by the Doctor during the course of time for further analysis of the disease is operated and alerted to the Patient via this page.
   - Initiate Treatment: To start the treatment of an intended patient, the Doctor can use this page to commence the process.
   - Contact Tracing: In this module, the portal gives additional privilege to capture the data of the people the infected was in immediate touch with. Through this, faster          diagnosis of the contacts can be done & treatments can be started much early to prevent further spread and the concerned lives could be saved without a hustle.
   - Close/Delete Case: There are several possibilities which can lead to closing of a case like of, recovery/death/lost contact, etc. Thus, the space for closing & deleting          the case is also provided to use it when needed. 
   - Re-initiating Case: There is a rare possibility that the recovered might develop Tuberculosis a second time. Thus, even if the case was closed before it can be re-initiated      anytime when needed.
    
5) Adherence Management System: This is a module which entertains the addition of a Prescription whenever needed for a patient intended. The doctor in this module will have the    privilege to add a Prescription & View at the time of need using the sub-module named as “Drug Management”. There are two major divisions:
   - Add prescription: The doctor can add the prescription of the concerned patient along with the prescription ID and patient ID which is cross checked with an internal              security module for authentication. If valid, the details are pushed to a centralised Database & a relevant QR Code is generated which is shared with the Chemist/Druggist        for updating the Purchase Status of the Medicines (Patient Tracking). If the details are not valid, then the entry into the centralised Database is denied & will not be          notified to the Chemist/Druggist
   - Drug Management: This is the module where the Doctor is given the privilege of accessing the Prescription Database of any patient under their supervision. This marks as the      first step towards Patient Tracking as they can supervise the Purchase Status updated by the Chemist/Druggist.
   
6) Comorbidity Management System: 
   - This page handles the Comorbidity Information of the Patients which is a important factor to handle the treatment of a patient.
   - Comorbidity information like HIV, Diabetes, Tobacco and Alcohol consumption can be added into the database respectively by the doctor.

7) Search & View Patients: 
   - The Doctor can search any Patients data and view them anytime which were taken during the registration process.
   - The doctor can search the patient based on Patient ID and Contact Number.
   - When the correct patient ID is given, information like Registration Details, Test Details, Treatment Details and Contact Tracing Details can be viewed. 
 
8) Edit Patient Records: 
 







