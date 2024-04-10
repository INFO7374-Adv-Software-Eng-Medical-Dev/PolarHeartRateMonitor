import streamlit as st
import time


def connect(devices_dict):
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