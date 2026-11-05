import pytest
from fastapi.testclient import TestClient

from app.dependencies import obterFontesLocalizacao, obterGerador
from app.main import aplicacao
from app.providers.recordStore import limparArmazenamento

saidaValida = {
    "urgencyLevel": "medium",
    "recommendedService": "basicUnit",
    "summary": "Sintomas de gripe sem sinais de gravidade.",
    "guidance": ["Beba bastante água.", "Descanse."],
    "warningSignsToWatch": ["Falta de ar", "Febre acima de 39 °C"],
    "rationale": "Quadro comum, sem sinais de alerta.",
}

requisicaoValida = {
    "symptoms": "Estou com dor de garganta e febre baixa desde ontem.",
    "ageRange": "adult",
    "duration": "oneToThreeDays",
    "warningSigns": [],
    "hasChronicCondition": False,
}


def sobrescreverGerador(gerar):
    aplicacao.dependency_overrides[obterGerador] = lambda: gerar


def sobrescreverFontes(fontes):
    aplicacao.dependency_overrides[obterFontesLocalizacao] = lambda: fontes


@pytest.fixture
def cliente():
    limparArmazenamento()
    sobrescreverGerador(lambda promptSistema, promptUsuario: dict(saidaValida))
    yield TestClient(aplicacao)
    aplicacao.dependency_overrides.clear()
