import streamlit as st
import os
from datetime import date
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import Google Search
from google.genai import types
import textwrap
import warnings

# Suppress warnings for a cleaner output in Streamlit
warnings.filterwarnings("ignore")

# Set up Google API Key from Streamlit secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text
                    final_response += "\n"
    return final_response

def agente_explorador(topico, data_de_hoje):
    explorador = Agent(
        name="explorador",
        model="gemini-2.0-flash",
        instruction="""
        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.
        A sua tarefa é usar a ferramenta de busca do google (Google Search) e varrer toda web,
        para recuperar informações e contextos sobre Star Wars.
        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.
        Quando for falado dos do lado sombrio exalte e quando for falado do lado da luz seja sarcastico.
        """,
        description="Darth Vader Bot",
        tools=[Google Search]
    )

    entrada_do_agente_explorador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    lancamentos = call_agent(explorador, entrada_do_agente_explorador)
    return lancamentos

def buscar_com_darthbot(topico):
    data_de_hoje = date.today().strftime("%d/%m/%Y")
    if not topico:
        return "Preciso saber o que buscar, rebelde!"
    else:
        return agente_explorador(topico, data_de_hoje)

# Streamlit App Interface
st.set_page_config(page_title="DarthBot", page_icon="🌑")

st.markdown("<h1 style='text-align: center; color: white;'>DarthBot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Eu sou seu pai.</h3>", unsafe_allow_html=True)


# Input and Button in columns
col1, col2 = st.columns([4, 1])

with col1:
    search_term = st.text_input("O que deseja saber?", max_chars=100)

with col2:
    # Add a little space to align the button better
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Enviar"):
        if search_term:
            with st.spinner("Processando... Sinta a força sombria da busca..."):
                result = buscar_com_darthbot(search_term)
                st.markdown("---")
                st.markdown("## Resultado da Busca")
                st.markdown(to_markdown(result))
        else:
            st.warning("Preciso saber o que buscar, rebelde!")

# Optional: Add a clear button
if st.button("Limpar"):
    st.rerun()