import streamlit as st
import os
from datetime import date
import textwrap
import warnings
import uuid
import google.generativeai as genai
import sys


# Importações do Google ADK e GenAI DEVEM ESTAR AQUI, ANTES DAS FUNÇÕES
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types as genai_types # Renomeado para evitar conflito com st.types
from datetime import date

# Configurações Iniciais
warnings.filterwarnings("ignore")

# Título e descrição do App
st.set_page_config(page_title="DarthVaderBot", page_icon="🤖")
st.title("DarthVaderBot 🌑")
st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")

# --- Carregamento da API Key ---
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("GOOGLE_API_KEY não encontrada ou vazia nos segredos. Adicione-a em 'Manage app' -> 'Settings' -> 'Secrets'.")
        st.stop()
    os.environ["GOOGLE_API_KEY"] = api_key
except Exception as e:
    st.error(f"Erro ao tentar acessar st.secrets['GOOGLE_API_KEY']: {e}. Certifique-se de que os segredos estão configurados.")
    st.stop()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY não está configurada como variável de ambiente após tentativa de carregar dos segredos. Verifique a configuração.")
    st.stop()


# --- Inicialização da sessão do ADK no st.session_state ---
if 'adk_session_id' not in st.session_state:
    st.session_state.adk_session_id = str(uuid.uuid4()) # Gera um ID único para a sessão do ADK
    # st.session_state.adk_session_service = InMemorySessionService() # Não é necessário persistir o serviço, apenas o ID

# Instancie o serviço de sessão UMA VEZ por rerun ou passe-o como argumento se necessário
# Como o InMemorySessionService é simples, podemos instanciá-lo na função, mas o importante é o session_id
# Ou melhor ainda, inicialize-o uma vez na sessão do Streamlit, garantindo que ele persista.
if 'session_service' not in st.session_state:
    st.session_state.session_service = InMemorySessionService()


# --- Funções do Agente (adaptadas do seu notebook) ---
def call_agent(agent: Agent, message_text: str) -> str:
    # Use o session_id persistente do Streamlit
    current_session_id = st.session_state.adk_session_id
    session_service = st.session_state.session_service # Use a instância persistente

    # Para depuração, verifique se a sessão é realmente criada
    # st.write(f"Tentando criar sessão com ID: {current_session_id}") # DEBUG
    try:
        # Tente criar a sessão APENAS se ela ainda não existir no serviço
        if not session_service.get_session(current_session_id):
            session = session_service.create_session(
                app_name=agent.name,
                user_id="streamlit_user",
                session_id=current_session_id
            )
            # st.write(f"Sessão criada: {session.session_id}. Sessões no serviço: {list(session_service._sessions.keys())}") # DEBUG
        else:
            # st.write(f"Sessão {current_session_id} já existe. Reutilizando.") # DEBUG
            pass # A sessão já existe, não precisa criar novamente
    except Exception as e:
        st.error(f"Erro ao CRIAR/VERIFICAR sessão {current_session_id}: {e}")
        return "Falha ao iniciar a comunicação com a Força."

    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=message_text)])

    final_response = ""
    try:
        # st.write(f"Runner iniciando com session_id: {current_session_id}") # DEBUG
        for event in runner.run(
            user_id="streamlit_user",
            session_id=current_session_id,
            new_message=content
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        final_response += "\n"
        # st.write(f"Runner concluiu para session_id: {current_session_id}") # DEBUG
    except ValueError as ve:
        st.error(f"ValueError no runner.run para session_id {current_session_id}: {ve}")
        st.error(f"Sessões existentes no service no momento do erro: {list(session_service._sessions.keys())}")
        return "Lorde Vader está enfrentando interferências na Força (sessão não encontrada)... Tente novamente mais tarde."
    except Exception as e:
        st.error(f"Erro ao executar o agente para session_id {current_session_id}: {e}")
        return "Lorde Vader está enfrentando interferências na Força... Tente novamente mais tarde."
    return final_response


def agente_explorador(topico: str, data_de_hoje: str) -> str:
    MODEL_NAME = "gemini-1.5-flash"

    explorador = Agent(
        name="explorador_vader",
        model=MODEL_NAME,
        instruction="""
        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.
        A sua tarefa é usar a ferramenta de busca do google (Google Search) e varrer toda web,
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

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Darth_Vader_original_helmet.jpg/800px-Darth_Vader_original_helmet.jpg", caption="Lorde Vader Aguarda Suas Ordens")
st.sidebar.markdown("## Sobre o DarthVaderBot")
st.sidebar.info(
    "Consulte o Lorde Sombrio dos Sith sobre qualquer tópico do universo Star Wars. "
    "Ele usará seus vastos recursos (e a Força Sombria) para encontrar as informações que você procura."
)
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com a Força (e Streamlit).")


# Usando st.session_state para manter o estado
if 'current_topic_input' not in st.session_state:
    st.session_state.current_topic_input = ""
if 'last_searched_topic' not in st.session_state:
    st.session_state.last_searched_topic = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""
if 'search_triggered_count' not in st.session_state:
    st.session_state.search_triggered_count = 0


# Exemplos de perguntas
st.subheader("Sugestões de Consultas:")
cols_exemplos = st.columns(3)
exemplos = ["A história da Ordem Sith", "Detalhes da Millennium Falcon", "Quem é Ahsoka Tano?"]

for i, col in enumerate(cols_exemplos):
    if col.button(exemplos[i], key=f"ex{i}", use_container_width=True):
        st.session_state.current_topic_input = exemplos[i]


with st.form(key="search_form"):
    topico_input_val = st.text_input(
        "O que deseja saber, rebelde?",
        value=st.session_state.current_topic_input,
        placeholder="Pergunte sobre personagens, naves, planetas, a Força...",
        help="Digite seu questionamento sobre o universo Star Wars.",
        key="topic_text_field"
    )

    submit_button = st.form_submit_button(label="Consultar Lorde Vader ⚡", use_container_width=True)


if submit_button:
    st.session_state.current_topic_input = topico_input_val

    if not st.session_state.current_topic_input:
        st.warning("A Força detecta uma falta de clareza. Preciso saber o que buscar, Padawan!")
    else:
        st.session_state.search_triggered_count += 1
        st.session_state.last_searched_topic = st.session_state.current_topic_input
        st.session_state.last_result = ""

        with st.spinner(f"Lorde Vader está canalizando a Força Sombria para buscar sobre '{st.session_state.last_searched_topic}'... Isso pode levar um momento..."):
            data_hoje = date.today().strftime("%d/%m/%Y")
            try:
                 resultado = agente_explorador(st.session_state.last_searched_topic, data_hoje)
                 st.session_state.last_result = resultado
            except Exception as e:
                st.error(f"Uma perturbação na Força impediu a busca: {e}")
                st.session_state.last_result = "Falha na consulta. O Imperador não está satisfeito."
        st.rerun()

# Botão para limpar tudo (fora do form)
if st.button("Limpar Tudo 🗑️", type="secondary"):
    st.session_state.current_topic_input = ""
    st.session_state.last_searched_topic = ""
    st.session_state.last_result = ""
    st.session_state.search_triggered_count = 0
    st.rerun()


# Exibir o último resultado
if st.session_state.search_triggered_count > 0:
    if st.session_state.last_result:
        st.markdown("---")
        st.subheader(f"📜 A Resposta de Lorde Vader sobre '{st.session_state.last_searched_topic}':")
        with st.container():
            st.markdown(st.session_state.last_result)

st.markdown("---")
st.caption("Que a Força (Sombria) esteja com você. Sempre.")
