# Guia de Uso - LinkedIn Optimizer Assistant

**Versão:** 1.0  
**Última atualização:** Janeiro 2025

---

## 🚀 Quick Start

### 1. Setup Inicial

```bash
# Clonar/copiar projeto para o Cursor
cd linkedin-optimizer

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
python src/cli.py info
```

### 2. Exportar Perfil do LinkedIn

1. Acede ao teu perfil LinkedIn
2. Clica em "Mais" → "Guardar como PDF"
3. Guarda o ficheiro (ex: `perfil.pdf`)
4. Coloca em `data/inputs/`

### 3. Analisar Perfil

```bash
# Análise básica
python src/cli.py analyze-perfil data/inputs/perfil.pdf

# Com output JSON
python src/cli.py analyze-perfil data/inputs/perfil.pdf -o relatorio.json

# Com output Markdown
python src/cli.py analyze-perfil data/inputs/perfil.pdf -o relatorio.md

# Modo verbose (debug)
python src/cli.py analyze-perfil data/inputs/perfil.pdf -v
```

---

## 📊 Entender os Resultados

### Score Geral (0-100)

- 🟢 **85-100**: Perfil Otimizado para 360Brew
- 🟡 **70-84**: Bom perfil, ajustes pontuais
- 🟠 **50-69**: Requer otimização significativa
- 🔴 **<50**: Necessita refatoração completa

### Análise por Critério

Cada critério é avaliado individualmente:

1. **Headline com pilares** (15 pts)
2. **Consistência Sobre** (15 pts)
3. **Posts consistentes** (10 pts) *
4. **Primeiras linhas** (8 pts) *
5. **CTA qualidade** (7 pts) *
6. **Conteúdo guardável** (10 pts) *
7. **Resposta comentários** (10 pts) *
8. **Comentários de valor** (10 pts) *
9. **Formatos dwell time** (5 pts) *
10. **Métricas certas** (5 pts)
11. **Zero red flags** (5 pts)

\* *Critérios marcados requerem dados de atividade (posts, comentários) não incluídos no PDF do perfil. Serão avaliados no Módulo 5 (Análise de Conteúdo).*

### Red Flags

Penalizações aplicadas automaticamente:

- **Inconsistência temática** (-15 pts)
- **Tópicos espalhados** (-10 pts)
- **Comentários genéricos** (-8 pts)
- **Engagement bait** (-12 pts)
- **Padrões de IA** (-10 pts)
- **Ghost posting** (-15 pts)
- **Vanity metrics** (-5 pts)
- **Conteúdo viral vazio** (-10 pts)

---

## 🎯 Interpretar Recomendações

### Pontos Fortes

Lista critérios com >80% score.  
**Ação:** Mantém estas práticas!

### Oportunidades de Melhoria

Lista critérios com <70% score, ordenados por prioridade.

**Estrutura:**
```
• Critério (score atual)
  Prioridade: Alta/Média
  → Sugestão específica 1
  → Sugestão específica 2
```

**Ação:** Implementa sugestões de cima para baixo (prioridade Alta primeiro).

### Próximos Passos

Roadmap personalizado baseado na categoria do score.

---

## 📁 Estrutura de Outputs

### JSON Output

```json
{
  "score_total": 72,
  "score_maximo": 100,
  "percentagem": 72.0,
  "categoria": "bom",
  "criterios": [
    {
      "id": "headline_pilares",
      "nome": "Headline com 2-3 pilares temáticos",
      "score": 12,
      "peso": 15,
      "percentagem": 80.0,
      "passou": true,
      "justificacao": "...",
      "sugestoes": [...]
    }
  ],
  "red_flags": [...],
  "pontos_fortes": [...],
  "oportunidades": [...],
  "headline_sugerido": "..."
}
```

**Use para:**
- Integração com outras ferramentas
- Tracking de progresso ao longo do tempo
- Análise comparativa de múltiplos perfis

### Markdown Output

Relatório formatado em Markdown, pronto para:
- Imprimir ou partilhar
- Converter para PDF
- Adicionar a documentação

---

## 🔧 Troubleshooting

### Erro: "PDF não encontrado"

**Causa:** Caminho incorreto para o PDF.

**Solução:**
```bash
# Verifica se ficheiro existe
ls data/inputs/perfil.pdf

# Usa caminho absoluto se necessário
python src/cli.py analyze-perfil /caminho/completo/perfil.pdf
```

### Erro: "PDF está vazio ou corrompido"

**Causa:** PDF não é válido ou não contém texto extraível.

**Solução:**
1. Verifica se é PDF real (não imagem scaneada)
2. Re-exporta do LinkedIn
3. Tenta abrir PDF noutro programa para validar

### Erro: "Checklist não encontrada"

**Causa:** Ficheiro de configuração em falta.

**Solução:**
```bash
# Verifica estrutura
ls config/checklists/360brew_checklist.yaml

# Se não existir, copia do repositório
```

### Score parece baixo

**Normal se:**
- Perfil não está otimizado para 360Brew (muitos estão)
- Secções em branco no PDF (sobre, experiências)
- Critérios de posts não aplicáveis (requerem Módulo 5)

**Foca em:**
1. Corrigir Red Flags primeiro
2. Implementar oportunidades de Prioridade Alta
3. Headline e Sobre (40 pontos combinados)

---

## 💡 Boas Práticas

### Antes da Análise

1. ✅ Preenche todas as secções do perfil LinkedIn
2. ✅ Headline tem 2-3 pilares claros
3. ✅ Secção Sobre tem >500 caracteres
4. ✅ Experiências com resultados quantificados

### Durante a Análise

1. ✅ Usa modo verbose (-v) na primeira vez
2. ✅ Guarda outputs para comparar depois
3. ✅ Lê recomendações completas, não só score

### Depois da Análise

1. ✅ Implementa top 3 oportunidades
2. ✅ Re-analisa após mudanças (1-2 semanas)
3. ✅ Tracking: guarda histórico de scores
4. ✅ Compara com benchmarks do setor

---

## 🔄 Workflow Recomendado

### Ciclo de Otimização (30 dias)

**Semana 1: Diagnóstico**
```bash
python src/cli.py analyze-perfil perfil.pdf -o baseline.json
```
- Identifica red flags
- Lista top 5 oportunidades
- Define prioridades

**Semana 2-3: Implementação**
- Corrige red flags
- Reescreve headline (se necessário)
- Otimiza secção Sobre
- Adiciona resultados quantificados nas experiências

**Semana 4: Re-avaliação**
```bash
python src/cli.py analyze-perfil perfil_v2.pdf -o progresso.json
```
- Compara scores (baseline vs progresso)
- Valida melhorias
- Identifica próximos passos

---

## 📚 Recursos Adicionais

### Documentação

- `README.md` - Visão geral do projeto
- `METODOLOGIA_360BREW.md` - Fundamentos algorítmicos
- `.cursorrules` - Guidelines de desenvolvimento

### Configuração

- `config/checklists/360brew_checklist.yaml` - Critérios detalhados
- `config/prompts/perfil.yaml` - Templates de análise

### Exemplos

- `data/inputs/exemplos/` - PDFs de exemplo
- `data/outputs/exemplos/` - Relatórios de exemplo

---

## 🆘 Suporte

### Problemas Comuns

Consulta a secção Troubleshooting acima.

### Bugs ou Sugestões

1. Documenta o erro (screenshot + comando usado)
2. Inclui versão do Python e sistema operativo
3. Anexa ficheiro de log se disponível

### Melhorias Futuras

- [ ] Módulo 2: Geração de Sobre (PROVA)
- [ ] Módulo 3: Estratégia Recomendações
- [ ] Módulo 4: Plano de Ação 90 dias
- [ ] Módulo 5: Análise de Conteúdo (Excel import)
- [ ] Módulo 6: Geração de Conteúdo (templates)

---

**Última atualização:** Janeiro 2025  
**Versão do guia:** 1.0
