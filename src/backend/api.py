from fastapi import FastAPI, Body
import asyncio
from polar_bluetooth_interface import DataStreamer
import numpy as np
import time


app = FastAPI(
    title="POLAR Heart Rate Monitor",
    description="Backend API to interface between Polar H10 Sensor and Frontend UI",
    version="0.1"
)

data_streamer = None   # Initialize outside of routes

@app.post('/start_stream')
async def start_stream(address: str = Body(...)):
    global data_streamer
    data_streamer = DataStreamer(address)
    await data_streamer.subscribe_to_data()
    return {"message": "Streaming started"}

@app.post('/stop_stream')
async def stop_stream():
    if not data_streamer:
        return {"error": "Stream not active"}

    data_streamer.stop_stream()
    return {"message": "Streaming stopped"}

@app.get('/current_hr')
async def get_current_hr():

    if not data_streamer:
        return {"error": "Stream not active"}

    if not data_streamer.ibi_queue_values: 
        return {"heart_rate": None}

    last_hr = data_streamer.ibi_queue_values[-1] 
    return {"heart_rate": last_hr}


