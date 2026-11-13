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

with st.container(width="content", height="content",horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Play"):
    st.switch_page("Gamepage.py")