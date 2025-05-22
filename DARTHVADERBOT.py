import streamlit as st
import google.generativeai as genai
import os # Para o exemplo de secrets, opcional
import time

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="DarthVaderBot", page_icon="🤖")
st.title("DarthVaderBot 🌑")
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

# --- Entrada da Chave API na Sidebar ---
with st.sidebar:
    st.header("🔑 Configuração da API")
    # Tenta carregar a chave dos secrets do Streamlit (ideal para deploy)
    # GOOGLE_API_KEY_SECRET = os.environ.get("GOOGLE_API_KEY") # Para deploy no Streamlit Cloud usando secrets
    # Se não encontrar no environment, tenta st.secrets (para secrets.toml local ou no Streamlit Cloud)
    try:
        GOOGLE_API_KEY_SECRET = st.secrets.get("GOOGLE_API_KEY")
    except Exception: # st.secrets não disponível localmente sem config ou em versões antigas
        GOOGLE_API_KEY_SECRET = None


    api_key_input = st.text_input(
        "Insira sua Chave API do Google Gemini e aperte enter",
        type="password",
        help="Sua chave API não será armazenada permanentemente. É usada apenas para esta sessão.",
        value=GOOGLE_API_KEY_SECRET if GOOGLE_API_KEY_SECRET else "" # Preenche se existir no secret
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
chat = None
api_ready = False

# Configurações do modelo (do seu código original)
# É uma boa prática definir a persona (system prompt) diretamente no modelo se a API suportar,
# ou como a primeira mensagem na inicialização do chat.
# Para Gemini, `system_instruction` é o parâmetro ideal para o GenerativeModel.
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
    "temperature": 0.7, # Ajustei um pouco para menos aleatoriedade, mas ainda criativo
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
            model_name='gemini-2.0-flash',
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=SYSTEM_INSTRUCTION_VADER # Adicionando a persona aqui!
        )
        api_ready = True
    except Exception as e:
        st.sidebar.error(f"Erro ao configurar a API do Google: {e}")
        st.error(f"Não foi possível conectar à API do Google com a chave fornecida. Verifique a chave e tente novamente. Detalhes: {e}")
        api_ready = False
        model = None # Garante que o modelo não seja usado
else:
    if "messages" not in st.session_state or not st.session_state.messages: # Se não há chave e nenhuma mensagem ainda
        st.info("⬅️ Por favor, insira sua Chave API do Google Gemini na barra lateral para ativar o chatbot.")


# --- Gerenciamento do Histórico e Inicialização do Chat ---
# O histórico do chat é armazenado no session_state do Streamlit
if "messages" not in st.session_state:
    # Mensagem inicial de Darth Vader (não depende da API para ser definida, mas o chat sim)
    st.session_state.messages = [] # Começa vazio, a primeira mensagem do Vader virá do system_instruction se usarmos chat_input,
                                  # ou podemos adicionar uma manualmente após a API estar pronta.

if "chat_history_gemini" not in st.session_state:
    st.session_state.chat_history_gemini = []


# Inicializar o objeto de chat do Gemini APENAS SE a API estiver pronta e o chat não existir
# E se o histórico de mensagens estiver vazio (para não reiniciar o chat com histórico antigo)
if api_ready and model and "chat_session" not in st.session_state:
    # Converte o histórico do Streamlit (se houver) para o formato do Gemini
    # Isso é útil se você quiser pré-carregar um histórico
    gemini_format_history = []
    if st.session_state.messages: # Se já houver mensagens no st.session_state (ex: recarregou a página com chave)
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_format_history.append({"role": role, "parts": [msg["content"]]})
    
    st.session_state.chat_session = model.start_chat(history=gemini_format_history)
    
    # Adiciona a primeira mensagem de saudação do Vader se não houver histórico prévio
    if not st.session_state.messages:
        # Podemos simular uma primeira "resposta" do Vader baseada no system_instruction
        # ou ter uma mensagem padrão.
        initial_vader_greeting = "Eu sou Darth Vader. O que você deseja, servo?" # Ou obtenha uma resposta real
        st.session_state.messages.append({"role": "assistant", "content": initial_vader_greeting})
        # Não precisamos adicionar isso ao `gemini_format_history` novamente se `start_chat` já o considerou
        # ou se o `system_instruction` já cobre a saudação.



# --- Exibição das Mensagens do Chat ---
for message in st.session_state.get("messages", []): # Usar .get para evitar erro se "messages" não existir
    with st.chat_message(message["role"]):
        st.markdown(message["content"])        


# --- Área de Input do Usuário e Botão de Envio ---
user_query = st.text_area("Sua pergunta para Lord Vader:", key="user_query_input", height=100, label_visibility="collapsed", placeholder="O que você ousa perguntar a Lord Vader?")

if st.button("Consultar Lord Vader ⚡", disabled=not api_ready): # Desabilita o botão se a API não estiver pronta
    if not api_ready or not model or "chat_session" not in st.session_state:
        st.warning("A Força não está com você. Por favor, insira uma Chave API válida na barra lateral.")
    elif not user_query.strip():
        st.warning("Fale! Ou será silenciado para sempre.")
    else:
        # Adiciona a pergunta do usuário ao histórico de exibição
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Exibe a pergunta do usuário imediatamente (feedback visual)
        with st.chat_message("user"):
            st.markdown(user_query)

        # Envia a mensagem para o Gemini através do objeto de chat
        with st.spinner("Lord Vader está consultando a Força..."):
            try:
                # O objeto `chat_session` já tem o histórico e as configurações do modelo.
                # `system_instruction` é aplicado pelo `GenerativeModel`.
                response = st.session_state.chat_session.send_message(user_query)
                vader_response_text = response.text

                # Adiciona a resposta de Vader ao histórico de exibição
                st.session_state.messages.append({"role": "assistant", "content": vader_response_text})
                
                # Limpa a caixa de texto da pergunta (opcional, mas bom para UX)
                # Isso requer um rerun, que faremos abaixo.
                # st.session_state.user_query_input = "" # Não funciona bem sem rerun para text_area
                st.rerun() # Re-executa o script para atualizar a interface com a nova mensagem

            
            except Exception as e:
                st.error(f"Um distúrbio na Força impediu a comunicação: {e}")
                # Adicionar a mensagem de erro ao chat pode ser útil para debug
                st.session_state.messages.append({"role": "assistant", "content": f"Erro da API: {e}"})
                st.rerun()
elif not api_ready and st.session_state.get("messages") and len(st.session_state.messages) > 0 :
    # Se a API não está pronta mas há mensagens (ex: chave removida após uso)
    pass # Apenas não mostra o botão de consulta ou o aviso de "insira a chave" se já há conversa.

# Se você quiser limpar o input de texto após enviar, `st.rerun()` geralmente faz isso
# ou você pode tentar redefinir o valor da chave do `st.text_area` antes do rerun,
# mas o `st.rerun()` é mais direto para atualizar todo o estado da UI.


