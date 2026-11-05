import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

chavesObrigatoriasTriagem = (
    "recordId",
    "protocol",
    "createdAt",
    "urgencyLevel",
    "recommendedService",
    "summary",
    "guidance",
    "warningSignsToWatch",
    "rationale",
    "ageRange",
    "disclaimer",
)

mensagemRespostaInvalida = "Recebemos uma resposta que não conseguimos entender. Tente novamente."


class ApiError(Exception):
    pass


def obterUrlApi():
    return os.getenv("APIURL", "http://localhost:8000")


def obterTempoLimite():
    return float(os.getenv("REQUESTTIMEOUT", "40"))


@st.cache_resource
def obterCliente():
    return httpx.Client(base_url=obterUrlApi(), timeout=obterTempoLimite())


def lerResposta(resposta):
    try:
        corpo = resposta.json()
    except ValueError:
        raise ApiError(mensagemRespostaInvalida) from None

    if resposta.status_code >= 400:
        mensagem = corpo.get("message") if isinstance(corpo, dict) else None
        raise ApiError(mensagem or "Algo deu errado. Tente novamente.")

    return corpo


def enviarRequisicao(metodo, caminho, carga=None):
    try:
        resposta = obterCliente().request(metodo, caminho, json=carga)
    except httpx.TimeoutException:
        raise ApiError("A análise demorou mais do que o esperado. Tente novamente em instantes.") from None
    except httpx.HTTPError:
        raise ApiError("Não conseguimos falar com o serviço agora. Tente novamente em alguns minutos.") from None

    return lerResposta(resposta)


@st.cache_data(ttl=3600, show_spinner=False)
def buscarOpcoes():
    corpo = enviarRequisicao("GET", "/meta/options")
    if not isinstance(corpo, dict) or "ageRanges" not in corpo:
        raise ApiError(mensagemRespostaInvalida)
    return corpo


def solicitarTriagem(carga):
    corpo = enviarRequisicao("POST", "/triage", carga)
    if not isinstance(corpo, dict) or any(chave not in corpo for chave in chavesObrigatoriasTriagem):
        raise ApiError(mensagemRespostaInvalida)
    return corpo


@st.cache_data(ttl=600, show_spinner=False)
def buscarUpasProximas(cep, limite):
    corpo = enviarRequisicao("POST", "/units/nearby", {"cep": cep, "limit": limite})
    if not isinstance(corpo, dict) or "units" not in corpo or "origin" not in corpo:
        raise ApiError(mensagemRespostaInvalida)
    return corpo


def enviarRevisao(carga):
    corpo = enviarRequisicao("POST", "/reviews", carga)
    if not isinstance(corpo, dict) or "finalUrgency" not in corpo:
        raise ApiError(mensagemRespostaInvalida)
    return corpo
