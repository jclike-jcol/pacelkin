# LinkedIn Optimizer Assistant

**Versão:** 1.0.0  
**Projeto:** Assistente inteligente para otimização de perfis e conteúdo LinkedIn baseado no algoritmo 360Brew

---

## 📋 Visão Geral

Sistema modular de análise e otimização de perfis LinkedIn, construído como projeto integrado no Cursor IDE. Combina prompts especializados com análise automatizada de dados para maximizar visibilidade e engagement no LinkedIn.

---

## 🎯 Módulos (Ordem de Implementação)

### ✅ FASE 1: Core & Análise de Perfil
1. **Análise de Perfil** - Upload PDF → Parsing → Checklist 360Brew → Scoring
2. **Otimização "Sobre"** - Wizard PROVA + Geração otimizada
3. **Recomendações Escritas** - Estratégia de coleta estruturada

### 🔄 FASE 2: Estratégia & Planeamento  
4. **Plano de Ação** - 9 perguntas → Roadmap personalizado 90 dias
5. **Análise de Conteúdo** - Import Excel → Métricas → Insights

### 🚀 FASE 3: Geração de Conteúdo (Roadmap)
6. **Criação de Conteúdo** - Templates 360Brew → Posts otimizados

---

## 🏗️ Arquitetura Técnica

```
linkedin-optimizer/
├── README.md
├── requirements.txt
├── .cursorrules                    # Regras específicas do Cursor
├── config/
│   ├── prompts/                    # Templates dos prompts
│   │   ├── perfil.yaml
│   │   ├── sobre.yaml
│   │   ├── recomendacoes.yaml
│   │   ├── plano_acao.yaml
│   │   └── analise_conteudo.yaml
│   └── checklists/
│       └── 360brew_checklist.yaml
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── pdf_parser.py          # Extração dados do PDF LinkedIn
│   │   ├── analyzer.py             # Motor de análise
│   │   └── scorer.py               # Sistema de scoring
│   ├── modules/
│   │   ├── perfil_analyzer.py      # Módulo 1
│   │   ├── sobre_generator.py      # Módulo 2
│   │   ├── recomendacoes.py        # Módulo 3
│   │   ├── plano_acao.py           # Módulo 4
│   │   ├── analise_conteudo.py     # Módulo 5
│   │   └── conteudo_generator.py   # Módulo 6 (futuro)
│   ├── utils/
│   │   ├── validators.py
│   │   └── formatters.py
│   └── cli.py                      # Interface CLI principal
├── data/
│   ├── inputs/                     # PDFs e ficheiros de input
│   └── outputs/                    # Relatórios gerados
├── tests/
│   └── test_modules/
└── docs/
    ├── METODOLOGIA_360BREW.md
    └── GUIA_USO.md
```

---

## 🔧 Stack Tecnológica

- **Python 3.11+**
- **PyPDF2 / pdfplumber** - Parsing de PDFs
- **pandas** - Análise de dados Excel (Fase 2)
- **PyYAML** - Configuração de prompts
- **rich** - Interface CLI elegante
- **anthropic** - Integração Claude API (futuro)

---

## 🚀 Quick Start

```bash
# 1. Setup inicial
cd linkedin-optimizer
pip install -r requirements.txt

# 2. Executar assistente
python src/cli.py

# 3. Comandos disponíveis
python src/cli.py analyze-perfil --pdf data/inputs/perfil.pdf
python src/cli.py generate-sobre --interactive
python src/cli.py plano-acao --interactive
```

---

## 📊 Checklist 360Brew Integrada

Sistema de scoring baseado nos critérios:

### Perfil (0-100 pontos)
- ✓ Headline clara com 2-3 pilares temáticos (15 pts)
- ✓ Secção Sobre reforça mesmos pilares (15 pts)
- ✓ Consistência temática nos últimos 10 posts (15 pts)
- ✓ Estrutura de posts otimizada (saves, dwell time) (10 pts)
- ✓ Engagement responsivo (<90min) (10 pts)
- ✓ Comentários de valor em nicho (10 pts)
- ✓ Conteúdo guardável presente (10 pts)
- ✓ Formatos alto dwell time (5 pts)
- ✓ Tracking de métricas certas (5 pts)
- ✓ Zero red flags (5 pts)

### Categorias de Score
- 🟢 **85-100**: Otimizado para 360Brew
- 🟡 **70-84**: Bom, precisa ajustes
- 🟠 **50-69**: Requer otimização significativa
- 🔴 **<50**: Necessita refatoração completa

---

## 🎯 Princípios 360Brew (Hardcoded)

1. **Semantic Understanding** > Keyword Stuffing
2. **Saves** > Likes (10x mais peso)
3. **Dwell Time** > Quick Reactions
4. **Density Relacional** > Tamanho Audiência
5. **Consistência Temática** > Diversidade Aleatória
6. **Engagement Genuíno** > Engagement Bait

---

## 📝 Roadmap

### v1.0 - Análise de Perfil (Sprint Atual)
- [x] Setup projeto
- [ ] PDF Parser
- [ ] Checklist automatizada
- [ ] Scoring system
- [ ] CLI interface

### v1.1 - Geração "Sobre"
- [ ] Wizard PROVA
- [ ] Template engine
- [ ] Validação 2600 chars

### v1.2 - Recomendações & Plano
- [ ] Estratégia recomendações
- [ ] Plano 90 dias
- [ ] Roadmap semanal

### v2.0 - Análise Conteúdo
- [ ] Import Excel
- [ ] Análise métricas
- [ ] Dashboards texto

### v3.0 - Geração Conteúdo
- [ ] Templates posts
- [ ] Otimização 360Brew
- [ ] A/B testing

---

## 🤝 Metodologia de Trabalho

**Desenvolvimento Iterativo:**
1. Criar módulo base
2. Testar com dados reais
3. Refinar algoritmos
4. Documentar padrões
5. Próximo módulo

**Validação:**
- Cada módulo testado com PDFs reais LinkedIn
- Scoring validado contra guidelines 360Brew
- Output comparado com best practices

---

## 📚 Referências

- LinkedIn Algorithm 2026 Edition (Ocean Labs)
- Guia Completo 360Brew
- Prompt Kit LinkedIn
- Workshop LinkedIn 2026

---

## 🔒 Nota de Privacidade

Todos os dados processados permanecem locais. Nenhum upload para servidores externos na versão base.

---

**Criado por:** JC | CloserPace  
**Última atualização:** Janeiro 2025  
**Licença:** Uso interno/proprietário
