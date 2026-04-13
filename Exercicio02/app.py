import streamlit as st
from enum import Enum

# =========================
# ENUMERAÇÕES
# =========================

class CorFonte(Enum):
    PRETO = "black"
    BRANCO = "white"
    AZUL = "blue"
    AMARELO = "yellow"
    CINZA = "gray"

class TipoComponente(Enum):
    TEXTO_SIMPLES = "Label"
    TEXTO_EDITAVEL = "Edit"
    TEXTO_MULTILINHA = "Memo"

# =========================
# FUNÇÃO DE EXIBIÇÃO
# =========================

def exibir_texto_formatado(conteudo, tamanho_fonte, cor_texto, cor_fundo):
    estilo_html = f"""
        <div style="
            font-size: {tamanho_fonte}px;
            color: {cor_texto};
            background-color: {cor_fundo};
            padding: 10px;
            border-radius: 5px;
        ">
            {conteudo}
        </div>
    """
    st.markdown(estilo_html, unsafe_allow_html=True)

# =========================
# INTERFACE STREAMLIT
# =========================

st.title("Sistema de Estilização de Texto")

# Painel lateral
st.sidebar.header("Configurações do Texto")

tamanho_fonte = st.sidebar.number_input(
    "Tamanho da Fonte",
    min_value=8,
    max_value=72,
    value=16
)

cor_texto = st.sidebar.selectbox(
    "Cor do Texto",
    list(CorFonte)
)

cor_fundo = st.sidebar.selectbox(
    "Cor do Fundo",
    list(CorFonte)
)

tipo_campo = st.sidebar.selectbox(
    "Tipo de Campo",
    list(TipoComponente)
)

# Entrada de texto
st.header("Área de Entrada")

if tipo_campo == TipoComponente.TEXTO_SIMPLES:
    entrada_texto = st.text_input("Digite o texto (Simples)")

elif tipo_campo == TipoComponente.TEXTO_EDITAVEL:
    entrada_texto = st.text_input("Digite o texto (Editável)")

elif tipo_campo == TipoComponente.TEXTO_MULTILINHA:
    entrada_texto = st.text_area("Digite o texto (Multilinha)", height=150)

# =========================
# SAÍDA
# =========================

st.header("Resultado")

if entrada_texto:
    exibir_texto_formatado(
        entrada_texto,
        tamanho_fonte,
        cor_texto.value,
        cor_fundo.value
    )