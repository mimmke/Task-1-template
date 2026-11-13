import streamlit as st
st.header("Movie Time")
st.subheader("Welcome to our movie guessing game.")

with st.container(width="stretch", height="content", horizontal=True, horizontal_alignment="center"):
    if st.button("Gamepage"):
            st.switch_page("Gamepage.py"),
            
    if st.button("Statistics"):
            st.switch_page("Statspage.py")