# 💰 Sistema de Cobranças — Interno

Sistema interno de lançamento e controle de cobranças.
Substitui planilhas manuais do Excel com uma interface rápida e centralizada.

---

## 📁 Estrutura de Pastas

```
cobrancas/
│
├── main.py                  ← Ponto de entrada (streamlit run main.py)
├── requirements.txt         ← Dependências Python
├── check_env.py             ← Verifica se o ambiente está OK
├── .gitignore
│
├── app/                     ← Páginas e componentes da interface
│   └── __init__.py
│
├── database/                ← Banco de dados e modelos
│   ├── __init__.py
│   ├── models.py            ← Definição das tabelas (SQLAlchemy ORM)
│   ├── connection.py        ← Conexão com SQLite
│   ├── init_db.py           ← Script para criar/verificar o banco
│   └── cobrancas.db         ← Gerado automaticamente (não versionar)
│
├── utils/                   ← Funções auxiliares reutilizáveis
│   └── __init__.py
│
├── exports/                 ← Arquivos Excel exportados pelo sistema
│   └── .gitkeep
│
└── imports/                 ← Arquivos Excel para importação
    └── .gitkeep
```

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- VS Code com extensão **Python** instalada

---

## 🚀 Como Executar no VS Code — Passo a Passo

### 1. Abrir o projeto

```
File → Open Folder → selecione a pasta cobrancas/
```

### 2. Criar ambiente virtual

Abra o terminal integrado do VS Code (`Ctrl + J` ou `Terminal → New Terminal`) e execute:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Verificar ambiente

```bash
python check_env.py
```

Saída esperada:
```
✅ Streamlit        1.35.0
✅ SQLAlchemy       2.0.30
✅ Pandas           2.2.2
✅ OpenPyXL         3.1.2
✅ Ambiente OK!
```

### 5. Inicializar o banco de dados

```bash
python database/init_db.py
```

Saída esperada:
```
✅ Tabelas criadas com sucesso:
   • empresas
   • cobrancas
✅ Banco pronto para uso!
```

### 6. Executar o sistema

```bash
streamlit run main.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

---

## 🗄️ Tabelas do Banco de Dados

### `empresas`
| Coluna      | Tipo     | Descrição                        |
|-------------|----------|----------------------------------|
| id          | INTEGER  | Chave primária                   |
| nome        | TEXT     | Nome da empresa (único)          |
| criado_em   | DATETIME | Data de cadastro                 |

### `cobrancas`
| Coluna           | Tipo     | Descrição                        |
|------------------|----------|----------------------------------|
| id               | INTEGER  | Chave primária                   |
| numero_nota      | TEXT     | Número da nota fiscal            |
| empresa_nome     | TEXT     | Nome da empresa                  |
| data_emissao     | DATE     | Data de emissão da nota          |
| data_vencimento  | DATE     | Data de vencimento               |
| valor            | FLOAT    | Valor da cobrança                |
| pago             | BOOLEAN  | Status de pagamento              |
| data_pagamento   | DATE     | Data em que foi pago (opcional)  |
| observacao       | TEXT     | Observações livres (opcional)    |
| criado_em        | DATETIME | Data de criação do registro      |
| atualizado_em    | DATETIME | Última atualização               |

---

## 🌐 Uso em Rede Compartilhada

Para que toda a equipe acesse o mesmo sistema:

1. Coloque a pasta `cobrancas/` em uma pasta de rede compartilhada
2. Execute `streamlit run main.py` na máquina servidora
3. Cada usuário acessa via navegador: `http://IP-DA-MAQUINA:8501`

---

## 📋 Roadmap de Etapas

- [x] **Etapa 1** — Estrutura base, banco de dados, modelagem
- [ ] **Etapa 2** — Lançamento em lote de cobranças
- [ ] **Etapa 3** — Pesquisa, filtros e marcação de pagamento
- [ ] **Etapa 4** — Exportação para Excel
- [ ] **Etapa 5** — Importação de Excel antigo
