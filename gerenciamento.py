from datetime import date

import streamlit as st

from database.queries import (
    atualizar_cobranca,
    atualizar_observacao,
    excluir_cobranca,
    listar_cobrancas,
    listar_empresas,
    marcar_cobranca_como_paga,
    obter_cobranca_por_id,
)


def _opcoes_cobrancas(df):
    opcoes = {}
    for _, linha in df.iterrows():
        rotulo = (
            f"#{linha['id']} | {linha['numero_nota']} | "
            f"{linha['empresa_nome']} | {linha['status']} | R$ {linha['valor']:.2f}"
        )
        opcoes[rotulo] = int(linha["id"])
    return opcoes


def _carregar_lista():
    empresas = ["Todas"] + listar_empresas()
    col1, col2, col3 = st.columns(3)
    empresa = col1.selectbox("Empresa", empresas)
    numero_nota = col2.text_input("Numero da nota")
    status = col3.selectbox("Status", ["Todos", "Pendente", "Vencido", "Pago"])

    return listar_cobrancas(
        empresa=empresa,
        numero_nota=numero_nota,
        status=None if status == "Todos" else status,
    )


def _aba_marcar_pago(cobranca):
    st.subheader("Marcar como paga")

    if cobranca["pago"]:
        st.info("Esta cobranca ja esta marcada como paga.")

    with st.form("form_marcar_pago"):
        data_pagamento = st.date_input(
            "Data de pagamento",
            value=cobranca["data_pagamento"] or date.today(),
        )
        observacao = st.text_area(
            "Observacao",
            value=cobranca["observacao"],
            height=120,
        )
        enviar = st.form_submit_button("Marcar como paga", type="primary")

    if enviar:
        marcar_cobranca_como_paga(
            cobranca["id"],
            data_pagamento=data_pagamento,
            observacao=observacao,
        )
        st.success("Cobranca marcada como paga.")
        st.rerun()


def _aba_editar(cobranca):
    st.subheader("Editar cobranca")

    with st.form("form_editar_cobranca"):
        col1, col2 = st.columns(2)
        numero_nota = col1.text_input("Numero da nota", value=cobranca["numero_nota"])
        empresa_nome = col2.text_input("Empresa", value=cobranca["empresa_nome"])

        col3, col4, col5 = st.columns(3)
        data_emissao = col3.date_input("Data de emissao", value=cobranca["data_emissao"])
        data_vencimento = col4.date_input(
            "Data de vencimento",
            value=cobranca["data_vencimento"],
        )
        valor = col5.number_input(
            "Valor",
            min_value=0.0,
            step=0.01,
            value=float(cobranca["valor"]),
            format="%.2f",
        )

        pago = st.checkbox("Pago", value=bool(cobranca["pago"]))
        data_pagamento = None
        if pago:
            data_pagamento = st.date_input(
                "Data de pagamento",
                value=cobranca["data_pagamento"] or date.today(),
            )

        observacao = st.text_area(
            "Observacao",
            value=cobranca["observacao"],
            height=120,
        )

        enviar = st.form_submit_button("Salvar alteracoes", type="primary")

    if enviar:
        if not numero_nota.strip():
            st.error("Informe o numero da nota.")
            return
        if not empresa_nome.strip():
            st.error("Informe a empresa.")
            return
        if valor <= 0:
            st.error("Informe um valor maior que zero.")
            return

        atualizar_cobranca(
            cobranca_id=cobranca["id"],
            numero_nota=numero_nota,
            empresa_nome=empresa_nome,
            data_emissao=data_emissao,
            data_vencimento=data_vencimento,
            valor=valor,
            pago=pago,
            data_pagamento=data_pagamento,
            observacao=observacao,
        )
        st.success("Cobranca atualizada.")
        st.rerun()


def _aba_observacao(cobranca):
    st.subheader("Observacao")

    with st.form("form_observacao"):
        observacao = st.text_area(
            "Observacao",
            value=cobranca["observacao"],
            height=180,
        )
        enviar = st.form_submit_button("Salvar observacao", type="primary")

    if enviar:
        atualizar_observacao(cobranca["id"], observacao)
        st.success("Observacao atualizada.")
        st.rerun()


def _aba_excluir(cobranca):
    st.subheader("Excluir cobranca")
    st.warning("Esta acao remove a cobranca salva do banco.")

    confirmar = st.checkbox(
        f"Confirmo a exclusao da cobranca #{cobranca['id']} - nota {cobranca['numero_nota']}"
    )

    if st.button("Excluir definitivamente", type="primary", disabled=not confirmar):
        excluir_cobranca(cobranca["id"])
        st.success("Cobranca excluida.")
        st.rerun()


def render_gerenciamento():
    st.title("Gerenciamento Operacional")
    st.caption("Edite, exclua, marque como paga e registre observacoes nas cobrancas.")

    with st.expander("Localizar cobranca", expanded=True):
        df = _carregar_lista()

    if df.empty:
        st.info("Nenhuma cobranca encontrada.")
        return

    opcoes = _opcoes_cobrancas(df)
    selecionada = st.selectbox("Cobranca", list(opcoes.keys()))
    cobranca_id = opcoes[selecionada]
    cobranca = obter_cobranca_por_id(cobranca_id)

    if cobranca is None:
        st.error("Cobranca nao encontrada. Atualize a tela e tente novamente.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Status", cobranca["status"])
    col2.metric("Valor", f"R$ {cobranca['valor']:,.2f}")
    col3.metric("Vencimento", cobranca["data_vencimento"].strftime("%d/%m/%Y"))
    pagamento = cobranca["data_pagamento"]
    col4.metric("Pagamento", pagamento.strftime("%d/%m/%Y") if pagamento else "-")

    st.markdown("---")
    aba_pago, aba_editar, aba_observacao, aba_excluir = st.tabs(
        ["Marcar como paga", "Editar", "Observacao", "Excluir"]
    )

    with aba_pago:
        _aba_marcar_pago(cobranca)

    with aba_editar:
        _aba_editar(cobranca)

    with aba_observacao:
        _aba_observacao(cobranca)

    with aba_excluir:
        _aba_excluir(cobranca)
