````md
# 💰 Sistema Interno de Cobranças

Sistema interno desenvolvido para substituir o controle manual em Excel utilizado pela equipe de cobrança.

O projeto foi construído com foco em:
- velocidade operacional;
- simplicidade;
- lançamento em lote;
- redução de erros humanos;
- facilidade de manutenção;
- operação em rede compartilhada.

---

# 🚀 Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python | Backend principal |
| Streamlit | Interface web |
| SQLite | Banco de dados local |
| SQLAlchemy | ORM e modelagem |
| Pandas | Manipulação de dados |
| OpenPyXL | Integração futura com Excel |

---

# 📁 Estrutura Atual do Projeto

```txt
Documentos cobrancas/
│
├── app/
│   ├── __init__.py
│   ├── lancamento.py
│   └── consulta.py
│
├── database/
│   ├── __init__.py
│   ├── cobrancas.db
│   ├── connection.py
│   ├── init_db.py
│   ├── models.py
│   └── queries.py
│
├── exports/
├── imports/
├── utils/
│
├── main.py
├── requirements.txt
├── check_env.py
├── README.md
└── .gitignore
````

---

# ⚙️ Pré-requisitos

* Python 3.12
* VS Code
* Extensão Python do VS Code

> ⚠️ Python 3.13 pode causar incompatibilidades com Pandas no Windows.

---

# 🚀 Como Executar

## 1. Abrir projeto no VS Code

```txt
Arquivo → Abrir Pasta
```

Selecione:

```txt
Documentos cobrancas
```

---

## 2. Criar ambiente virtual

### Windows

```bash
python -m venv .venv
```

---

## 3. Ativar ambiente virtual

### PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

### CMD

```cmd
.venv\Scripts\activate.bat
```

---

## 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 5. Verificar ambiente

```bash
python check_env.py
```

---

## 6. Inicializar banco

```bash
python database/init_db.py
```

---

## 7. Executar sistema

```bash
streamlit run main.py
```

---

# 🌐 Acesso

Após executar:

```txt
http://localhost:8501
```

---

# 📋 Funcionalidades Implementadas

# ✅ Etapa 1 — Estrutura Base

* Banco SQLite
* Modelagem ORM
* Conexão SQLAlchemy
* Inicialização automática
* Estrutura modular
* Navegação inicial

---

# ✅ Etapa 2 — Lançamento em Lote

## Funcionalidades

* Data de vencimento única
* Tabela editável
* Múltiplas cobranças simultâneas
* Salvamento em lote
* Persistência no SQLite
* Empresas criadas automaticamente
* Estrutura otimizada para velocidade operacional

## Campos

* Número da nota
* Empresa
* Data de emissão
* Valor
* Vencimento

---

# ✅ Etapa 3 — Consulta de Cobranças

## Funcionalidades

* Consulta completa de cobranças
* Pesquisa rápida
* Filtros avançados
* Status automático
* Totalizadores
* Destaque visual
* Atalhos rápidos

## Filtros

* Empresa
* Número da nota
* Status
* Vencimento inicial
* Vencimento final

## Status automáticos

* 🟡 Pendente
* 🔴 Vencido
* ✅ Pago

---

# 🧠 Decisões Arquiteturais

## Streamlit + SQLite

Escolhido por:

* simplicidade;
* rapidez de desenvolvimento;
* facilidade de manutenção;
* ótimo desempenho local;
* ideal para pequenas equipes.

---

# Queries Separadas da Interface

Toda lógica SQL fica em:

```txt
database/queries.py
```

A interface nunca acessa o banco diretamente.

Isso melhora:

* organização;
* manutenção;
* escalabilidade.

---

# Status Derivado

O sistema NÃO salva "Vencido" no banco.

O status é calculado automaticamente:

```txt
Pago = pago == True
Vencido = pago == False && vencimento < hoje
Pendente = pago == False && vencimento >= hoje
```

---

# 🎯 Objetivo do Projeto

O foco do sistema NÃO é ser um ERP completo.

O objetivo é:

* acelerar lançamento de cobranças;
* reduzir dependência do Excel;
* melhorar produtividade da equipe;
* reduzir erros humanos;
* simplificar operação diária.

---

# 📌 Próximas Etapas

## 🔜 Etapa 4 — Gerenciamento Operacional

Planejado:

* excluir cobrança;
* editar cobrança;
* marcar como pago;
* adicionar observações.

---

## 🔜 Etapa 5 — Excel

Planejado:

* exportar Excel;
* importar planilhas antigas;
* compatibilidade com operação atual.

---

## 🔜 Etapa 6 — Inteligência Operacional

Planejado:

* OCR de notas;
* leitura automática de PDF;
* IA para preenchimento automático;
* automações futuras.

---

# ⚠️ Observações Importantes

* Projeto focado em uso interno.
* Sistema otimizado para velocidade operacional.
* Arquitetura mantida simples propositalmente.
* O Excel continuará sendo compatível futuramente para exportação/importação.

---

# 👨‍💻 Desenvolvimento

Projeto desenvolvido utilizando:

* VS Code
* Claude Sonnet 4.6
* Streamlit
* SQLAlchemy
* SQLite

```
```
