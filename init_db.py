import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_engine, init_db
from database.models import Base


def main():
    print("=" * 50)
    print("  Inicializando banco de dados...")
    print("=" * 50)

    init_db()
    get_engine()

    print("\nTabelas verificadas:")
    for tabela in Base.metadata.tables.keys():
        print(f" - {tabela}")

    print("\nBanco pronto para uso.")
    print("=" * 50)


if __name__ == "__main__":
    main()
