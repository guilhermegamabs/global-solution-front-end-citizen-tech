import streamlit as st


def iniciarEstado():
    st.session_state.setdefault("registros", [])
    st.session_state.setdefault("idAtual", None)


def obterRegistros():
    return st.session_state["registros"]


def adicionarRegistro(registro):
    st.session_state["registros"].insert(0, {**registro, "review": None})
    st.session_state["idAtual"] = registro["recordId"]


def obterRegistroAtual():
    idAtual = st.session_state["idAtual"]
    for registro in st.session_state["registros"]:
        if registro["recordId"] == idAtual:
            return registro
    return None


def aplicarRevisao(idRegistro, revisao):
    for registro in st.session_state["registros"]:
        if registro["recordId"] == idRegistro:
            registro["review"] = revisao


def limparAtual():
    st.session_state["idAtual"] = None
