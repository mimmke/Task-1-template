import streamlit as st
import pandas as pd
import random
import regex
from openai import OpenAI, AuthenticationError, OpenAIError
import json
st.set_page_config(page_title= "Gamepage",page_icon="🎲")

#if no ai key was given, get a new one, normally one should be given on the homepage
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

#initialize a new client with the user key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=st.session_state.user_key,
)

#load our movie data set and save it under movies
@st.cache_data
def load_movie_data():
    return pd.read_csv("assets/Movies_to_Emojis.csv")
movies=load_movie_data()


# set up the session states we use throughout the app, initialize them for the first use
if "attempts" not in st.session_state: # to save the current amount of guesses for the current movie
    st.session_state.attempts=0
if "final_score" not in st.session_state: # to save how many guesses it took to correctly guess the movie or if the user failed
    st.session_state.final_score=[0,0,0,0,0,0]
if "current_movie" not in st.session_state: #to get a random movie that stays consistent hroughout guesses
    st.session_state.current_movie=random.randint(1,99)
if "prev_mov" not in st.session_state:# a list to be able to check if the random movie was already used in the game
    st.session_state.prev_mov=[]

# write a function to find new random movie if the user guessed correctly or is out of attempts
def new_movie_to_guess():
    while True:
            st.session_state.current_movie=random.randint(1,99)
            movie= movies.loc[st.session_state.current_movie,"Movies"]
            if len(st.session_state.prev_mov)>80:   #if the list of already used movies gets too long, delete the first elements so they can be used again
                del st.session_state.prev_mov[:50]
            if movie not in st.session_state.prev_mov:
                break
    st.session_state.prev_mov.append(movie) 
    return st.session_state.current_movie

#create our first movie
movie= movies.loc[st.session_state.current_movie,"Movies"]
emoji= movies.loc[st.session_state.current_movie,"Emojis"]
emoji_list= regex.findall(r"\X", emoji) #to get a list of clearly separated emojis
if st.session_state.prev_mov == []:  # this is only for the very first movie, the others will be added through the function beforehand
    st.session_state.prev_mov.append(movie)
emoji_space=st.empty()# set up a space to display our emojis in (to make sure it is in the correct position even if we reassign emojis later in the code)

#the prompt we give our model to handle the input
system_prompt="""You are a witty gamemaster. Evaluate the user guess by comparing it to the movie to be guessed and the current emojis. Your answer must be a valid JSON object with different values. “Message” should contain a witty answer evaluating the user guess. If hint_status is 0, provide a short answer, if hint_status is 1 give a hint regarding the genre of the movie to be guessed in your answer and if hint_status is 2 provide a hint in your answer with one prominent movie character. NEVER give away the movie title or plot (if the prominent character's name is the same as the movie title, describe the character instead of naming them).Consider the current available emojis in your answer and see if the user guessed movie could also be described by them.If the user provides nonsense input, give a witty answer that they wasted a guess. If the user guessed correctly, provide a funny message congratulating the user. “is_exact_match” should be true if the user guess refers to the exact movie to be guessed or the corresponding franchise ,otherwise false. Ignore spelling mistakes (e.g., "the avangers" for "The Avengers") and ignore missing subtitles or extra phrases after the main title (e.g., "E.T." for "E.T. the Extra-Terrestrial"). “increase_attempts” should be 0 if “is_exact_match” is true, otherwise 1. Output ONLY raw JSON. Do not include markdown formatting, backticks,new line, or any introductory text. Your response should look something like this: {"Message": "...", "increase_attempts": 1, "is_exact_match": false}"""
with st.form("Guess",clear_on_submit=True):# create the form where the user can guess
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit",type="primary")
    if submitted:
        ##st.write(f"current attempts(if submitted): {st.session_state.attempts}")
        
        if guess: #to check whether the user actuelly guessed something before submitting
            #st.session_state.attempts+=1
            ##st.write(f"current attempts(if guess): {st.session_state.attempts}")
            if st.session_state.attempts<5:# the user has 5 attempts, otherwise the guess is invalid
                if st.session_state.attempts <2: #the current emojis are used to be given to the model to analyze
                    current_emojis="".join(emoji_list[:st.session_state.attempts+1])
                else:
                    current_emojis="".join(emoji_list)
                if st.session_state.attempts<2:# depending on how many guesses  the user uses, the model later provides more detailed hints
                    hint_status=0
                elif st.session_state.attempts==2: # the model will provide a hint for the genre of the movie to be guessed
                    hint_status=1
                else: # for the last guess the model will give a hint regarding an important character
                    hint_status=2
                try:# try sending the message to the model
                    with st.spinner("Your guess is being evaluated..."):
                        response=client.chat.completions.create(
                            model="RedHatAI/gemma-4-31B-it-FP8-Dynamic",
                            messages= [
                                {"role":"system","content":system_prompt}, #our pormpt so the model knows what to do wioth the data
                                {"role":"user","content":f"movie to be guessed: {movie} user guess: {guess} current emojis:{current_emojis} hint status: {hint_status}  " } # the model is handed th euser guess and additional current info to create an answer
                            ]
                        )
                    ##st.write(repr(response.choices[0].message.content))
                    result=None #this is to make the try except block possible
                    try: #the model is supposed to return a JSON dictionary. Sometimes this does not work, which is why we have the try except
                        result=json.loads(response.choices[0].message.content.strip()) 
                        ##st.write(result)
                    except json.JSONDecodeError: #in case the model returns an unusable response
                        st.error("The model has not given an accurate answer. Please retry submitting your guess")
                    if result != None:# if the JSON load worked
                        if result["is_exact_match"]==True: # the model decides if guess was correct or not and if the attempts should be increased
                            st.success("You guessed correctly!")                            #this block saves final score, resets attempts and creates a new movie
                            st.snow()
                            st.write(result["Message"])
                            st.session_state.final_score[st.session_state.attempts]+=1
                            #st.write(st.session_state.final_score)
                            st.session_state.attempts=0
                            st.session_state.current_movie=new_movie_to_guess()
                        else:
                            st.session_state.attempts=st.session_state.attempts+result["increase_attempts"]
                            if st.session_state.attempts==5:
                                st.error("I'm sorry, you have run out of guesses") 
                                st.write(f"The movie described by the emojis {emoji} was {movie}!")
                                st.session_state.final_score[5]+=1
                                #st.write(st.session_state.final_score)
                                st.session_state.attempts=0
                                st.session_state.current_movie=new_movie_to_guess()
                            else:
                                st.error(f"This is not correct. Guess again! You have {5-st.session_state.attempts} attempts left")
                                st.write(result["Message"])
                        
                except AuthenticationError:   # if there are problems with the key etc.
                    st.error("API was not accepted, please check it!")
                except OpenAIError:
                    st.error("API AI request has failed, please checkt it and try again!")
                
            else: # in case of 5 (or more) guesses, tell the user the solution, save final score as failed and reset attempts and current movie
                st.error("I'm sorry, you have run out of guesses") 
                st.write(f"The movie described by the emojis {emoji} was {movie}!")
                st.session_state.final_score[5]+=1
                ##st.write(st.session_state.final_score)
                st.session_state.attempts=0
                st.session_state.current_movie=new_movie_to_guess()
             
        else: # in case the user submitted without typing anything in
            st.write("Please guess a movie") 
#get the current movie and emojis using the session state index, depending on how the state changed through user behaviour
movie= movies.loc[st.session_state.current_movie,"Movies"]
emoji= movies.loc[st.session_state.current_movie,"Emojis"]
emoji_list= regex.findall(r"\X", emoji)
##st.write(f"Emojis: {emoji}")
##st.write(f"Movie: {movie}")
##st.write(f"Previous movies: {st.session_state.prev_mov}")

#if the user guessed less then 2 times, show as many emojis for the movie as attempts
if st.session_state.attempts <2:
    emoji_space.markdown(
        f"<span style='font-size: 100px;'>{"".join(emoji_list[:st.session_state.attempts+1])}</span>",
    unsafe_allow_html=True,)
else:# after 2 guesses all emojis will be displayed
     emoji_space.markdown(
            f"<span style='font-size: 100px;'>{"".join(emoji_list)}</span>",
        unsafe_allow_html=True,)

#button to switch to the statistics page
with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Game Statistics", type="primary"):
        st.switch_page("Statspage.py")
        

 