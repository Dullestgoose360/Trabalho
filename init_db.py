# database/init_db.py
# Execute este arquivo UMA VEZ para criar/verificar o banco.
# Uso: python database/init_db.py

import sys
from pathlib import Path

# Garante que a raiz do projeto está no sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import init_db, get_engine
from database.models import Base


def main():
    print("=" * 50)
    print("  Inicializando banco de dados...")
    print("=" * 50)

    init_db()

    # Lista as tabelas criadas
    engine = get_engine()
    tabelas = Base.metadata.tables.keys()
    print(f"\n✅ Tabelas criadas com sucesso:")
    for tabela in tabelas:
        print(f"   • {tabela}")

    print("\n✅ Banco pronto para uso!")
    print("=" * 50)


if __name__ == "__main__":
    main()
