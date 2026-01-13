import streamlit as st
from chat import StoryTeller


chat_container = st.container(height=650)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "ai" not in st.session_state:
        st.session_state.bot = StoryTeller()
    
    if "questions" not in st.session_state:
        st.session_state.questions = st.session_state.bot.questions
        

def display_chat_messages():
    with chat_container:
        for message in st.session_state.messages:   
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def handle_user_input():
    question_input = None
    bot = st.session_state.bot
    
    question_input = get_questions()
    input = st.chat_input("Talk to StoryTeller")
    
    prompt = question_input or input
    if prompt:
            
        st.session_state.messages.append({"role": "user", "content": prompt})

        bot_response = bot.chat(prompt).get("ai")

        response = f"StoryTeller: {bot_response}"

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("ai"):
                st.markdown(response)

        st.session_state.messages.append({"role": "ai", "content": response})
        st.session_state.questions = bot.questions
        st.session_state.bot = bot
        
        st.rerun()
    
    
def get_questions():
    cols = st.columns(len(st.session_state.questions))
    for i, q in enumerate(st.session_state.questions):
        if cols[i].button(q, key=f"q_{i}"):
            return q
    


def layout():
    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    init_session_state()
    layout()
