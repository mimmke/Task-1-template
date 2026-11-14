import streamlit as st
import pandas as pd

st.set_page_config(page_title= "Statspage")
st.header("Your Game Statistics", text_alignment="center")
st.space(size="medium")

data = {
    "Tries": ["1 Try", "2 Tries", "3 Tries", "Failed"],
    "Counts": [1, 3, 5, 2]    
}

df = pd.DataFrame(data)
st.bar_chart(df, x="Tries", y="Counts", x_label=" ", color="#DAA520")

with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Play", type="primary"):
        st.switch_page("Gamepage.py")

if st.button("Let it Snow!"):
    st.snow()