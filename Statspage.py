import streamlit as st
import pandas as pd

#initialising "final_score" with 6 elements
if "final_score" not in st.session_state:
    st.session_state.final_score=[0,0,0,0,0,0]

#configering the page and giving it a header with its title    
st.set_page_config(page_title= "Statspage",page_icon="📊")
st.header("Your Game Statistics", text_alignment="center")

st.space(size="medium")

with st.container(width="stretch", height="content", horizontal_alignment="center"):
    #setting up a pageview that appears when no game has been played yet, that sends you to the playpage to start a game
    if sum(st.session_state.final_score) == 0:
        st.subheader("You have not yet played a round." ,text_alignment="center")
        
        st.space(size="medium")
        
        if st.button("Press here to play.", type="primary"):
            st.switch_page("Gamepage.py")
    else: 
        #if at least one game has been played, a data frame will be configered including the st.session_state.final_score for the different amounts of guesses
        data = {
                    "Guesses": ["1 Guess", "2 Guesses", "3 Guesses", "4 Guesses", "5 Guesses", "Failed"],
                    "final_score": [st.session_state.final_score[0], st.session_state.final_score[1], st.session_state.final_score[2], st.session_state.final_score[3], st.session_state.final_score[4], st.session_state.final_score[5]]
        }

        df = pd.DataFrame(data)
        #the bar chart shows how often the player needed an amount of guesses from 1 to 5 guesses per movie and how many movies the player failed to guess
        st.bar_chart(df, x="Guesses", y="final_score", x_label=" ",y_label=" ", color="#DAA520")

        #with rounds we show how many rounds of the game the player has played in this session state
        rounds = st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2] + st.session_state.final_score[3] + st.session_state.final_score[4] + st.session_state.final_score[5]
        if rounds == 1:
            st.subheader("You have played :green[one] round",divider="grey",text_alignment="center")
        else:
            st.subheader(f"You have played :green[{rounds}] rounds",divider="grey", text_alignment="center")  
        
        #next we compute the amount of correctly guessed movies and the average amount of guesses per movie            
        guessed_movies = st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2] + st.session_state.final_score[3] + st.session_state.final_score[4]
        average_guesses = (1 * st.session_state.final_score[0] + 2 * st.session_state.final_score[1] + 3 * st.session_state.final_score[2] + 4 * st.session_state.final_score[3] + 5 * st.session_state.final_score[4]+ 6 * st.session_state.final_score[5]) / rounds
        
        st.space(size="small")
        
        #with the average amount of guesses we categorize the player by their guissing quality into one of three ranks 
        if average_guesses <= 1.66:
            st.success('You have reached HUMAN NETFLIX level 🎬', icon="🥇")
        elif average_guesses <= 3.22:
            st.warning('You are a POPCORN ADDICT 🍿', icon="🥈")
        else:
            st.error('You seem to be a CASUAL VIEWER 📺', icon="🥉")
        
        st.space(size="small")
        
        #amount of rightly guessed movies and failed to guess movies
        if guessed_movies == 1:
            st.markdown(f"You have rightly guessed :green[one] movie.",unsafe_allow_html=True, text_alignment="center")
        elif guessed_movies == 0:
            st.markdown(f":red[You have not yet guessed any movie right.]",unsafe_allow_html=True, text_alignment="center")
        else:
            st.markdown(f"You have rightly guessed :green[{guessed_movies}] movies.",unsafe_allow_html=True, text_alignment="center")
                    
        if st.session_state.final_score[5]==1:
            st.markdown(f"You have failed to guess :red[one] movie.",unsafe_allow_html=True, text_alignment="center")
        elif st.session_state.final_score[5]==0:
            st.markdown(f":green[You have not yet failed to guess a movie.]",unsafe_allow_html=True, text_alignment="center")
        else:
            st.markdown(f"You have failed to guess :red[{st.session_state.final_score[5]}] movies.",unsafe_allow_html=True, text_alignment="center")
            
        st.space(size="xsmall")
        
        #average amount of guesses per movie
        if guessed_movies > 0:
            st.markdown(f"Your average amount of guesses per movie is :green[{average_guesses}]",unsafe_allow_html=True, text_alignment="center")
            
        st.space(size="small")
        
        #button to get back to the playpage
        with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
            if st.button("Play", type="primary"):
                st.switch_page("Gamepage.py")
                
        st.space(size="small")
        
        if st.button("Let it Snow!"):
            st.snow()
            
