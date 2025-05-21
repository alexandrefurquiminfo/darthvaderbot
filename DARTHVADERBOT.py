import uuid # Adicionar no topo do app.py

def call_agent(agent: Agent, message_text: str) -> str:
    current_session_id = f"streamlit_session_{uuid.uuid4()}" # ID de sessão único
    session_service = InMemorySessionService()

    # Para depuração, verifique se a sessão é realmente criada
    st.write(f"Tentando criar sessão com ID: {current_session_id}") # DEBUG
    try:
        session = session_service.create_session(
            app_name=agent.name,
            user_id="streamlit_user",
            session_id=current_session_id # Usar o ID único
        )
        st.write(f"Sessão criada: {session.session_id}. Sessões no serviço: {list(session_service._sessions.keys())}") # DEBUG
    except Exception as e:
        st.error(f"Erro ao CRIAR sessão {current_session_id}: {e}")
        return "Falha ao iniciar a comunicação com a Força."

    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=message_text)])

    final_response = ""
    try:
        st.write(f"Runner iniciando com session_id: {current_session_id}") # DEBUG
        # O Runner usa o session_id passado aqui
        for event in runner.run(
            user_id="streamlit_user",
            session_id=current_session_id, # Usar o ID único
            new_message=content
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        final_response += "\n"
        st.write(f"Runner concluiu para session_id: {current_session_id}") # DEBUG
    except ValueError as ve:
        st.error(f"ValueError no runner.run para session_id {current_session_id}: {ve}") # DEBUG específico
        # Adicione mais detalhes do session_service se possível
        st.error(f"Sessões existentes no service no momento do erro: {list(session_service._sessions.keys())}")
        return "Lorde Vader está enfrentando interferências na Força (sessão não encontrada)... Tente novamente mais tarde."
    except Exception as e:
        st.error(f"Erro ao executar o agente para session_id {current_session_id}: {e}") # DEBUG
        return "Lorde Vader está enfrentando interferências na Força... Tente novamente mais tarde."
    return final_response
##

import streamlit as st
import os
from datetime import date
import textwrap
import warnings
import uuid 

# Importações do Google ADK e GenAI PRIMEIRO
from google.adk.agents import Agent 
from google.adk.runners import Runner 
from google.adk.sessions import InMemorySessionService 
from google.adk.tools import google_search 
from google.genai import types as genai_types 

# Configurações Iniciais
warnings.filterwarnings("ignore")

# Título e descrição do App
st.set_page_config(page_title="DarthVaderBot", page_icon="🤖")
st.title("DarthVaderBot 🌑")
st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")

# --- Carregamento da API Key ---
# Para rodar localmente com secrets.toml
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    st.error("Arquivo secrets.toml não encontrado. Crie .streamlit/secrets.toml com sua GOOGLE_API_KEY.")
    st.stop()
except KeyError:
    st.error("GOOGLE_API_KEY não encontrada no secrets.toml. Adicione-a.")
    st.stop()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY não está configurada. Verifique seus segredos.")
    st.stop()

# --- Funções do Agente (adaptadas do seu notebook) ---

def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="streamlit_user", session_id="streamlit_session")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=message_text)])

    final_response = ""
    try:
        for event in runner.run(user_id="streamlit_user", session_id="streamlit_session", new_message=content):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        final_response += "\n"
    except Exception as e:
        st.error(f"Erro ao executar o agente: {e}")
        return "Lorde Vader está enfrentando interferências na Força... Tente novamente mais tarde."
    return final_response

def agente_explorador(topico: str, data_de_hoje: str) -> str:
    # Use um nome de modelo válido. "gemini-2.0-flash" não é um modelo público.
    # "gemini-pro" ou "gemini-1.5-flash-latest" são boas opções.
    # Vou usar "gemini-pro" como padrão. Se "gemini-2.0-flash" é um modelo específico que você tem acesso,
    # você pode tentar usá-lo, mas pode não funcionar no ambiente do Streamlit Cloud.
    MODEL_NAME = "gemini-pro" # Ou "gemini-1.5-flash-latest"

    explorador = Agent(
        name="explorador_vader", # Nomes de agentes devem ser únicos se você tiver múltiplos
        model=MODEL_NAME,
        instruction="""
        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.
        A sua tarefa é usar a ferramenta de busca do google (google_search) e varrer toda web,
        para recuperar informações e contextos sobre Star Wars.
        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.
        Quando for falado do lado sombrio exalte e quando for falado do lado da luz seja sarcastico e deprecie.
        Responda em português brasileiro.
        """,
        description="Darth Vader Bot que busca informações sobre Star Wars.",
        tools=[google_search]
    )

    entrada_do_agente_explorador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    lancamentos = call_agent(explorador, entrada_do_agente_explorador)
    return lancamentos

# --- Interface do Usuário Streamlit ---

# Usando st.session_state para manter o último tópico e resultado
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

# Campo de entrada para o tópico
topico_input = st.text_input("O que deseja saber, rebelde?", value=st.session_state.last_topic, placeholder="Ex: A história dos Sith")

# Botão de busca
if st.button("Consultar Lorde Vader Force"):
    if not topico_input:
        st.warning("Preciso saber o que buscar, Padawan!")
    else:
        st.session_state.last_topic = topico_input
        with st.spinner(f"Lorde Vader está usando a Força para buscar sobre '{topico_input}'... Aguarde..."):
            data_hoje = date.today().strftime("%d/%m/%Y")
            try:
                resultado = agente_explorador(topico_input, data_hoje)
                st.session_state.last_result = resultado
            except Exception as e:
                st.error(f"Uma perturbação na Força impediu a busca: {e}")
                st.session_state.last_result = "Falha na consulta. O Imperador não está satisfeito."

# Exibir o último resultado
if st.session_state.last_result:
    st.subheader("Resposta de Lorde Vader:")
    
    # Simples formatação para markdown (o agente já deve retornar um texto bem formatado)
    # A função to_markdown original era para IPython, aqui usamos st.markdown diretamente.
    # Se quiser a indentação de blockquote, pode usar textwrap, mas o ideal é o agente formatar.
    # Markdown_result = textwrap.indent(st.session_state.last_result.replace('•', '  *'), '> ', predicate=lambda _: True)
    # st.markdown(Markdown_result)
    
    # Mais simples:
    st.markdown(st.session_state.last_result)

# Rodapé (opcional)
st.markdown("---")
st.markdown("Que a Força (Sombria) esteja com você.")
