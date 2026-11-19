import streamlit as st

#configuring the entrypoint file and defining the three available pages of our game
st.set_page_config(page_title= "Homepage",page_icon="🎬")


homepage= st.Page("Homepage.py", title = "Homepage", default=True)
gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
pg=st.navigation(pages=([homepage,gamepage,statspage]))
pg.run()
