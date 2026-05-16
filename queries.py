from datetime import date
import unicodedata

import pandas as pd
from sqlalchemy import select

from database.connection import get_session
from database.models import Cobranca, Empresa


def _texto_limpo(valor):
    if valor is None or pd.isna(valor):
        return ""
    return str(valor).strip()


def _normalizar_busca(valor):
    texto = _texto_limpo(valor).casefold()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def _valor_float(valor):
    if valor is None or pd.isna(valor) or valor == "":
        return 0.0
    return float(valor)


def _status_cobranca(cobranca, hoje=None):
    hoje = hoje or date.today()
    if cobranca.pago:
        return "Pago"
    if cobranca.data_vencimento < hoje:
        return "Vencido"
    return "Pendente"


def _cobranca_para_dict(cobranca):
    return {
        "id": cobranca.id,
        "numero_nota": cobranca.numero_nota,
        "empresa_nome": cobranca.empresa_nome,
        "data_emissao": cobranca.data_emissao,
        "data_vencimento": cobranca.data_vencimento,
        "valor": cobranca.valor,
        "pago": bool(cobranca.pago),
        "data_pagamento": cobranca.data_pagamento,
        "observacao": cobranca.observacao or "",
        "status": _status_cobranca(cobranca),
        "criado_em": cobranca.criado_em,
        "atualizado_em": cobranca.atualizado_em,
    }


def obter_ou_criar_empresa(session, nome):
    nome_limpo = _texto_limpo(nome)
    if not nome_limpo:
        raise ValueError("Informe o nome da empresa.")

    nome_normalizado = _normalizar_busca(nome_limpo)
    empresas = session.scalars(select(Empresa)).all()
    for empresa in empresas:
        if _normalizar_busca(empresa.nome) == nome_normalizado:
            return empresa

    empresa = Empresa(nome=nome_limpo)
    session.add(empresa)
    session.flush()
    return empresa


def listar_empresas():
    session = get_session()
    try:
        empresas = session.scalars(select(Empresa).order_by(Empresa.nome)).all()
        return [empresa.nome for empresa in empresas]
    finally:
        session.close()


def salvar_cobrancas_lote(linhas):
    session = get_session()
    try:
        total = 0
        for linha in linhas:
            empresa_nome = _texto_limpo(linha.get("empresa_nome"))
            numero_nota = _texto_limpo(linha.get("numero_nota"))

            if not empresa_nome or not numero_nota:
                continue

            empresa = obter_ou_criar_empresa(session, empresa_nome)
            cobranca = Cobranca(
                numero_nota=numero_nota,
                empresa_nome=empresa.nome,
                data_emissao=linha["data_emissao"],
                data_vencimento=linha["data_vencimento"],
                valor=_valor_float(linha["valor"]),
                pago=False,
                observacao=_texto_limpo(linha.get("observacao")) or None,
            )
            session.add(cobranca)
            total += 1

        session.commit()
        return total
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _filtrar_por_empresa(cobrancas, empresa):
    termo_empresa = _normalizar_busca(empresa)
    if not termo_empresa or termo_empresa == _normalizar_busca("Todas"):
        return cobrancas

    return [
        cobranca
        for cobranca in cobrancas
        if termo_empresa in _normalizar_busca(cobranca.empresa_nome)
    ]


def listar_cobrancas(
    empresa=None,
    numero_nota=None,
    status=None,
    vencimento_inicio=None,
    vencimento_fim=None,
):
    session = get_session()
    try:
        stmt = select(Cobranca)

        numero_nota = _texto_limpo(numero_nota)
        status = _texto_limpo(status)

        if numero_nota:
            stmt = stmt.where(Cobranca.numero_nota.ilike(f"%{numero_nota}%"))

        if vencimento_inicio:
            stmt = stmt.where(Cobranca.data_vencimento >= vencimento_inicio)

        if vencimento_fim:
            stmt = stmt.where(Cobranca.data_vencimento <= vencimento_fim)

        hoje = date.today()
        if status == "Pago":
            stmt = stmt.where(Cobranca.pago.is_(True))
        elif status == "Vencido":
            stmt = stmt.where(Cobranca.pago.is_(False))
            stmt = stmt.where(Cobranca.data_vencimento < hoje)
        elif status == "Pendente":
            stmt = stmt.where(Cobranca.pago.is_(False))
            stmt = stmt.where(Cobranca.data_vencimento >= hoje)

        stmt = stmt.order_by(Cobranca.data_vencimento.asc(), Cobranca.id.asc())
        cobrancas = session.scalars(stmt).all()
        cobrancas = _filtrar_por_empresa(cobrancas, empresa)
        dados = [_cobranca_para_dict(cobranca) for cobranca in cobrancas]
        return pd.DataFrame(dados)
    finally:
        session.close()


def obter_cobranca_por_id(cobranca_id):
    session = get_session()
    try:
        cobranca = session.get(Cobranca, int(cobranca_id))
        if cobranca is None:
            return None
        return _cobranca_para_dict(cobranca)
    finally:
        session.close()


def atualizar_cobranca(
    cobranca_id,
    numero_nota,
    empresa_nome,
    data_emissao,
    data_vencimento,
    valor,
    pago=False,
    data_pagamento=None,
    observacao=None,
):
    session = get_session()
    try:
        cobranca = session.get(Cobranca, int(cobranca_id))
        if cobranca is None:
            return False

        empresa_nome = _texto_limpo(empresa_nome)
        numero_nota = _texto_limpo(numero_nota)
        if not empresa_nome:
            raise ValueError("Informe o nome da empresa.")
        if not numero_nota:
            raise ValueError("Informe o número da nota.")

        empresa = obter_ou_criar_empresa(session, empresa_nome)

        cobranca.numero_nota = numero_nota
        cobranca.empresa_nome = empresa.nome
        cobranca.data_emissao = data_emissao
        cobranca.data_vencimento = data_vencimento
        cobranca.valor = _valor_float(valor)
        cobranca.pago = bool(pago)
        cobranca.data_pagamento = data_pagamento if cobranca.pago else None
        cobranca.observacao = _texto_limpo(observacao) or None

        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def marcar_cobranca_como_paga(cobranca_id, data_pagamento=None, observacao=None):
    session = get_session()
    try:
        cobranca = session.get(Cobranca, int(cobranca_id))
        if cobranca is None:
            return False

        cobranca.pago = True
        cobranca.data_pagamento = data_pagamento or date.today()

        observacao_limpa = _texto_limpo(observacao)
        if observacao_limpa:
            cobranca.observacao = observacao_limpa

        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def atualizar_observacao(cobranca_id, observacao):
    session = get_session()
    try:
        cobranca = session.get(Cobranca, int(cobranca_id))
        if cobranca is None:
            return False

        cobranca.observacao = _texto_limpo(observacao) or None
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def excluir_cobranca(cobranca_id):
    session = get_session()
    try:
        cobranca = session.get(Cobranca, int(cobranca_id))
        if cobranca is None:
            return False

        session.delete(cobranca)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
