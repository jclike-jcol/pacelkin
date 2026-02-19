# Instrução para o workspace do closerpace.com

O **closerpace.com** é a base central. A migração/integração com o Pacelkin deve ser **conduzida no workspace do closerpace.com**. Este ficheiro contém a instrução que podes colar nesse workspace (Cursor) e como ter ambos os projetos no mesmo workspace.

---

## 1. Ter Pacelkin e closerpace.com no mesmo workspace

**Opção A — Workspace multi-root no Cursor**

1. No Cursor: **File → Add Folder to Workspace** (ou **File → Open Workspace from File** se já tiveres um `.code-workspace`).
2. Adiciona a pasta do **closerpace.com** (raiz do projeto do site).
3. Adiciona a pasta do **Pacelkin** (a pasta que contém `imported/` com a app FastAPI, ou a raiz `pacelkin`).
4. **File → Save Workspace As** e guarda como `closerpace-pacelkin.code-workspace` (ou outro nome).

Ficas com duas raizes no mesmo workspace, por exemplo:

```
closerpace.com/    (raiz 1)
pacelkin/          (raiz 2)
  imported/
    app/
    docs/
    ...
```

Assim podes editar os dois projetos no mesmo Cursor e referenciar ficheiros de ambos (ex.: no closerpace.com a apontar para o código ou docs do Pacelkin).

**Opção B — Pacelkin como subpasta do closerpace.com (monorepo)**

1. No repositório do closerpace.com, cria uma pasta, por exemplo `apps/pacelkin/` ou `tools/pacelkin/`.
2. Copia ou faz merge do conteúdo do Pacelkin (a pasta `imported/` ou a estrutura completa) para dentro dessa pasta.
3. O workspace do Cursor passa a ser só a raiz do closerpace.com; o Pacelkin fica em `apps/pacelkin/` (ou similar).

Vantagem: um único repo e um único workspace. Desvantagem: tens de decidir se o Pacelkin continua como repo separado (git submodule) ou se todo o código fica no repo do closerpace.com.

---

## 2. Onde fazer as perguntas e a integração

**Sim — é preferível fazer as perguntas e a implementação da integração no workspace do closerpace.com**, porque:

- O closerpace.com é a **base central**; o Pacelkin é um módulo/ferramenta que se liga a ela.
- As decisões (link, SSO, iframe, API) e o código novo (botão “Aceder ao Pacelkin”, geração de token SSO, páginas que consomem API) ficam no projeto do closerpace.com.
- No workspace do Pacelkin (este) só é preciso ajustar o que “recebe” do CloserPace (ex.: rota `/sso`, configuração de CORS, variáveis de ambiente).

Assim, **no workspace do closerpace.com** deves:
- Fazer as perguntas de contexto (tecnologia do site, tipo de login, como queres integrar).
- Implementar o lado CloserPace (links, tokens SSO, chamadas API, etc.).
- Decidir se o Pacelkin fica noutro repo/servidor ou dentro do mesmo repo (monorepo).

**No workspace do Pacelkin** (este repo) só precisas de:
- Ajustes para “receber” a integração (ex.: rota `/sso`, documentação).
- Manter a documentação de integração (`INTEGRACAO_CLOSERSPACE.md`) como referência para quem trabalha no closerpace.com.

---

## 3. Instrução para colar no workspace do closerpace.com

Copia o bloco abaixo e cola num novo chat no Cursor **com o workspace do closerpace.com aberto** (e, se usares multi-root, com a pasta do Pacelkin também no workspace). Ajusta os caminhos se a estrutura for diferente.

---

**INÍCIO DA INSTRUÇÃO (copiar daqui para baixo)**

Preciso de integrar o módulo **Pacelkin** (LinkedIn 360Brew Optimizer) com este projeto **closerpace.com**. O closerpace.com é a base central; o Pacelkin é uma app FastAPI (análise de perfil LinkedIn em PDF, chat, KPIs, roadmaps) que deve ficar disponível a partir daqui.

**Objetivos:**
1. Definir como integrar: link simples, subdomínio, SSO (um único login), iframe ou API.
2. Se for SSO: no closerpace.com gerar token e redirecionar para o Pacelkin; no Pacelkin já existe (ou será adicionada) rota `/sso` que valida o token e cria sessão.
3. Ter ambos os projetos no mesmo workspace (multi-root ou Pacelkin como subpasta) para a migração.

**Contexto do Pacelkin (referência no outro workspace):**
- App FastAPI em Python (pasta `imported/` ou `pacelkin/imported/`): landing, registo, login, backoffice, análise de perfil PDF, chat, KPIs, histórico.
- Autenticação atual: cookie de sessão (HMAC), tabela `users` (email, password_hash, etc.).
- Documentação de integração: no repo Pacelkin, ficheiro `docs/INTEGRACAO_CLOSERSPACE.md` descreve cenários A (link), B (subdomínio), C (SSO), D (iframe), E (API) e o que implementar em cada lado.

**Perguntas que preciso de responder neste workspace (closerpace.com):**
- Que tecnologia é o closerpace.com (WordPress, Next.js, React, estático, outro)?
- Já existe login? Se sim, como (email/password, OAuth)?
- Quero que o utilizador aceda ao Pacelkin por: link noutra aba, subdomínio (ex.: app.closerpace.com), SSO (login só aqui e redirecionar para o Pacelkin com token), iframe, ou API (closerpace.com consome APIs do Pacelkin)?

**Pedido:**
1. Com base nas respostas acima (ou nas predefinições que fizeres), indica o cenário de integração recomendado (A, B, C, D ou E).
2. Se o Pacelkin estiver já numa pasta neste workspace (ex.: `pacelkin/` ou `apps/pacelkin/`), usa essa pasta como referência; senão, assume que o Pacelkin está noutro repo/servidor e descreve o que este projeto (closerpace.com) deve implementar (URLs, token SSO, etc.).
3. Dá passos concretos para implementar no closerpace.com: onde colocar link/botão, como gerar token SSO (se for o caso), formato do token e URL de redirecionamento para o Pacelkin.

**FIM DA INSTRUÇÃO**

---

## 4. Resumo

| Onde | O que fazer |
|------|-------------|
| **Workspace closerpace.com** | Abrir este workspace (e, se quiseres, adicionar a pasta Pacelkin como segunda raiz). Colar a instrução acima e responder às perguntas. Implementar o lado CloserPace (link, SSO, API, etc.). |
| **Workspace Pacelkin** | Manter documentação (`INTEGRACAO_CLOSERSPACE.md`, este ficheiro). Quando o CloserPace definir o formato (ex.: SSO), implementar aqui a rota `/sso` ou outros ajustes que “recebem” a integração. |
| **Workspace unificado** | File → Add Folder to Workspace: adicionar a pasta do closerpace.com e a pasta do Pacelkin; Save Workspace As. Assim ambos estão no mesmo workspace para a migração. |

Se quiseres, no workspace do Pacelkin posso depois adicionar a rota `/sso` e a lógica de validação do token assim que o formato (JWT ou HMAC) e o segredo partilhado estiverem definidos no closerpace.com.
