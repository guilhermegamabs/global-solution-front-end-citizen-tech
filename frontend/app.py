import streamlit as st

from features.aboutScreen import renderizarSobre
from features.dashboardScreen import renderizarPainel
from features.historyScreen import renderizarHistorico
from features.sidebarPanel import renderizarBarraLateral
from features.triageScreen import renderizarTriagem
from features.unitsScreen import renderizarUpas
from state.sessionState import iniciarEstado
from ui.theme import aplicarTema

st.set_page_config(page_title="Orienta Saúde", page_icon="✚", layout="wide")

iniciarEstado()
aplicarTema()
renderizarBarraLateral()

st.markdown(
    '<div class="appHeader"><h1>✚ Orienta Saúde</h1>'
    "<p>Descubra onde buscar atendimento, em linguagem simples.</p></div>",
    unsafe_allow_html=True,
)

abaTriagem, abaUpas, abaHistorico, abaPainel, abaSobre = st.tabs(
    ["🩺 Triagem", "🗺️ UPAs próximas", "🗂️ Histórico", "📊 Painel", "ℹ️ Sobre"]
)

with abaTriagem:
    renderizarTriagem()
with abaUpas:
    renderizarUpas()
with abaHistorico:
    renderizarHistorico()
with abaPainel:
    renderizarPainel()
with abaSobre:
    renderizarSobre()
