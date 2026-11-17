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
st.write(guessed_movies)       
st.write(f"You have guessed {st.session_state.final_score[0] + st.session_state.final_score[1] + st.session_state.final_score[2]} movies.")
st.write(f"You have failed to guess {st.session_state.final_score[3]} movies.")
st.space(size="small")
st.write(f"Your average amount of guesses per movie is ...")

if st.button("Let it Snow!"):
    st.snow()