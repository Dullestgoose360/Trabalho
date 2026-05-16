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
        print(f"  OK   {name:<15} {version}")
    except ImportError:
        print(f"  ERRO {name:<15} NAO INSTALADO")
        all_ok = False

print()
if all_ok:
    print("Ambiente OK. Pode executar: streamlit run main.py")
else:
    print("Execute: pip install -r requirements.txt")
print("=" * 50)
