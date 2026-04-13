import streamlit as st
from enum import Enum

# Enum de direção
class DirecaoMovimento(Enum):
    SUBIR = "CIMA"
    DESCER = "BAIXO"
    IR_DIREITA = "DIREITA"
    IR_ESQUERDA = "ESQUERDA"

# Classe personagem
class Personagem:
    def __init__(self, apelido):
        self.apelido = apelido
        self.pos_x = 0
        self.pos_y = 0
        self.direcao_atual = DirecaoMovimento.SUBIR

    def mover_personagem(self, direcao_mov):
        self.direcao_atual = direcao_mov
        
        if direcao_mov == DirecaoMovimento.SUBIR:
            self.pos_y += 1
        elif direcao_mov == DirecaoMovimento.DESCER:
            self.pos_y -= 1
        elif direcao_mov == DirecaoMovimento.IR_DIREITA:
            self.pos_x += 1
        elif direcao_mov == DirecaoMovimento.IR_ESQUERDA:
            self.pos_x -= 1

    def subir(self):
        self.mover_personagem(DirecaoMovimento.SUBIR)

    def descer(self):
        self.mover_personagem(DirecaoMovimento.DESCER)

    def direita(self):
        self.mover_personagem(DirecaoMovimento.IR_DIREITA)

    def esquerda(self):
        self.mover_personagem(DirecaoMovimento.IR_ESQUERDA)

    def obter_posicao(self):
        return self.pos_x, self.pos_y

    def definir_direcao(self, direcao_mov):
        self.direcao_atual = direcao_mov


# ---------------- STREAMLIT ---------------- #

st.title("🎮 Controle do Personagem")

# Sessão do personagem
if "personagem" not in st.session_state:
    st.session_state.personagem = None

# Criar personagem
nome_personagem = st.text_input("Nome do Personagem:")

if st.button("Criar Personagem"):
    if nome_personagem:
        st.session_state.personagem = Personagem(nome_personagem)
        st.success("Personagem criado com sucesso!")
    else:
        st.warning("Informe um nome!")

# Controle do personagem
if st.session_state.personagem:
    personagem = st.session_state.personagem

    st.subheader(f"Personagem: {personagem.apelido}")

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        if st.button("⬆️ Subir"):
            personagem.subir()
        if st.button("⬇️ Descer"):
            personagem.descer()

    with coluna2:
        if st.button("➡️ Direita"):
            personagem.direita()
        if st.button("⬅️ Esquerda"):
            personagem.esquerda()

    pos_x, pos_y = personagem.obter_posicao()

    st.write(f"📍 Coordenada X: {pos_x}")
    st.write(f"📍 Coordenada Y: {pos_y}")