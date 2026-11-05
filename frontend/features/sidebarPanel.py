import streamlit as st

from state.sessionState import obterRegistros
from ui.components import renderizarCartaoInfo


def renderizarBarraLateral():
    with st.sidebar:
        st.markdown("## ✚ Orienta Saúde")
        renderizarCartaoInfo(
            "Telefones de emergência",
            ["SAMU: 192", "Bombeiros: 193", "Disque Saúde: 136"],
            "📞",
        )
        st.caption(f"Análises feitas nesta sessão: {len(obterRegistros())}")
        st.caption("Em caso de dúvida ou piora, procure atendimento presencial.")
