import streamlit as st
from datetime import datetime
from ranking import RankingManager
from usuarios import UserManager

# Classe responsável por implementar a lógica do jogo da velha
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Inicializa o tabuleiro com 9 posições vazias
        self.current_player = "X"  # Define o jogador inicial como "X"
        self.players = {"X": None, "O": None}  # Armazena os jogadores atuais (X e O)
        self.last_move_time = datetime.now()  # Registra o momento da última jogada

    def reset_board(self):
        self.board = [' ' for _ in range(9)]  # Redefine o tabuleiro para posições vazias
        self.current_player = "X"  # Reseta o jogador atual para "X"
        self.last_move_time = datetime.now()  # Atualiza o horário da última jogada
        st.session_state["game_message"] = None  # Reseta a mensagem de status

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player  # Marca a posição com o símbolo do jogador atual
            self.last_move_time = datetime.now()  # Atualiza o horário da última jogada
            if self.check_winner():
                st.session_state["game_message"] = f"Vitória do(a) jogador(a) {self.players[self.current_player]}!"
                return True  # Indica que o jogo terminou
            elif self.check_draw():
                st.session_state["game_message"] = "Empate!"
                return True  # Indica que o jogo terminou
            self.current_player = "O" if self.current_player == "X" else "X"  # Alterna para o próximo jogador
            st.session_state["game_message"] = None  # Nenhuma mensagem para jogada válida
            return False
        else:
            st.session_state["game_message"] = "Movimento inválido! Escolha outra posição."
            return False

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
            [0, 4, 8], [2, 4, 6]             # Diagonais
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                return True
        return False

    def check_draw(self):
        return ' ' not in self.board  # Retorna True se não houver mais posições vazias no tabuleiro

# Função responsável por exibir a interface gráfica do jogo
def jogo_da_velha_view():
    st.title("Jogo da Velha")  # Título da página

    # Inicializar gerenciadores de ranking e usuários
    ranking_manager = RankingManager()
    user_manager = UserManager()
    users = list(user_manager.get_users().keys())

    # Sidebar para configuração dos jogadores
    st.sidebar.title("Configuração do Jogo")
    player_x = st.sidebar.selectbox("Jogador X:", ["Selecione um jogador"] + users)
    player_o = st.sidebar.selectbox("Jogador O:", ["Selecione um jogador"] + users)

    if player_x == player_o and player_x != "Selecione um jogador":
        st.sidebar.error("Os jogadores devem ser diferentes!")
    elif player_x != "Selecione um jogador" and player_o != "Selecione um jogador":
        if "game" not in st.session_state:
            st.session_state["game"] = TicTacToe()
        game = st.session_state["game"]
        game.players["X"] = player_x
        game.players["O"] = player_o
        st.sidebar.success(f"Jogadores: {player_x} (X) e {player_o} (O)")

        # Layout principal
        container = st.container()
        c1, c2, c3 = container.columns([1, 1, 2])

        # Exibição dos jogadores
        with c1:
            st.subheader("Jogadores")
            with st.container():
                active_style = (
                    "background-color: rgba(0, 255, 0, 0.5); padding: 10px; border-radius: 10px; text-align: center; "
                    "color: black; font-weight: bold; font-size: 18px;"
                )
                inactive_style = (
                    "background-color: rgba(200, 200, 200, 0.8); padding: 10px; border-radius: 10px; text-align: center; "
                    "color: rgba(109, 109, 109, 0.8); font-weight: bold; font-size: 18px;"
                )
                st.markdown(
                    f"""
                    <div style="{active_style if game.current_player == 'X' else inactive_style}">
                        {game.players["X"]} (❌)
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div style="{active_style if game.current_player == 'O' else inactive_style}">
                        {game.players["O"]} (⭕)
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Exibição do tabuleiro
        with c2:
            st.markdown("<h4 style='text-align: center;'>Tabuleiro</h4>", unsafe_allow_html=True)
            cols = st.columns(3)
            for row in range(3):
                for col in range(3):
                    idx = row * 3 + col
                    with cols[col]:
                        marker = game.board[idx]
                        button_label = "❌" if marker == "X" else "⭕" if marker == "O" else " "
                        if st.button(button_label, key=f"button_{idx}"):
                            if not game.make_move(idx):  # Processa a jogada
                                pass

        # Exibição da mensagem de status abaixo do tabuleiro
        if "game_message" in st.session_state and st.session_state["game_message"]:
            st.markdown(
                f"""
                <div style="
                    background-color: #f9f9f9; 
                    padding: 15px; 
                    margin-top: 20px; 
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    text-align: center;
                    font-size: 18px; 
                    color: #333;">
                    {st.session_state["game_message"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Botão para reiniciar o jogo
        if st.button("Reiniciar Jogo", key="restart_game"):
            game.reset_board()
            st.success("Jogo reiniciado!")
    else:
        st.warning("Selecione jogadores válidos para começar o jogo.")
