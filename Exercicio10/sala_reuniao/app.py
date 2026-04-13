import pandas as pd
import streamlit as st
from datetime import datetime, date
from models import SalaReuniao, Funcionario, Reuniao, AgendaDiaria

st.set_page_config(page_title="Gestão de Salas", page_icon="📅")
st.title("Sistema de Gestão de Salas de Reunião")

# ---------------- ESTADO ---------------- #

if "lista_salas" not in st.session_state:
    st.session_state.lista_salas = []

if "lista_funcionarios" not in st.session_state:
    st.session_state.lista_funcionarios = []

if "agenda_atual" not in st.session_state:
    st.session_state.agenda_atual = AgendaDiaria(date.today())

agenda = st.session_state.agenda_atual

# ---------------- ABAS ---------------- #

aba_salas, aba_func, aba_agendar, aba_realocar, aba_consulta = st.tabs([
    "Salas",
    "Funcionários",
    "Agendar",
    "Realocar",
    "Consultas"
])

# ===================== ABA SALAS ===================== #
with aba_salas:
    st.subheader("Cadastro de Sala")

    with st.form("form_sala"):
        id_sala = st.number_input("Número da sala", min_value=1, step=1)
        capacidade = st.number_input("Capacidade", min_value=1, step=1)
        salvar_sala = st.form_submit_button("Salvar")

    if salvar_sala:
        existe_sala = any(s.numero == int(id_sala) for s in st.session_state.lista_salas)

        if existe_sala:
            st.warning("Sala já cadastrada.")
        else:
            st.session_state.lista_salas.append(SalaReuniao(int(id_sala), int(capacidade)))
            st.success("Sala cadastrada com sucesso!")

    if st.session_state.lista_salas:
        df_salas = pd.DataFrame([s.exibir() for s in st.session_state.lista_salas])
        st.dataframe(df_salas, use_container_width=True)

# ===================== ABA FUNCIONÁRIOS ===================== #
with aba_func:
    st.subheader("Cadastro de Funcionário")

    with st.form("form_func"):
        nome_func = st.text_input("Nome")
        cargo_func = st.text_input("Cargo")
        ramal_func = st.text_input("Ramal")
        salvar_func = st.form_submit_button("Salvar")

    if salvar_func:
        if not nome_func.strip():
            st.warning("Informe o nome.")
        else:
            st.session_state.lista_funcionarios.append(Funcionario(nome_func, cargo_func, ramal_func))
            st.success("Funcionário cadastrado!")

    if st.session_state.lista_funcionarios:
        df_func = pd.DataFrame([f.exibir() for f in st.session_state.lista_funcionarios])
        st.dataframe(df_func, use_container_width=True)

# ===================== ABA AGENDAR ===================== #
with aba_agendar:
    st.subheader("Agendar Reunião")

    if not st.session_state.lista_salas:
        st.info("Cadastre salas primeiro.")
    elif not st.session_state.lista_funcionarios:
        st.info("Cadastre funcionários primeiro.")
    else:
        with st.form("form_agenda"):
            assunto_reuniao = st.text_input("Assunto")
            data_agenda = st.date_input("Data", value=agenda.data)

            horario_escolhido = st.selectbox(
                "Horário",
                ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
            )

            sala_escolhida = st.selectbox(
                "Sala",
                [s.numero for s in st.session_state.lista_salas]
            )

            responsavel = st.selectbox(
                "Responsável",
                [f.nome for f in st.session_state.lista_funcionarios]
            )

            salvar_reuniao = st.form_submit_button("Agendar")

        if salvar_reuniao:
            sala_obj = next(s for s in st.session_state.lista_salas if s.numero == sala_escolhida)
            func_obj = next(f for f in st.session_state.lista_funcionarios if f.nome == responsavel)

            horario_obj = datetime.strptime(horario_escolhido, "%H:%M").time()

            if not sala_obj.verificar_disponibilidade(agenda.reunioes, data_agenda, horario_obj):
                st.error("Sala ocupada nesse horário.")
            else:
                reuniao = Reuniao(
                    assunto=assunto_reuniao,
                    data=data_agenda,
                    horario=horario_obj,
                    sala=sala_obj,
                    funcionario=func_obj
                )
                agenda.adicionar_reuniao(reuniao)
                st.success("Reunião agendada!")

# ===================== ABA REALOCAR ===================== #
with aba_realocar:
    st.subheader("Realocar Reunião")

    lista_reunioes = agenda.reunioes

    if not lista_reunioes:
        st.info("Nenhuma reunião cadastrada.")
    else:
        opcoes = [
            f"{i} - {r.assunto} | {r.data.strftime('%d/%m/%Y')} {r.horario.strftime('%H:%M')} | Sala {r.sala.numero}"
            for i, r in enumerate(lista_reunioes)
        ]

        escolha_reuniao = st.selectbox("Selecione", opcoes)
        idx = int(escolha_reuniao.split(" - ")[0])
        reuniao = lista_reunioes[idx]

        nova_data = st.date_input("Nova data", value=reuniao.data, key="nova_data")
        novo_horario_str = st.selectbox(
            "Novo horário",
            ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"],
            key="novo_horario"
        )

        nova_sala_num = st.selectbox(
            "Nova sala",
            [s.numero for s in st.session_state.lista_salas],
            key="nova_sala"
        )

        if st.button("Confirmar realocação"):
            nova_sala = next(s for s in st.session_state.lista_salas if s.numero == nova_sala_num)
            novo_horario = datetime.strptime(novo_horario_str, "%H:%M").time()

            conflito = any(
                i != idx and r.sala.numero == nova_sala.numero and r.data == nova_data and r.horario == novo_horario
                for i, r in enumerate(lista_reunioes)
            )

            if conflito:
                st.error("Conflito de horário na sala.")
            else:
                reuniao.realocar(nova_sala, nova_data, novo_horario)
                st.success("Reunião realocada!")

# ===================== ABA CONSULTA ===================== #
with aba_consulta:
    st.subheader("Reuniões do Dia")

    data_filtro = st.date_input("Data", value=agenda.data, key="data_filtro")
    agenda.data = data_filtro

    reunioes_dia = agenda.listar_reunioes()

    if reunioes_dia:
        df_reunioes = pd.DataFrame([r.exibir() for r in reunioes_dia])
        st.dataframe(df_reunioes, use_container_width=True)
    else:
        st.info("Sem reuniões nesta data.")

    st.subheader("Salas livres")

    if st.session_state.lista_salas:
        horario_filtro = st.selectbox(
            "Horário",
            ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"],
            key="horario_filtro"
        )

        if st.button("Ver disponibilidade"):
            horario_obj = datetime.strptime(horario_filtro, "%H:%M").time()
            livres = agenda.consultar_salas_livres(st.session_state.lista_salas, horario_obj)

            if livres:
                df_livres = pd.DataFrame([s.exibir() for s in livres])
                st.dataframe(df_livres, use_container_width=True)
            else:
                st.warning("Nenhuma sala livre nesse horário.")