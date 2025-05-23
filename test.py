import streamlit as st
import google.generativeai as genai
import os 
import time

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Darth Vader Bot", page_icon="https://e7.pngegg.com/pngimages/418/493/png-clipart-darth-vader-illustration-anakin-skywalker-walt-disney-imagineering-computer-icons-sith-star-wars-darth-vader-fictional-character-jedi.png")
st.title("Darth Vader Bot 🌑")
st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")

# --- Sidebar ---
st.sidebar.image("https://www.pngarts.com/files/11/Vector-Darth-Vader-Helmet-Transparent-Image.png", caption="Lorde Vader Aguarda Suas Ordens")
st.sidebar.markdown("## Sobre o DarthVaderBot")
st.sidebar.info(
    "Consulte o Lorde Sombrio dos Sith sobre qualquer tópico do universo Star Wars. "
    "Ele usará seus vastos recursos (e a Força Sombria) para encontrar as informações que você procura."
)
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com a Força (e Streamlit) por Alexandre Furquim - @bit01tec.")

# --- Carregamento da Chave API dos Secrets do Streamlit ---
with st.sidebar:
    st.header("🔑 Configuração da API")
    GOOGLE_API_KEY_SECRET = None
    try:
        GOOGLE_API_KEY_SECRET = st.secrets["GOOGLE_API_KEY"] # Acessa diretamente, vai gerar erro se não existir
        st.success("Chave API carregada dos secrets!")
    except KeyError:
        st.error("Chave API não encontrada nos secrets do Streamlit. Por favor, adicione 'GOOGLE_API_KEY' ao seu arquivo secrets.toml ou à configuração de secrets no Streamlit Cloud.")
        st.markdown(
            "**Como configurar seus secrets no Streamlit:**\n"
            "1. Crie um arquivo `.streamlit/secrets.toml` na raiz do seu projeto (para desenvolvimento local).\n"
            "2. Adicione sua chave lá: `GOOGLE_API_KEY = \"sua_chave_aqui\"`\n"
            "3. Para deploy no Streamlit Cloud, vá em 'Settings' -> 'Secrets' e adicione o secret com o mesmo nome.\n"
        )

    st.markdown("---")
    if GOOGLE_API_KEY_SECRET:
        st.success("Chave API pronta para ser usada!")
    else:
        st.info("Para consultar Lord Vader, a Chave API precisa ser configurada nos secrets.")

# --- Configuração do Modelo Gemini e Chat (Condicional à API Key) ---
model = None
chat = None
api_ready = False

SYSTEM_INSTRUCTION_VADER = (
        """
        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.
        A sua tarefa é usar a ferramenta de busca do google (Google Search) e varrer toda web,
        para recuperar informações e contextos sobre Star Wars.
        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.
        Quando for falado do lado sombrio exalte e quando for falado do lado da luz seja sarcastico e deprecie.
        Responda em português brasileiro."
        """
)

generation_config = {
    "candidate_count": 1,
    "temperature": 0.7,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

if GOOGLE_API_KEY_SECRET: # Verifica se a chave foi carregada com sucesso
    try:
        genai.configure(api_key=GOOGLE_API_KEY_SECRET)
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=SYSTEM_INSTRUCTION_VADER
        )
        api_ready = True
    except Exception as e:
        st.sidebar.error(f"Erro ao configurar a API do Google: {e}")
        st.error(f"Não foi possível conectar à API do Google com a chave fornecida. Verifique a chave e tente novamente. Detalhes: {e}")
        api_ready = False
        model = None
else:
    if "messages" not in st.session_state or not st.session_state.messages:
        st.info("⬅️ Por favor, configure sua Chave API do Google Gemini nos secrets para ativar o chatbot.")

# --- Gerenciamento do Histórico e Inicialização do Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history_gemini" not in st.session_state:
    st.session_state.chat_history_gemini = []

if api_ready and model and "chat_session" not in st.session_state:
    gemini_format_history = []
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_format_history.append({"role": role, "parts": [msg["content"]]})
    
    st.session_state.chat_session = model.start_chat(history=gemini_format_history)
    
    if not st.session_state.messages:
        initial_vader_greeting = "Eu sou Darth Vader. O que você deseja, servo?"
        st.session_state.messages.append({"role": "assistant", "content": initial_vader_greeting})

# --- Exibição das Mensagens do Chat ---
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])        

# --- Área de Input do Usuário e Botão de Envio ---
user_query = st.text_area("Sua pergunta para Lord Vader:", key="user_query_input", height=100, label_visibility="collapsed", placeholder="O que você ousa perguntar a Lord Vader?")

if st.button("Consultar Lord Vader ⚡", disabled=not api_ready):
    if not api_ready or not model or "chat_session" not in st.session_state:
        st.warning("A Força não está com você. Por favor, configure sua Chave API nos secrets.")
    elif not user_query.strip():
        st.warning("Fale! Ou será silenciado para sempre.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Lord Vader está consultando a Força..."):
            try:
                response = st.session_state.chat_session.send_message(user_query)
                vader_response_text = response.text

                st.session_state.messages.append({"role": "assistant", "content": vader_response_text})
                st.rerun()

            except Exception as e:
                st.error(f"Um distúrbio na Força impediu a comunicação: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Erro da API: {e}"})
                st.rerun()
elif not api_ready and st.session_state.get("messages") and len(st.session_state.messages) > 0 :
    pass
