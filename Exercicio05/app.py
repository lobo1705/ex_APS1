import streamlit as st
from enum import Enum
from datetime import date

# ---------------- ENUMS ---------------- #

class CategoriaGasto(Enum):
    VESTUARIO = "ROUPAS"
    MEDICAMENTO = "REMEDIO"
    ALIMENTOS = "ALIMENTACAO"

class MetodoPagamento(Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    VALE_ALIMENTACAO = "TICKET_ALIMENTACAO"
    VALE_REFEICAO = "VALE_REFEICAO"

# ---------------- CLASSE ITEM ---------------- #

class RegistroGasto:
    def __init__(self, categoria, data_compra, valor_total, metodo_pagamento):
        self.categoria = categoria
        self.data_compra = data_compra
        self.valor_total = valor_total
        self.metodo_pagamento = metodo_pagamento

    def salvar(self):
        return "Registro adicionado com sucesso!"

    def mostrar(self):
        return f"{self.data_compra} | {self.categoria.value} | R$ {self.valor_total:.2f} | {self.metodo_pagamento.value}"

# ---------------- CLASSE CONTROLE ---------------- #

class GestorFinanceiro:
    def __init__(self):
        self.lista_registros = []

    def adicionar(self, registro):
        self.lista_registros.append(registro)

    def total_geral(self):
        return sum(r.valor_total for r in self.lista_registros)

    def total_por_categoria(self):
        resumo = {}
        for r in self.lista_registros:
            resumo[r.categoria] = resumo.get(r.categoria, 0) + r.valor_total
        return resumo

    def total_por_pagamento(self):
        resumo = {}
        for r in self.lista_registros:
            resumo[r.metodo_pagamento] = resumo.get(r.metodo_pagamento, 0) + r.valor_total
        return resumo


# ---------------- STREAMLIT ---------------- #

st.title("💰 Sistema de Controle Financeiro")

# Inicialização
if "gestor" not in st.session_state:
    st.session_state.gestor = GestorFinanceiro()

gestor = st.session_state.gestor

# ---------- FORMULÁRIO ---------- #
st.subheader("➕ Novo Registro")

categoria = st.selectbox("Categoria", list(CategoriaGasto))
data_registro = st.date_input("Data", value=date.today())
valor_gasto = st.number_input("Valor", min_value=0.0, format="%.2f")
pagamento = st.selectbox("Forma de Pagamento", list(MetodoPagamento))

if st.button("Salvar Gasto"):
    registro = RegistroGasto(categoria, data_registro, valor_gasto, pagamento)
    gestor.adicionar(registro)
    st.success(registro.salvar())

# ---------- LISTA ---------- #
st.subheader("📋 Registros")

if gestor.lista_registros:
    for r in gestor.lista_registros:
        st.write(r.mostrar())
else:
    st.info("Nenhum registro encontrado.")

# ---------- TOTAL GERAL ---------- #
st.subheader("💵 Total Geral")
st.write(f"Total: R$ {gestor.total_geral():.2f}")

# ---------- POR CATEGORIA ---------- #
st.subheader("📊 Total por Categoria")

resumo_cat = gestor.total_por_categoria()
for cat, valor in resumo_cat.items():
    st.write(f"{cat.value}: R$ {valor:.2f}")

# ---------- POR PAGAMENTO ---------- #
st.subheader("💳 Total por Pagamento")

resumo_pag = gestor.total_por_pagamento()
for pag, valor in resumo_pag.items():
    st.write(f"{pag.value}: R$ {valor:.2f}")