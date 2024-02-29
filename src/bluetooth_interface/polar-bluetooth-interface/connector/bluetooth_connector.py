import asyncio
from bleak import BleakClient
import asyncio



class BluetoothConnector:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
    
    async def make_connection(self):
        async with self.client as client:
            is_connected = await client.is_connected()
            print(f"Connected: {is_connected}")
            return is_connected
    async def make_disconnection(self):
        async with self.client as client:
            is_connected = await client.disconnect()
            print(f"Disconnected: {is_connected}")
            return is_connected
        
    def connect(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.make_connection())
    
    def disconnect(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.make_disconnection())

if __name__ == "__main__":
    address = 'C44F5830-8359-25F6-C6C8-D392D1E6B89A'
    connector = BluetoothConnector(address)
    connector.connect()
    # connector.disconnect()