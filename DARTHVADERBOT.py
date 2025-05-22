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
#def call_agent(agent: Agent, message_text: str) -> str:
#    current_session_id = f"streamlit_session_{uuid.uuid4()}"
#    session_service = InMemorySessionService()

    def call_agent_test(agent: Agent, message_text: str) -> str:
    session_id = f"test_session_{uuid.uuid4()}"
    session_service = InMemorySessionService() # Nova instância para cada chamada de teste aqui

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
    MODEL_NAME = "gemini-2.5-flash-preview-05-20" # Usando um modelo mais recente e geralmente disponível

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
if 'current_topic_input' not in st.session_state: # Usaremos este para o valor do text_input
    st.session_state.current_topic_input = ""
if 'last_searched_topic' not in st.session_state: # O tópico que foi efetivamente buscado
    st.session_state.last_searched_topic = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""
if 'search_triggered_count' not in st.session_state: # Para diferenciar cliques de submit
    st.session_state.search_triggered_count = 0


# Título e Introdução
# st.set_page_config(page_title="DarthVaderBot", page_icon="🌑") # Deve estar no topo do script
# st.title("DarthVaderBot 🌑")
# st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")
# st.markdown("---")

# Exemplos de perguntas
st.subheader("Sugestões de Consultas:")
cols_exemplos = st.columns(3)
exemplos = ["A história da Ordem Sith", "Detalhes da Millennium Falcon", "Quem é Ahsoka Tano?"]

for i, col in enumerate(cols_exemplos):
    if col.button(exemplos[i], key=f"ex{i}", use_container_width=True):
        st.session_state.current_topic_input = exemplos[i] # Apenas preenche o campo
        # Não precisa de rerun aqui, o text_input pegará o valor na próxima renderização

# Usando st.form para agrupar input e botão
with st.form(key="search_form"):
    topico_input_val = st.text_input( # O widget text_input em si
        "O que deseja saber, rebelde?",
        value=st.session_state.current_topic_input, # Controlado pelo session_state
        placeholder="Pergunte sobre personagens, naves, planetas, a Força...",
        help="Digite seu questionamento sobre o universo Star Wars.",
        key="topic_text_field" # Dando uma chave explícita
    )

    submit_button = st.form_submit_button(label="Consultar Lorde Vader ⚡", use_container_width=True)
    # O botão de limpar foi removido do form para simplificar, pode ser adicionado fora se necessário

if submit_button:
    # Atualiza current_topic_input com o valor do campo no momento da submissão
    # Isso é importante porque o usuário pode ter editado o texto após clicar no exemplo
    st.session_state.current_topic_input = topico_input_val # Captura o valor do campo de texto no submit

    if not st.session_state.current_topic_input: # Verifica o valor do session_state
        st.warning("A Força detecta uma falta de clareza. Preciso saber o que buscar, Padawan!")
    else:
        st.session_state.search_triggered_count += 1
        st.session_state.last_searched_topic = st.session_state.current_topic_input # Salva o tópico que será buscado
        st.session_state.last_result = "" # Limpa o resultado anterior

        with st.spinner(f"Lorde Vader está canalizando a Força Sombria para buscar sobre '{st.session_state.last_searched_topic}'... Isso pode levar um momento..."):
            data_hoje = date.today().strftime("%d/%m/%Y")
            try:
                # -------- SUBSTITUA PELO SEU CÓDIGO REAL ABAIXO --------
                 resultado = agente_explorador(st.session_state.last_searched_topic, data_hoje)
                 st.session_state.last_result = resultado
                # -------- BLOCO DE SIMULAÇÃO PARA TESTE DA UI --------
               # import time
               # time.sleep(2)
               # if "erro" in st.session_state.last_searched_topic.lower():
               #     st.session_state.last_result = "O lado sombrio detectou uma falha em seus sistemas. Tente novamente."
                #    st.error("Uma perturbação na Força impediu a busca: Erro simulado.")
               # else:
                #    st.session_state.last_result = f"**Sobre '{st.session_state.last_searched_topic}':**\n\nLorde Vader encontrou o seguinte:\n\n* Detalhe 1 sobre {st.session_state.last_searched_topic}.\n* Detalhe 2 sobre {st.session_state.last_searched_topic}."
                # -------- FIM DO BLOCO DE SIMULAÇÃO --------
            except Exception as e:
                st.error(f"Uma perturbação na Força impediu a busca: {e}")
                st.session_state.last_result = "Falha na consulta. O Imperador não está satisfeito."
        st.rerun() # Reexecuta para atualizar a exibição do resultado e limpar o campo de exemplo

# Botão para limpar tudo (fora do form)
if st.button("Limpar Tudo 🗑️", type="secondary"):
    st.session_state.current_topic_input = ""
    st.session_state.last_searched_topic = ""
    st.session_state.last_result = ""
    st.session_state.search_triggered_count = 0
    st.rerun()


# Exibir o último resultado
if st.session_state.search_triggered_count > 0: # Mostra se alguma busca já foi feita
    if st.session_state.last_result:
        st.markdown("---")
        st.subheader(f"📜 A Resposta de Lorde Vader sobre '{st.session_state.last_searched_topic}':")
        with st.container():
            st.markdown(st.session_state.last_result)
    # Se last_result estiver vazio após uma busca, o erro já foi mostrado

st.markdown("---")
st.caption("Que a Força (Sombria) esteja com você. Sempre.")
