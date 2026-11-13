import streamlit as st

st.set_page_config(page_title= "Statspage")
st.header("Your Statistics")

if st.button("Let it Snow!"):
    st.snow()


with st.container(width="content", height="content",horizontal_alignment="right", vertical_alignment="bottom"):
    if st.button("Play"):
        st.switch_page("Gamepage.py")