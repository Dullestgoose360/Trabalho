from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.models import Base


DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "cobrancas.db"

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{DB_PATH}",
            connect_args={"check_same_thread": False},
            echo=False,
        )
        Base.metadata.create_all(_engine)
    return _engine


def get_session() -> Session:
    SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return SessionLocal()


def init_db() -> None:
    get_engine()
    print(f"[DB] Banco inicializado em: {DB_PATH.resolve()}")
