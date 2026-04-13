import streamlit as st

# ---------------- CLASSE DISCO ---------------- #

class DiscoMusical:
    def __init__(self, artista, nome_album, ano_lancamento):
        self.artista = artista
        self.nome_album = nome_album
        self.ano_lancamento = ano_lancamento

    def salvar(self):
        return "Disco cadastrado com sucesso!"

    def mostrar(self):
        return f"{self.nome_album} - {self.artista} ({self.ano_lancamento})"


# ---------------- CLASSE ACERVO ---------------- #

class AcervoCD:
    def __init__(self):
        self.lista_discos = []

    def adicionar_disco(self, disco):
        self.lista_discos.append(disco)

    def listar_discos(self):
        return [d.mostrar() for d in self.lista_discos]

    def buscar_por_album(self, nome_album):
        for disco in self.lista_discos:
            if disco.nome_album.lower() == nome_album.lower():
                return disco
        return None

    def buscar_por_artista(self, nome_artista):
        return [d for d in self.lista_discos if nome_artista.lower() in d.artista.lower()]


# ---------------- STREAMLIT ---------------- #

st.set_page_config(layout="wide")
st.title("💿 Acervo de CDs")

# Estado
if "acervo" not in st.session_state:
    st.session_state.acervo = AcervoCD()

acervo = st.session_state.acervo

# -------- CADASTRO -------- #
st.subheader("➕ Adicionar CD")

col1, col2 = st.columns(2)

with col1:
    nome_artista = st.text_input("Artista / Banda")
    nome_album = st.text_input("Nome do Álbum")

with col2:
    ano_lanc = st.number_input("Ano de Lançamento", min_value=1900, max_value=2100, step=1)

if st.button("Cadastrar"):
    if nome_artista and nome_album:
        disco = DiscoMusical(nome_artista, nome_album, ano_lanc)
        acervo.adicionar_disco(disco)
        st.success(disco.salvar())
    else:
        st.warning("Preencha todos os campos!")

# -------- LISTAGEM -------- #
st.subheader("📋 Lista de CDs")

if acervo.lista_discos:
    for disco in acervo.lista_discos:
        st.write(disco.mostrar())
else:
    st.info("Nenhum CD cadastrado.")

# -------- BUSCA -------- #
st.subheader("🔍 Buscar CD")

tipo_busca = st.radio("Buscar por:", ["Álbum", "Artista"])

texto_busca = st.text_input("Digite a busca")

if st.button("Buscar"):
    if tipo_busca == "Álbum":
        resultado = acervo.buscar_por_album(texto_busca)
        if resultado:
            st.success(resultado.mostrar())
        else:
            st.error("CD não encontrado.")
    else:
        resultados = acervo.buscar_por_artista(texto_busca)
        if resultados:
            for disco in resultados:
                st.write(disco.mostrar())
        else:
            st.error("Nenhum resultado encontrado.")

# -------- REMOVER -------- #
st.subheader("❌ Remover CD")

if acervo.lista_discos:
    opcoes = [d.mostrar() for d in acervo.lista_discos]
    escolha = st.selectbox("Selecione um CD", opcoes)

    if st.button("Remover"):
        index = opcoes.index(escolha)
        acervo.lista_discos.pop(index)
        st.success("CD removido!")
        st.rerun()

# -------- ESTATÍSTICAS -------- #
st.subheader("📊 Estatísticas")

if acervo.lista_discos:
    total = len(acervo.lista_discos)
    mais_antigo = min(acervo.lista_discos, key=lambda d: d.ano_lancamento)
    mais_novo = max(acervo.lista_discos, key=lambda d: d.ano_lancamento)

    st.write(f"Total de CDs: {total}")
    st.write(f"Mais antigo: {mais_antigo.mostrar()}")
    st.write(f"Mais recente: {mais_novo.mostrar()}")