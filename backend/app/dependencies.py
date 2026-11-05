from app.providers.cepProvider import buscarCoordenadasPorCep, buscarEnderecoPorCep
from app.providers.cnesProvider import listarUpasDoMunicipio
from app.providers.geminiProvider import gerarEstruturado
from app.providers.geocodeProvider import buscarPontoPorNome, geocodificar


def obterGerador():
    return gerarEstruturado


def obterFontesLocalizacao():
    return {
        "buscarCep": buscarEnderecoPorCep,
        "geocodificar": geocodificar,
        "listarUnidades": listarUpasDoMunicipio,
        "coordenadasPorCep": buscarCoordenadasPorCep,
        "pontoPorNome": buscarPontoPorNome,
    }
