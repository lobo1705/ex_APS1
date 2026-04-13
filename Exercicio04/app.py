import streamlit as st
from datetime import datetime, timedelta, time

# =========================
# Classe Horario
# =========================
class AgendaHorario:
    def __init__(self, horario_base):
        self.horario_base = horario_base
        self.status_tomado = False
        self.status_atraso = False

    def alterar_horario(self, novo_horario):
        self.horario_base = novo_horario

    def mostrar(self):
        situacao = "✔️ Tomado" if self.status_tomado else "⏳ Pendente"
        if self.status_atraso:
            situacao += " (Atrasado)"
        return f"{self.horario_base.strftime('%H:%M')} - {situacao}"


# =========================
# Classe Medicamento
# =========================
class Medicamento:
    def __init__(self, paciente_nome, inicio_tratamento, dias_tratamento, frequencia_diaria, dose, remedio_nome):
        self.paciente_nome = paciente_nome
        self.inicio_tratamento = inicio_tratamento
        self.dias_tratamento = dias_tratamento
        self.frequencia_diaria = frequencia_diaria
        self.dose = dose
        self.remedio_nome = remedio_nome
        self.lista_horarios = []

    def registrar(self):
        return f"Medicamento {self.remedio_nome} cadastrado para {self.paciente_nome}"

    def gerar_horarios(self):
        intervalo_horas = 24 // self.frequencia_diaria
        lista = []

        for i in range(self.frequencia_diaria):
            horario_calc = time(hour=(8 + i * intervalo_horas) % 24, minute=0)
            lista.append(AgendaHorario(horario_calc))

        self.lista_horarios = lista

    def data_final(self):
        return self.inicio_tratamento + timedelta(days=self.dias_tratamento)

    def montar_arquivo(self):
        planilha = []
        data_atual = self.inicio_tratamento

        for _ in range(self.dias_tratamento):
            for horario in self.lista_horarios:
                planilha.append({
                    "Data": data_atual.strftime("%d/%m/%Y"),
                    "Hora": horario.horario_base.strftime("%H:%M"),
                    "Medicamento": self.remedio_nome,
                    "Dose": self.dose
                })
            data_atual += timedelta(days=1)

        return planilha

    def ordenar_horarios(self):
        self.lista_horarios.sort(key=lambda h: h.horario_base)


# =========================
# INTERFACE STREAMLIT
# =========================
st.title("💊 Sistema de Controle de Medicamentos")

st.sidebar.header("Cadastro")

nome_paciente = st.sidebar.text_input("Paciente")
nome_remedio = st.sidebar.text_input("Medicamento")
dose_remedio = st.sidebar.text_input("Dose")
data_inicio = st.sidebar.date_input("Início do tratamento")
dias = st.sidebar.number_input("Dias de uso", min_value=1)
frequencia = st.sidebar.number_input("Vezes ao dia", min_value=1, max_value=24)

if st.sidebar.button("Salvar"):
    med = Medicamento(
        nome_paciente,
        data_inicio,
        dias,
        frequencia,
        dose_remedio,
        nome_remedio
    )

    med.gerar_horarios()
    med.ordenar_horarios()

    st.session_state["medicamento"] = med
    st.success(med.registrar())


# =========================
# EXIBIÇÃO
# =========================
if "medicamento" in st.session_state:
    med = st.session_state["medicamento"]

    st.subheader("📋 Dados do Paciente")
    st.write(f"Paciente: {med.paciente_nome}")
    st.write(f"Medicamento: {med.remedio_nome}")
    st.write(f"Dose: {med.dose}")
    st.write(f"Data final: {med.data_final()}")

    st.subheader("⏰ Horários")

    for i, horario in enumerate(med.lista_horarios):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.write(horario.mostrar())

        with c2:
            if st.button(f"Tomado {i}"):
                horario.status_tomado = True

        with c3:
            if st.button(f"Atrasado {i}"):
                horario.status_atraso = True

    st.subheader("📊 Planilha")
    st.dataframe(med.montar_arquivo())