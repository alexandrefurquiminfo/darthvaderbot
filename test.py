import streamlit as st
import google.generativeai as genai

# --- Configuração da Página ---
st.set_page_config(
    page_title="DarthVaderBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS (mantidos do seu código original) ---
st.markdown("""
    <style>
    .reportview-container {
        background: #000000;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    h1 {
        color: #ff0000; /* Vermelho Sith */
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    .stTextInput label {
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #4a0000; /* Vermelho escuro */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #8b0000; /* Vermelho mais vibrante no hover */
    }
    .stTextArea label {
        color: #e0e0e0;
    }
    .css-1d391kg { /* Estilo da caixa de texto input */
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 5px;
    }
    .css-q8sde7 { /* Estilo da caixa de texto input quando focada */
        border-color: #ff0000;
        box-shadow: 0 0 0 0.1rem #ff0000;
    }
    .stMarkdown p {
        color: #e0e0e0;
    }
    /* Estilos para as mensagens do chat */
    .stChatMessage {
        background-color: #222222; /* Fundo mais escuro para as mensagens */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .user-message {
        background-color: #3a3a3a; /* Cinza para mensagens do usuário */
        color: #ffffff;
        text-align: right;
    }
    .assistant-message {
        background-color: #5a0000; /* Vermelho escuro para mensagens do bot */
        color: #ffffff;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)
# --- Fim dos Estilos CSS ---

# --- Título do Aplicativo ---
st.title("DarthVaderBot 🤖")
st.markdown("Bem-vindo ao lado sombrio! Eu sou o DarthVaderBot. Fale-me seus segredos e eu os dominarei.")

# --- Inicialização da API Gemini (AQUI ESTÁ A MUDANÇA PRINCIPAL) ---
# Tenta carregar a API Key dos secrets do Streamlit
try:
    google_api_key = st.secrets["google_api_key"]
    genai.configure(api_key=google_api_key)
except KeyError:
    st.error("Erro: Sua Google API Key não foi encontrada nos segredos do Streamlit. Por favor, adicione-a em `.streamlit/secrets.toml` ou nas configurações de segredos do Streamlit Cloud.")
    st.stop() # Interrompe a execução do aplicativo se a chave não estiver configurada

# --- Inicialização do Modelo Gemini ---
# Certifique-se de que o modelo 'gemini-pro' é o que você quer usar
model = genai.GenerativeModel("gemini-pro")

# --- Inicialização do Histórico do Chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Exibir Histórico do Chat ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada do Usuário ---
prompt = st.chat_input("Fale-me seus segredos...", key="chat_input")

if prompt:
    # Adiciona a mensagem do usuário ao histórico e exibe
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Chama a API Gemini com o prompt do usuário
        # Aqui você pode adicionar lógica para dar um "toque" de Darth Vader na resposta
        # Por exemplo:
        # full_prompt = f"Finja ser Darth Vader e responda a isso: '{prompt}'"
        # response = model.generate_content(full_prompt)
        response = model.generate_content(prompt)
        ai_response = response.text

        # Adiciona a resposta do assistente ao histórico e exibe
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)
    except Exception as e:
        st.error(f"Não consigo sentir a Força... Ocorreu um erro ao gerar a resposta: {e}")
        st.error("Por favor, tente novamente mais tarde. Verifique se sua API Key está correta e se há cotas disponíveis.")

# --- Botão para Limpar Histórico ---
if st.button("Limpar Histórico", key="clear_button"):
    st.session_state.chat_history = []
    st.experimental_rerun() # Recarrega o app para limpar o histórico visualmente
