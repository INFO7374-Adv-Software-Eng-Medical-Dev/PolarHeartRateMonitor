import asyncio
from bleak import BleakClient
import numpy as np
import time 
from collections import deque
import sqlite3
import os
import streamlit as st
import signal

class DataStreamer:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
        self.ibi_queue_values = []  # Initialize IBI values queue
        self.ibi_queue_times = []   # Initialize IBI timestamps queue
        self.stop = False
    
    async def notification_handler(self, sender, data: bytearray):
        self.hr_data_conv(sender, data)

    async def subscribe_to_data(self):

        async with self.client as client:
            await client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", self.notification_handler)
            # Await the signal to stop the stream
            while not self.stop:
                await asyncio.sleep(1)
            await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")

            #Delete the database if the stop signal is received
            # os.remove('data/data_buffer.db')
        # except asyncio.CancelledError:
        #     pass  
        # finally:  # Ensure cleanup
        #     await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")
        #     os.remove('data/data_buffer.db')
                
    # async def unsubscribe(self):
    #     async with self.client as client:
    #         await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")

    def stop_stream(self):
        # break the process
        self.stop = True

    def stream_data(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.subscribe_to_data())

    def hr_data_conv(self, sender, data): 
        """
        `data` is formatted according to the GATT ... (rest of the parser docstring)
        """
        byte0 = data[0] # heart rate format
        uint8_format = (byte0 & 1) == 0
        energy_expenditure = ((byte0 >> 3) & 1) == 1
        rr_interval = ((byte0 >> 4) & 1) == 1

        if not rr_interval:
            return

        first_rr_byte = 2
        if uint8_format:
            hr = data[1]
        else:
            hr = (data[2] << 8) | data[1] # uint16
            first_rr_byte += 1
        
        if energy_expenditure:
            # ee = (data[first_rr_byte + 1] << 8) | data[first_rr_byte]
            first_rr_byte += 2

        for i in range(first_rr_byte, len(data), 2):
            ibi = (data[i + 1] << 8) | data[i]
            ibi = np.ceil(ibi / 1024 * 1000)  
            self.ibi_queue_values.append(np.array([ibi]))
            self.ibi_queue_times.append(np.array([time.time_ns()/1.0e9]))
        print(hr)
        self.store_data(hr, ibi)

    #Store the data in the database with timestamp
    def store_data(self, hr, ibi):
        # Create a buffer to store the data
        conn = sqlite3.connect('data/data_buffer.db')
        c = conn.cursor()
        #Create the table if it does not exist
        c.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, hr REAL, ibi REAL, timestamp REAL)''')
        c.execute("INSERT INTO data (hr, ibi, timestamp) VALUES (?, ?, ?)", (hr, ibi, time.time_ns()/1.0e9))
        #Remove the 120th element from the database if the buffer is full
        # c.execute("DELETE FROM data WHERE id IN (SELECT id FROM data ORDER BY id ASC LIMIT 1)")
        conn.commit()
        conn.close()

    async def start_stream(self):
        self._stream_task = asyncio.create_task(self.subscribe_to_data())
        try:
            await self._stream_task
        except asyncio.CancelledError:
            pass
            
    async def stop_stream(self):
        await self.client.disconnect() 

def main(address):
    streamer = DataStreamer(address)
    streamer.stream_data()



def stop_handler(signum, frame):  # Function to handle stop signals
    streamer.stop_stream()

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        address = sys.argv[1]
        streamer = DataStreamer(address)  # Instantiate the DataStreamer
        main(address)

        # Register signal handlers for termination
        signal.signal(signal.SIGINT, stop_handler)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, stop_handler)  # Handle other termination signals



