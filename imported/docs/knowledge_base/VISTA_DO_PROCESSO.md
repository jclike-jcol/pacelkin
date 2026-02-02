# Vista do Processo — LinkedIn 360Brew Optimization (Pacelkin)

Documento que integra a especificação completa (PROMPT_CURSOR_LINKEDIN_360BREW_V1.0), a base de conhecimento e a aplicação atual para uma visão de ponta a ponta.

---

## 1. Visão geral

| Camada | Conteúdo |
|--------|----------|
| **Especificação** | PROMPT_CURSOR_LINKEDIN_360BREW_V1.0.md — missão, 360Brew, PROVA, BARM, scoring, prompts, arquitetura alvo |
| **Base de conhecimento** | prompt_kit.pdf, PROMPT_CURSOR (este doc), caramez (ABOUT, HEADLINE, etc.) |
| **Aplicação atual** | FastAPI: landing, registo, login, backoffice, análise de perfil (PDF), chat, KPIs, histórico |

A análise de perfil (PDF) e a base de conhecimento servem para **ajudar o utilizador** de forma contextual (chat, recomendações, roadmaps).

---

## 2. Jornada do utilizador (atual)

1. **Landing** → Registo / Login  
2. **Registo** → Dados + password (regras visuais)  
3. **Login** → Acesso ao backoffice  
4. **Backoffice**  
   - Importar perfil em PDF (instruções passo a passo)  
   - Análise 360Brew (scoring, recomendações, relatório)  
   - Roadmaps, insights, estatísticas  
5. **Chat** → Mensagens com contexto futuro (base de conhecimento + análise)  
6. **KPIs** → Registo de métricas e publicações  
7. **Histórico** → Análises, chat, roadmaps, insights  

---

## 3. Onde a especificação (PROMPT_CURSOR) se cruza com a app

- **Análise de perfil (PDF)**  
  Já existe: extração de texto, scoring por secção (headline, sobre, experiência, competências, consistência), recomendações e red flags.  
  A especificação detalha critérios 360Brew (pesos, PROVA, BARM) e pode alinhar ainda mais o scoring e os textos de recomendação.

- **Base de conhecimento**  
  O loader inclui:  
  - **prompt_kit.pdf** (pypdf)  
  - **PROMPT_CURSOR_LINKEDIN_360BREW_V1.0.md** (raiz de `knowledge_base`)  
  - **caramez/** (ABOUT_*.txt, HEADLINE_ABOUT_FINAL.md, etc.)  
  Tudo isto está disponível em `get_knowledge_base_text()` para chat e futuras recomendações.

- **Chat**  
  Hoje guarda mensagens e um placeholder. O próximo passo é usar `get_knowledge_base_text()` + última análise de perfil do utilizador como contexto para um LLM e responder com recomendações alinhadas a 360Brew, PROVA e BARM.

- **Roadmaps / plano de ação**  
  A app já tem criação de roadmaps e insights. A especificação define um roadmap de 90 dias em 3 fases (clarificação de identidade, otimização de sinais, engagement relacional) e KPIs; pode guiar templates e sugestões automáticas a partir da análise.

- **Relatórios**  
  A especificação prevê PDF/Word/Markdown. Na app, a análise é mostrada no backoffice e no histórico; exportação em PDF/Word pode ser uma extensão futura.

---

## 4. Fundamentos 360Brew (resumo para contexto)

- **Perfil 360** — Algoritmo cruza perfil, posts, comentários, interações e consistência.  
- **Sinais fortes** — Saves > Likes; Dwell Time; comentários de qualidade (modelo A3); consistência temática (2–4 pilares); densidade de relacionamento.  
- **Formatos** — Documentos/carrosséis e artigos performam melhor; vídeos e conteúdo fragmentado penalizados.  
- **Metodologias** — PROVA (Sobre), BARM (Experiências), A3 (Comentários), Headline [Cargo | Especialidade | Valor].  

Isto está descrito em detalhe em PROMPT_CURSOR e no prompt_kit; a base de conhecimento carregada na app reflete estes princípios.

---

## 5. Próximos passos sugeridos (a partir da especificação)

1. **Chat com LLM** — Usar `get_knowledge_base_text()` + última análise de perfil como contexto e gerar respostas e recomendações 360Brew.  
2. **Alinhar scoring** — Revisar pesos e critérios em `profile_analysis` com a secção de scoring do PROMPT_CURSOR.  
3. **Roadmap 90 dias** — Oferecer um template ou geração automática a partir da análise (3 fases, checklist, KPIs).  
4. **Prompts integrados** — Quando houver LLM, usar os prompts do PROMPT_CURSOR (perfil, headline, sobre, experiência, competências, plano de ação) como templates.  
5. **Exportação de relatórios** — PDF/Word/Markdown com estrutura descrita na especificação (resumo executivo, análise por secção, roadmap).  

---

## 6. Ficheiros de referência

| Ficheiro | Descrição |
|----------|-----------|
| `PROMPT_CURSOR_LINKEDIN_360BREW_V1.0.md` | Especificação completa do projeto (contexto, 360Brew, PROVA, BARM, arquitetura, prompts, requisitos) |
| `prompt kit.pdf` | Kit de prompts (incoming/caramez), texto extraído via pypdf |
| `caramez/ABOUT_*.txt`, `HEADLINE_ABOUT_FINAL.md` | Conteúdos Caramez na base de conhecimento |
| `app/services/knowledge_base.py` | Loader: PDF + raiz de knowledge_base + caramez |
| `app/services/profile_analysis.py` | Análise de perfil (PDF → scoring, recomendações) |
| `app/main.py` | Rotas; chat e backoffice usam `get_knowledge_base_text()` |

---

*Documento criado para complementar a vista do processo após integração do PROMPT_CURSOR_LINKEDIN_360BREW_V1.0 na base de conhecimento.*
