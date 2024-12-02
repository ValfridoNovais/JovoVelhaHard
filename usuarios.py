import json  # Para manipulação de arquivos JSON
import requests  # Para requisições HTTP
from datetime import datetime  # Para trabalhar com datas e horários
from github import Github  # Biblioteca para manipulação da API do GitHub


# Função para atualizar o arquivo no GitHub
def update_github_file(file_path, repo_name, branch, token):
    """
    Atualiza o arquivo JSON no repositório GitHub.
    """
    try:
        # Ler o conteúdo do arquivo local
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Conectar ao GitHub
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        # Obter o conteúdo do arquivo do repositório
        contents = repo.get_contents(file_path, ref=branch)
        
        # Atualizar o arquivo existente
        repo.update_file(
            path=contents.path,
            message="Atualizando usuarios.json via Streamlit",
            content=content,
            sha=contents.sha,
            branch=branch,
        )
        print("Arquivo atualizado no GitHub!")
    except Exception as e:
        print(f"Erro ao atualizar o arquivo no GitHub: {e}")


# Classe para gerenciar usuários
class UserManager:
    def __init__(self, file_path='usuarios.json'):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("users", {})  # Retorna os usuários ou um dicionário vazio
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Retorna um dicionário vazio se o arquivo não existir ou estiver corrompido


    def save_users(self):
        data = {"users": self.users}  # Encapsula os usuários na chave 'users'
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  # Salva com indentação e sem escape Unicode


    def register_user(self, name, birth_date, city, state, password):
        if name in self.users:
            return "Usuário já cadastrado."  # Verifica se o usuário já está cadastrado
        
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")  # Converte data de nascimento
        age = datetime.now().year - birth_date_obj.year  # Calcula a idade
        
        # Adiciona o usuário com suas informações
        self.users[name] = {
            "birth_date": birth_date,
            "age": age,
            "city": city,
            "state": state,
            "password": password,  # Armazena a senha (idealmente como hash)
            "ranking": {
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "forfeits": 0,
                "points": 0
            }
        }
        self.save_users()  # Salva os dados atualizados no arquivo JSON
        return "Usuário cadastrado com sucesso!"


    def authenticate_user(self, name, password):
        user = self.users.get(name)  # Obtém o usuário pelo nome
        if user and user["password"] == password:  # Verifica a senha
            return True
        return False


    def get_users(self):
        return self.users


# Função para exibir a interface de cadastro de usuários
def cadastro_view():
    import streamlit as st  # Importa Streamlit apenas na função para evitar problemas ao usar a API

    st.title("Cadastro de Usuários")
    user_manager = UserManager()

    # Formulário de Cadastro
    st.subheader("Novo Cadastro")
    name = st.text_input("Nome do Usuário:")
    password = st.text_input("Senha:", type="password")
    current_year = datetime.now().year

    birth_date = st.date_input(
        "Data de Nascimento:",
        value=datetime(current_year - 18, 1, 1),
        min_value=datetime(current_year - 100, 1, 1),
        max_value=datetime.now()
    ).strftime("%Y-%m-%d")

    states = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados").json()
    state_options = {state["nome"]: state["id"] for state in states}
    selected_state_name = st.selectbox("Estado:", list(state_options.keys()))
    selected_state_id = state_options[selected_state_name]

    cities = requests.get(
        f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{selected_state_id}/municipios"
    ).json()
    city_names = [city["nome"] for city in cities]
    selected_city = st.selectbox("Município:", city_names)

    if st.button("Cadastrar"):
        if not name or not password:
            st.error("Por favor, preencha todos os campos!")
        else:
            message = user_manager.register_user(name, birth_date, selected_city, selected_state_name, password)
            st.success(message)

    # Exibição de Usuários
    st.subheader("Usuários Cadastrados")
    users = user_manager.get_users()
    if users:
        st.table([
            {"Nome": user, "Idade": info["age"], "Cidade": info["city"], "Estado": info["state"]}
            for user, info in users.items()
        ])
    else:
        st.info("Nenhum usuário cadastrado ainda.")
