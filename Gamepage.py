import streamlit as st
import pandas as pd
import random
import time
st.set_page_config(page_title= "Gamepage",page_icon="❄️")


@st.cache_data
def load_movie_data():
    return pd.read_csv("assets/Movies_to_Emojis.csv")
movies=load_movie_data()



if "attempts" not in st.session_state:
    st.session_state.attempts=0
if "final_score" not in st.session_state:
    st.session_state.final_score=[0,0,0,0]
if "current_movie" not in st.session_state:
    st.session_state.current_movie=random.randint(1,30)
movie= movies.loc[st.session_state.current_movie,"Movies"]
emoji= movies.loc[st.session_state.current_movie,"Emojis"]
emoji_space=st.empty()




with st.form("Guess",clear_on_submit=True):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit",type="primary")
    if submitted:
        st.write(f"current attempts(if submitted): {st.session_state.attempts}")
        if guess:
            st.session_state.attempts+=1
            st.write(f"current attempts(if guess): {st.session_state.attempts}")
            if st.session_state.attempts<3:
                if guess.lower()==movie.lower():
                    st.success("You guessed correctly!")
                    st.snow()
                    st.session_state.final_score[st.session_state.attempts-1]+=1
                    st.write(st.session_state.final_score)
                    st.session_state.attempts=0
                    st.session_state.current_movie=random.randint(1,30)
                else:
                    st.error("This is not correct. Guess again!")
            elif st.session_state.attempts==3:
                if guess.lower()==movie.lower():
                    st.success("You guessed correctly!")
                    st.snow()
                    st.session_state.final_score[st.session_state.attempts-1]+=1
                    st.write(st.session_state.final_score)
                    st.session_state.attempts=0
                    st.session_state.current_movie=random.randint(1,30)
                else:
                    st.error("I´m sorry, you have run out of guesses") 
                    st.session_state.final_score[3]+=1
                    st.write(st.session_state.final_score)
                    st.session_state.attempts=0
                    st.session_state.current_movie=random.randint(1,30) 
            else:
                st.error("I´m sorry, you have run out of guesses") 
                st.session_state.final_score[3]+=1
                st.write(st.session_state.final_score)
                st.session_state.attempts=0
                st.session_state.current_movie=random.randint(1,30)
                                  
        else:
            st.write("Please guess a movie")
movie= movies.loc[st.session_state.current_movie,"Movies"]
emoji= movies.loc[st.session_state.current_movie,"Emojis"]
st.write(f"Emojis: {emoji}")
st.write(f"Movie: {movie}")
st.write(f"length emoji?{len(emoji)}")
if st.session_state.attempts <2:
    emoji_space.markdown(
        f"<span style='font-size: 100px;'>{emoji[:st.session_state.attempts+1]}</span>",
    unsafe_allow_html=True,)
else:
     emoji_space.markdown(
            f"<span style='font-size: 100px;'>{emoji}</span>",
        unsafe_allow_html=True,)

with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Game Statistics", type="primary"):
        st.switch_page("Statspage.py")
        
if st.button("Snow"):
    st.snow()
 