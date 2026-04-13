import streamlit as st

# ---------------- CLASSES ---------------- #

class ItemProduto:
    def __init__(self, nome_produto, preco_unitario):
        self.nome_produto = nome_produto
        self.preco_unitario = preco_unitario

    def mostrar(self):
        return f"{self.nome_produto} - R$ {self.preco_unitario:.2f}"


class ItemPedido:
    def __init__(self, qtd, produto_ref):
        self.qtd = qtd
        self.produto_ref = produto_ref
        self.valor_total_item = 0.0

    def calcular_total_item(self):
        self.valor_total_item = self.qtd * self.produto_ref.preco_unitario
        return self.valor_total_item


class Pedido:
    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        self.lista_itens = []
        self.valor_total_pedido = 0.0

    def adicionar_produto(self, produto, qtd):
        novo_item = ItemPedido(qtd, produto)
        novo_item.calcular_total_item()
        self.lista_itens.append(novo_item)

    def excluir_item(self, indice):
        if 0 <= indice < len(self.lista_itens):
            del self.lista_itens[indice]

    def calcular_total_pedido(self):
        self.valor_total_pedido = sum(item.calcular_total_item() for item in self.lista_itens)
        return self.valor_total_pedido

    def fechar_pedido(self):
        return f"Pedido {self.id_pedido} finalizado! Total: R$ {self.calcular_total_pedido():.2f}"


# ---------------- CARDÁPIO ---------------- #

lista_cardapio = [
    ItemProduto("Hamburguer", 15.0),
    ItemProduto("Pizza", 30.0),
    ItemProduto("Refrigerante", 6.0),
    ItemProduto("Suco", 8.0),
]

# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("🍽️ Sistema de Pedidos")

# Inicialização
if "pedidos" not in st.session_state:
    st.session_state.pedidos = {}

if "pedido_ativo" not in st.session_state:
    st.session_state.pedido_ativo = None


# -------- CRIAR PEDIDO -------- #
st.sidebar.header("📌 Pedidos")

novo_id = st.sidebar.number_input("Novo Pedido", min_value=1, step=1)

if st.sidebar.button("Criar"):
    if novo_id not in st.session_state.pedidos:
        st.session_state.pedidos[novo_id] = Pedido(novo_id)
        st.success(f"Pedido {novo_id} criado!")

# Selecionar pedido
if st.session_state.pedidos:
    pedido_selecionado = st.sidebar.selectbox(
        "Selecionar Pedido",
        list(st.session_state.pedidos.keys())
    )
    st.session_state.pedido_ativo = st.session_state.pedidos[pedido_selecionado]

# -------- ÁREA PRINCIPAL -------- #
if st.session_state.pedido_ativo:

    pedido = st.session_state.pedido_ativo
    st.subheader(f"🧾 Pedido #{pedido.id_pedido}")

    col1, col2 = st.columns(2)

    # -------- ADICIONAR ITEM -------- #
    with col1:
        st.subheader("➕ Adicionar Item")

        produto_escolhido = st.selectbox(
            "Produto",
            lista_cardapio,
            format_func=lambda p: p.mostrar()
        )

        quantidade_item = st.number_input("Quantidade", min_value=1, step=1)

        if st.button("Adicionar"):
            pedido.adicionar_produto(produto_escolhido, quantidade_item)
            st.success("Item adicionado!")

    # -------- LISTA DE ITENS -------- #
    with col2:
        st.subheader("📋 Itens do Pedido")

        if pedido.lista_itens:
            for i, item in enumerate(pedido.lista_itens):
                colA, colB, colC = st.columns([3,1,1])

                with colA:
                    st.write(f"{item.produto_ref.nome_produto} (R$ {item.produto_ref.preco_unitario:.2f})")

                with colB:
                    nova_qtd = st.number_input(
                        "Qtd",
                        min_value=1,
                        value=item.qtd,
                        key=f"qtd_{i}"
                    )
                    item.qtd = nova_qtd
                    item.calcular_total_item()

                with colC:
                    if st.button("❌", key=f"rem_{i}"):
                        pedido.excluir_item(i)
                        st.rerun()

                st.write(f"Subtotal: R$ {item.valor_total_item:.2f}")
                st.divider()
        else:
            st.info("Nenhum item no pedido.")

    # -------- TOTAL -------- #
    st.subheader("💰 Total do Pedido")
    total_pedido = pedido.calcular_total_pedido()
    st.write(f"### R$ {total_pedido:.2f}")

    # -------- FINALIZAR -------- #
    if st.button("✅ Finalizar Pedido"):
        st.success(pedido.fechar_pedido())

else:
    st.info("Crie ou selecione um pedido no menu lateral.")