import streamlit as st

st.set_page_config(page_title= "Statspage")
st.header("Your Statistics")

if st.button("Let it Snow!"):
    st.snow()


with st.container(width="stretch", height="content", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Play", type="primary"):
        st.switch_page("Gamepage.py")
        
Tries= ["1 Try","2 Tries", "3 Tries", "Failed"]
        
st.bar_chart(data=None, x=Tries, y=list(range(15)) * 3, x_label=Tries, color=None, horizontal=False, sort=True, stack=None, width="stretch", height="content")

