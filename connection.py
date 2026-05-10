# database/connection.py
# Gerencia a conexão com o banco SQLite e cria as tabelas automaticamente.

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base

# ── Caminho do banco ──────────────────────────────────────────────────────────
# O arquivo .db fica na pasta database/, ao lado deste módulo.
_DB_DIR = Path(__file__).parent
_DB_PATH = _DB_DIR / "cobrancas.db"

# ── Engine singleton ──────────────────────────────────────────────────────────
_engine = None


def get_engine():
    """Retorna (e cria, se necessário) a engine SQLAlchemy."""
    global _engine
    if _engine is None:
        _DB_DIR.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{_DB_PATH}",
            connect_args={"check_same_thread": False},  # necessário para Streamlit
            echo=False,  # True → imprime SQL no terminal (útil para debug)
        )
        # Cria todas as tabelas que ainda não existem
        Base.metadata.create_all(_engine)
    return _engine


def get_session() -> Session:
    """Retorna uma nova sessão vinculada ao banco."""
    SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return SessionLocal()


def init_db() -> None:
    """
    Inicializa o banco explicitamente.
    Chamado uma vez na inicialização do app Streamlit.
    """
    get_engine()
    print(f"[DB] Banco inicializado em: {_DB_PATH.resolve()}")
