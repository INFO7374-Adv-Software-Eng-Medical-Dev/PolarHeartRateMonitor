import asyncio
from bleak import BleakScanner

"""
This class is used to scan for bluetooth devices and store them in a dictionary.
"""
class BluetoothScanner:
    def __init__(self):
        self.devices = {}
    
    async def scan(self):
        """
        This function scans for bluetooth devices and stores them in a dictionary.
        """
        devices = await BleakScanner.discover()
        #Parsing the devices and storing them in a dictionary
        for device in devices:
             device_info = str(device).split(": ")
             device_address = device_info[0]
             device_name = device_info[1]
             if device_name != None or device_name != "None":
                    self.devices.update({device_name: device_address})
             else: 
                 pass
             
    def get_devices(self):
        """
        This function returns the dictionary of devices.
        """
        return self.devices
    
    def clear_devices(self):
        """
        This function clears the dictionary of devices.
        """
        self.devices = {}
    
    def print_devices(self):
        """
        This function prints the dictionary of devices.
        """
        print(self.devices)
        

    def discover_devices(self):
        """
        This function is used to run the scan function in a loop.
        """
        loop = asyncio.run(self.scan())


if __name__ == "__main__":
    scanner = BluetoothScanner()
    scanner.discover_devices()
    scanner.print_devices()