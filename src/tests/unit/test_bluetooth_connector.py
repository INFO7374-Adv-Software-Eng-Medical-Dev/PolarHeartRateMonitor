import streamlit as st
import pytest
from unittest.mock import patch  # For mocking Streamlit session state

from frontend.utils.bluetooth_connector import connect, disconnect  # Replace 'your_app_module' with your file name

# Fixtures for mocking session state
@pytest.fixture
def mock_session_state():
    with patch.object(st, "session_state", {"selected_device": None}):
        yield

@pytest.fixture
def mock_selected_device_session_state():
    with patch.object(st, "session_state", {"selected_device": "Test Device"}):
        yield


# Test the connect function       
def test_connect(mock_session_state):
    devices_dict = {"Test Device": "address_123"}
    connect(devices_dict)

    assert st.session_state.get("selected_device_address") == "address_123"
    assert st.session_state.get("selected_device_name") == "Test Device"

# Test the disconnect function
def test_disconnect(mock_selected_device_session_state):
    disconnect()

    assert st.session_state.get("selected_device_address") is None
    assert st.session_state.get("selected_device_name") is None
