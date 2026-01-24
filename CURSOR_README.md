# LinkedIn Optimizer - Quick Start no Cursor

Este README é específico para trabalhar com o projeto no **Cursor IDE**.

---

## 🎯 Setup Rápido

### 1. Abrir Projeto no Cursor

```bash
# No terminal do Cursor
cd caminho/para/linkedin-optimizer
code .  # ou abrir via File > Open Folder
```

### 2. Instalar Dependências

O Cursor vai detectar automaticamente o `requirements.txt`.

**Opção A: Terminal Integrado**
```bash
pip install -r requirements.txt
```

**Opção B: Cursor Command**
- Cmd/Ctrl + Shift + P
- Digite: "Python: Create Environment"
- Selecione `requirements.txt`

### 3. Verificar Instalação

```bash
python src/cli.py info
```

Se vires o banner do LinkedIn Optimizer, está tudo OK! ✅

---

## 🚀 Usar no Cursor

### Comando Principal

```bash
python src/cli.py analyze-perfil data/inputs/perfil.pdf
```

### Com Composer/Chat do Cursor

Podes usar o chat do Cursor para:

**1. Analisar código:**
```
@README.md explica-me a arquitetura do projeto
```

**2. Fazer modificações:**
```
@src/core/analyzer.py adiciona um novo critério para avaliar certificações
```

**3. Gerar código:**
```
@config/prompts/perfil.yaml cria um novo prompt para análise de educação
```

**4. Debug:**
```
@src/cli.py porque é que o comando analyze-perfil falha com este PDF?
```

### Usar .cursorrules

O ficheiro `.cursorrules` contém instruções para o Cursor sobre como trabalhar neste projeto.

**O Cursor vai automaticamente:**
- Seguir convenções de naming
- Usar os padrões de documentação corretos
- Sugerir código alinhado com a arquitetura

---

## 📁 Estrutura para Cursor

### Ficheiros Principais

```
linkedin-optimizer/
├── .cursorrules          ← Regras do Cursor (lê isto!)
├── README.md             ← Visão geral
├── requirements.txt      ← Dependências
├── src/
│   ├── cli.py           ← CLI principal (entry point)
│   ├── core/
│   │   ├── pdf_parser.py   ← Parser de PDFs
│   │   └── analyzer.py     ← Motor de análise
│   └── modules/         ← Módulos futuros
├── config/
│   ├── checklists/      ← Critérios de avaliação
│   └── prompts/         ← Templates de análise
├── data/
│   ├── inputs/          ← PDFs para analisar
│   └── outputs/         ← Resultados
└── docs/
    └── GUIA_USO.md      ← Documentação completa
```

### Atalhos Úteis

**Terminal Integrado:** `` Ctrl + ` ``  
**Command Palette:** `Cmd/Ctrl + Shift + P`  
**File Search:** `Cmd/Ctrl + P`  
**Symbol Search:** `Cmd/Ctrl + T`

---

## 🔧 Desenvolvimento no Cursor

### Criar Novo Módulo

```bash
# 1. Cria ficheiro em src/modules/
touch src/modules/novo_modulo.py

# 2. Usa o Cursor para gerar boilerplate
# No chat: "@.cursorrules cria estrutura para novo_modulo.py"
```

### Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Teste específico
pytest tests/test_basic.py::TestPDFParser -v

# Com coverage
pytest tests/ --cov=src --cov-report=html
```

### Debug no Cursor

**Opção 1: Python Debugger**
1. Coloca breakpoint (clica à esquerda do nº da linha)
2. F5 → Seleciona "Python File"
3. Debug interativo

**Opção 2: Print Debugging**
```python
from rich import print as rprint
rprint("[red]Debug:[/red]", variavel)
```

---

## 💡 Workflows Comuns

### 1. Adicionar Novo Critério

```
Chat: "@config/checklists/360brew_checklist.yaml adiciona critério 
para avaliar qualidade das certificações"

→ Cursor gera YAML
→ Review e aceita
→ Chat: "@src/core/analyzer.py implementa avaliador para novo critério"
```

### 2. Corrigir Bug

```
Chat: "@src/core/pdf_parser.py o parser não consegue extrair 
experiências de PDFs em inglês. Como corrigir?"

→ Cursor sugere fix
→ Testa: python src/cli.py analyze-perfil test.pdf -v
→ Commit se OK
```

### 3. Adicionar Funcionalidade

```
Chat: "Quero adicionar export para Excel. Como implementar?"

→ Cursor cria plano
→ Gera código em src/utils/excel_exporter.py
→ Atualiza cli.py com novo comando
→ Testa: python src/cli.py analyze-perfil test.pdf -o results.xlsx
```

---

## 🎓 Aprender Mais

### Documentação do Projeto

- **[README.md](README.md)** - Arquitetura completa
- **[GUIA_USO.md](docs/GUIA_USO.md)** - Como usar
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões

### Documentação 360Brew

Os prompts e checklists são baseados em:
- `config/checklists/360brew_checklist.yaml`
- Ficheiros do projeto: `LinkedIn_360Brew_Guia_Completo.pdf`

### Cursor Features

Explora no chat:
```
Como usar o Cursor para [tarefa específica]?
```

---

## ⚡ Atalhos do Projeto

### Análise Rápida

```bash
# Alias útil (adicionar ao .bashrc/.zshrc)
alias lkd-analyze='python src/cli.py analyze-perfil'

# Usar
lkd-analyze perfil.pdf -o relatorio.json
```

### Watch Mode (Dev)

```bash
# Auto-reload ao editar
pip install watchdog
watchmedo auto-restart --pattern="*.py" --recursive python src/cli.py info
```

---

## 🐛 Troubleshooting no Cursor

### "Module not found"

```bash
# Verifica Python path
which python
python --version

# Reinstala dependências
pip install -r requirements.txt --force-reinstall
```

### "Import errors"

- Verifica que estás no root do projeto
- Cursor pode estar usando Python errado
  - Cmd+Shift+P → "Python: Select Interpreter"
  - Escolhe o da venv se criaste uma

### "Cursor não sugere código"

- Verifica que `.cursorrules` existe
- Restart do Cursor (Cmd+Q, reabrir)
- Chat: "Estás a seguir as regras em .cursorrules?"

---

## 📞 Suporte

**Issues com o código:**
- Usa o chat do Cursor com `@ficheiro.py`
- Consulta `docs/GUIA_USO.md`

**Issues com o Cursor:**
- [Cursor Documentation](https://docs.cursor.com)
- [Cursor Discord](https://discord.gg/cursor)

---

**Bom desenvolvimento! 🚀**

*Última atualização: Janeiro 2025*
