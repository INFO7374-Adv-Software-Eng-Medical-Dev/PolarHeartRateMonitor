import streamlit as st
from utils.bluetooth_scanner import BluetoothScanner
from utils.background import add_background

def main():
    add_background()
    st.title("Device Management :bluetooth: ")

    # #Button to scan for bluetooth devices
    # if st.button("Scan for Devices"):
    #     st.title("Search for Bluetooth Devices")
    #     devices = BluetoothScanner()
    #     devices.discover_devices()
    #     devices = devices.get_devices()
    #     #Output the list of devices to the user to select from and store the selected device's address in st.session_state
    #     st.write("Select a device to connect to:")
    #     selected_device = st.selectbox("Devices", list(devices.keys()))
    #     st.session_state["selected_device"] = devices[selected_device]
    #     st.write("Selected Device: ", selected_device)
    #     st.write("Device Address: ", devices[selected_device])


if __name__ == "__main__":
    main()
