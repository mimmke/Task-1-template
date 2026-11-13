import streamlit as st

st.set_page_config(page_title= "Homepage")
st.title("Hello world")

st.write("This is our guessing game.")

if st.button("Gamepage"):
    st.switch_page("Gamepage.py")


gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
st.navigation(pages=([gamepage,statspage]))

