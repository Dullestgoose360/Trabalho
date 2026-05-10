# main.py
# Ponto de entrada do sistema.
# Execute com: streamlit run main.py

import streamlit as st
from database.init_db import init_db

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

# ── Interface provisória (Etapa 1) ────────────────────────────────────────────
st.title("💰 Sistema de Cobranças")
st.markdown("---")

st.success("✅ Banco de dados inicializado com sucesso!")

st.info(
    "**Etapa 1 concluída** — estrutura base, banco e modelagem prontos.\n\n"
    "A interface de lançamento de cobranças será implementada na **Etapa 2**."
)

# Diagnóstico rápido
with st.expander("🔧 Informações do sistema"):
    from database.connection import _DB_PATH
    from pathlib import Path

    st.write(f"**Banco de dados:** `{Path(_DB_PATH).resolve()}`")
    st.write(f"**Python path OK:** ✅")
    st.write(f"**SQLAlchemy OK:** ✅")
    st.write(f"**Streamlit OK:** ✅")
