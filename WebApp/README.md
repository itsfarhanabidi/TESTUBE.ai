This is a web application created by TESTUBE.ai for doctors and chemists. The application helps doctors handle the patient treatment cycle effectively and helps the chemist with drug administration and control. The entire application is built using Streamlit which is an open source framework written in Python. A Sqlite3 database is used to store the information of patient records.

The Web application comprises of the following pages in the specified order:
1) Home page: This is the inception of the entire web application. The page has the following details present:
    - Overview on TESTUBE.ai
    - A brief introduction to Tuberculosis
    - A video that provides information on the symptoms and prevention of Tuberculosis
    - Provision for Data visualization of the top 5 countries infected with TB along with a world map highlighting the countries with the most number of TB cases.
    - Provision for a doctor or a chemist to register/login into the web application. Once a doctor is successfully registered, they shall receive a private key on their mobile       phone which will help with future operations in the web application.

2) Navigation window: Once the Doctor has logged in succesfully, they are redirected to the Navigation Window where six operations can be carried out:
    - Diagnosis window: A doctor can upload Chest X-Ray images and predict whether the patient has Tuberculosis or not. A deep ConvNet model built from scratch helps with this         prediciton. The model achieved an accuracy of **100%** and functions in the backend.
    - Search & View Patients: The Doctor is given an opportunity to search and view any patient who is registered to obtain brief information by using his/her unique Patient-ID       which is provided during the registration process.
    - Edit Patient Records: - If any Patient’s details have to be edited at any course of time, an option is provided to do the needful.
    - Add Patient Test: The doctor can add all types of patient tests prescribed to them to help with further analayis of the disease.
    - Add prescription: For effective treatment, a patient under the treatment cycle is given medications for a specific duration. The doctor can add the prescription in this         window and also facilitate follow ups.
    - Data Analysis Report: Helps with the generation of the **NATIONAL TUBERCULOSIS REPORT** which gives insights on different factors that infleunce Tuberculosis. The report         is generated using libraries such as Pandas, Matplotlib, Seaborne and Fpdf

3) Diagnosis Window:  
    - This is where a doctor can predict Tuberculosis from Chest X-Ray images using the deep Convolutional Neural Network model running in the backend.
    - There is also a sidebar where the doctor can shift to any other page of operation like: Search & View Patients Window, Edit Patient Records Window, Patient Managment             System Window (PMS) & Adherence Management System Window (AMS).
    - If a patient is tested positive for Tuberculosis, the doctor can admit the patient and begin the patient treatment cycle.

4) Patient Management System: The onset of the patient treatment cycle begins from this page where a doctor can admit a patient and enter his/her details in the portal. There      are six different pages:
    -
    
   
 







