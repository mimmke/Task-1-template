import streamlit as st
import pandas as pd

st.set_page_config(page_title= "Statspage")
st.header("Your Game Statistics", text_alignment="center")
st.space(size="medium")

data = {
    "Tries": ["1 Try", "2 Tries", "3 Tries", "Failed"],
    "final_score": [st.session_state.final_score[0],st.session_state.final_score[1],st.session_state.final_score[2],st.session_state.final_score[3]]
}

df = pd.DataFrame(data)
st.bar_chart(df, x="Tries", y="final_score", x_label=" ",y_label=" ", color="#DAA520")

with st.container(width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):
    if st.button("Play", type="primary"):
        st.switch_page("Gamepage.py")
        
guessed_movies = st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2]
if guessed_movies == 1:
    st.write(f"You have rightly guessed one movie.")
elif guessed_movies == 0:
    st.write(f"You have not yet guessed any movie right.")
else:
    st.write(f"You have rightly guessed {guessed_movies} movies.")
    
if st.session_state.final_score[3]==1:
    st.write(f"you have failed to guess one movie.")
elif st.session_state.final_score[3]==0:
    st.write(f"You have not yet failed to guess a movie.")
else:
    st.write(f"You have failed to guess {st.session_state.final_score[3]} movies.")
st.space(size="small")
st.write(f"Your average amount of guesses per movie is ...")

if st.button("Let it Snow!"):
    st.snow()