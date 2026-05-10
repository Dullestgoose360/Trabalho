# check_env.py
# Verifica se todas as dependências estão instaladas corretamente.
# Uso: python check_env.py

import sys

print("=" * 50)
print("  Verificando ambiente...")
print("=" * 50)
print(f"\nPython: {sys.version}")

checks = [
    ("streamlit", "Streamlit"),
    ("sqlalchemy", "SQLAlchemy"),
    ("pandas", "Pandas"),
    ("openpyxl", "OpenPyXL"),
]

all_ok = True
for module, name in checks:
    try:
        mod = __import__(module)
        version = getattr(mod, "__version__", "instalado")
        print(f"  ✅ {name:<15} {version}")
    except ImportError:
        print(f"  ❌ {name:<15} NÃO INSTALADO")
        all_ok = False

print()
if all_ok:
    print("✅ Ambiente OK! Pode executar: streamlit run main.py")
else:
    print("❌ Execute: pip install -r requirements.txt")
print("=" * 50)
