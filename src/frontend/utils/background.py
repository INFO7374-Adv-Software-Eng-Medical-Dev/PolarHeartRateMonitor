import base64
import streamlit as st

def get_image_as_base64(url):
    with open(url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def add_background():
    background_image = get_image_as_base64("images/background.jpeg")
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{background_image}");
            background-repeat: no-repeat;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )