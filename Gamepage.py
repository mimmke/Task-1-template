import streamlit as st
import pandas as pd
st.set_page_config(page_title= "Gamepage",page_icon="❄️")


@st.cache_data
def load_movie_data():
    return pd.read_csv("assets/Movies_to_Emojis.csv")
movies=load_movie_data()

st.write( "Hier könnte ihre Werbung stehen")
movie= movies.loc[0,"Movies"]
st.write("First Movie Dataset: {movie}")
st.image("assets/Default Movie.png")
if "attempts" not in st.session_state:
    st.session_state.attempts=0
if "final_score" not in st.session_state:
    st.session_state.final_score=[]
with st.form("Guess"):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit",type="primary")
    if submitted:
        if guess:
            st.session_state.attempts+=1
            if guess==movie:
                st.success("You guessed correctly!")
                st.snow()
                st.session_state.final_score.append(st.session_state.attempts)
                st.write(st.session_state.final_score)
                st.session_state.attempts=0
            else:
                st.error("This is not correct, guess again")
        else:
            st.write("Please guess a movie")
with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Game Statistics", type="primary"):
        st.switch_page("Statspage.py")
if st.button("Snow"):
    st.snow()
 