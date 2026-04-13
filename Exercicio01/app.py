import streamlit as st
import pandas as pd

st.title("📊 Controle de Energia Residencial")

# Inicialização da memória da sessão
if "historico_consumo" not in st.session_state:
    st.session_state.historico_consumo = []

# Formulário
st.subheader("➕ Inserir novo registro de energia")

data_medicao = st.date_input("Data da medição")
leitura_kwh = st.number_input("Leitura do medidor", min_value=0)
consumo_kwh_mes = st.number_input("Consumo mensal (kWh)", min_value=0.0)
valor_fatura = st.number_input("Valor da fatura (R$)", min_value=0.0)
data_quitacao = st.date_input("Data de pagamento")

if st.button("Salvar registro"):
    st.session_state.historico_consumo.append({
        "data_medicao": data_medicao,
        "leitura_kwh": leitura_kwh,
        "consumo_kwh_mes": consumo_kwh_mes,
        "valor_fatura": valor_fatura,
        "data_quitacao": data_quitacao
    })
    st.success("Registro salvo com sucesso!")

# Exibição dos dados
if st.session_state.historico_consumo:
    tabela = pd.DataFrame(st.session_state.historico_consumo)

    tabela["data_medicao"] = pd.to_datetime(tabela["data_medicao"])
    tabela = tabela.sort_values(by="data_medicao")

    st.subheader("📋 Histórico de consumo de energia")
    st.dataframe(tabela)

    # Média mensal
    media_consumo_mensal = tabela["consumo_kwh_mes"].mean()
    st.write(f"📊 Média mensal de consumo: {media_consumo_mensal:.2f} kWh")

    # Média diária
    if len(tabela) > 1:
        tabela["intervalo_dias"] = tabela["data_medicao"].diff().dt.days
        tabela["consumo_diario"] = tabela["consumo_kwh_mes"] / tabela["intervalo_dias"]

        media_diaria_consumo = tabela["consumo_diario"].dropna().mean()
        st.write(f"📅 Média diária de consumo: {media_diaria_consumo:.2f} kWh/dia")
    else:
        st.info("Adicione pelo menos 2 registros para calcular a média diária.")

    # Maior consumo
    registro_maior = tabela.loc[tabela["consumo_kwh_mes"].idxmax()]
    st.write("🔥 Maior consumo registrado:")
    st.write(registro_maior)

    # Menor consumo
    registro_menor = tabela.loc[tabela["consumo_kwh_mes"].idxmin()]
    st.write("❄️ Menor consumo registrado:")
    st.write(registro_menor)