import streamlit as st
import pandas as pd
import random
import time
from openai import OpenAI, AuthenticationError, OpenAIError
import json
st.set_page_config(page_title= "Gamepage",page_icon="🎲")

if "user_key" not in st.session_state:
    with st.sidebar:
        gamepage_api_key=st.text_input(
            "UOS AI API-Key",
            type="password",
            key="gamepage_uos_api_key",
            placeholder="sk-..."
            ).strip()
    if not gamepage_api_key:
        st.info("Please enter your UOS API Key")
        st.stop()
    else:
        st.session_state.user_key=gamepage_api_key

client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=st.session_state.user_key,
)

@st.cache_data
def load_movie_data():
    return pd.read_csv("assets/Movies_to_Emojis.csv")
movies=load_movie_data()



if "attempts" not in st.session_state:
    st.session_state.attempts=0
if "final_score" not in st.session_state:
    st.session_state.final_score=[0,0,0,0,0,0]
if "current_movie" not in st.session_state:
    st.session_state.current_movie=random.randint(1,30)
if "trial_and_error" not in st.session_state:
    st.session_state["trial_and_error"]=random.randint(1,10)
movie= movies.loc[st.session_state.current_movie,"Movies"]
emoji= movies.loc[st.session_state.current_movie,"Emojis"]
emoji_space=st.empty()


system_prompt="""You are a witty gamemaster. Evaluate the user guess by comparing it to the movie to be guessed and the current emojis. Your answer must be a valid JSON object with different values. “Message” should contain a witty answer evaluating the user guess. If hint_status is 0, provide a short answer, if hint_status is 1 give a hint regarding the genre of the movie to be guessed and if hint_status is 2 provide a hint with one prominent movie character. NEVER give away the movie title or plot (if the prominent character's name is the same as the movie title, describe the character instead of naming them). “is_exact_match” should be true if the user guess refers to the exact movie to be guessed or the corresponding franchise ,otherwise false. Ignore spelling mistakes (e.g., "the avangers" for "The Avengers") and ignore missing subtitles or extra phrases after the main title (e.g., "E.T." for "E.T. the Extra-Terrestrial"). “increase_attempts” should be 0 if “is_exact_match” is true, otherwise 1. Output ONLY raw JSON. Do not include markdown formatting, backticks,new line, or any introductory text. Your response should look something like this: {"Message": "...", "increase_attempts": 1, "is_exact_match": false}"""
with st.form("Guess",clear_on_submit=True):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit",type="primary")
    if submitted:
        st.write(f"current attempts(if submitted): {st.session_state.attempts}")
        
        if guess:
            #st.session_state.attempts+=1
            st.write(f"current attempts(if guess): {st.session_state.attempts}")
            if st.session_state.attempts<5:
                if st.session_state.attempts <2:
                    current_emojis=emoji[:st.session_state.attempts+1]
                else:
                    current_emojis=emoji
                if st.session_state.attempts<2:
                    hint_status=0
                elif st.session_state.attempts==2:
                    hint_status=1
                else:
                    hint_status=2
                try:
                    with st.spinner("Your guess is being evaluated..."):
                        response=client.chat.completions.create(
                            model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
                            messages= [
                                {"role":"system","content":system_prompt},
                                {"role":"user","content":f"movie to be guessed: {movie} user guess: {guess} current emojis:{current_emojis} hint status: {hint_status}  " }
                            ]
                        )
                    st.write(repr(response.choices[0].message.content))
                    result=None
                    try:
                        result=json.loads(response.choices[0].message.content.strip())
                        st.write(result)
                    except json.JSONDecodeError:
                        st.error("The model has not given an accurate answer. Please retry submitting your guess")
                    if result != None:
                        if result["is_exact_match"]==True:
                            st.success("You guessed correctly!")
                            st.snow()
                            st.write(result["Message"])
                            st.session_state.final_score[st.session_state.attempts]+=1
                            st.write(st.session_state.final_score)
                            st.session_state.attempts=0
                            st.session_state.current_movie=random.randint(1,30)
                        else:
                            st.session_state.attempts=st.session_state.attempts+result["increase_attempts"]
                            if st.session_state.attempts==5:
                                st.error("I´m sorry, you have run out of guesses") 
                                st.session_state.final_score[5]+=1
                                st.write(st.session_state.final_score)
                                st.session_state.attempts=0
                                st.session_state.current_movie=random.randint(1,30) 
                            else:
                                st.error(f"This is not correct. Guess again! You have {5-st.session_state.attempts} attempts left")
                                st.write(result["Message"])
                        
                except AuthenticationError:
                    st.error("API was not accepted, please check it!")
                except OpenAIError:
                    st.error("API AI request has failed, please checkt it and try again!")
                
            else:
                st.error("I´m sorry, you have run out of guesses") 
                st.session_state.final_score[5]+=1
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
 