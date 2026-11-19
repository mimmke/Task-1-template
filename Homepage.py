import streamlit as st

#configuring a homepage with the games title and a welcome to the player 
with st.container(width="stretch", height="content", horizontal_alignment="center"):
    st.header("Movie Time" ,text_alignment="center")
    
    st.subheader("Welcome to our movie guessing game." ,text_alignment="center")
    
    st.space(size="medium")
    
    #two buttons that lead the player to the game and stats page
    if st.button("Play",type="primary"):
            st.switch_page("Gamepage.py"),
            
    if st.button("Game Statistics",type="primary"):
            st.switch_page("Statspage.py")

#initialising "final_score" in new session state
if "final_score" not in st.session_state:
    st.session_state.final_score=[]            
