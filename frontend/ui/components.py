from html import escape

import streamlit as st

from ui.theme import estilosUrgencia


def montarHtmlSelo(nivel, grande=False):
    estilo = estilosUrgencia[nivel]
    tamanho = " large" if grande else ""
    return (
        f'<span class="urgencyBadge{tamanho}" style="color:{estilo["cor"]};'
        f'background:{estilo["fundo"]};border-color:{estilo["borda"]}">'
        f'{estilo["icone"]} Urgência {estilo["rotulo"].lower()}</span>'
    )


def renderizarSeloUrgencia(nivel, grande=False):
    st.markdown(montarHtmlSelo(nivel, grande), unsafe_allow_html=True)


def renderizarCartaoMetrica(rotulo, valor, dica=""):
    st.markdown(
        f'<div class="metricCard"><div class="metricLabel">{escape(rotulo)}</div>'
        f'<div class="metricValue">{escape(str(valor))}</div>'
        f'<div class="metricHint">{escape(dica)}</div></div>',
        unsafe_allow_html=True,
    )


def renderizarCartaoInfo(titulo, itens, icone="•"):
    itensLista = "".join(f"<li>{escape(item)}</li>" for item in itens)
    st.markdown(
        f'<div class="infoCard"><h4>{escape(icone)} {escape(titulo)}</h4><ul>{itensLista}</ul></div>',
        unsafe_allow_html=True,
    )


def renderizarEstadoVazio(icone, titulo, mensagem):
    st.markdown(
        f'<div class="emptyState"><div class="emptyIcon" aria-hidden="true">{escape(icone)}</div>'
        f"<strong>{escape(titulo)}</strong><br>{escape(mensagem)}</div>",
        unsafe_allow_html=True,
    )


def renderizarCartaoProtocolo(protocolo):
    st.markdown(
        f'<div class="protocolCard"><span class="protocolLabel">Guarde este protocolo</span>'
        f'<span class="protocolCode">{escape(protocolo)}</span></div>',
        unsafe_allow_html=True,
    )


def renderizarAviso(texto):
    st.markdown(
        f'<div class="noticeCard">ℹ️ {escape(texto)}</div>',
        unsafe_allow_html=True,
    )


def renderizarCartaoConfirmacao(protocolo, nivel):
    st.markdown(
        f'<div class="confirmCard" role="status"><strong>✅ Resposta registrada</strong>'
        f'<div class="confirmLine">Protocolo {escape(protocolo)}</div>'
        f'<div class="confirmLine">{montarHtmlSelo(nivel)}</div></div>',
        unsafe_allow_html=True,
    )


def renderizarFaixaEmergencia(mensagem):
    st.markdown(
        f'<div class="alertBanner" role="alert">🚨 {escape(mensagem)}</div>',
        unsafe_allow_html=True,
    )


def renderizarFaixaErro(mensagem):
    st.error(mensagem, icon="⚠️")
