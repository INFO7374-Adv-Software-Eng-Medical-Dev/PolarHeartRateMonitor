import asyncio
import pytest
from unittest.mock import patch
from frontend.utils.bluetooth_scanner import BluetoothScanner

@pytest.fixture
def mock_discover():
    return ["AA:BB:CC:DD:EE:FF: Device 1", "11:22:33:44:55:66: Device 2", "FF:EE:DD:CC:BB:AA: None"]

def test_scan(mock_discover):
    scanner = BluetoothScanner()
    asyncio.run(scanner.scan())
    devices = scanner.get_devices()
    # Check if devices is not empty
    assert devices != {}

def test_get_devices(mock_discover):
    scanner = BluetoothScanner()
    scanner.devices = {"Device 1": "AA:BB:CC:DD:EE:FF", "Device 2": "11:22:33:44:55:66"}
    assert scanner.get_devices() == scanner.devices

def test_clear_devices(mock_discover):
    scanner = BluetoothScanner()
    scanner.devices = {"Device 1": "AA:BB:CC:DD:EE:FF"}
    scanner.clear_devices()
    assert scanner.devices == {}

def test_discover_devices(mock_discover):
    scanner = BluetoothScanner()
    scanner.discover_devices()
    devices = scanner.get_devices()
    expected_devices = {'Polar H10 CE1E0720': 'C44F5830-8359-25F6-C6C8-D392D1E6B89A','Midhun’s iPhone': 'BEA1A0C8-90C2-A24E-5317-13BFF9C1E721'}

    # Check if expected_devices is in devices and try 3 times
    for _ in range(3):
        if expected_devices.items() <= devices.items():
            break
        else:
            scanner.clear_devices()
            scanner.discover_devices()
            devices = scanner.get_devices()
    assert expected_devices.items() <= devices.items()