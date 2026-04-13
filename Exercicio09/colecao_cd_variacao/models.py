from __future__ import annotations


class Artista:
    def __init__(self, nome_artista: str):
        self.nome_artista = nome_artista

    def exibir(self) -> dict:
        return {"Nome": self.nome_artista}


class Faixa:
    def __init__(self, nome_faixa: str, tempo_duracao: str):
        self.nome_faixa = nome_faixa
        self.tempo_duracao = tempo_duracao

    def exibir(self) -> dict:
        return {
            "Título": self.nome_faixa,
            "Duração": self.tempo_duracao
        }


class AlbumCD:
    def __init__(self, nome_album: str, ano_lancamento: int, e_coletanea: bool, e_duplo: bool):
        self.nome_album = nome_album
        self.ano_lancamento = ano_lancamento
        self.e_coletanea = e_coletanea
        self.e_duplo = e_duplo
        self.lista_artistas: list[Artista] = []
        self.lista_faixas: list[Faixa] = []

    def cadastrar(self) -> None:
        pass

    def exibir(self) -> dict:
        return {
            "Título": self.nome_album,
            "Ano": self.ano_lancamento,
            "Coletânea": "Sim" if self.e_coletanea else "Não",
            "Duplo": "Sim" if self.e_duplo else "Não",
            "Artistas": ", ".join(a.nome_artista for a in self.lista_artistas) if self.lista_artistas else "-",
            "Faixas": ", ".join(f.nome_faixa for f in self.lista_faixas) if self.lista_faixas else "-"
        }

    def listar_artistas(self) -> list[str]:
        return [a.nome_artista for a in self.lista_artistas]

    def listar_faixas(self) -> list[str]:
        return [f.nome_faixa for f in self.lista_faixas]

    def adicionar_artista(self, artista: Artista) -> None:
        if all(a.nome_artista.lower() != artista.nome_artista.lower() for a in self.lista_artistas):
            self.lista_artistas.append(artista)

    def adicionar_faixa(self, faixa: Faixa) -> None:
        if all(f.nome_faixa.lower() != faixa.nome_faixa.lower() for f in self.lista_faixas):
            self.lista_faixas.append(faixa)


class AcervoCD:
    def __init__(self):
        self.lista_cds: list[AlbumCD] = []

    def adicionar_cd(self, cd: AlbumCD) -> None:
        self.lista_cds.append(cd)

    def listar_cds(self) -> list[dict]:
        return [cd.exibir() for cd in self.lista_cds]

    def buscar_por_artista(self, nome: str) -> list[AlbumCD]:
        resultados = []
        for cd in self.lista_cds:
            for artista in cd.lista_artistas:
                if nome.lower() in artista.nome_artista.lower():
                    resultados.append(cd)
                    break
        return resultados

    def buscar_por_faixa(self, titulo: str) -> list[AlbumCD]:
        resultados = []
        for cd in self.lista_cds:
            for faixa in cd.lista_faixas:
                if titulo.lower() in faixa.nome_faixa.lower():
                    resultados.append(cd)
                    break
        return resultados