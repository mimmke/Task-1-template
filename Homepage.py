import streamlit as st


with st.container(width="stretch", height="content", horizontal_alignment="center"):
    st.header("Movie Time" ,text_alignment="center")
    
    st.subheader("Welcome to our movie guessing game." ,text_alignment="center")
    
    st.space(size="medium")
    
    if st.button("Play",type="primary"):
            st.switch_page("Gamepage.py"),
            
    if st.button("Game Statistics",type="primary"):
            st.switch_page("Statspage.py")
            
st.write(st.session_state.final_score)