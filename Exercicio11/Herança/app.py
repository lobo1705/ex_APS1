import streamlit as st
from datetime import date, datetime

# =========================
# CLASSES DO MODELO
# =========================

class Localizacao:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str, cep: str):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - CEP: {self.cep}"


class Contato:
    def __init__(self, numero: str, tipo: str):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        return f"{self.numero} ({self.tipo})"


class PessoaBase:
    def __init__(self, nome: str, data_nascimento: date, localizacao: Localizacao, contato: Contato):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.localizacao = localizacao
        self.contato = contato

    def cadastrar(self):
        return f"{self.nome} cadastrado com sucesso."

    def calcular_idade(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade


class Colaborador(PessoaBase):
    def __init__(self, nome: str, data_nascimento: date, localizacao: Localizacao, contato: Contato,
                 id_func: int, funcao: str, salario: float):
        super().__init__(nome, data_nascimento, localizacao, contato)
        self.id_func = id_func
        self.funcao = funcao
        self.salario = salario

    def admitir(self):
        return f"Colaborador {self.nome} admitido."

    def reajustar(self, percentual: float):
        self.salario += self.salario * (percentual / 100)

    def promover(self, nova_funcao: str):
        self.funcao = nova_funcao


class Cliente(PessoaBase):
    def __init__(self, nome: str, data_nascimento: date, localizacao: Localizacao, contato: Contato,
                 codigo_cliente: str, profissao: str):
        super().__init__(nome, data_nascimento, localizacao, contato)
        self.codigo_cliente = codigo_cliente
        self.profissao = profissao


# =========================
# FUNÇÕES AUXILIARES
# =========================

def iniciar_sessao():
    if "lista_clientes" not in st.session_state:
        st.session_state.lista_clientes = []

    if "lista_colaboradores" not in st.session_state:
        st.session_state.lista_colaboradores = []


def criar_localizacao(rua, numero, bairro, cidade, cep):
    return Localizacao(rua, numero, bairro, cidade, cep)


def criar_contato(numero, tipo):
    return Contato(numero, tipo)


# =========================
# INTERFACE
# =========================

st.set_page_config(page_title="Gestão de Pessoas", layout="wide")
iniciar_sessao()

st.title("Sistema de Cadastro - Pessoas")

menu_opcao = st.sidebar.selectbox(
    "Menu",
    [
        "Novo Cliente",
        "Novo Colaborador",
        "Clientes",
        "Colaboradores",
        "Gestão de Colaboradores"
    ]
)

# =========================
# NOVO CLIENTE
# =========================
if menu_opcao == "Novo Cliente":
    st.header("Cadastro de Cliente")

    with st.form("form_cliente"):
        nome_cliente = st.text_input("Nome")
        nascimento_cliente = st.date_input("Data de nascimento", min_value=date(1900, 1, 1), max_value=date.today())

        st.subheader("Endereço")
        rua = st.text_input("Rua")
        numero = st.number_input("Número", min_value=0, step=1)
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")

        st.subheader("Contato")
        tel_numero = st.text_input("Telefone")
        tel_tipo = st.selectbox("Tipo", ["Celular", "Residencial", "Comercial"])

        st.subheader("Dados do Cliente")
        codigo = st.text_input("Código")
        profissao = st.text_input("Profissão")

        enviar = st.form_submit_button("Salvar")

        if enviar:
            loc = criar_localizacao(rua, numero, bairro, cidade, cep)
            contato = criar_contato(tel_numero, tel_tipo)

            cliente = Cliente(
                nome_cliente,
                nascimento_cliente,
                loc,
                contato,
                codigo,
                profissao
            )

            st.session_state.lista_clientes.append(cliente)
            st.success(cliente.cadastrar())
            st.info(f"Idade: {cliente.calcular_idade()} anos")


# =========================
# NOVO COLABORADOR
# =========================
elif menu_opcao == "Novo Colaborador":
    st.header("Cadastro de Colaborador")

    with st.form("form_colaborador"):
        nome_colab = st.text_input("Nome")
        nascimento_colab = st.date_input("Data de nascimento", min_value=date(1900, 1, 1), max_value=date.today())

        st.subheader("Endereço")
        rua = st.text_input("Rua")
        numero = st.number_input("Número", min_value=0, step=1)
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        cep = st.text_input("CEP")

        st.subheader("Contato")
        tel_numero = st.text_input("Telefone")
        tel_tipo = st.selectbox("Tipo", ["Celular", "Residencial", "Comercial"])

        st.subheader("Dados do Colaborador")
        id_func = st.number_input("ID", min_value=1, step=1)
        funcao = st.text_input("Função")
        salario = st.number_input("Salário", min_value=0.0, step=100.0)

        enviar = st.form_submit_button("Salvar")

        if enviar:
            loc = criar_localizacao(rua, numero, bairro, cidade, cep)
            contato = criar_contato(tel_numero, tel_tipo)

            colaborador = Colaborador(
                nome_colab,
                nascimento_colab,
                loc,
                contato,
                id_func,
                funcao,
                salario
            )

            st.session_state.lista_colaboradores.append(colaborador)
            st.success(colaborador.cadastrar())
            st.info(colaborador.admitir())
            st.info(f"Idade: {colaborador.calcular_idade()} anos")


# =========================
# LISTA CLIENTES
# =========================
elif menu_opcao == "Clientes":
    st.header("Clientes")

    if not st.session_state.lista_clientes:
        st.warning("Nenhum cliente.")
    else:
        for i, c in enumerate(st.session_state.lista_clientes, 1):
            with st.expander(f"Cliente {i} - {c.nome}"):
                st.write(f"Código: {c.codigo_cliente}")
                st.write(f"Profissão: {c.profissao}")
                st.write(f"Idade: {c.calcular_idade()}")
                st.write(f"Endereço: {c.localizacao}")
                st.write(f"Contato: {c.contato}")


# =========================
# LISTA COLABORADORES
# =========================
elif menu_opcao == "Colaboradores":
    st.header("Colaboradores")

    if not st.session_state.lista_colaboradores:
        st.warning("Nenhum colaborador.")
    else:
        for i, c in enumerate(st.session_state.lista_colaboradores, 1):
            with st.expander(f"Colaborador {i} - {c.nome}"):
                st.write(f"ID: {c.id_func}")
                st.write(f"Função: {c.funcao}")
                st.write(f"Salário: R$ {c.salario:.2f}")
                st.write(f"Idade: {c.calcular_idade()}")
                st.write(f"Endereço: {c.localizacao}")
                st.write(f"Contato: {c.contato}")


# =========================
# GESTÃO COLABORADORES
# =========================
elif menu_opcao == "Gestão de Colaboradores":
    st.header("Gestão")

    if not st.session_state.lista_colaboradores:
        st.warning("Nenhum colaborador.")
    else:
        opcoes = [f"{c.nome} - ID {c.id_func}" for c in st.session_state.lista_colaboradores]
        escolha = st.selectbox("Selecionar", opcoes)
        idx = opcoes.index(escolha)
        colaborador = st.session_state.lista_colaboradores[idx]

        st.subheader("Atual")
        st.write(colaborador.funcao)
        st.write(f"R$ {colaborador.salario:.2f}")

        st.divider()

        novo_percentual = st.number_input("Reajuste (%)", min_value=0.0, step=1.0)
        if st.button("Reajustar"):
            colaborador.reajustar(novo_percentual)
            st.success(f"Novo salário: R$ {colaborador.salario:.2f}")

        st.divider()

        nova_funcao = st.text_input("Nova função")
        if st.button("Promover"):
            if nova_funcao.strip():
                colaborador.promover(nova_funcao)
                st.success("Promoção realizada!")
            else:
                st.error("Informe a função.")