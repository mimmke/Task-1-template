import streamlit as st

st.set_page_config(page_title= "First page")


homepage= st.Page("Homepage.py", title = "Welcome, Player", default = True)
gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
st.navigation(pages=([homepage,gamepage,statspage]))
pg.run()
