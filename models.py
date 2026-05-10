# database/models.py
# Definição das tabelas do banco de dados via SQLAlchemy ORM

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Boolean,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Empresa(Base):
    """
    Tabela de empresas.
    Simples — apenas nome para autocomplete.
    """

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True)
    criado_em = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Empresa id={self.id} nome={self.nome!r}>"


class Cobranca(Base):
    """
    Tabela principal de cobranças.
    Cada linha representa uma nota/cobrança individual.
    """

    __tablename__ = "cobrancas"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Dados da nota
    numero_nota = Column(String(100), nullable=False)
    empresa_nome = Column(String(255), nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)

    # Status
    pago = Column(Boolean, default=False, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    observacao = Column(Text, nullable=True)

    # Auditoria
    criado_em = Column(DateTime, default=func.now())
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (
            f"<Cobranca id={self.id} nota={self.numero_nota!r} "
            f"empresa={self.empresa_nome!r} valor={self.valor:.2f} pago={self.pago}>"
        )
