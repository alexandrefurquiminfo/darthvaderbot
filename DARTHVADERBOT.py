import streamlit as st
import os
from datetime import date
import textwrap
import warnings

# Google AI SDK imports
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types as genai_types # Aliasing to avoid potential name conflicts

# --- Configuration and Setup ---
warnings.filterwarnings("ignore")

# API Key Setup (using Streamlit secrets)
try:
    # Attempt to get the API key from Streamlit secrets
    # For local development, ensure you have .streamlit/secrets.toml
    # For deployment, configure secrets in Streamlit Community Cloud or your platform
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        # Fallback to environment variable if not in secrets (useful for some environments)
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        st.error("🚨 GOOGLE_API_KEY not found! Please add it to Streamlit secrets (secrets.toml) or as an environment variable.")
        st.stop()
    else:
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY # ADK might expect it as an env var

except Exception as e:
    st.error(f"An error occurred during API key setup: {e}")
    st.stop()


# --- Core Agent Logic (Adapted from your notebook) ---
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
        st.error(f"Error during agent execution: {e}")
        return f"An error occurred while communicating with the agent: {str(e)}"
    return final_response

def agente_explorador(topico: str, data_de_hoje: str) -> str:
    # IMPORTANT: Verify the model name. "gemini-2.0-flash" might be an internal or preview name.
    # Publicly available models include "gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro".
    # If "gemini-2.0-flash" works for you, keep it. Otherwise, try a public alternative.
    MODEL_NAME = "gemini-1.5-flash-latest" # Or "gemini-2.0-flash" if you have access

    explorador = Agent(
        name="explorador",
        model=MODEL_NAME,
        instruction="""
        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.
        A sua tarefa é usar a ferramenta de busca do google (google_search) e varrer toda web,
        para recuperar informações e contextos sobre Star Wars.
        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.
        Quando for falado do lado sombrio exalte e quando for falado do lado da luz seja sarcastico e deprecie.
        """,
        description="Darth Vader Bot",
        tools=[google_search]
    )
    entrada_do_agente_explorador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    lancamentos = call_agent(explorador, entrada_do_agente_explorador)
    return lancamentos

def format_darth_response(text: str) -> str:
    """Formats the text for Markdown display, similar to your to_markdown."""
    if not text:
        return ""
    text = text.replace('•', '  *') # Convert bullets to Markdown list items
    # Indent every line to make it a blockquote, as in your notebook output
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def buscar_com_darthbot(topico: str) -> str:
    data_de_hoje = date.today().strftime("%d/%m/%Y")
    if not topico:
        return "> Preciso saber o que buscar, rebelde!" # Formatted as blockquote
    else:
        raw_result = agente_explorador(topico, data_de_hoje)
        return format_darth_response(raw_result)


# --- Streamlit UI ---
st.set_page_config(page_title="DarthBot", layout="wide")

# Custom CSS for a more "Darth Vader" theme and centering
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

    .stApp {
        background-color: #111111; /* Dark background */
        color: #dddddd; /* Light grey text */
    }
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #FFD700; /* Gold-ish, like Vader's details or Sith holocrons */
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    .stMarkdown p, .stTextInput > div > div > input, .stButton > button {
        color: #cccccc;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        border: 1px solid #555555;
    }
    .stButton > button {
        background-color: #8B0000; /* Dark red */
        color: #FFFFFF;
        border: 1px solid #FF0000;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF0000; /* Brighter red on hover */
        color: #FFFFFF;
        border: 1px solid #FF4500;
    }
    .block-container { /* Center the main content block */
        max-width: 800px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Style for the output markdown blockquote */
    .stMarkdown blockquote {
        background-color: #222222;
        border-left: 5px solid #FFD700;
        padding: 10px 20px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    .stMarkdown blockquote p { /* Specificity for paragraphs inside blockquote */
        color: #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>DarthBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #aaaaaa;'>Eu sou seu pai.</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False # To control initial display of output area

# Input and Buttons
# Use columns for a more compact layout
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input(
        "O que deseja saber, verme insignificante?",
        value=st.session_state.search_term,
        key="darth_text_input", # Unique key for text input
        placeholder="Digite seu comando..."
    )

with col2:
    search_button = st.button("Consultar a Força", key="darth_search_button", use_container_width=True)

# Handle search action
if search_button:
    st.session_state.search_term = user_input # Update state with current input
    if st.session_state.search_term:
        with st.spinner("A Força está em ação... Consultando os arquivos imperiais..."):
            st.session_state.output_text = buscar_com_darthbot(st.session_state.search_term)
        st.session_state.search_triggered = True
    else:
        st.session_state.output_text = format_darth_response("Preciso saber o que buscar, rebelde!")
        st.session_state.search_triggered = True

# Display output only if a search was triggered
if st.session_state.search_triggered and st.session_state.output_text:
    st.markdown("---")
    st.markdown("### Resposta do Lorde Vader:", help="A sabedoria (ou sarcasmo) do Lado Sombrio.")
    # The output_text is already formatted with ">" by buscar_com_darthbot
    st.markdown(st.session_state.output_text, unsafe_allow_html=True) # unsafe_allow_html for custom styling if any

# Clear button functionality
if st.button("Limpar Memória (como se fosse apagar a República)", key="darth_clear_button", use_container_width=True):
    st.session_state.search_term = ""
    st.session_state.output_text = ""
    st.session_state.search_triggered = False
    # Use st.experimental_rerun() or st.rerun() for newer Streamlit versions to clear input field
    st.rerun()


st.markdown("---")
st.caption("Um aplicativo construído com o poder do Lado Sombrio e Streamlit. Que a Força (Sombria) esteja com você.")
