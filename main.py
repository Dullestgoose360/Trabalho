import streamlit as st

from database.connection import init_db


st.set_page_config(
    page_title="Sistema de Cobranças",
    page_icon="$",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def startup():
    init_db()
    return True


startup()


with st.sidebar:
    st.title("Cobranças")
    st.markdown("---")

    pagina = st.radio(
        label="Navegação",
        options=[
            "Lançamento",
            "Consultar Cobranças",
            "Gerenciamento Operacional",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("v0.4 - Etapa 4")


if pagina == "Lançamento":
    from app.lancamento import render_lancamento

    render_lancamento()

elif pagina == "Consultar Cobranças":
    from app.consulta import render_consulta

    render_consulta()

elif pagina == "Gerenciamento Operacional":
    from app.gerenciamento import render_gerenciamento

    render_gerenciamento()
