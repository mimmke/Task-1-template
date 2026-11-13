import streamlit as st
st.set_page_config(page_title= "Gamepage")

st.write( "Hier könnte ihre Werbung stehen")
movie= "It"
st.image("assets/Default Movie.png")
with st.form("Guess"):
    guess=st.text_input("What movie is this?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if guess:
            if guess==movie:
                st.success("You guessed correctly!")
                st.snow()
            else:
                st.error("This is not correct, guess again")
        else:
            st.write("Please guess a movie")
if st.button("Snow"):
    st.snow()