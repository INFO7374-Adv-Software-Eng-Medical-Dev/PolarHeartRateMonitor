from utils.background import add_background
import streamlit as st
import sqlite3
import pandas as pd
st.set_page_config(page_title="Device Management", layout="wide")
add_background()


# Fetch the names of the patients from the database and display them in a selectbox
def select_patients():
    conn = sqlite3.connect('data/patients.db')
    c = conn.cursor()
    result = c.execute('''SELECT * FROM patients''')
    patients = result.fetchall()
    conn.close()
    
    return patients

# Get Patient data from the database
    # c.execute('''CREATE TABLE IF NOT EXISTS hr_data (id INTEGER PRIMARY KEY, name TEXT, hr REAL, timestamp REAL, session_id TEXT)''')
    # for i in range(data.shape[0]):
    #     c.execute("INSERT INTO hr_data (name, hr, timestamp, session_id) VALUES (?, ?, ?, ?)", (data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2], data.iloc[i, 3]))

def patient_data(patient):
    conn = sqlite3.connect('data/heart_rate_data.db')
    c = conn.cursor()
    result = c.execute(f'''SELECT * FROM hr_data WHERE name = "{patient}"''')
    data = result.fetchall()
    conn.close()
    
    return data


def main():
    patients = select_patients()
    if len(patients) == 0:
        st.write("No patients found. Please add a patient to continue")
    else:
        st.title("Patient History")
        patient = st.selectbox("Select a patient", ["Select a patient"] + [patient[1] for patient in patients], index=0, key="selected_patient_history")
        if patient != "Select a patient":
            # st.session_state["selected_patient_history"] = patient
            st.write(f"Selected Patient: {patient}")
            data = patient_data(patient)
            # Group the data by session_id
            data_dict = {}
            for row in data:
                if row[4] not in data_dict:
                    data_dict[row[4]] = []
                data_dict[row[4]].append(row)

            # Convert to a dataframe and filter and group the data by session_id and take the average of the heart rate
            data = pd.DataFrame()
            for key in data_dict:
                df = pd.DataFrame(data_dict[key], columns=["id", "name", "hr", "timestamp", "session_id"])
                data = pd.concat([data, df])
            data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")
            #Convert to eastern time zone
            data["timestamp"] = data["timestamp"].dt.tz_localize("UTC").dt.tz_convert("US/Eastern")
            data["hr"] = data["hr"].astype(float)
            data = data.groupby("session_id").agg({"hr": "mean", "timestamp": "first"}).reset_index()
            # Rename column name to average heart rate
            data = data.rename(columns={"hr": "Average Heart Rate", "timestamp": "Start Time"})
            drop_columns = ["session_id"]
            data = data.drop(columns=drop_columns)
            st.table(data)

if __name__ == "__main__":
    main()
