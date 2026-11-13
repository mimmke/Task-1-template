import streamlit as st

st.set_page_config(page_title= "Startpage")
st.title("Hello world")

st.write("This is our guessing game.")

if st.button("IDK"):
    st.balloons()


gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
st.navigation(pages=([gamepage,statspage]))

