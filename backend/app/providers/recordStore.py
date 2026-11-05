import threading

maximoRegistros = 1000
registros = {}
revisoes = {}
trava = threading.Lock()


def salvarRegistro(registro):
    with trava:
        registros[registro.recordId] = registro
        while len(registros) > maximoRegistros:
            maisAntigo = next(iter(registros))
            registros.pop(maisAntigo)
            revisoes.pop(maisAntigo, None)


def buscarRegistro(idRegistro):
    with trava:
        return registros.get(idRegistro)


def salvarRevisao(idRegistro, revisao):
    with trava:
        revisoes[idRegistro] = revisao


def limparArmazenamento():
    with trava:
        registros.clear()
        revisoes.clear()
