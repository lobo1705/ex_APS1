from datetime import date, time


class SalaReuniao:
    def __init__(self, numero: int, quantidade_lugares: int):
        self.numero = numero
        self.quantidade_lugares = quantidade_lugares

    def verificar_disponibilidade(self, reunioes: list, data: date, horario: time) -> bool:
        for reuniao in reunioes:
            if (
                reuniao.sala.numero == self.numero
                and reuniao.data == data
                and reuniao.horario == horario
            ):
                return False
        return True

    def exibir(self) -> dict:
        return {
            "Sala": self.numero,
            "Lugares": self.quantidade_lugares
        }


class Funcionario:
    def __init__(self, nome: str, cargo: str, ramal: str):
        self.nome = nome
        self.cargo = cargo
        self.ramal = ramal

    def exibir(self) -> dict:
        return {
            "Nome": self.nome,
            "Cargo": self.cargo,
            "Ramal": self.ramal
        }


class Reuniao:
    def __init__(self, assunto: str, data: date, horario: time, sala: SalaReuniao, funcionario: Funcionario):
        self.assunto = assunto
        self.data = data
        self.horario = horario
        self.sala = sala
        self.funcionario = funcionario

    def agendar(self) -> None:
        pass

    def realocar(self, nova_sala: SalaReuniao, nova_data: date, novo_horario: time) -> None:
        self.sala = nova_sala
        self.data = nova_data
        self.horario = novo_horario

    def exibir(self) -> dict:
        return {
            "Assunto": self.assunto,
            "Data": self.data.strftime("%d/%m/%Y"),
            "Horário": self.horario.strftime("%H:%M"),
            "Sala": self.sala.numero,
            "Funcionário": self.funcionario.nome,
            "Cargo": self.funcionario.cargo,
            "Ramal": self.funcionario.ramal
        }


class AgendaDiaria:
    def __init__(self, data: date):
        self.data = data
        self.reunioes = []

    def adicionar_reuniao(self, reuniao: Reuniao) -> None:
        self.reunioes.append(reuniao)

    def listar_reunioes(self) -> list:
        return [r for r in self.reunioes if r.data == self.data]

    def consultar_salas_livres(self, salas: list, horario: time) -> list:
        salas_livres = []

        for sala in salas:
            ocupada = False
            for reuniao in self.reunioes:
                if reuniao.data == self.data and reuniao.horario == horario and reuniao.sala.numero == sala.numero:
                    ocupada = True
                    break

            if not ocupada:
                salas_livres.append(sala)

        return salas_livres