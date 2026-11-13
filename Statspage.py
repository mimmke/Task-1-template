import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title= "Statspage")
st.header("Your Statistics")



if st.button("Let it Snow!"):
    st.snow()


#st.bar_chart(
   # x=list(range(20)) * 3,
   # y=list(range(20)) * 3,
   # x_label="Tries"  
#)

if st.button("Play",horizontal_alignment="right"):
    st.switch_page("Gamepage.py")