import asyncio
from bleak import BleakClient
import asyncio


class DataStreamer:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
    
    async def notification_handler(self, sender, data):
        print(f"Data: {data}")

    async def subscribe_to_data(self):
        async with self.client as client:
            await client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", self.notification_handler)
            # Timeout after 30 seconds
            await asyncio.sleep(30)  
            await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")
        
    def stream_data(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.subscribe_to_data())
    
if __name__ == "__main__":
    address = 'C44F5830-8359-25F6-C6C8-D392D1E6B89A'
    data_streamer = DataStreamer(address)
    data_streamer.stream_data()

# async def notification_handler(sender, data):
#     print(f"Heart Rate Data: {data}")

# async def subscribe_to_heart_rate(address):
#     async with BleakClient(address) as client:
#         await client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", notification_handler)
#         await asyncio.sleep(30)  # Keep the subscription active for 30 seconds
#         await client.stop_notify("00002a37-0000-1000-8000-00805f9b34fb")

# loop.run_until_complete(subscribe_to_heart_rate(address))