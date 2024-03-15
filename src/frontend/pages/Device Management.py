import streamlit as st
from utils.bluetooth_scanner import BluetoothScanner
from utils.background import add_background

st.set_page_config(page_title="Device Management", layout="wide")

def main():
    add_background()
    selected_device = None
    # Button to scan for bluetooth devices
    if st.button("Scan for Devices"):
        with st.spinner("Scanning for Devices..."):
            devices = BluetoothScanner()
            devices.discover_devices()
            devices_dict = devices.get_devices()
            
            # Output the list of devices to the user to select from and store the selected device's address in st.session_state
            st.write("Select a device to connect to:")
            list_devices = list(devices_dict.keys())
            
            if len(list_devices) == 0:
                st.write("No devices found")
            else:
                # selected_device = st.selectbox("Devices", ["Select a device"] + list_devices, index=0, on_change=set_session_state, args=(devices_dict, ))
                selected_device = st.selectbox("Devices", ["Select a device"] + list_devices, index=0)

    while selected_device is not None:
        set_session_state(devices_dict)
        break
                

# Set device address and name in session state
def set_session_state(devices_dict):
    selected_device = st.session_state.get('selected_device')
    if selected_device and selected_device != "Select a device":
        st.session_state["selected_device_address"] = devices_dict[selected_device]
        st.session_state["selected_device_name"] = selected_device  
        st.write("Selected Device: ", selected_device)
        st.write("Device Address: ", devices_dict[selected_device])

        if st.session_state["selected_device_address"]:
            st.button("Disconnect", on_click=disconnect)

#Disconnect from the selected device
def disconnect():
    st.session_state["selected_device_address"] = None
    st.session_state["selected_device_name"] = None



def display_active_connections():
    st.title("Active Connections")
    
    with st.spinner("Updating Connections..."):
        if "selected_device_address" in st.session_state:
            st.write("Connected to: ", st.session_state["selected_device_name"])
            st.write("Device Address: ", st.session_state["selected_device_address"])
        else:
            st.write("No active connections found")

if __name__ == "__main__":
    display_active_connections()
    main()
    