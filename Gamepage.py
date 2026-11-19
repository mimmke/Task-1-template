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
st.write(f"trial and error {st.session_state["trial_and_error"]}")
user_guess=st.chat_input("Guess a movie")

system_prompt="""You are a witty gamemaster. Evaluate the user input by comparing it to a given movie and the current emojis. Your answer must be a valid JSON object with several different values. “Message” should contain a witty answer where you evaluate the guessers answer by evaluating whether the current emojis could also be used for the user input movie. Also compare the genres of the user guess and the movie to be guessed. Please also take into account if the movie the user guessed is in the same franchise and adjust your message accordingly. Provide a nice, witty and funny message taking all this into account, without providing too much detailed help.Never give away the movie title and do not talk about the plot at all. The next value in the dictionary should be “increase_attempts”  which you fill with 0 if the movie that was guessed is a movie of the same franchise or fill with 1 if not. Lastly the dictionary should contain a value “is_exact_match” which should be true if the guessed movie and the movie to be guessed are the same, otherwise false. Please ignore any spelling mistakes in the guess and ignore when the user forgets additional words in the title that follow after a : or - .Never give away the right movie title. Output ONLY raw JSON. Do not include markdown formatting, backticks, or any introductory text. your response should look something like this: {"Message": "...", "increase_attempts": 1, "is_exact_match": false})"""
with st.form("Guess",clear_on_submit=True):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit",type="primary")
    if submitted:
        st.write(f"current attempts(if submitted): {st.session_state.attempts}")
        
        if guess:
            st.session_state.attempts+=1
            st.write(f"current attempts(if guess): {st.session_state.attempts}")
            if st.session_state.attempts<5:
                try:
                    with st.spinner("Your guess is being evaluated..."):
                        response=client.chat.completions.create(
                            model="google/gemma-4-E4B-it",
                            messages= [
                                {"role":"system","content":system_prompt},
                                {"role":"user","content":f"movie to be guessed: {movie} user guess: {guess}"}
                            ]
                        )
                    st.write(f"raw output: {response.choices[0].message.content}")
                    result=json.loads(response.choices[0].message.content)
                    st.write(result)
                    if result["is_exact_match"]==True:
                        st.success("You guessed correctly!")
                        st.snow()
                        st.write(result["Message"])
                        st.session_state.final_score[st.session_state.attempts-1]+=1
                        st.write(st.session_state.final_score)
                        st.session_state.attempts=0
                        st.session_state.current_movie=random.randint(1,30)
                    else:
                        st.error("This is not correct. Guess again!")
                        st.write(result["Message"])
                except AuthenticationError:
                    st.error("API was not accepted, please check it!")
                except OpenAIError:
                    st.error("API AI request has failed, please checkt it and try again!")
                
            elif st.session_state.attempts==5:
                try:
                    with st.spinner("Your guess is being evaluated..."):
                        response=client.chat.completions.create(
                            model="google/gemma-4-E4B-it",
                            messages= [
                                {"role":"system","content":system_prompt},
                                {"role":"user","content":f"movie to be guessed: {movie} user guess: {guess}"}
                                            ]
                        )
                    result=json.loads(response.choices[0].message.content)
                                    
                    if result["is_exact_match"]==True:
                        st.success("You guessed correctly!")
                        st.snow()
                        st.write(result["Message"])
                        st.session_state.final_score[st.session_state.attempts-1]+=1
                        st.write(st.session_state.final_score)
                        st.session_state.attempts=0
                        st.session_state.current_movie=random.randint(1,30)
                    else:
                        st.error("I´m sorry, you have run out of guesses") 
                        st.session_state.final_score[5]+=1
                        st.write(st.session_state.final_score)
                        st.session_state.attempts=0
                        st.session_state.current_movie=random.randint(1,30) 
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
 