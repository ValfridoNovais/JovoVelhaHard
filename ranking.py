import streamlit as st  # Importa a biblioteca Streamlit para criar interfaces gráficas na web
import json  # Importa a biblioteca JSON para manipulação de arquivos JSON


# Classe para gerenciar o ranking dos jogadores
class RankingManager:
    def __init__(self, file_path='pages/js/ranking.json'):
        # Inicializa o gerenciador com o caminho do arquivo JSON onde o ranking será armazenado
        self.file_path = file_path
        # Carrega os dados do ranking ao inicializar a classe
        self.ranking = self.load_ranking()

    # Método para carregar os dados do ranking a partir de um arquivo JSON
    def load_ranking(self):
        try:
            # Abre o arquivo JSON e carrega o conteúdo em formato de dicionário
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Retorna um dicionário vazio se o arquivo não for encontrado ou estiver corrompido
            return {}

    # Método para salvar os dados do ranking no arquivo JSON
    def save_ranking(self):
        with open(self.file_path, 'w') as file:
            # Salva o dicionário do ranking no arquivo com indentação de 4 espaços
            json.dump(self.ranking, file, indent=4)

    # Método para atualizar o ranking de um jogador específico com base no resultado do jogo
    def update_ranking(self, player_name, result):
        # Se o jogador não estiver no ranking, inicializa seus dados
        if player_name not in self.ranking:
            self.ranking[player_name] = {"points": 0, "wins": 0, "draws": 0, "losses": 0}

        # Atualiza os dados do jogador com base no resultado
        if result == "win":  # Vitória
            self.ranking[player_name]["points"] += 3  # Adiciona 3 pontos
            self.ranking[player_name]["wins"] += 1  # Incrementa o número de vitórias
        elif result == "draw":  # Empate
            self.ranking[player_name]["points"] += 1  # Adiciona 1 ponto
            self.ranking[player_name]["draws"] += 1  # Incrementa o número de empates
        elif result == "loss":  # Derrota
            self.ranking[player_name]["losses"] += 1  # Incrementa o número de derrotas

        # Salva o ranking atualizado no arquivo
        self.save_ranking()

    # Método para obter o ranking ordenado por pontos
    def get_ranking(self):
        return sorted(
            self.ranking.items(),  # Converte o dicionário do ranking em uma lista de pares (nome, dados)
            key=lambda x: x[1]["points"],  # Ordena pela quantidade de pontos
            reverse=True,  # Ordem decrescente (maior pontuação primeiro)
        )


# Função para renderizar a interface gráfica do ranking no Streamlit
def ranking_view():
    st.title("Ranking")  # Define o título da página
    ranking_manager = RankingManager()  # Instancia o gerenciador de ranking
    ranking = ranking_manager.get_ranking()  # Obtém o ranking ordenado

    # Renderiza a tabela de ranking no Streamlit
    if ranking:  # Verifica se o ranking não está vazio
        st.table([  # Exibe uma tabela com os dados do ranking
            {
                "Posição": idx + 1,  # Posição do jogador no ranking
                "Jogador": player_name,  # Nome do jogador
                "Pontos": stats["points"],  # Total de pontos do jogador
                "Vitórias": stats["wins"],  # Número de vitórias
                "Empates": stats["draws"],  # Número de empates
                "Derrotas": stats["losses"],  # Número de derrotas
            }
            for idx, (player_name, stats) in enumerate(ranking)  # Itera sobre o ranking com índice
        ])
    else:
        # Exibe uma mensagem informativa se não houver jogadores no ranking
        st.info("Nenhum jogador registrado no ranking ainda.")
