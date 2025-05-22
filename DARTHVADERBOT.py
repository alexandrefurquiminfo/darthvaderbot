import streamlit as st
import os
from datetime import date
import textwrap
import warnings
import uuid
import google.generativeai as genai
import streamlit as st


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
# (Seu código de carregamento de API Key aqui)
# Para rodar localmente com secrets.toml
try:
    # Tenta carregar dos segredos do Streamlit (funciona no Cloud e localmente se st.secrets estiver configurado)
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("GOOGLE_API_KEY não encontrada ou vazia nos segredos. Adicione-a em 'Manage app' -> 'Settings' -> 'Secrets'.")
        st.stop()
    os.environ["GOOGLE_API_KEY"] = api_key
except Exception as e: # Captura genérica para problemas com st.secrets
    st.error(f"Erro ao tentar acessar st.secrets['GOOGLE_API_KEY']: {e}. Certifique-se de que os segredos estão configurados.")
    st.stop()

if not os.getenv("GOOGLE_API_KEY"): # Verificação final
    st.error("GOOGLE_API_KEY não está configurada como variável de ambiente após tentativa de carregar dos segredos. Verifique a configuração.")
    st.stop()


# --- Funções do Agente (adaptadas do seu notebook) ---
# AGORA Agent, Runner, etc., são conhecidos aqui
def call_agent(agent: Agent, message_text: str) -> str:
    current_session_id = f"streamlit_session_{uuid.uuid4()}"
    session_service = InMemorySessionService()

    # Para depuração, verifique se a sessão é realmente criada
    # st.write(f"Tentando criar sessão com ID: {current_session_id}") # DEBUG
    try:
        session = session_service.create_session(
            app_name=agent.name,
            user_id="streamlit_user",
            session_id=current_session_id # Usar o ID único
        )
        # st.write(f"Sessão criada: {session.session_id}. Sessões no serviço: {list(session_service._sessions.keys())}") # DEBUG
    except Exception as e:
        st.error(f"Erro ao CRIAR sessão {current_session_id}: {e}")
        return "Falha ao iniciar a comunicação com a Força."

    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = genai_types.Content(role="user", parts=[genai_types.Part(text=message_text)])

    final_response = ""
    try:
        # st.write(f"Runner iniciando com session_id: {current_session_id}") # DEBUG
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
        # st.write(f"Runner concluiu para session_id: {current_session_id}") # DEBUG
    except ValueError as ve:
        st.error(f"ValueError no runner.run para session_id {current_session_id}: {ve}") # DEBUG específico
        # Adicione mais detalhes do session_service se possível
        st.error(f"Sessões existentes no service no momento do erro: {list(session_service._sessions.keys())}")
        return "Lorde Vader está enfrentando interferências na Força (sessão não encontrada)... Tente novamente mais tarde."
    except Exception as e:
        st.error(f"Erro ao executar o agente para session_id {current_session_id}: {e}") # DEBUG
        return "Lorde Vader está enfrentando interferências na Força... Tente novamente mais tarde."
    return final_response


def agente_explorador(topico: str, data_de_hoje: str) -> str:
    MODEL_NAME = "gemini-1.5-flash-latest" # Usando um modelo mais recente e geralmente disponível

    explorador = Agent(
        name="explorador_vader",
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

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Darth_Vader_original_helmet.jpg/800px-Darth_Vader_original_helmet.jpg", caption="Lorde Vader Aguarda Suas Ordens")
st.sidebar.markdown("## Sobre o DarthVaderBot")
st.sidebar.info(
    "Consulte o Lorde Sombrio dos Sith sobre qualquer tópico do universo Star Wars. "
    "Ele usará seus vastos recursos (e a Força Sombria) para encontrar as informações que você procura."
)
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com a Força (e Streamlit).")


# Usando st.session_state para manter o estado
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False # Para controlar a exibição da mensagem "sem resultados"

# Título e Introdução já definidos no seu código principal, ex:
# st.set_page_config(page_title="DarthVaderBot", page_icon="🌑")
# st.title("DarthVaderBot 🌑")
# st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")
# st.markdown("---")

# Exemplos de perguntas
st.subheader("Exemplos de Consultas ao Lorde Vader:")
cols_exemplos = st.columns(3)
exemplos = ["A história da Ordem Sith", "Detalhes da Millennium Falcon", "Quem é Ahsoka Tano?"]
if 'example_topic' not in st.session_state:
    st.session_state.example_topic = ""

for i, col in enumerate(cols_exemplos):
    if col.button(exemplos[i], key=f"ex{i}"):
        st.session_state.example_topic = exemplos[i] # Guarda o exemplo clicado
        # Não precisa mais de st.experimental_rerun() aqui, o valor será usado no text_input

# Usando st.form para agrupar input e botão
with st.form(key="search_form"):
    # Campo de entrada para o tópico
    # Se um exemplo foi clicado, usa ele, senão o último tópico ou vazio
    valor_inicial_topico = st.session_state.example_topic if st.session_state.example_topic else st.session_state.last_topic
    topico_input = st.text_input(
        "O que deseja saber, rebelde?",
        value=valor_inicial_topico, # Usa o valor do exemplo se clicado
        placeholder="Pergunte sobre personagens, naves, planetas, a Força...",
        help="Digite seu questionamento sobre o universo Star Wars."
    )
    st.session_state.example_topic = "" # Limpa o exemplo após usar

    # Botão de busca dentro do form
    col1_submit, col2_clear = st.columns([3,1])
    with col1_submit:
        submit_button = st.form_submit_button(label="Consultar Lorde Vader ⚡", use_container_width=True)
    with col2_clear:
        clear_button_form = st.form_submit_button(label="Limpar Busca", use_container_width=True, type="secondary")


if clear_button_form:
    st.session_state.last_topic = ""
    st.session_state.last_result = ""
    st.session_state.search_triggered = False
    topico_input = "" # Limpa visualmente o campo de input (após rerun)
    st.rerun() # Força o rerun para limpar o campo de texto imediatamente

if submit_button: # Se o botão de submit do form foi pressionado
    if not topico_input:
        st.warning("A Força detecta uma falta de clareza. Preciso saber o que buscar, Padawan!")
    else:
        st.session_state.search_triggered = True
        st.session_state.last_topic = topico_input # Salva o tópico atual
        st.session_state.last_result = "" # Limpa o resultado anterior antes da nova busca

        # Mostrar spinner e processar a busca
        with st.spinner(f"Lorde Vader está canalizando a Força Sombria para buscar sobre '{topico_input}'... Isso pode levar um momento..."):
            # Simulando a chamada ao agente (substitua pelo seu código real)
            # data_hoje = date.today().strftime("%d/%m/%Y")
            # try:
            #     resultado = agente_explorador(topico_input, data_hoje)
            #     st.session_state.last_result = resultado
            # except Exception as e:
            #     st.error(f"Uma perturbação na Força impediu a busca: {e}")
            #     st.session_state.last_result = "Falha na consulta. O Imperador não está satisfeito."

            # -------- INÍCIO DO BLOCO DE SIMULAÇÃO (REMOVA E USE SEU CÓDIGO REAL) --------
            import time
            time.sleep(3) # Simula o tempo de processamento
            if "erro" in topico_input.lower():
                 st.session_state.last_result = "O lado sombrio detectou uma falha em seus sistemas. Tente novamente."
                 st.error("Uma perturbação na Força impediu a busca: Erro simulado.")
            else:
                 st.session_state.last_result = f"**Sobre '{topico_input}':**\n\nLorde Vader encontrou o seguinte, seu verme insignificante:\n\n*   Detalhe importante 1 sobre {topico_input}.\n*   Detalhe importante 2, mais impressionante, sobre {topico_input}.\n*   Os Jedi nunca entenderiam a profundidade de {topico_input}."
            # -------- FIM DO BLOCO DE SIMULAÇÃO --------


# Exibir o último resultado
if st.session_state.search_triggered: # Só mostra a seção de resultados se uma busca foi feita
    if st.session_state.last_result:
        st.markdown("---")
        st.subheader("📜 A Resposta de Lorde Vader:")
        with st.container(): # Usar um container para poder aplicar estilo se desejado
            # Você pode usar st.info(), st.success() ou apenas st.markdown()
            # st.info(st.session_state.last_result)
            st.markdown(st.session_state.last_result)
    elif not st.session_state.last_result and topico_input: # Se houve busca mas sem resultado (ex: erro)
        # A mensagem de erro já foi exibida no bloco try/except
        pass
    # Não mostrar "nenhum resultado ainda" se a página acabou de carregar

st.markdown("---")
st.caption("Que a Força (Sombria) esteja com você. Sempre.")
