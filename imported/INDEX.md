# 📑 LinkedIn Optimizer Assistant - Índice de Navegação

**Versão:** 1.0.0  
**Data:** 24 Janeiro 2025  
**Status:** ✅ Pronto para usar

---

## 🚀 START HERE

### Para Começar Já
1. 👉 **[IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md)** - Como abrir no Cursor
2. 👉 **[setup.sh](setup.sh)** - Script de instalação automática
3. 👉 **[CURSOR_README.md](CURSOR_README.md)** - Guia rápido Cursor

### Depois de Configurado
4. 👉 **[GUIA_USO.md](docs/GUIA_USO.md)** - Como usar o sistema

---

## 📚 Documentação Principal

### Essenciais
- **[README.md](README.md)** - Visão geral e arquitetura completa
- **[PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md)** - O que foi construído (este documento!)
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões e roadmap

### Para Desenvolver
- **[.cursorrules](.cursorrules)** - Guidelines para desenvolvimento no Cursor
- **[requirements.txt](requirements.txt)** - Dependências Python

---

## 💻 Código Fonte

### Core (Motor Principal)
```
src/
├── cli.py                    ← Interface linha de comando
├── core/
│   ├── pdf_parser.py        ← Extração de PDFs
│   └── analyzer.py          ← Motor de análise 360Brew
└── __init__.py
```

**Começar por:**
1. `src/cli.py` - Ponto de entrada, comandos
2. `src/core/pdf_parser.py` - Como PDFs são processados
3. `src/core/analyzer.py` - Como scoring funciona

### Configuração
```
config/
├── checklists/
│   └── 360brew_checklist.yaml    ← Critérios e pesos
└── prompts/
    └── perfil.yaml               ← Templates de análise
```

**Começar por:**
1. `360brew_checklist.yaml` - Entender critérios
2. `perfil.yaml` - Ver estrutura de prompts

### Testes
```
tests/
└── test_basic.py            ← Testes unitários
```

---

## 📁 Diretórios de Trabalho

### Dados
```
data/
├── inputs/           ← Coloca PDFs aqui para analisar
│   └── .gitkeep
└── outputs/          ← Relatórios gerados aparecem aqui
    └── .gitkeep
```

### Docs
```
docs/
└── GUIA_USO.md      ← Manual completo de uso
```

---

## 🎯 Uso Rápido

### Comandos Essenciais

```bash
# Info do sistema
python src/cli.py info

# Análise básica
python src/cli.py analyze-perfil data/inputs/perfil.pdf

# Com relatório JSON
python src/cli.py analyze-perfil perfil.pdf -o results.json

# Com relatório Markdown
python src/cli.py analyze-perfil perfil.pdf -o results.md

# Modo debug
python src/cli.py analyze-perfil perfil.pdf -v
```

---

## 🔍 Por Onde Navegar

### Se Queres...

**...Usar o sistema agora:**
→ [IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md) → [setup.sh](setup.sh) → Executar análise

**...Entender a arquitetura:**
→ [README.md](README.md) → [src/core/](src/core/) → [config/](config/)

**...Desenvolver novos módulos:**
→ [.cursorrules](.cursorrules) → [CHANGELOG.md](CHANGELOG.md) → [Próximos módulos]

**...Troubleshooting:**
→ [GUIA_USO.md](docs/GUIA_USO.md) secção Troubleshooting

**...Entender 360Brew:**
→ [config/checklists/360brew_checklist.yaml](config/checklists/360brew_checklist.yaml)

**...Ver o que foi entregue:**
→ [PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md)

---

## 📊 Estrutura Visual

```
linkedin-optimizer/
│
├── 📖 DOCUMENTAÇÃO
│   ├── INDEX.md (este ficheiro)
│   ├── README.md
│   ├── CURSOR_README.md
│   ├── IMPORTAR_CURSOR.md
│   ├── PROJETO_ENTREGUE.md
│   ├── CHANGELOG.md
│   └── docs/
│       └── GUIA_USO.md
│
├── ⚙️ CONFIGURAÇÃO
│   ├── .cursorrules
│   ├── requirements.txt
│   ├── setup.sh
│   └── config/
│       ├── checklists/360brew_checklist.yaml
│       └── prompts/perfil.yaml
│
├── 💻 CÓDIGO FONTE
│   └── src/
│       ├── cli.py
│       ├── core/
│       │   ├── pdf_parser.py
│       │   └── analyzer.py
│       ├── modules/
│       └── utils/
│
├── 🧪 TESTES
│   └── tests/
│       └── test_basic.py
│
└── 📁 DADOS
    └── data/
        ├── inputs/
        └── outputs/
```

---

## ✅ Checklist de Orientação

### Primeiro Contacto
- [ ] Li o [IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md)
- [ ] Executei `./setup.sh`
- [ ] Testei `python src/cli.py info`
- [ ] Li [CURSOR_README.md](CURSOR_README.md)

### Uso Básico
- [ ] Exportei meu perfil LinkedIn como PDF
- [ ] Coloquei em `data/inputs/`
- [ ] Executei primeira análise
- [ ] Li o relatório gerado
- [ ] Consultei [GUIA_USO.md](docs/GUIA_USO.md)

### Compreensão
- [ ] Li [README.md](README.md) completo
- [ ] Entendi arquitetura em [src/core/](src/core/)
- [ ] Vi critérios em [360brew_checklist.yaml](config/checklists/360brew_checklist.yaml)
- [ ] Li [PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md)

### Desenvolvimento
- [ ] Li [.cursorrules](.cursorrules)
- [ ] Vi roadmap em [CHANGELOG.md](CHANGELOG.md)
- [ ] Testei modificar código
- [ ] Rodei testes: `pytest tests/ -v`

---

## 🎓 Fluxo de Aprendizagem Recomendado

### Dia 1: Setup e Primeiro Uso
1. **Configuração** (30 min)
   - [IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md)
   - Executar `./setup.sh`
   - Verificar instalação

2. **Primeiro Teste** (15 min)
   - Exportar perfil LinkedIn
   - Executar análise
   - Ler relatório

3. **Compreensão Básica** (30 min)
   - [CURSOR_README.md](CURSOR_README.md)
   - [GUIA_USO.md](docs/GUIA_USO.md)

### Dia 2: Compreensão Profunda
1. **Arquitetura** (45 min)
   - [README.md](README.md)
   - [PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md)

2. **Código** (60 min)
   - `src/cli.py`
   - `src/core/pdf_parser.py`
   - `src/core/analyzer.py`

3. **Metodologia** (30 min)
   - `config/checklists/360brew_checklist.yaml`
   - Entender critérios e pesos

### Dia 3: Desenvolvimento
1. **Guidelines** (30 min)
   - [.cursorrules](.cursorrules)
   - [CHANGELOG.md](CHANGELOG.md) roadmap

2. **Prática** (90 min)
   - Modificar um critério
   - Adicionar logging
   - Testar modificações

3. **Planear Próximos** (30 min)
   - Escolher próximo módulo
   - Ler prompts relevantes
   - Planear implementação

---

## 🆘 Em Caso de Dúvida

### Problemas Técnicos
→ [GUIA_USO.md](docs/GUIA_USO.md) secção "Troubleshooting"

### Questões sobre Uso
→ [CURSOR_README.md](CURSOR_README.md) ou [GUIA_USO.md](docs/GUIA_USO.md)

### Entender Arquitetura
→ [README.md](README.md) secção "Arquitetura Técnica"

### Desenvolvimento
→ [.cursorrules](.cursorrules) + [CHANGELOG.md](CHANGELOG.md)

### O Que Foi Construído
→ [PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md)

---

## 🎯 Quick Links por Objetivo

| Objetivo | Documentos |
|----------|-----------|
| **Começar já** | [IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md) → [setup.sh](setup.sh) |
| **Primeiro uso** | [CURSOR_README.md](CURSOR_README.md) → [GUIA_USO.md](docs/GUIA_USO.md) |
| **Entender código** | [README.md](README.md) → [src/core/](src/core/) |
| **Desenvolver** | [.cursorrules](.cursorrules) → [CHANGELOG.md](CHANGELOG.md) |
| **Metodologia 360Brew** | [360brew_checklist.yaml](config/checklists/360brew_checklist.yaml) |
| **O que foi feito** | [PROJETO_ENTREGUE.md](PROJETO_ENTREGUE.md) |

---

## 📞 Contacto e Suporte

**Para:**
- Issues técnicos → Documentar em `CHANGELOG.md`
- Dúvidas gerais → Consultar documentação apropriada
- Melhorias → Ver roadmap em `CHANGELOG.md`

---

## 🎉 Próximo Passo

**A tua próxima ação deve ser:**

👉 Abrir [IMPORTAR_CURSOR.md](IMPORTAR_CURSOR.md) e seguir o guia de setup.

**Depois:**

👉 Executar primeira análise seguindo [CURSOR_README.md](CURSOR_README.md)

**E depois:**

👉 Explorar código e planear desenvolvimento seguindo [.cursorrules](.cursorrules)

---

**Versão deste índice:** 1.0  
**Última atualização:** 24 Janeiro 2025  
**Status:** ✅ Completo

---

**Boa exploração! 🚀**
