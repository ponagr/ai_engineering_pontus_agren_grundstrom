import streamlit as st
from bot import ChatBot


chat_container = st.container(height=625)



def choose_chatbot():    
    choice = st.sidebar.radio("Choose chatbot theme", ["Stories", "Programming", "Sports", "Jokes"])
    bot_names = ["StoryBot", "CodeBot", "SportBot", "JokeBot"]
    
    if choice == "Stories":
        st.session_state.ai = st.session_state.story
        st.session_state.choice = bot_names[0]
    if choice == "Programming":
        st.session_state.ai = st.session_state.programming
        st.session_state.choice = bot_names[1]
    if choice == "Sports":
        st.session_state.ai = st.session_state.sport
        st.session_state.choice = bot_names[2]
    if choice == "Jokes":
        st.session_state.ai = st.session_state.joke
        st.session_state.choice = bot_names[3]



def init_session_state():
    if "story" not in st.session_state:
        st.session_state.story = ChatBot(system_prompt = "Generera korta berättelser för barn, samt 3 frågor relaterade till ämnet", questions = ["Skriv en historia om en kanin", "Skriv en historia om en apa", "Skriv en historia om en drake"])
    
    if "programming" not in st.session_state:
        st.session_state.programming = ChatBot(system_prompt = "Du är en programmerings instruktör, ge tips, förslag och förklaringar, samt 3 frågor relaterade till ämnet", questions = ["Vad är C#", "Vad kan man göra med Python?", "Vad är Bash?"])
    
    if "sport" not in st.session_state:
        st.session_state.sport = ChatBot(system_prompt = "Du är en sport kommentator som alltid svarar med coola sport kommentarer, samt 3 frågor relaterade till ämnet", questions = ["Vilken är den coolaste sporten?", "Ge mig 3 förslag på populära sporter", "Nämn en känd idrottare."])
    
    if "joke" not in st.session_state:
        st.session_state.joke = ChatBot(system_prompt = "Generera roliga skämt och historier, samt 3 frågor relaterade till ämnet", questions = ["Ge mig ett roligt skämt", "Skriv en rolig historia", "Ge mig ett torrt skämt om Göteborg"])
    
    if "ai" not in st.session_state:
        st.session_state.ai = st.session_state.story
    
    if "choice" not in st.session_state:
        st.session_state.choice = "StoryBot"

        

def display_chat_messages():
    with chat_container:
        for message in st.session_state.ai.messages:   
            with st.chat_message(message["role"]):
                st.markdown(message["content"])



def handle_user_input():
    name = st.session_state.choice
    question_input = None
    bot = st.session_state.ai
    
    question_input = get_questions()
    input = st.chat_input(f"Talk to {name}")
    
    prompt = question_input or input
    if prompt:
        st.session_state.ai.messages.append({"role": "user", "content": prompt})

        bot_response = bot.chat(prompt).get("ai")

        response = f"{name}: {bot_response}"

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("ai"):
                st.markdown(response)

        st.session_state.ai.messages.append({"role": "ai", "content": response})
        
        st.rerun()
    
    
    
def get_questions():
    cols = st.columns(len(st.session_state.ai.questions))
    for i, q in enumerate(st.session_state.ai.questions):
        if cols[i].button(q, key=f"q_{i}"):
            return q
    


def layout():
    display_chat_messages()
    handle_user_input()



if __name__ == "__main__":
    init_session_state()
    choose_chatbot()
    layout()
