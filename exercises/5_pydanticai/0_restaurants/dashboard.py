import streamlit as st
from helpers import ask_chatbot, show_all

if __name__ == "__main__":
    st.title("Restaurant suggestbot")
    

    button = st.button("Show all restaurants")
    if button:
        all = show_all()
        st.dataframe(all)

    input = st.chat_input()
    if input:
        msg = st.chat_message("user")
        msg.text(input)
        output = ask_chatbot(input)
        if output:
            bot_msg = st.chat_message("ai")
            bot_msg.dataframe(output)
            # send input to agent