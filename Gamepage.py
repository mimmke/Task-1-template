import streamlit as st
st.set_page_config(page_title= "Gamepage")

st.write( "Hier könnte ihre Werbung stehen")
movie= "It"
st.image("assets/Default Movie.png")

guess=st.text_input("What movie is this?")

if movie==guess:
    st.success("You guessed correctly!")
    st.snow()
else:
    st.error("This is not correct, guess again")
if st.button("Snow"):
    st.snow()