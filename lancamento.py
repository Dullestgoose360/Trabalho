from datetime import date

import pandas as pd
import streamlit as st

from database.queries import salvar_cobrancas_lote


COLUNAS = ["numero_nota", "empresa_nome", "data_emissao", "valor", "observacao"]
OPCOES_LINHAS = [1, 2, 3, 4, 5, 10, 15, 20, 30]
TABELA_KEY = "lancamento_tabela"


def _valor_numerico(valor):
    if pd.isna(valor) or valor == "":
        return 0.0
    return float(valor)


def _texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def _data(valor):
    if hasattr(valor, "date") and not isinstance(valor, date):
        return valor.date()
    return valor


def _nova_linha():
    return {
        "numero_nota": "",
        "empresa_nome": "",
        "data_emissao": None,
        "valor": 0.0,
        "observacao": "",
    }


def _criar_tabela_vazia():
    return pd.DataFrame(columns=COLUNAS)


def _criar_linhas(quantidade):
    return pd.DataFrame([_nova_linha() for _ in range(quantidade)], columns=COLUNAS)


def _garantir_tabela():
    if TABELA_KEY not in st.session_state:
        st.session_state[TABELA_KEY] = _criar_tabela_vazia()


def _adicionar_linhas(tabela, quantidade):
    novas_linhas = _criar_linhas(quantidade)
    if tabela.empty:
        st.session_state[TABELA_KEY] = novas_linhas
        return

    st.session_state[TABELA_KEY] = pd.concat([tabela, novas_linhas], ignore_index=True)


def _preparar_linhas(tabela, data_vencimento):
    linhas = []
    erros = []

    for indice, linha in tabela.iterrows():
        numero_nota = _texto(linha.get("numero_nota", ""))
        empresa_nome = _texto(linha.get("empresa_nome", ""))
        valor = _valor_numerico(linha.get("valor", 0))
        data_emissao = linha.get("data_emissao")

        linha_vazia = (
            not numero_nota
            and not empresa_nome
            and valor == 0
            and pd.isna(data_emissao)
        )
        if linha_vazia:
            continue

        if not numero_nota:
            erros.append(f"Linha {indice + 1}: informe o número da nota.")
        if not empresa_nome:
            erros.append(f"Linha {indice + 1}: informe a empresa.")
        if valor <= 0:
            erros.append(f"Linha {indice + 1}: informe um valor maior que zero.")
        if pd.isna(data_emissao):
            erros.append(f"Linha {indice + 1}: informe a data de emissão.")

        linhas.append(
            {
                "numero_nota": numero_nota,
                "empresa_nome": empresa_nome,
                "data_emissao": _data(data_emissao),
                "data_vencimento": data_vencimento,
                "valor": valor,
                "observacao": _texto(linha.get("observacao", "")),
            }
        )

    return linhas, erros


def render_lancamento():
    _garantir_tabela()

    st.title("Lançamento")
    st.caption("Cadastre cobranças com a mesma data de vencimento.")

    data_vencimento = st.date_input(
        "Data de vencimento",
        value=date.today(),
        format="DD/MM/YYYY",
    )

    tabela = st.data_editor(
        st.session_state[TABELA_KEY],
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        key="editor_lancamento",
        column_config={
            "numero_nota": st.column_config.TextColumn("Número da nota"),
            "empresa_nome": st.column_config.TextColumn("Empresa"),
            "data_emissao": st.column_config.DateColumn(
                "Data de emissão",
                format="DD/MM/YYYY",
            ),
            "valor": st.column_config.NumberColumn(
                "Valor",
                min_value=0.0,
                step=0.01,
                format="R$ %.2f",
            ),
            "observacao": st.column_config.TextColumn("Observação"),
        },
    )
    st.session_state[TABELA_KEY] = tabela

    col_qtd, col_add, col_salvar = st.columns([1, 1, 2])

    quantidade_linhas = col_qtd.selectbox(
        "Quantidade de linhas",
        options=OPCOES_LINHAS,
        index=0,
    )

    if col_add.button("Adicionar linhas", use_container_width=True):
        _adicionar_linhas(tabela, quantidade_linhas)
        st.rerun()

    salvar = col_salvar.button(
        "Salvar lançamentos",
        type="primary",
        use_container_width=True,
    )

    if salvar:
        linhas, erros = _preparar_linhas(tabela, data_vencimento)

        if erros:
            for erro in erros:
                st.error(erro)
            return

        if not linhas:
            st.warning("Adicione e preencha pelo menos uma cobrança para salvar.")
            return

        total = salvar_cobrancas_lote(linhas)
        st.success(f"{total} cobrança(s) salva(s) com sucesso.")
        st.session_state[TABELA_KEY] = _criar_tabela_vazia()
        st.rerun()
