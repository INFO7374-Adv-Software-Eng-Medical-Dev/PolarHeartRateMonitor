import asyncio
from bleak import BleakScanner

class BluetoothScanner:

    def __init__(self):
        self.devices = {}
    
    async def scan(self):
        devices = await BleakScanner.discover()
        for device in devices:
             device_info = str(device).split(": ")
             device_address = device_info[0]
             device_name = device_info[1]
             if device_name != None:
                    self.devices.update({device_name: device_address})
             else: 
                 pass
             
    def get_devices(self):
        return self.devices
    
    def clear_devices(self):
        self.devices = {}
    
    def print_devices(self):
        print(self.devices)
        

    def discover_devices(self):
        loop = asyncio.run(self.scan())


if __name__ == "__main__":
    scanner = BluetoothScanner()
    scanner.discover_devices()
    scanner.print_devices()