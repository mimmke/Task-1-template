import streamlit as st


with st.container(width="stretch", height="content", horizontal_alignment="center"):
    st.header("Movie Time")
    
    st.subheader("Welcome to our movie guessing game.")
    
    if st.button("Gamepage",type="primary"):
            st.switch_page("Gamepage.py"),
            
    if st.button("Statistics",type="primary"):
            st.switch_page("Statspage.py")