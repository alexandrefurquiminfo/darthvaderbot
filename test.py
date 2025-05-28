import streamlit as st
import requests

# --- Configurações da SWAPI.info ---
SWAPI_BASE_URL = "https://swapi.info/api/"

# --- Funções para interagir com a SWAPI.info ---
def get_swapi_data(category, query=""):
    """
    Faz uma requisição para a SWAPI.info para buscar dados.
    category: 'people', 'planets', 'films', etc.
    query: Termo de busca (opcional, para pesquisa).
    """
    url = f"{SWAPI_BASE_URL}{category}/"
    params = {}
    if query:
        params["search"] = query

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta um erro para respostas de status ruins
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar à SWAPI: {e}")
        return None

# --- Início do Layout do Bot ---
st.title("Darth Vader Bot: O Poder da Força (e da SWAPI!)")
st.markdown("""
Olá, eu sou o Darth Vader Bot! Eu posso te ajudar a explorar o vasto universo de Star Wars.
""")

# --- Suas funcionalidades ATUAIS VÃO AQUI ---
# Por exemplo, se você tem um sistema de perguntas e respostas ou
# alguma funcionalidade baseada em dados locais, elas podem ser colocadas aqui.
# Exemplo (apenas para ilustração, substitua pelo seu código real):
st.header("Seções Atuais do Bot")
st.write("Aqui é onde suas funcionalidades originais do bot seriam exibidas.")
if st.checkbox("Mostrar mensagem secreta do Lado Sombrio"):
    st.info("A Força é forte em você... mas não é páreo para o Lado Sombrio!")

st.markdown("---") # Separador para organizar o layout

# --- NOVAS Funcionalidades da SWAPI.info ---

st.header("Explore o Universo Star Wars com a SWAPI!")

# 1. Encontrar Personagens
st.subheader("Encontre um Personagem")
character_name = st.text_input("Digite o nome de um personagem (ex: Leia Organa, Chewbacca):", key="char_input")

if st.button("Buscar Personagem", key="char_button"):
    if character_name:
        with st.spinner("Buscando na galáxia..."):
            data = get_swapi_data("people", character_name)
            if data and data["results"]:
                for person in data["results"]:
                    st.write(f"**Nome:** {person['name']}")
                    st.write(f"Altura: {person['height']} cm, Peso: {person['mass']} kg")
                    st.write(f"Cor do Cabelo: {person['hair_color']}, Cor dos Olhos: {person['eye_color']}")
                    st.write(f"Ano de Nascimento: {person['birth_year']}, Gênero: {person['gender']}")
                    # Você pode adicionar mais detalhes aqui, como o planeta natal (homeworld)
                    # Exemplo: buscar o planeta natal
                    # if 'homeworld' in person:
                    #     homeworld_url = person['homeworld']
                    #     # Fazer outra requisição para obter o nome do planeta
                    #     try:
                    #         homeworld_response = requests.get(homeworld_url)
                    #         homeworld_response.raise_for_status()
                    #         homeworld_data = homeworld_response.json()
                    #         st.write(f"Planeta Natal: {homeworld_data['name']}")
                    #     except requests.exceptions.RequestException:
                    #         st.write("Planeta Natal: Não disponível")
                    st.markdown("---")
            else:
                st.warning(f"Personagem '{character_name}' não encontrado.")
    else:
        st.info("Por favor, digite o nome de um personagem para buscar.")

st.markdown("---")

# 2. Listar Filmes
st.subheader("Informações sobre Filmes")
if st.button("Ver Todos os Filmes", key="films_button"):
    with st.spinner("Carregando filmes..."):
        data = get_swapi_data("films")
        if data and data["results"]:
            # Ordena os filmes pelo ID do episódio
            for film in sorted(data["results"], key=lambda x: x["episode_id"]):
                st.write(f"**Episódio {film['episode_id']}: {film['title']}**")
                st.write(f"Diretor: {film['director']}")
                st.write(f"Produtor: {film['producer']}")
                st.write(f"Data de Lançamento: {film['release_date']}")
                st.markdown(f"***Crawl de Abertura:***\n{film['opening_crawl']}")
                st.markdown("---")
        else:
            st.error("Não foi possível carregar os filmes.")

st.markdown("---")

# 3. Explorar Planetas (Exemplo de funcionalidade adicional)
st.subheader("Explore os Planetas")
planet_name = st.text_input("Digite o nome de um planeta (ex: Tatooine, Hoth):", key="planet_input")

if st.button("Buscar Planeta", key="planet_button"):
    if planet_name:
        with st.spinner("Buscando informações do planeta..."):
            data = get_swapi_data("planets", planet_name)
            if data and data["results"]:
                for planet in data["results"]:
                    st.write(f"**Nome:** {planet['name']}")
                    st.write(f"Período de Rotação: {planet['rotation_period']} horas")
                    st.write(f"Período Orbital: {planet['orbital_period']} dias")
                    st.write(f"Diâmetro: {planet['diameter']} km")
                    st.write(f"Clima: {planet['climate']}")
                    st.write(f"Gravidade: {planet['gravity']}")
                    st.write(f"Terreno: {planet['terrain']}")
                    st.write(f"População: {planet['population']}")
                    st.markdown("---")
            else:
                st.warning(f"Planeta '{planet_name}' não encontrado.")
    else:
        st.info("Por favor, digite o nome de um planeta para buscar.")

st.markdown("---")
st.markdown("Que a Força esteja com você!")
