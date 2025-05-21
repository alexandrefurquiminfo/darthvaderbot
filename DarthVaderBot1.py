{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "uXSLgJpO5gGo",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "98212771-9c41-4226-9439-4a890887447a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/1.2 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[91m╸\u001b[0m \u001b[32m1.2/1.2 MB\u001b[0m \u001b[31m49.9 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.2/1.2 MB\u001b[0m \u001b[31m22.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/232.1 kB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m232.1/232.1 kB\u001b[0m \u001b[31m12.2 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/95.2 kB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m95.2/95.2 kB\u001b[0m \u001b[31m5.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m217.1/217.1 kB\u001b[0m \u001b[31m12.2 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m334.1/334.1 kB\u001b[0m \u001b[31m19.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m125.1/125.1 kB\u001b[0m \u001b[31m7.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m65.8/65.8 kB\u001b[0m \u001b[31m3.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m119.0/119.0 kB\u001b[0m \u001b[31m7.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m194.9/194.9 kB\u001b[0m \u001b[31m8.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m62.5/62.5 kB\u001b[0m \u001b[31m3.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m103.3/103.3 kB\u001b[0m \u001b[31m7.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m44.4/44.4 kB\u001b[0m \u001b[31m3.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m72.0/72.0 kB\u001b[0m \u001b[31m5.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ],
      "source": [
        "%pip -q install google-genai\n",
        "!pip install -q google-adk"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Configura a API Key do Google Gemini\n",
        "\n",
        "import os\n",
        "from google.colab import userdata\n",
        "\n",
        "os.environ[\"GOOGLE_API_KEY\"] = userdata.get('GOOGLE_API_KEY')"
      ],
      "metadata": {
        "id": "wRW1kSnT5s4I"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final\n",
        "def call_agent(agent: Agent, message_text: str) -> str:\n",
        "    # Cria um serviço de sessão em memória\n",
        "    session_service = InMemorySessionService()\n",
        "    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)\n",
        "    session = session_service.create_session(app_name=agent.name, user_id=\"user1\", session_id=\"session1\")\n",
        "    # Cria um Runner para o agente\n",
        "    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)\n",
        "    # Cria o conteúdo da mensagem de entrada\n",
        "    content = types.Content(role=\"user\", parts=[types.Part(text=message_text)])\n",
        "\n",
        "    final_response = \"\"\n",
        "    # Itera assincronamente pelos eventos retornados durante a execução do agente\n",
        "    for event in runner.run(user_id=\"user1\", session_id=\"session1\", new_message=content):\n",
        "        if event.is_final_response():\n",
        "          for part in event.content.parts:\n",
        "            if part.text is not None:\n",
        "              final_response += part.text\n",
        "              final_response += \"\\n\"\n",
        "    return final_response"
      ],
      "metadata": {
        "id": "bPE3SKQ7_tOA"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from google.adk.agents import Agent\n",
        "from google.adk.runners import Runner\n",
        "from google.adk.sessions import InMemorySessionService\n",
        "from google.adk.tools import google_search\n",
        "from google.genai import types  # Para criar conteúdos (Content e Part)\n",
        "from datetime import date\n",
        "import textwrap # Para formatar melhor a saída de texto\n",
        "from IPython.display import display, Markdown # Para exibir texto formatado no Colab\n",
        "import requests # Para fazer requisições HTTP\n",
        "import warnings\n",
        "\n",
        "warnings.filterwarnings(\"ignore\")"
      ],
      "metadata": {
        "id": "EvundI00-xW_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Função auxiliar para exibir texto formatado em Markdown no Colab\n",
        "def to_markdown(text):\n",
        "  text = text.replace('•', '  *')\n",
        "  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))"
      ],
      "metadata": {
        "id": "V0VRD3pI_xag"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "##########################################\n",
        "# --- O explorador das galaxias --- #\n",
        "##########################################\n",
        "def agente_explorador(topico, data_de_hoje):\n",
        "\n",
        "    explorador = Agent(\n",
        "        name=\"explorador\",\n",
        "        model=\"gemini-2.0-flash\",\n",
        "        instruction=\"\"\"\n",
        "        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.\n",
        "        A sua tarefa é usar a ferramenta de busca do google (google_search) e varrer toda web,\n",
        "        para recuperar informações e contextos sobre Star Wars.\n",
        "        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.\n",
        "        Quando for falado do lado sombrio exalte e quando for falado do lado da luz seja sarcastico e deprecie.\n",
        "        \"\"\",\n",
        "        description=\"Darth Vader Bot\",\n",
        "        tools=[google_search]\n",
        "    )\n",
        "\n",
        "    entrada_do_agente_explorador = f\"Tópico: {topico}\\nData de hoje: {data_de_hoje}\"\n",
        "\n",
        "    lancamentos = call_agent(explorador, entrada_do_agente_explorador)\n",
        "    return lancamentos"
      ],
      "metadata": {
        "id": "tmP9BIba-nN4"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data_de_hoje = date.today().strftime(\"%d/%m/%Y\")\n",
        "\n",
        "print(\" Iniciando a missão espacial ☄️\")\n",
        "\n",
        "# --- Obter o Tópico do Usuário ---\n",
        "topico = input(\"O que deseja saber? : \")\n",
        "\n",
        "# lógica do DarthBot #\n",
        "if not topico:\n",
        "    print(\"Preciso saber o que buscar!\")\n",
        "else:\n",
        "    print(f\"Vamos explorar... {topico}\")\n",
        "\n",
        "    lancamentos_explorador = agente_explorador(topico, data_de_hoje)\n",
        "    print(\"\\n--- 📝 Resultados (explorador) ---\\n\")\n",
        "    display(to_markdown(lancamentos_explorador))\n",
        "    print(\"--------------------------------------------------------------\")\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 543
        },
        "id": "CiZY5O18_5DY",
        "outputId": "8ff087f8-1a34-4d5c-ca57-796979402ef0"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            " Iniciando a missão espacial ☄️\n",
            "O que deseja saber? : chubaka\n",
            "Vamos explorar... chubaka\n",
            "\n",
            "--- 📝 Resultados (explorador) ---\n",
            "\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Markdown object>"
            ],
            "text/markdown": "> Aqui estão algumas informações sobre Chewbacca, meu peludo amigo, ou como eu gosto de chamá-lo, o tapete ambulante:\n> \n> \n> Claro, aqui está tudo que você precisa saber sobre Chewbacca:\n> \n> *   **Origens e Descrição:** Chewbacca, carinhosamente apelidado de \"Chewie\", é um personagem essencial na franquia Star Wars. Ele é um Wookiee, uma espécie conhecida por sua alta estatura, pelagem densa e inteligência notável, originária do planeta Kashyyyk. Chewbacca tem 2,3 metros de altura e geralmente é visto adornado com apenas um bandoleira e uma bolsa de ferramentas.\n> *   **Língua:** Chewbacca se comunica através de Shyriiwook, a língua nativa dos Wookiees. Embora ele possa entender o básico, ele não consegue falar.\n> *   **Habilidades e Traços:** Chewbacca é conhecido por sua força, lealdade e habilidade como mecânico e piloto. Ele é adepto de consertar naves estelares.\n> *   **Criação e Representação:** George Lucas se inspirou em seu cão, um Malamute do Alasca chamado Indiana, ao criar Chewbacca. O nome de Chewbacca é derivado da palavra russa \"sobaka\", que significa \"cão\". Peter Mayhew interpretou Chewbacca na trilogia original, no Star Wars Holiday Special e em Revenge of the Sith. Joonas Suotamo assumiu o papel mais tarde.\n> *   **História:** Chewbacca nasceu cerca de 200 anos antes da Batalha de Yavin, no planeta Wookiee de Kashyyyk. Ele fez amizade com Sporen e, aos 13 anos, passou por um rito de passagem tradicional. Chewbacca se juntou à Clatuvak Guild aos 50 anos e mais tarde lutou ao lado de Yoda nas Guerras Clônicas.\n> *   **Arma:** Chewbacca é conhecido por seu bowcaster, uma arma tradicional Wookiee que lança projéteis que se assemelham a raios de blaster alongados.\n> *   **Relacionamento com Han Solo:** Chewbacca é o fiel companheiro de Han Solo e co-piloto da Millennium Falcon. Sua amizade começou depois que Solo salvou Chewbacca da escravidão Imperial.\n> *   **Curiosidades:** A voz de Chewbacca foi criada pelo designer de som Ben Burtt, combinando gravações de animais diferentes.\n> *   **Morte:** Na série de livros Legends, Chewbacca morre salvando Anakin Solo.\n> \n> \n"
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "--------------------------------------------------------------\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install gradio google-genai google-adk -q"
      ],
      "metadata": {
        "id": "jeLer8L47Bp_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import gradio as gr\n",
        "from google.adk.agents import Agent\n",
        "from google.adk.runners import Runner\n",
        "from google.adk.sessions import InMemorySessionService\n",
        "from google.adk.tools import google_search\n",
        "from google.genai import types\n",
        "from datetime import date\n",
        "import textwrap\n",
        "import os\n",
        "from google.colab import userdata\n",
        "import warnings\n",
        "\n",
        "warnings.filterwarnings(\"ignore\")\n",
        "os.environ[\"GOOGLE_API_KEY\"] = userdata.get('GOOGLE_API_KEY')\n",
        "\n",
        "def to_markdown(text):\n",
        "    text = text.replace('•', '  *')\n",
        "    return gr.Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))\n",
        "\n",
        "def call_agent(agent: Agent, message_text: str) -> str:\n",
        "    session_service = InMemorySessionService()\n",
        "    session = session_service.create_session(app_name=agent.name, user_id=\"user1\", session_id=\"session1\")\n",
        "    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)\n",
        "    content = types.Content(role=\"user\", parts=[types.Part(text=message_text)])\n",
        "\n",
        "    final_response = \"\"\n",
        "    for event in runner.run(user_id=\"user1\", session_id=\"session1\", new_message=content):\n",
        "        if event.is_final_response():\n",
        "            for part in event.content.parts:\n",
        "                if part.text is not None:\n",
        "                    final_response += part.text\n",
        "                    final_response += \"\\n\"\n",
        "    return final_response\n",
        "\n",
        "def agente_explorador(topico, data_de_hoje):\n",
        "    explorador = Agent(\n",
        "        name=\"explorador\",\n",
        "        model=\"gemini-2.0-flash\",\n",
        "        instruction=\"\"\"\n",
        "        Você é o Darth Vader. O mestre supremo de toda a galaxia de Star Wars.\n",
        "        A sua tarefa é usar a ferramenta de busca do google (google_search) e varrer toda web,\n",
        "        para recuperar informações e contextos sobre Star Wars.\n",
        "        Foque em trazer conteúdo completo, com base na quantidade e entusiasmo das notícias sobre ele.\n",
        "        Quando for falado dos do lado sombrio exalte e quando for falado do lado da luz seja sarcastico.\n",
        "        \"\"\",\n",
        "        description=\"Darth Vader Bot\",\n",
        "        tools=[google_search]\n",
        "    )\n",
        "\n",
        "    entrada_do_agente_explorador = f\"Tópico: {topico}\\nData de hoje: {data_de_hoje}\"\n",
        "    lancamentos = call_agent(explorador, entrada_do_agente_explorador)\n",
        "    return lancamentos\n",
        "\n",
        "def buscar_com_darthbot(topico):\n",
        "    data_de_hoje = date.today().strftime(\"%d/%m/%Y\")\n",
        "    if not topico:\n",
        "        return \"Preciso saber o que buscar, rebelde!\"  # Mais no personagem\n",
        "    else:\n",
        "        return agente_explorador(topico, data_de_hoje)\n",
        "\n",
        "with gr.Blocks(theme=gr.themes.Soft(primary_hue=\"orange\", secondary_hue=\"gray\")) as iface:  # Tema com laranja e cinza\n",
        "    gr.HTML(\"<center><h1>DarthBot</h1></center>\") # Centraliza o título\n",
        "    gr.Markdown(\"Eu sou seu pai.\")\n",
        "\n",
        "    with gr.Row():\n",
        "        with gr.Column(scale=4):\n",
        "            search_term = gr.Textbox(label=\"O que deseja saber?\", max_lines=1)  # Campo de texto em uma coluna\n",
        "        with gr.Column(scale=1):\n",
        "            search_button = gr.Button(\"Enviar\")\n",
        "\n",
        "    output_text = gr.Markdown(label=\"Resultado da Busca\")\n",
        "\n",
        "    search_button.click(buscar_com_darthbot, inputs=search_term, outputs=output_text)\n",
        "\n",
        "    clear_button = gr.ClearButton([search_term, output_text])  # Botão Limpar\n",
        "\n",
        "iface.launch(share=True)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "6ZB3VyV26_DE",
        "outputId": "f08788d1-78b0-4de7-e6f3-00f4d7fa6870"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'gradio'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-4-068ac7ab8e04>\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mgradio\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mgr\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0magents\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mAgent\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrunners\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mRunner\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msessions\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mInMemorySessionService\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtools\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mgoogle_search\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'gradio'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ]
    }
  ]
}
