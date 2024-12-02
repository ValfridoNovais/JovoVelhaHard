# Importações necessárias
import requests  # Para realizar requisições HTTP
import json  # Para manipulação de arquivos JSON
import streamlit as st  # Biblioteca para criação de interfaces web
from datetime import datetime  # Para manipulação de datas e horários


# Classe para gerenciar usuários
class UserManager:
    def __init__(self, file_path='pages/js/usuarios.json'):
        # Inicializa o gerenciador com o caminho do arquivo JSON de usuários
        self.file_path = file_path
        # Carrega os usuários existentes do arquivo
        self.users = self.load_users()

    # Método para carregar usuários a partir de um arquivo JSON
    def load_users(self):
        try:
            # Abre o arquivo JSON e carrega os dados
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Retorna um dicionário vazio se o arquivo não existir ou estiver corrompido
            return {}

    # Método para salvar usuários no arquivo JSON
    def save_users(self):
        with open(self.file_path, 'w') as file:
            # Salva os dados no arquivo com indentação de 4 espaços
            json.dump(self.users, file, indent=4)

    # Método para registrar um novo usuário
    def register_user(self, name, birth_date, city, state):
        # Verifica se o nome do usuário já está cadastrado
        if name in self.users:
            return "Usuário já cadastrado."
        # Converte a data de nascimento de string para um objeto datetime
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        # Calcula a idade do usuário com base na data atual
        age = datetime.now().year - birth_date_obj.year
        # Adiciona o usuário ao dicionário com suas informações
        self.users[name] = {"birth_date": birth_date, "age": age, "city": city, "state": state}
        # Salva os dados no arquivo JSON
        self.save_users()
        return "Usuário cadastrado com sucesso!"

    # Método para obter todos os usuários cadastrados
    def get_users(self):
        return self.users


# Função para exibir a interface de cadastro de usuários
def cadastro_view():
    st.title("Cadastro de Usuários")  # Título da página
    user_manager = UserManager()  # Instancia o gerenciador de usuários

    # Campo de texto para o nome do usuário
    name = st.text_input("Nome do Usuário:")

    # Campo de data para a data de nascimento
    current_year = datetime.now().year  # Ano atual
    birth_date = st.date_input(
        "Data de Nascimento:",  # Título do campo
        value=datetime(current_year - 18, 1, 1),  # Data padrão: 18 anos atrás
        min_value=datetime(current_year - 100, 1, 1),  # Data mínima: 100 anos atrás
        max_value=datetime.now()  # Data máxima: data atual
    ).strftime("%Y-%m-%d")  # Converte a data selecionada para o formato de string

    # Obter estados através da API do IBGE
    states = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados").json()
    # Cria um dicionário com o nome e o ID de cada estado
    state_options = {state["nome"]: state["id"] for state in states}
    # Campo de seleção para escolher o estado
    selected_state_name = st.selectbox("Estado:", list(state_options.keys()))
    # Obtém o ID do estado selecionado
    selected_state_id = state_options[selected_state_name]

    # Obter municípios do estado selecionado através da API do IBGE
    cities = requests.get(
        f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{selected_state_id}/municipios"
    ).json()
    # Cria uma lista com os nomes dos municípios
    city_names = [city["nome"] for city in cities]
    # Campo de seleção para escolher o município
    selected_city = st.selectbox("Município:", city_names)

    # Botão para cadastrar o usuário
    if st.button("Cadastrar"):
        # Chama o método de registro do usuário e exibe a mensagem de retorno
        message = user_manager.register_user(name, birth_date, selected_city, selected_state_name)
        st.success(message)  # Exibe a mensagem de sucesso

    # Exibir a lista de usuários cadastrados
    st.subheader("Usuários Cadastrados")  # Subtítulo da seção
    users = user_manager.get_users()  # Obtém os usuários cadastrados

    # Renderizar tabela com os dados dos usuários
    if users:  # Verifica se há usuários cadastrados
        st.table([  # Exibe os dados em formato de tabela
            {"Nome": user, "Idade": info["age"], "Cidade": info["city"], "Estado": info["state"]}
            for user, info in users.items()  # Itera sobre os usuários e suas informações
        ])
    else:
        # Exibe uma mensagem informativa caso não haja usuários cadastrados
        st.info("Nenhum usuário cadastrado ainda.")
