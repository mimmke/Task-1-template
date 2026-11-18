import streamlit as st
import pandas as pd

if "final_score" not in st.session_state:
    st.session_state.final_score=[0,0,0,0,0,0]
    
st.set_page_config(page_title= "Statspage")
st.header("Your Game Statistics", text_alignment="center")

st.space(size="medium")

with st.container(width="stretch", height="content", horizontal_alignment="center"):
    if sum(st.session_state.final_score) == 0:
        st.subheader("You have not yet played a round." ,text_alignment="center")
        
        st.space(size="medium")
        
        if st.button("Press here to play.", type="primary"):
            st.switch_page("Gamepage.py")
    else:   
        data = {
                    "Guesses": ["1 Guess", "2 Guesses", "3 Guesses", "4 Guesses", "5 Guesses", "Failed"],
                    "final_score": [st.session_state.final_score[0], st.session_state.final_score[1], st.session_state.final_score[2], st.session_state.final_score[3], st.session_state.final_score[4], st.session_state.final_score[5]]
        }

        df = pd.DataFrame(data)
        st.bar_chart(df, x="Guesses", y="final_score", x_label=" ",y_label=" ", color="#DAA520")

        rounds = st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2] + st.session_state.final_score[3] + st.session_state.final_score[4] + st.session_state.final_score[5]
        if rounds == 1:
            st.subheader("You have played one round.")
        else:
            st.subheader(f"You have played {rounds} rounds.")  
                     
        guessed_movies = st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2] + st.session_state.final_score[3] + st.session_state.final_score[4]
        average_guesses = (1 * st.session_state.final_score[0] + 2 * st.session_state.final_score[1] + 3 * st.session_state.final_score[2] + 4 * st.session_state.final_score[3] + 5 * st.session_state.final_score[4]) / guessed_movies
        
        st.space(size="small")
        
        if average_guesses <= 1.66:
            st.success('You have reached HUMAN NETFLIX level 🎬', icon="🥇")
        elif average_guesses <= 3.22:
            st.warning('You are a POPCORN ADDICT 🍿', icon="🥈")
        else:
            st.error('You seem to be a CASUAL VIEWER 📺', icon="🥉")
        
        st.space(size="small")
        
        if guessed_movies == 1:
            st.write(f"You have rightly guessed one movie.")
        elif guessed_movies == 0:
            st.write(f"You have not yet guessed any movie right.")
        else:
            st.write(f"You have rightly guessed {guessed_movies} movies.")
                    
        if st.session_state.final_score[5]==1:
            st.write(f"You have failed to guess one movie.")
        elif st.session_state.final_score[5]==0:
            st.write(f"You have not yet failed to guess a movie.")
        else:
            st.write(f"You have failed to guess {st.session_state.final_score[5]} movies.")
            
        st.space(size="xsmall")
        
        if guessed_movies > 0:
            st.write(f"Your average amount of guesses per guessed movie is {average_guesses}")
            
        st.space(size="small")
        
        with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
            if st.button("Play", type="primary"):
                st.switch_page("Gamepage.py")
                
        st.space(size="small")
        
        if st.button("Let it Snow!"):
            st.snow()
            
