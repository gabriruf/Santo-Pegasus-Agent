import streamlit as st
from src.rag.rag import asking_to_llm, asking_to_rag
#from random import choice
#from time import sleep

# Streamed response emulator
# def response_generator():
#     response = choice(
#         [
#             "Olá, eu sou o assistente virtual da Santo Pegasus, como vai?, em que posso ser útil?",
#             "Olá, colaborador, eu sou o assistente virtual da Santo Pegasus, alguma dúvida?",
#             "Olá, eu sou o assistente virtual da Santo Pegasus, precisa de ajuda?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         sleep(0.05)

st.header("🐎 Santo Pegasus Agent", divider=True)

# Mensagem inicial do assistente (será refatorado posteriormente)
# with st.chat_message("assistant"):
#    response = st.write_stream(response_generator())

def assistant(prompt: str):
    knowledge = asking_to_rag(prompt)

    return asking_to_llm(prompt, knowledge)

def app():
    # Caso as mensagens não estejam na memória do Streamlit, criamos uma nova memória.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Carregar histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input("Digite aqui a sua duvida sobre a nossa empresa")
    if user_prompt:
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        with st.chat_message("assistant"):
            response = st.markdown(assistant(str(user_prompt)))
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    app()