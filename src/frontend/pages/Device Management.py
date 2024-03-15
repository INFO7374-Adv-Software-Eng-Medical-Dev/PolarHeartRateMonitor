import streamlit as st
from utils.bluetooth_scanner import BluetoothScanner
from utils.background import add_background
import time
st.set_page_config(page_title="Device Management", layout="wide")
add_background()
def main():

    # Button to scan for bluetooth devices
    if st.button("Scan for Devices", key="scan"):
        with st.spinner("Scanning for Devices..."):
            devices = BluetoothScanner()
            devices.discover_devices()
            devices_dict = devices.get_devices()
            
            # Output the list of devices to the user to select from
            st.write("Select a device to connect to:")
            list_devices = list(devices_dict.keys())
            
            if len(list_devices) == 0:
                st.write("No devices found")
            else:
                # Use the on_change parameter to update the session state when a new device is selected
                selected_device = st.selectbox("Devices", ["Select a device"] + list_devices, index=0, key="selected_device", on_change=set_session_state, args=(devices_dict, ))
        #Exit the function after the scan is complete
        return 

                

def set_session_state(devices_dict):
    #Wait for 2 seconds to ensure the session state is updated
    with st.spinner("Connecting..."):
        time.sleep(1)
    selected_device = st.session_state.get('selected_device')
    if selected_device and selected_device != "Select a device":
        st.session_state["selected_device_address"] = devices_dict[selected_device]
        st.session_state["selected_device_name"] = selected_device  

#Disconnect from the selected device
def disconnect():
    st.session_state["selected_device_address"] = None
    st.session_state["selected_device_name"] = None



def display_active_connections():
    st.title("Active Connections")
    
    with st.spinner("Updating Connections..."):
        if "selected_device_address" in st.session_state:
            st.sidebar.write("Connected to: ", st.session_state["selected_device_name"])
            st.write("Connected to: ", st.session_state["selected_device_name"])
            st.write("Device Address: ", st.session_state["selected_device_address"])
            if st.button("Disconnect", key="disconnect"):
                disconnect()
        else:
            st.write("No active connections found")

if __name__ == "__main__":
    display_active_connections()
    main()
    