import streamlit as st

st.write("Welcome to our guessing game.")

if st.button("Gamepage"):
    st.switch_page("pages/Gamepage.py")

if st.button("Statistics"):
    st.switch_page("pages/statspage")