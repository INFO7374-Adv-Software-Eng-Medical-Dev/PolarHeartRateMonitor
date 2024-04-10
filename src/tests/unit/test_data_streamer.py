import asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import sqlite3
from bleak import BleakClient

from frontend.utils.data_streamer import DataStreamer  

# Fixtures for a temporary database, and mocking BleakClient 
@pytest.fixture()
def test_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()  
    cursor.execute('''CREATE TABLE data (id INTEGER PRIMARY KEY, hr REAL, ibi REAL, timestamp REAL)''')
    yield conn
    conn.close()

@pytest.fixture()
def mock_bleak_client(mocker):
    mock_client = AsyncMock(BleakClient)
    mock_client.is_connected = AsyncMock(return_value=True) 
    mocker.patch('your_module.BleakClient', return_value=mock_client) 
    return mock_client

# Test the hr_data_conv method
@pytest.mark.asyncio
@patch('your_module.time.time_ns', return_value=123456789000000000) # Control time 
async def test_hr_data_conv(mock_time_ns, test_db, mock_bleak_client):
    data = bytearray([0x00, 100, 0x3E, 0x08])  # Simulate notification data
    streamer = DataStreamer("test_address")

    await streamer.hr_data_conv("sender", data) 

    # Retrieve data from the database to check if it was stored correctly
    conn = test_db
    c = conn.cursor()
    c.execute("SELECT hr, ibi, timestamp FROM data")
    result = c.fetchone()

    assert result[0] == 100  # Check heart rate
    assert result[1] == 1000.0  # Check calculated IBI
    assert result[2] == 1234567.89  # Check timestamp
    
# Test for subscribe_to_data to trigger notifications with mock data
@pytest.mark.asyncio
@patch('your_module.time.sleep')
async def test_subscribe_to_data(mock_sleep, mock_bleak_client, test_db):
    mock_bleak_client.start_notify = AsyncMock()
    notification_handler = MagicMock()  # Just need to check if it's called  
    mock_bleak_client.start_notify.side_effect = [notification_handler]

    streamer = DataStreamer("test_address")
    await streamer.subscribe_to_data()
    
    mock_bleak_client.start_notify.assert_called_once()
    notification_handler.assert_called_once()  
