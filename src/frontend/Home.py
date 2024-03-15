import streamlit as st
from utils.background import add_background


def main():
    st.title("Heart Rate Monitor")
    #Add background image from images/background.jpeg
    add_background()


if __name__ == "__main__":
    main()