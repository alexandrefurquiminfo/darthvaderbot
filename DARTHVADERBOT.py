import os
from google.colab import userdata
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
# from IPython.display import display, Markdown # Comment out Colab display
import requests # Para fazer requisições HTTP
import warnings
import gradio as gr
from google.genai import types
import textwrap

# %pip -q install google-genai  # Use pip directly in a .py file
# !pip install -q google-adk # Use pip directly in a .py file

# Configura a API Key do Google Gemini
# Use a simple print for interactive input in a .py file
# For running as a script, you might need to prompt the user or use environment variables
if 'GOOGLE_API_KEY' not in os.environ:
    try:
        os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')
    except Exception as e:
        print(f"Error getting GOOGLE_API_KEY from userdata: {e}")
        print("Please set the GOOGLE_API_KEY environment variable.")
        # You might want to exit or raise an error here if the key is essential


# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

warnings.filterwarnings("ignore")
# Função auxiliar para exibir texto formatado em Markdown no Colab
# def to_markdown(text): # Comment out Colab specific function
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
##########################################
# --- O explorador das galaxias --- #
##########################################
def agente_explorador(topico, data_de_hoje):

    explorador = Agent(
        name="explorador",
        model="gemini-2.0-flash",
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

# The following part is for the command line execution, remove if only using Gradio
# data_de_hoje = date.today().strftime("%d/%m/%Y")

# print(" Iniciando a missão espacial ☄️")

# --- Obter o Tópico do Usuário ---
# topico = input("O que deseja saber? : ")

# # lógica do DarthBot #
# if not topico:
#     print("Preciso saber o que buscar!")
# else:
#     print(f"Vamos explorar... {topico}")

#     lancamentos_explorador = agente_explorador(topico, data_de_hoje)
#     print("\n--- 📝 Resultados (explorador) ---\n")
#     # display(to_markdown(lancamentos_explorador)) # Comment out Colab display
#     print(lancamentos_explorador) # Use print for console output
#     print("--------------------------------------------------------------")

# !pip install gradio google-genai google-adk -q # Use pip directly in a .py file

warnings.filterwarnings("ignore")
# os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY') # Already done above

def to_markdown(text):
    text = text.replace('•', '  *')
    # Use gr.Markdown for Gradio interface
    return gr.Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

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
        A sua tarefa é usar a ferramenta de busca do google (google_search) e varrer toda web,
        para recuperar informações e contextos sobre Star Wars.
        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.
        Quando for falado dos do lado sombrio exalte e quando for falado do lado da luz seja sarcastico.
        """,
        description="Darth Vader Bot",
        tools=[google_search]
    )

    entrada_do_agente_explorador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    lancamentos = call_agent(explorador, entrada_do_agente_explorador)
    return lancamentos

def buscar_com_darthbot(topico):
    data_de_hoje = date.today().strftime("%d/%m/%Y")
    if not topico:
        return "Preciso saber o que buscar, rebelde!"  # Mais no personagem
    else:
        return agente_explorador(topico, data_de_hoje)

# This block creates the Gradio interface and is intended for interactive use,
# potentially with a server running this script.
if __name__ == "__main__":
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="gray")) as iface:  # Tema com laranja e cinza
        gr.HTML("<center><h1>DarthBot</h1></center>") # Centraliza o título
        gr.Markdown("Eu sou seu pai.")

        with gr.Row():
            with gr.Column(scale=4):
                search_term = gr.Textbox(label="O que deseja saber?", max_lines=1)  # Campo de texto em uma coluna
            with gr.Column(scale=1):
                search_button = gr.Button("Enviar")

        output_text = gr.Markdown(label="Resultado da Busca")

        search_button.click(buscar_com_darthbot, inputs=search_term, outputs=output_text)

        clear_button = gr.ClearButton([search_term, output_text])  # Botão Limpar

    # Use launch without share=True for local execution as a script
    # If running in a Colab-like environment where sharing is desired, you can add share=True
    iface.launch()
