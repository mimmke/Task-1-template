import streamlit as st
st.set_page_config(page_title= "Gamepage")

st.write( "Hier könnte ihre Werbung stehen")
movie= "It"
st.image("assets/Default Movie.png")
if "attempts" not in st.session_state:
    st.session_state.attempts=0
if "final_score" not in st.session_state:
    st.session_state.final_score=[]
with st.form("Guess"):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit")
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
if st.button("Snow"):
    st.snow()