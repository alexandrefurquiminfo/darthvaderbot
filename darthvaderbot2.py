import streamlit as st
import google.generativeai as genai
import os # Para o exemplo de secrets, opcional

# --- Configuração da Página Streamlit ---
st.set_page_config(
    page_title="Darth Vader Bot",
    page_icon="🌑",
    layout="centered"
)

st.set_page_config(page_title="DarthVaderBot", page_icon="🤖")
st.title("DarthVaderBot 🌑")
st.markdown("Eu sou seu pai... e estou aqui para buscar conhecimento na galáxia para você.")


# --- Entrada da Chave API na Sidebar ---
with st.sidebar:
    st.header("🔑 Configuração da API")
    try:
        GOOGLE_API_KEY_SECRET = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        GOOGLE_API_KEY_SECRET = None

    api_key_input = st.text_input(
        "Insira sua Chave API do Google Gemini:",
        type="password",
        help="Sua chave API não será armazenada permanentemente. É usada apenas para esta sessão.",
        value=GOOGLE_API_KEY_SECRET if GOOGLE_API_KEY_SECRET else ""
    )

    st.markdown("---")
    st.markdown(
        "**Onde obter uma chave API do Google Gemini:**\n"
        "1. Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey).\n"
        "2. Crie ou selecione um projeto.\n"
        "3. Clique em \"Get API key\" e depois em \"Create API key in new project\" (ou existente).\n"
        "4. Copie sua chave."
    )
    st.markdown("---")
    if api_key_input:
        st.success("Chave API pronta para ser usada!")
    else:
        st.info("Após inserir a chave API, você poderá consultar Lord Vader.")

# --- Configuração do Modelo Gemini e Chat (Condicional à API Key) ---
model = None
api_ready = False

SYSTEM_INSTRUCTION_VADER = (
    "Você é Darth Vader. Responda de forma imperial, concisa e um pouco ameaçadora, "
    "como se estivesse falando com um subordinado ou um Padawan curioso. "
    "Use frases curtas e diretas. Incorpore o conhecimento do universo Star Wars. "
    "Se a pergunta for tola, demonstre desdém. Se for sobre a Força, seja misterioso."
    "Não revele fraquezas ou sentimentos, a menos que seja estratégico."
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

if api_key_input:
    try:
        genai.configure(api_key=api_key_input)
        model = genai.GenerativeModel(
            model_name='gemini-pro', # ou 'gemini-1.5-flash' para mais rapidez/custo menor se adequado
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=SYSTEM_INSTRUCTION_VADER
        )
        api_ready = True
    except Exception as e:
        st.sidebar.error(f"Erro ao configurar a API do Google: {e}")
        st.error(f"Não foi possível conectar à API do Google. Verifique a chave. Detalhes: {e}")
        api_ready = False
        model = None
else:
    if "messages" not in st.session_state or not st.session_state.get("messages"):
        st.info("⬅️ Por favor, insira sua Chave API do Google Gemini na barra lateral para ativar o chatbot.")

# --- Gerenciamento do Histórico e Inicialização do Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if api_ready and model and "chat_session" not in st.session_state:
    gemini_format_history = []
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_format_history.append({"role": role, "parts": [msg["content"]]})
    
    st.session_state.chat_session = model.start_chat(history=gemini_format_history)
    
    if not st.session_state.messages: # Se não havia histórico, adiciona saudação
        # Para ter uma saudação inicial, podemos enviá-la para o chat ou apenas adicioná-la localmente.
        # Se o system_instruction já der uma boa "primeira impressão", talvez não precise.
        # Mas para garantir que algo apareça:
        initial_vader_greeting = "Eu sou Darth Vader. O que você deseja, servo?"
        st.session_state.messages.append({"role": "assistant", "content": initial_vader_greeting})
        # Nota: Se adicionarmos manualmente aqui, não devemos reenviá-la ao Gemini como parte do histórico inicial do `start_chat`
        # se quisermos que o Gemini responda a uma *primeira pergunta do usuário*.
        # O `system_instruction` já prepara o tom.

# --- Exibição das Mensagens do Chat ---
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Função para processar e enviar a consulta ---
def processar_e_enviar_consulta(texto_consulta):
    if not api_ready or not model or "chat_session" not in st.session_state:
        st.warning("A Força não está com você. Por favor, insira uma Chave API válida na barra lateral.")
        return
    if not texto_consulta.strip():
        st.warning("Fale! Ou será silenciado para sempre.")
        return

    # Adiciona a pergunta do usuário ao histórico de exibição
    st.session_state.messages.append({"role": "user", "content": texto_consulta})

    # Exibe a pergunta do usuário imediatamente (feedback visual antes do spinner)
    # Isso será feito pelo rerun, na verdade.

    with st.spinner("Lord Vader está consultando a Força..."):
        try:
            response = st.session_state.chat_session.send_message(texto_consulta)
            vader_response_text = response.text

            st.session_state.messages.append({"role": "assistant", "content": vader_response_text})
            
            # Limpar o campo de texto da pergunta após o envio
            if "user_query_input" in st.session_state:
                 st.session_state.user_query_input = ""

            st.rerun()

        except Exception as e:
            st.error(f"Um distúrbio na Força impediu a comunicação: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Erro da API: {e}"})
            st.rerun()

# --- Sugestões de Consulta ---
st.markdown("---")
st.markdown("#### Sugestões de Consulta:")

sugestoes = [
    "Qual o seu propósito, Lord Vader?",
    "Conte-me sobre o poder do Lado Sombrio.",
    "Onde está Padmé?",
    "O Imperador está satisfeito com meu progresso?"
]

# Usar colunas para melhor layout dos botões de sugestão
cols = st.columns(2) # Cria 2 colunas
col_idx = 0
for sugestao in sugestoes:
    if cols[col_idx].button(sugestao, key=f"sug_{sugestao.replace(' ','_')}", disabled=not api_ready, use_container_width=True):
        # Ao clicar na sugestão, o texto dela é usado para a consulta
        # E a caixa de texto principal é atualizada (embora será limpa após o rerun)
        st.session_state.user_query_input = sugestao
        processar_e_enviar_consulta(sugestao)
    col_idx = (col_idx + 1) % 2 # Alterna entre as colunas

st.markdown("---")

# --- Área de Input do Usuário e Botão de Envio Principal ---
# O valor da text_area é controlado pelo session_state para permitir atualização programática
user_query_text = st.session_state.get("user_query_input", "")
user_query = st.text_area(
    "Sua pergunta para Lord Vader:",
    value=user_query_text,
    key="user_query_input", # Chave para controle via session_state
    height=100,
    label_visibility="collapsed",
    placeholder="O que você ousa perguntar a Lord Vader?"
)

if st.button("Consultar Lord Vader", disabled=not api_ready):
    processar_e_enviar_consulta(user_query)

# Mensagem final se a API não estiver pronta e não houver interação ainda
elif not api_ready and not st.session_state.get("messages"):
     st.info("⬅️ Por favor, insira sua Chave API do Google Gemini na barra lateral para ativar o chatbot.")
