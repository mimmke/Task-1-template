import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title= "Statspage")
st.header("Statistics")


st.write( "Hier könnte ihre Werbung stehen")
if st.button("Let it Snow!"):
    st.snow()

df = pd.DataFrame(
    {
        "tries": list(range(20)) * 3,
        "stats": list(range(20)) * 3
        }
)

st.bar_chart(
    df,
    X= "stats",
    y= "tries",
    x_label= "Tries",
    horizontal = False    
)