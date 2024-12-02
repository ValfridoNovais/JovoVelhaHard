import streamlit as st  # Para interface gráfica
import json  # Para manipular arquivos JSON
from github import Github  # Biblioteca para interagir com o GitHub

# Classe para gerenciar o ranking dos jogadores
class RankingManager:
    def __init__(self, file_path='pages/js/ranking.json', repo_name='', branch='main', token=''):
        self.file_path = file_path  # Caminho do arquivo local
        self.repo_name = repo_name  # Nome do repositório GitHub
        self.branch = branch  # Nome da branch GitHub
        self.token = token  # Token de acesso pessoal ao GitHub
        self.ranking = self.load_ranking()  # Carrega os dados ao inicializar

    def load_ranking(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_ranking(self):
        # Atualiza o arquivo local
        with open(self.file_path, 'w') as file:
            json.dump(self.ranking, file, indent=4)

        # Atualiza o arquivo no GitHub
        if self.repo_name and self.token:
            try:
                g = Github(self.token)
                repo = g.get_repo(self.repo_name)
                contents = repo.get_contents(self.file_path, ref=self.branch)
                with open(self.file_path, 'r') as file:
                    content = file.read()
                repo.update_file(
                    path=contents.path,
                    message="Atualizando ranking.json via Streamlit",
                    content=content,
                    sha=contents.sha,
                    branch=self.branch,
                )
                print("Ranking atualizado no GitHub!")
            except Exception as e:
                print(f"Erro ao atualizar o ranking no GitHub: {e}")

    def update_ranking(self, player_name, result):
        if player_name not in self.ranking:
            self.ranking[player_name] = {"points": 0, "wins": 0, "draws": 0, "losses": 0}

        if result == "win":
            self.ranking[player_name]["points"] += 3
            self.ranking[player_name]["wins"] += 1
        elif result == "draw":
            self.ranking[player_name]["points"] += 1
            self.ranking[player_name]["draws"] += 1
        elif result == "loss":
            self.ranking[player_name]["losses"] += 1

        self.save_ranking()

    def get_ranking(self):
        return sorted(
            self.ranking.items(),
            key=lambda x: x[1]["points"],
            reverse=True,
        )


def ranking_view():
    st.title("Ranking")
    repo_name = st.secrets["REPO_NAME"]
    branch = st.secrets["BRANCH"]
    token = st.secrets["GITHUB_TOKEN"]

    ranking_manager = RankingManager(repo_name=repo_name, branch=branch, token=token)
    ranking = ranking_manager.get_ranking()

    if ranking:
        st.table([
            {
                "Posição": idx + 1,
                "Jogador": player_name,
                "Pontos": stats["points"],
                "Vitórias": stats["wins"],
                "Empates": stats["draws"],
                "Derrotas": stats["losses"],
            }
            for idx, (player_name, stats) in enumerate(ranking)
        ])
    else:
        st.info("Nenhum jogador registrado no ranking ainda.")
