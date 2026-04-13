import streamlit as st

# ---------------- CLASSE ITEM ---------------- #

class ItemLista:
    def __init__(self, nome_produto, unidade_medida, consumo_mensal, quantidade_compra, preco_unitario):
        self.nome_produto = nome_produto
        self.unidade_medida = unidade_medida
        self.consumo_mensal = consumo_mensal
        self.quantidade_compra = quantidade_compra
        self.preco_unitario = preco_unitario
        self.valor_parcial = 0.0

    def calcular_valor(self):
        self.valor_parcial = self.quantidade_compra * self.preco_unitario
        return self.valor_parcial

    def alterar_preco(self, novo_preco):
        self.preco_unitario = novo_preco
        self.calcular_valor()

    def mostrar_item(self):
        return f"{self.nome_produto} | {self.quantidade_compra} {self.unidade_medida} | R$ {self.preco_unitario:.2f} | Subtotal: R$ {self.valor_parcial:.2f}"


# ---------------- CLASSE LISTA ---------------- #

class CarrinhoCompra:
    def __init__(self):
        self.lista_produtos = []
        self.valor_total = 0.0

    def adicionar_item(self, item):
        item.calcular_valor()
        self.lista_produtos.append(item)

    def calcular_total(self):
        self.valor_total = sum(p.calcular_valor() for p in self.lista_produtos)
        return self.valor_total

    def listar_itens(self):
        return [p.mostrar_item() for p in self.lista_produtos]

    def atualizar_preco(self, item, novo_preco):
        item.alterar_preco(novo_preco)


# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("🛒 Sistema Inteligente de Compras")

# Estado
if "carrinho" not in st.session_state:
    st.session_state.carrinho = CarrinhoCompra()

carrinho = st.session_state.carrinho

# -------- ADICIONAR ITEM -------- #
st.subheader("➕ Adicionar Item")

col1, col2 = st.columns(2)

with col1:
    nome_item = st.text_input("Nome do Produto")
    unidade_item = st.selectbox("Unidade", ["kg", "litro", "unidade"])
    consumo_item = st.number_input("Consumo mensal", min_value=0.0)

with col2:
    quantidade_item = st.number_input("Quantidade de compra", min_value=0.0)
    preco_item = st.number_input("Preço unitário", min_value=0.0)

if st.button("Adicionar Item"):
    if nome_item:
        item = ItemLista(nome_item, unidade_item, consumo_item, quantidade_item, preco_item)
        carrinho.adicionar_item(item)
        st.success("Item adicionado com sucesso!")
    else:
        st.warning("Informe o nome do produto!")

# -------- LISTAGEM -------- #
st.subheader("📋 Lista de Produtos")

if carrinho.lista_produtos:
    for i, item in enumerate(carrinho.lista_produtos):
        colA, colB, colC = st.columns([3,1,1])

        with colA:
            st.write(item.nome_produto)

        with colB:
            preco_editado = st.number_input(
                "Preço",
                value=item.preco_unitario,
                key=f"preco_{i}"
            )
            if preco_editado != item.preco_unitario:
                carrinho.atualizar_preco(item, preco_editado)

        with colC:
            if st.button("❌", key=f"del_{i}"):
                carrinho.lista_produtos.pop(i)
                st.rerun()

        item.calcular_valor()
        st.write(item.mostrar_item())
        st.divider()
else:
    st.info("Nenhum item cadastrado.")

# -------- TOTAL -------- #
st.subheader("💰 Total Geral")

total_geral = carrinho.calcular_total()
st.write(f"### R$ {total_geral:.2f}")