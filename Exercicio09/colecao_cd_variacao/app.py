import pandas as pd
import streamlit as st
from models import Musico, Musica, CD, ColecaoCD

st.set_page_config(page_title="Acervo Musical", page_icon="💿")
st.title("Acervo de CDs - Sistema Completo")

# ---------------- ESTADO ---------------- #

if "acervo_cd" not in st.session_state:
    st.session_state.acervo_cd = ColecaoCD()

if "lista_musicos" not in st.session_state:
    st.session_state.lista_musicos = []

if "lista_musicas" not in st.session_state:
    st.session_state.lista_musicas = []

acervo = st.session_state.acervo_cd

# ---------------- ABAS ---------------- #

aba1, aba2, aba3, aba4 = st.tabs([
    "Músicos",
    "Músicas",
    "CDs",
    "Pesquisa"
])

# ===================== ABA 1 ===================== #
with aba1:
    st.subheader("Cadastro de Músico")

    with st.form("form_artista"):
        nome_artista = st.text_input("Nome do artista ou grupo")
        salvar_artista = st.form_submit_button("Salvar")

    if salvar_artista:
        if not nome_artista.strip():
            st.warning("Informe o nome do artista.")
        else:
            existe_artista = any(a.nome.lower() == nome_artista.lower() for a in st.session_state.lista_musicos)

            if existe_artista:
                st.warning("Artista já cadastrado.")
            else:
                st.session_state.lista_musicos.append(Musico(nome_artista))
                st.success("Artista cadastrado com sucesso!")

    if st.session_state.lista_musicos:
        st.write("Artistas cadastrados:")
        tabela = pd.DataFrame([a.exibir() for a in st.session_state.lista_musicos])
        st.dataframe(tabela, use_container_width=True)

# ===================== ABA 2 ===================== #
with aba2:
    st.subheader("Cadastro de Música")

    with st.form("form_faixa"):
        nome_faixa = st.text_input("Título da faixa")
        duracao_faixa = st.text_input("Duração (ex: 03:45)")
        salvar_faixa = st.form_submit_button("Salvar")

    if salvar_faixa:
        if not nome_faixa.strip() or not duracao_faixa.strip():
            st.warning("Preencha todos os campos.")
        else:
            existe_faixa = any(f.titulo.lower() == nome_faixa.lower() for f in st.session_state.lista_musicas)

            if existe_faixa:
                st.warning("Faixa já cadastrada.")
            else:
                st.session_state.lista_musicas.append(Musica(nome_faixa, duracao_faixa))
                st.success("Faixa cadastrada com sucesso!")

    if st.session_state.lista_musicas:
        st.write("Faixas cadastradas:")
        tabela = pd.DataFrame([f.exibir() for f in st.session_state.lista_musicas])
        st.dataframe(tabela, use_container_width=True)

# ===================== ABA 3 ===================== #
with aba3:
    st.subheader("Cadastro de CD")

    nomes_artistas = [a.nome for a in st.session_state.lista_musicos]
    nomes_faixas = [f.titulo for f in st.session_state.lista_musicas]

    with st.form("form_album"):
        titulo_album = st.text_input("Título do álbum")
        ano_lancamento = st.number_input("Ano de lançamento", min_value=1900, max_value=2100, step=1)
        e_coletanea = st.checkbox("Coletânea")
        e_duplo = st.checkbox("Duplo")

        artistas_selecionados = st.multiselect(
            "Artistas",
            options=nomes_artistas
        )

        faixas_selecionadas = st.multiselect(
            "Músicas",
            options=nomes_faixas
        )

        salvar_album = st.form_submit_button("Salvar CD")

    if salvar_album:
        if not titulo_album.strip():
            st.warning("Informe o título do CD.")
        elif not artistas_selecionados:
            st.warning("Selecione pelo menos um artista.")
        elif not faixas_selecionadas:
            st.warning("Selecione pelo menos uma música.")
        else:
            album = CD(
                titulo=titulo_album,
                ano_lancamento=int(ano_lancamento),
                coletanea=e_coletanea,
                duplo=e_duplo
            )

            for nome in artistas_selecionados:
                artista = next((a for a in st.session_state.lista_musicos if a.nome == nome), None)
                if artista:
                    album.adicionar_musico(artista)

            for nome in faixas_selecionadas:
                faixa = next((f for f in st.session_state.lista_musicas if f.titulo == nome), None)
                if faixa:
                    album.adicionar_musica(faixa)

            acervo.adicionar_cd(album)
            st.success("CD cadastrado com sucesso!")

    if acervo.cds:
        st.write("CDs cadastrados:")
        tabela = pd.DataFrame(acervo.listar_cds())
        st.dataframe(tabela, use_container_width=True)

# ===================== ABA 4 ===================== #
with aba4:
    st.subheader("Busca por artista")

    busca_artista = st.text_input("Nome do artista", key="busca_artista")

    if st.button("Buscar por artista"):
        resultado = acervo.buscar_cds_por_musico(busca_artista)
        if resultado:
            tabela = pd.DataFrame([cd.exibir() for cd in resultado])
            st.dataframe(tabela, use_container_width=True)
        else:
            st.warning("Nenhum CD encontrado.")

    st.subheader("Busca por música")

    busca_faixa = st.text_input("Nome da música", key="busca_faixa")

    if st.button("Buscar por música"):
        resultado = acervo.buscar_cds_por_musica(busca_faixa)
        if resultado:
            tabela = pd.DataFrame([cd.exibir() for cd in resultado])
            st.dataframe(tabela, use_container_width=True)
        else:
            st.warning("Nenhum CD encontrado.")