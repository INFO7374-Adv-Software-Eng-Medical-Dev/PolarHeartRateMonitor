import streamlit as st
from utils.background import add_background
import time
import random
import pandas as pd

st.set_page_config(page_title="Live Heart Rate Monitor", layout="wide")

def fetch_live_heart_rate():
    # This function simulates fetching live heart rate data.
    rate = random.randint(60, 100)
    if rate < 70:
        zone = "Fat Burn"
    elif rate < 80:
        zone = "Cardio"
    else:
        zone = "Peak"
    return rate, zone

add_background()

# Create a placeholder for the metric and the graph

heart_rate_metric, heart_rate_zone = st.empty(), st.empty()

# Initialize a dataframe to store the data
data = pd.DataFrame({
    'Time': [],
    'Heart Rate': []
})

# Create a line chart with an empty dataframe
chart = st.line_chart(data)

while True:
    # Fetch the latest heart rate data
    latest_heart_rate, zone = fetch_live_heart_rate()
    
    #Convert heart_rate_metric and heart_rate_zone to columns
    
    heart_rate_metric.metric(label="Heart Rate", value=f"{latest_heart_rate} bpm")
    heart_rate_zone.metric(label="Heart Rate Zone", value=f"{zone}", delta_color="inverse")
    

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