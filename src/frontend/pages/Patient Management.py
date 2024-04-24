import streamlit as st
import sqlite3
import pandas as pd
from utils.background import add_background

st.set_page_config(page_title="Device Management", layout="wide")
add_background()


def create_patients_table():
    conn = sqlite3.connect('data/patients.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, height REAL, weight REAL)''')
    conn.commit()
    conn.close()

# #Streamlit page to add/ edit/ delete patients into the sqlite database
# def main():
#     #Add a title to the page
#     st.title("Patient Management")
#     st.selectbox("Select an option", ["Make a selection","Add Patient", "Edit Patient", "Delete Patient", "View Patients"], index=0, key="options", on_change=display_page)

# def display_page():
#     options = st.session_state.get("options")
#     if options == "Add Patient":
#         add_patient()
#     elif options == "Delete Patient":
#         delete_patient()
#     elif options == "View Patients":
#         view_patients()


# Function to add a new patient with basic data validation
def add_patient():
    create_patients_table()
    st.title("Add Patient")
    with st.form(key="add_patient"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=150)
        height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=400.0)

        if st.form_submit_button("Submit"):
            with st.spinner("Adding patient..."):
                try:
                    conn = sqlite3.connect('data/patients.db')
                    c = conn.cursor()
                    c.execute('''INSERT INTO patients (name, age, height, weight) 
                                VALUES (?, ?, ?, ?)''', (name, age, height, weight))
                    conn.commit()
                    st.success("Patient added successfully")
                except sqlite3.Error as e:
                    st.error(f"Error adding patient: {e}")
                finally:
                    conn.close()


def delete_patient():
    st.title("Delete Patient")
    with st.form(key="delete_patient"):
        #Connect to the database
        conn = sqlite3.connect('data/patients.db')
        c = conn.cursor()
        #Get the list of patients from the database
        result = c.execute('''SELECT * FROM patients''')
        patients = result.fetchall()
        #Create a list of patient names
        patient_names = [patient[1] for patient in patients]
        #Add a dropdown to select a patient
        selected_patient = st.selectbox("Select a patient", ["Select a patient"] + patient_names, index=0)

        #Add selected patient id to session state
        st.session_state["selected_patient_id"] = selected_patient
        #Add a button to delete the patient
        if st.form_submit_button("Delete"):
            #Delete the patient from the database
            c.execute('''DELETE FROM patients WHERE id = ?''', (patients[patient_names.index(selected_patient)][0],))
            conn.commit()
            conn.close()
            #Display a success message
            st.success("Patient deleted successfully")

def view_patients():
    st.title("View Patients")
    with st.spinner("Loading..."):
        #Connect to the database
        conn = sqlite3.connect('data/patients.db')
        c = conn.cursor()
        try:
            #Get the list of patients from the database
            result = c.execute('''SELECT * FROM patients''')
            patients = result.fetchall()
            conn.close()

            # Convert the list of patients to a pandas dataframe
            patients = pd.DataFrame(patients, columns=["ID", "Name", "Age", "Height", "Weight"])
            #Display the list of patients
            st.write(patients)
        except:
            st.write("No patients found")

if __name__ == "__main__":
    add_patient()
    delete_patient()
    view_patients()