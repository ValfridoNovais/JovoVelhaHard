import streamlit as st  # Importa a biblioteca Streamlit para criar interfaces web
from streamlit_option_menu import option_menu  # Importa o componente de menu com ícones do Streamlit
from jogo import jogo_da_velha_view  # Importa a função que renderiza a página do jogo da velha
from usuarios import cadastro_view  # Importa a função que renderiza a página de cadastro de usuários
from ranking import ranking_view  # Importa a função que renderiza a página de ranking

# Configuração inicial do Streamlit (deve ser a primeira linha que usa Streamlit)
st.set_page_config(page_title="Jogo da Velha HARD", layout="wide")
# Configura o título da página exibido no navegador e define o layout como "wide" (amplo)

# Adiciona estilos do Bootstrap 5 para customizar a interface
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <style>
    /* Ajustes personalizados para a largura da interface */
    .container {
        max-width: 900px;  /* Define a largura máxima da área central da interface */
    }
    </style>
    """,
    unsafe_allow_html=True,  # Permite a execução de código HTML na interface do Streamlit
)

# Função principal para gerenciar a navegação entre as páginas
def main():
    # Cria um menu de navegação dentro da sidebar (barra lateral)
    with st.sidebar:
        menu = option_menu(
            "Menu de Navegação",  # Título do menu exibido no topo
            ["Jogo da Velha", "Cadastro de Usuários", "Ranking"],  # Lista de opções disponíveis no menu
            icons=["grid", "person-add", "trophy"],  # Ícones para cada opção do menu
            menu_icon="menu",  # Ícone para o menu em si (localizado no topo)
            default_index=0,  # Define a opção padrão como "Jogo da Velha" (primeira opção)
        )

    # Verifica a opção selecionada no menu e exibe a página correspondente
    if menu == "Jogo da Velha":
        jogo_da_velha_view()  # Chama a função para exibir a página do jogo da velha
    elif menu == "Cadastro de Usuários":
        cadastro_view()  # Chama a função para exibir a página de cadastro de usuários
    elif menu == "Ranking":
        ranking_view()  # Chama a função para exibir a página do ranking

# Ponto de entrada do programa
if __name__ == "__main__":
    main()  # Chama a função principal
