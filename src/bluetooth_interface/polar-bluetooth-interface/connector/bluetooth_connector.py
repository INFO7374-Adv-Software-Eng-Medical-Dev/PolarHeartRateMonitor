import asyncio
from bleak import BleakClient
import asyncio
loop = asyncio.get_event_loop()


class BluetoothConnector:
    def __init__(self, address):
        self.address = address
        self.client = BleakClient(address)
    
    async def connect(self):
        async with self.client as client:
            is_connected = await client.is_connected()
            print(f"Connected: {is_connected}")
            return is_connected
    async def disconnect(self):
        async with self.client as client:
            is_connected = await client.disconnect()
            print(f"Disconnected: {is_connected}")
            return is_connected

if __name__ == "__main__":
    address = "C44F5830-8359-25F6-C6C8-D392D1E6B89A"
    connector = BluetoothConnector(address)
    loop.run_until_complete(connector.connect())
    loop.run_until_complete(connector.disconnect())
    loop.close()