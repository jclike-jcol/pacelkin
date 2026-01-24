# 🚀 Como Importar para o Cursor IDE

**Data:** 24 Janeiro 2025  
**Projeto:** LinkedIn Optimizer Assistant v1.0

---

## 📥 Passo a Passo

### 1. Descarregar o Projeto

O projeto completo está em: `linkedin-optimizer/`

**Opções de download:**

**A) Zip completo** (recomendado)
```bash
# Compactar pasta
cd /caminho/onde/está
zip -r linkedin-optimizer.zip linkedin-optimizer/

# Ou usar interface gráfica para compactar
```

**B) Clonar estrutura**
```bash
# Copiar pasta completa para local desejado
cp -r linkedin-optimizer ~/Projetos/
```

---

### 2. Abrir no Cursor

#### Opção A: Via Interface
1. Abre Cursor IDE
2. `File` → `Open Folder...`
3. Navega até `linkedin-optimizer/`
4. Seleciona a pasta
5. Clica `Open`

#### Opção B: Via Terminal
```bash
cd linkedin-optimizer
cursor .
# ou
code .  # se Cursor está aliasado como 'code'
```

---

### 3. Setup Inicial no Cursor

Quando o Cursor abrir o projeto:

#### 3.1 Python Interpreter
1. `Cmd/Ctrl + Shift + P`
2. Digita: "Python: Select Interpreter"
3. Escolhe Python 3.11+ (sistema ou cria venv)

#### 3.2 Terminal Integrado
```bash
# Abre terminal no Cursor
Ctrl + `  (backtick)

# Verifica Python
python --version  # Deve ser 3.11+

# Instala dependências
pip install -r requirements.txt
```

**OU usa o script:**
```bash
chmod +x setup.sh
./setup.sh
```

#### 3.3 Verifica Instalação
```bash
python src/cli.py info
```

Deves ver:
```
🚀 LinkedIn Optimizer Assistant
📦 Módulos disponíveis:
  ✓ Análise de Perfil...
```

✅ Se vires isto, está pronto!

---

### 4. Configurar Cursor para o Projeto

#### 4.1 Verificar .cursorrules
O ficheiro `.cursorrules` deve estar na raiz:
```
linkedin-optimizer/
├── .cursorrules  ← Este ficheiro
├── README.md
└── ...
```

O Cursor vai automaticamente:
- Seguir convenções do projeto
- Sugerir código alinhado
- Usar padrões corretos

#### 4.2 Testar AI do Cursor
No chat do Cursor, testa:
```
@README.md qual é a arquitetura deste projeto?
```

O Cursor deve responder com base no README.

---

### 5. Primeiro Uso

#### 5.1 Prepara um PDF
1. Vai ao LinkedIn
2. Teu perfil → Mais → Guardar como PDF
3. Guarda em `data/inputs/perfil.pdf`

#### 5.2 Primeira Análise
No terminal do Cursor:
```bash
python src/cli.py analyze-perfil data/inputs/perfil.pdf
```

Deves ver:
```
🚀 LinkedIn Optimizer Assistant
📄 A parsear PDF...
✓ PDF parseado

✓ Perfil extraído: [Teu Nome]
  📍 [Localização]
  💼 X experiências
  🎯 Y competências

🔍 A analisar perfil...
✓ Análise completa

📊 Score Geral: XX/100 (XX.X%)
[tabela com critérios]
...
```

✅ Funcionou! Podes agora explorar o sistema.

---

## 🎓 Workflows no Cursor

### Explorar o Código
```
# No chat:
@src/core/analyzer.py explica como funciona o scoring

@config/checklists/360brew_checklist.yaml 
lista todos os critérios implementados
```

### Modificar Código
```
# No chat:
@src/core/analyzer.py adiciona logging mais detalhado 
na função _avaliar_headline_pilares

# Cursor gera código
# Review, aceita ou ajusta
# Testa: python src/cli.py analyze-perfil test.pdf -v
```

### Adicionar Funcionalidade
```
# No chat:
Quero adicionar export para Excel. Como implementar?

# Cursor vai:
1. Criar src/utils/excel_exporter.py
2. Atualizar cli.py com comando
3. Sugerir testes
```

### Debug
```
# No chat com código selecionado:
Porque é que esta função não está a extrair 
o headline corretamente?

# Cursor analisa e sugere fix
```

---

## 📁 Estrutura no Cursor

Quando abrires, verás:

```
EXPLORER (sidebar esquerda):
├── 📄 CURSOR_README.md       ← Lê isto primeiro!
├── 📄 README.md              ← Arquitetura
├── 📄 PROJETO_ENTREGUE.md    ← Este documento
├── 📄 .cursorrules           ← Guidelines AI
├── 📁 config/
│   ├── 📁 checklists/
│   │   └── 360brew_checklist.yaml
│   └── 📁 prompts/
│       └── perfil.yaml
├── 📁 src/
│   ├── cli.py                ← Entry point
│   └── 📁 core/
│       ├── pdf_parser.py
│       └── analyzer.py
├── 📁 data/
│   ├── 📁 inputs/     ← Coloca PDFs aqui
│   └── 📁 outputs/    ← Relatórios aqui
├── 📁 docs/
│   └── GUIA_USO.md
└── 📁 tests/
```

---

## 🔧 Configurações Opcionais

### Extensões Recomendadas

Se o Cursor sugerir instalar extensões:

**Essenciais:**
- Python (Microsoft) - Já deve estar
- Pylance - IntelliSense melhorado

**Opcionais:**
- YAML - Syntax highlighting
- Markdown All in One - Preview MD
- GitLens - Git integrado

### Settings.json do Cursor

Opcional, para melhores sugestões:

```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

Para adicionar:
1. `Cmd/Ctrl + ,` (Settings)
2. Clica no ícone `{}` (Open Settings JSON)
3. Adiciona as configurações

---

## 🐛 Troubleshooting

### "Module not found" ao executar
```bash
# Verifica que estás na raiz do projeto
pwd  # Deve mostrar .../linkedin-optimizer

# Reinstala
pip install -r requirements.txt
```

### Cursor não reconhece .cursorrules
```bash
# Restart do Cursor
Cmd+Q (Mac) / Alt+F4 (Windows)
# Reabre projeto
```

### Python Interpreter errado
```
Cmd/Ctrl + Shift + P
→ Python: Select Interpreter
→ Escolhe Python 3.11+
```

### Import errors
```python
# Se vires erros como:
# ImportError: No module named 'src'

# Solução: adiciona ao início dos scripts
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

---

## 🎯 Quick Reference

### Comandos Frequentes
```bash
# Análise básica
python src/cli.py analyze-perfil data/inputs/perfil.pdf

# Com output JSON
python src/cli.py analyze-perfil perfil.pdf -o results.json

# Modo verbose (debug)
python src/cli.py analyze-perfil perfil.pdf -v

# Info do sistema
python src/cli.py info

# Executar testes
pytest tests/ -v
```

### Atalhos Cursor
- **Terminal:** `` Ctrl + ` ``
- **Command Palette:** `Cmd/Ctrl + Shift + P`
- **Search Files:** `Cmd/Ctrl + P`
- **AI Chat:** `Cmd/Ctrl + L`
- **Composer:** `Cmd/Ctrl + I`

### Usar AI do Cursor
```
# Referencia ficheiros
@ficheiro.py pergunta sobre este código

# Múltiplos ficheiros
@src/core/pdf_parser.py @tests/test_basic.py
cria teste para nova função

# Codebase completo
@Codebase como adicionar export Excel?
```

---

## ✅ Checklist Final

Antes de começar a usar:

- [ ] Cursor aberto no projeto
- [ ] Python 3.11+ selecionado
- [ ] `pip install -r requirements.txt` executado
- [ ] `python src/cli.py info` funciona
- [ ] PDF de teste em `data/inputs/`
- [ ] Primeira análise executada com sucesso
- [ ] Lido `CURSOR_README.md` e `GUIA_USO.md`

---

## 📚 Próximos Passos

1. **Familiariza-te:**
   - Roda análise no teu perfil
   - Explora relatório gerado
   - Lê código em `src/core/`

2. **Experimenta:**
   - Modifica critérios em `config/checklists/360brew_checklist.yaml`
   - Re-analisa e compara resultados
   - Usa AI do Cursor para perguntas

3. **Desenvolve:**
   - Escolhe próximo módulo (ver `CHANGELOG.md`)
   - Usa `.cursorrules` como guia
   - Desenvolve iterativamente

---

## 🆘 Suporte

**Problemas com setup:**
- Consulta `CURSOR_README.md`
- Troubleshooting acima

**Dúvidas sobre código:**
- Usa AI chat: `@README.md explica X`
- Consulta `docs/GUIA_USO.md`

**Issues técnicos:**
- Documenta erro
- Inclui: comando usado, Python version, SO
- Anexa logs se disponível

---

## 🎉 Pronto!

Se seguiste os passos, tens agora:

✅ Cursor com projeto configurado  
✅ Dependências instaladas  
✅ Primeiro teste executado  
✅ Sistema funcional  

**Comando para validar tudo:**
```bash
python src/cli.py analyze-perfil data/inputs/perfil.pdf -o relatorio.json && \
echo "✅ SISTEMA FUNCIONAL!"
```

---

**Boa análise! 🚀**

*Última atualização: 24 Janeiro 2025*
