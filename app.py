import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
#configuring the entrypoint file and defining the three available pages of our game
st.set_page_config(page_title= "Homepage",page_icon="🎬")

with st.sidebar:
    api_key=st.text_input(
        "UOS AI API-Key",
        type="password",
        key="uos_api_key",
        placeholder="sk-..."
    ).strip()


if "user_key" not in st.session_state:
    if not api_key:
        st.info("Please enter your UOS API Key")
        st.stop()
    else:
        st.session_state.user_key=api_key



homepage= st.Page("Homepage.py", title = "Homepage", default=True)
gamepage= st.Page("Gamepage.py",title ="The Game Page")
statspage=st.Page("Statspage.py",title="The Statistics")
pg=st.navigation(pages=([homepage,gamepage,statspage]))
pg.run()
