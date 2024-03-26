import streamlit as st
from utils.background import add_background
import time
import random
import pandas as pd
from utils.data_streamer import DataStreamer
import sqlite3

st.set_page_config(page_title="Live Heart Rate Monitor", layout="wide")

#Connect to the database
# '''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, hr REAL, ibi REAL, timestamp REAL)'''

def fetch_live_heart_rate():
    # This function simulates fetching live heart rate data.
    conn = sqlite3.connect('/Users/mohan/Projects/PolarHeartRateMonitor/data_buffer.db')
    c = conn.cursor()
    result = c.execute('''SELECT hr, timestamp FROM data ORDER BY id DESC LIMIT 1''')
    rate, timestamp = result.fetchone()
    #Differece between the current time and the timestamp
    diff = time.time() - timestamp
    if rate < 70:
        zone = "Fat Burn"
    elif rate < 80:
        zone = "Cardio"
    else:
        zone = "Peak"
    return rate, zone, diff

add_background()

# Create a placeholder for the metric and the graph

heart_rate_metric, heart_rate_zone, latency = st.empty(), st.empty(), st.empty()

# Initialize a dataframe to store the data
data = pd.DataFrame({
    'Time': [],
    'Heart Rate': []
})

# Create a line chart with an empty dataframe
chart = st.line_chart(data)

while True:
    # Fetch the latest heart rate data
    latest_heart_rate, zone, live_latency = fetch_live_heart_rate()
    
    #Convert heart_rate_metric and heart_rate_zone to columns
    
    heart_rate_metric.metric(label="Heart Rate", value=f"{latest_heart_rate} bpm")
    heart_rate_zone.metric(label="Heart Rate Zone", value=f"{zone}", delta_color="inverse")
    latency.metric(label="Latency", value=f"{live_latency:.2f} seconds", delta_color="inverse")
    

    # Update the dataframe with the new data point
    new_data = pd.DataFrame({
        'Time': [data.shape[0]],  # Assuming each update is 1 second apart
        'Heart Rate': [latest_heart_rate]
    })
    data = pd.concat([data, new_data], ignore_index=True).tail(300)  # Keep only the last 300 data points
    
    # Update the line chart
    chart.line_chart(data.set_index('Time'), color="#FF0000", width=0, use_container_width=True)
    
    # Wait for a short period before fetching new data
    time.sleep(1)  # Adjust the sleep time as needed based on your data source's update frequency