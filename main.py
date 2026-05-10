# main.py
# Ponto de entrada do sistema.
# Execute com: streamlit run main.py

import streamlit as st
from database.connection import init_db

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistema de Cobranças",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inicializa o banco uma única vez por sessão ───────────────────────────────
@st.cache_resource
def startup():
    init_db()
    return True

startup()

# ── Navegação lateral ─────────────────────────────────────────────────────────
with st.sidebar:
    st.title("💰 Cobranças")
    st.markdown("---")

    pagina = st.radio(
        label="Navegação",
        options=[
            "📋 Lançamento em Lote",
            "🔍 Consultar Cobranças",
            # Etapas futuras:
            # "📤 Exportar Excel",
            # "📥 Importar Excel",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("v0.3 — Etapa 3")

# ── Roteamento de páginas ─────────────────────────────────────────────────────
if pagina == "📋 Lançamento em Lote":
    from app.lancamento import render_lancamento
    render_lancamento()

elif pagina == "🔍 Consultar Cobranças":
    from app.consulta import render_consulta
    render_consulta()
