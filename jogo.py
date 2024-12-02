import streamlit as st  # Biblioteca para criar a interface gráfica
from datetime import datetime  # Para trabalhar com datas e horários
from ranking import RankingManager  # Classe para gerenciar o ranking dos jogadores
from usuarios import UserManager  # Classe para gerenciar os usuários cadastrados


# Classe responsável por implementar a lógica do jogo da velha
class TicTacToe:
    def __init__(self):
        # Inicializa o tabuleiro com 9 posições vazias
        self.board = [' ' for _ in range(9)]
        # Define o jogador inicial como "X"
        self.current_player = "X"
        # Armazena os jogadores atuais (X e O)
        self.players = {"X": None, "O": None}
        # Registra o momento da última jogada
        self.last_move_time = datetime.now()

    # Método para reiniciar o tabuleiro
    def reset_board(self):
        # Redefine o tabuleiro para posições vazias
        self.board = [' ' for _ in range(9)]
        # Reseta o jogador atual para "X"
        self.current_player = "X"
        # Atualiza o horário da última jogada
        self.last_move_time = datetime.now()

    # Método para realizar uma jogada em uma posição específica
    def make_move(self, position):
        # Verifica se a posição está vazia
        if self.board[position] == ' ':
            # Marca a posição com o símbolo do jogador atual
            self.board[position] = self.current_player
            # Atualiza o horário da última jogada
            self.last_move_time = datetime.now()
            # Verifica se há um vencedor
            if self.check_winner():
                return f"Vitória do jogador {self.players[self.current_player]}!"
            # Verifica se o jogo terminou em empate
            elif self.check_draw():
                return "Empate!"
            # Alterna para o próximo jogador
            self.current_player = "O" if self.current_player == "X" else "X"
            return None
        else:
            # Retorna mensagem de erro se a posição já estiver ocupada
            return "Movimento inválido! Escolha outra posição."

    # Método para verificar se há um vencedor
    def check_winner(self):
        # Condições de vitória (linhas, colunas e diagonais)
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
            [0, 4, 8], [2, 4, 6]             # Diagonais
        ]
        # Verifica se alguma condição de vitória foi atingida
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                return True
        return False

    # Método para verificar se o jogo terminou em empate
    def check_draw(self):
        # Retorna True se não houver mais posições vazias no tabuleiro
        return ' ' not in self.board


# Função responsável por exibir a interface gráfica do jogo
def jogo_da_velha_view():
    st.title("Jogo da Velha")  # Título da página

    # Inicializar gerenciadores de ranking e usuários
    ranking_manager = RankingManager()  # Gerenciador de ranking
    user_manager = UserManager()  # Gerenciador de usuários
    users = list(user_manager.get_users().keys())  # Lista de usuários cadastrados

    # Sidebar para configuração dos jogadores
    st.sidebar.title("Configuração do Jogo")  # Título da sidebar

    # Seleção do jogador X
    player_x = st.sidebar.selectbox("Jogador X:", ["Selecione um jogador"] + users)
    # Seleção do jogador O
    player_o = st.sidebar.selectbox("Jogador O:", ["Selecione um jogador"] + users)

    # Verificação se os jogadores são diferentes
    if player_x == player_o and player_x != "Selecione um jogador":
        st.sidebar.error("Os jogadores devem ser diferentes!")  # Exibe erro se forem iguais
    elif player_x != "Selecione um jogador" and player_o != "Selecione um jogador":
        # Inicializa o jogo se ainda não estiver na sessão
        if "game" not in st.session_state:
            st.session_state["game"] = TicTacToe()
        game = st.session_state["game"]  # Recupera o jogo da sessão
        game.players["X"] = player_x  # Define o jogador X
        game.players["O"] = player_o  # Define o jogador O
        st.sidebar.success(f"Jogadores: {player_x} (X) e {player_o} (O)")  # Mensagem de sucesso

        # Adicionar estilos CSS para botões
        st.markdown(
            """
            <style>
            .tic-tac-toe-button {
                height: 80px;
                width: 80px;
                margin: 5px;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                background-color: #f8f9fa;
                border: 2px solid #ced4da;
                border-radius: 5px;
                cursor: pointer;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Exibir o tabuleiro
        st.subheader(f"Jogador Atual: {game.players[game.current_player]}")  # Mostra o jogador atual
        cols = st.columns(3)  # Cria 3 colunas para o tabuleiro
        for row in range(3):  # Itera sobre as linhas
            for col in range(3):  # Itera sobre as colunas
                idx = row * 3 + col  # Calcula o índice da posição no tabuleiro
                with cols[col]:  # Adiciona o botão na coluna correspondente
                    marker = game.board[idx]  # Obtém o marcador atual da posição
                    button_label = "❌" if marker == "X" else "⭕" if marker == "O" else " "  # Define o texto do botão
                    if st.button(button_label, key=f"button_{idx}", help="Clique para jogar"):  # Botão para jogar
                        if game.board[idx] == " ":
                            message = game.make_move(idx)  # Realiza a jogada
                            if message:
                                st.success(message)  # Exibe mensagem de vitória ou empate
                                if "Vitória" in message:
                                    winner = game.players[game.current_player]  # Jogador vencedor
                                    loser = game.players["O" if game.current_player == "X" else "X"]  # Jogador perdedor
                                    ranking_manager.update_ranking(winner, "win")  # Atualiza o ranking do vencedor
                                    ranking_manager.update_ranking(loser, "loss")  # Atualiza o ranking do perdedor
                                elif "Empate" in message:
                                    ranking_manager.update_ranking(game.players["X"], "draw")  # Atualiza empate para X
                                    ranking_manager.update_ranking(game.players["O"], "draw")  # Atualiza empate para O
                                game.reset_board()  # Reseta o tabuleiro

        # Botão para reiniciar o jogo
        if st.button("Reiniciar Jogo"):
            game.reset_board()  # Reseta o tabuleiro
            st.success("Jogo reiniciado!")  # Exibe mensagem de sucesso
    else:
        # Mensagem de aviso se os jogadores não forem válidos
        st.warning("Selecione jogadores válidos para começar o jogo.")
