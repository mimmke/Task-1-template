import streamlit as st

st.title("Hello world")

st.write("This is my first web app.")

if st.button("IDK"):
    st.balloons()
#hallo
#hallo lara
st.button("Hallo")

gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
st.navigation(pages=([gamepage,statspage]))

