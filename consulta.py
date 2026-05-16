import streamlit as st

from database.queries import listar_cobrancas


def _formatar_tabela(df):
    if df.empty:
        return df

    tabela = df.copy()
    tabela = tabela[
        [
            "id",
            "status",
            "numero_nota",
            "empresa_nome",
            "data_emissao",
            "data_vencimento",
            "valor",
            "data_pagamento",
            "observacao",
        ]
    ]
    tabela = tabela.rename(
        columns={
            "id": "ID",
            "status": "Status",
            "numero_nota": "Nota",
            "empresa_nome": "Empresa",
            "data_emissao": "Emissão",
            "data_vencimento": "Vencimento",
            "valor": "Valor",
            "data_pagamento": "Pagamento",
            "observacao": "Observação",
        }
    )
    return tabela


def _totalizadores(df):
    total = len(df)
    valor_total = float(df["valor"].sum()) if not df.empty else 0.0
    vencidas = int((df["status"] == "Vencido").sum()) if not df.empty else 0
    pagas = int((df["status"] == "Pago").sum()) if not df.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros", total)
    col2.metric("Valor total", f"R$ {valor_total:,.2f}")
    col3.metric("Vencidas", vencidas)
    col4.metric("Pagas", pagas)


def render_consulta():
    st.title("Consultar Cobranças")
    st.caption("Consulte cobranças salvas e filtre por empresa, nota, status ou vencimento.")

    with st.expander("Filtros", expanded=True):
        col1, col2, col3 = st.columns(3)
        empresa = col1.text_input("Empresa")
        numero_nota = col2.text_input("Número da nota")
        status = col3.selectbox("Status", ["Todos", "Pendente", "Vencido", "Pago"])

        col4, col5 = st.columns(2)
        usar_periodo = col4.checkbox("Filtrar por vencimento")
        vencimento_inicio = None
        vencimento_fim = None

        if usar_periodo:
            vencimento_inicio = col4.date_input(
                "Vencimento inicial",
                format="DD/MM/YYYY",
            )
            vencimento_fim = col5.date_input(
                "Vencimento final",
                format="DD/MM/YYYY",
            )

    df = listar_cobrancas(
        empresa=empresa,
        numero_nota=numero_nota,
        status=None if status == "Todos" else status,
        vencimento_inicio=vencimento_inicio,
        vencimento_fim=vencimento_fim,
    )

    _totalizadores(df)

    st.markdown("---")
    if df.empty:
        st.info("Nenhuma cobrança encontrada para os filtros informados.")
        return

    tabela = _formatar_tabela(df)
    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "Emissão": st.column_config.DateColumn("Emissão", format="DD/MM/YYYY"),
            "Vencimento": st.column_config.DateColumn("Vencimento", format="DD/MM/YYYY"),
            "Pagamento": st.column_config.DateColumn("Pagamento", format="DD/MM/YYYY"),
        },
    )

    csv = tabela.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar CSV filtrado",
        data=csv,
        file_name="cobrancas_filtradas.csv",
        mime="text/csv",
    )
