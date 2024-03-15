import asyncio
from bleak import BleakClient
import numpy as np
import time 

class DataStreamer:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
        self.ibi_queue_values = []  # Initialize IBI values queue
        self.ibi_queue_times = []   # Initialize IBI timestamps queue
    
    async def notification_handler(self, sender, data: bytearray):
        self.hr_data_conv(sender, data)

    async def subscribe_to_data(self):
        async with self.client as client:
            await client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", self.notification_handler)
            await asyncio.sleep(200)  
            await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")
        
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

        print(f"Heart Rate: {hr}")

if __name__ == "__main__":
    address = 'C44F5830-8359-25F6-C6C8-D392D1E6B89A'
    data_streamer = DataStreamer(address)
    data_streamer.stream_data()