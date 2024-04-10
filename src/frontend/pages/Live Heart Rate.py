import streamlit as st
from utils.background import add_background
import time
import random
import pandas as pd
from utils.data_streamer import DataStreamer
import sqlite3
import asyncio
import subprocess
import os
import signal
import uuid

st.set_page_config(page_title="Live Heart Rate Monitor", layout="wide")
streamer = DataStreamer(st.session_state.get("selected_device_address"))
start_time = None
end_time = None
#Connect to the database
# '''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, hr REAL, ibi REAL, timestamp REAL)'''

# Function to select patients from the database
def select_patients():
    conn = sqlite3.connect('data/patients.db')
    c = conn.cursor()
    result = c.execute('''SELECT * FROM patients''')
    patients = result.fetchall()
    conn.close()
    
    return patients

#Function to fetch live heart rate data for the selected patient and add button to start and stop the stream
def main():
    # Check if a device address is in session state
    if st.session_state.get("selected_device_address") is None:
        st.warning("Please select a device to continue")
    else:
        # Initialize a dataframe to store the data
        data = pd.DataFrame({
            'Patient': [],
            'Time': [],
            'Heart Rate': []
        })

        patients = select_patients()
        if len(patients) == 0:
            st.write("No patients found. Please add a patient to continue")
        else:
            # Add a title to the page
            st.title("Live Heart Rate Monitor")

            # Select a patient from the list of patients and add a button to start the stream
            patient = st.selectbox("Select a patient", ["Select a patient"] + [patient[1] for patient in patients], index=0, key="selected_patient_live")
            if patient != "Select a patient":
                # st.session_state["selected_patient_live"] = patient
                st.write(f"Selected Patient: {patient}")

                # Call live_data when the "Start Stream" button is clicked
                if st.button("Start Stream", key="start"):
                    live_data(patient, data)  # Pass the selected patient and data DataFrame

                if st.button("Stop Stream", key="stop"):
                    streamer.stop = True
                    streamer.stop_stream() 
                            

#Store patient data in the database
def store_data(data: dict):
    conn = sqlite3.connect('data/heart_rate_data.db')
    c = conn.cursor()
    # create table with name, heart rate, timestamp and session_id
    c.execute('''CREATE TABLE IF NOT EXISTS hr_data (id INTEGER PRIMARY KEY, name TEXT, hr REAL, timestamp REAL, session_id TEXT)''')
    c.execute("INSERT INTO hr_data (name, hr, timestamp, session_id) VALUES (?, ?, ?, ?)", (data["name"], data["hr"], data["timestamp"], str(data['session_id'])))
    conn.commit()
    conn.close()


def fetch_live_heart_rate(patient, session_id):
    # create a connection to the database or create a new one if it does not exist

    conn = sqlite3.connect('data/data_buffer.db')
    c = conn.cursor()
    execute = c.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, hr REAL, ibi REAL, timestamp REAL)''')
    result = c.execute('''SELECT hr, timestamp FROM data ORDER BY id DESC LIMIT 1''')
    tries = 0
    max_tries = 20
    while result is None:
        # Wait for 1 second if no data is found
        time.sleep(1)
        result = c.execute('''SELECT hr, timestamp FROM data ORDER BY id DESC LIMIT 1''')
        if result.fetchone() is None:
            tries += 1
        else:
            pass
        if tries == max_tries:
            st.error("No data found. Please check the device connection")
            st.stop()
    rate, timestamp = result.fetchone()
    #Differece between the current time and the timestamp
    diff = time.time() - timestamp
    if rate < 70:
        zone = "Fat Burn"
    elif rate < 80:
        zone = "Cardio"
    else:
        zone = "Peak"
    values = {"name": patient, "hr": rate, "timestamp": time.time(), "session_id": session_id}
    store_data(values)
    return rate, zone, diff


add_background()

def live_data(patient, data):
    run = True
    # Create a placeholder for the metric and the graph
    session_id = uuid.uuid4()
    heart_rate_metric, heart_rate_zone, latency = st.empty(), st.empty(), st.empty()
    # streamer = DataStreamer(st.session_state.get("selected_device_address"))
    #Run streamer.start_stream() as a subprocess
    stream_process = subprocess.Popen(["python", "/Users/mohan/Projects/PolarHeartRateMonitor/src/frontend/utils/data_streamer.py", st.session_state.get("selected_device_address")])
    st.write(stream_process.pid)

    if st.button("Stop Stream", key="stop"):
        if stream_process:  # Ensure the process exists
            os.kill(stream_process.pid, signal.SIGINT)  # Send SIGINT (Ctrl+C like)
            # stream_process = None
            run = False
        
        # streamer.stop_stream()
        # store_data(data)
        os.remove('data/data_buffer.db')
        # st.stop()

    # Add a button to stop the stream

    # Create a line chart with an empty dataframe
    chart = st.line_chart(data)

    while run:
        # Fetch the latest heart rate data
        latest_heart_rate, zone, live_latency = fetch_live_heart_rate(patient, session_id)

        
        #Convert heart_rate_metric and heart_rate_zone to columns
        
        heart_rate_metric.metric(label="Heart Rate", value=f"{latest_heart_rate} bpm")
        heart_rate_zone.metric(label="Heart Rate Zone", value=f"{zone}", delta_color="inverse")
        latency.metric(label="Latency", value=f"{live_latency:.2f} seconds", delta_color="inverse")
        

        # Update the dataframe with the new data point
        new_data = pd.DataFrame({
            'Patient': [patient],
            'Time': [data.shape[0]],  # Assuming each update is 1 second apart
            'Heart Rate': [latest_heart_rate]
        })
        data = pd.concat([data, new_data], ignore_index=True).tail(300)  # Keep only the last 300 data points
        
        # Update the line chart
        chart.line_chart(data[['Time', 'Heart Rate']].set_index('Time'), color="#FF0000", width=0, use_container_width=True)

        
        # Wait for a short period before fetching new data
        time.sleep(1)  # Adjust the sleep time as needed based on your data source's update frequency



    



if __name__ == "__main__":
    main()
