# Integração do módulo Pacelkin com closerpace.com

Este documento explica **como integrar** a aplicação Pacelkin (LinkedIn 360Brew Optimizer) com o site **closerpace.com**, em função do que o CloserPace já tem (site, domínio, base de utilizadores).

---

## 0. Migração e workspace unificado (closerpace.com como base central)

- **Ter ambos no mesmo workspace:** Ver **`INSTRUCAO_WORKSPACE_CLOSERSPACE.md`** — descreve como juntar o projeto closerpace.com e o Pacelkin no mesmo Cursor (multi-root ou Pacelkin como subpasta).
- **Onde fazer as perguntas e a integração:** É preferível fazer **no workspace do closerpace.com** (base central). O ficheiro `INSTRUCAO_WORKSPACE_CLOSERSPACE.md` contém a **instrução para colar num chat no Cursor com o workspace do closerpace.com aberto**, para aí responderes às perguntas de contexto e implementares o lado CloserPace (link, SSO, API, etc.). O Pacelkin (este repo) fica com os ajustes que “recebem” a integração (ex.: rota `/sso`).

---

## 1. O que é preciso definir primeiro

Antes de implementar, convém esclarecer:

| Pergunta | Impacto |
|----------|--------|
| O closerpace.com é um site estático, WordPress, ou aplicação própria (ex.: React, Next.js)? | Define se a integração é por link, iframe ou API. |
| Os utilizadores do Pacelkin devem ser os **mesmos** do closerpace.com (uma só conta) ou podem ser contas separadas? | Define se fazemos SSO (Single Sign-On) ou apenas link entre sites. |
| O Pacelkin deve aparecer **dentro** do closerpace.com (iframe / mesma navegação) ou como **aplicação separada** (subdomínio ou domínio próprio)? | Define deploy e cookies (domínio, CORS). |
| O closerpace.com já tem login? Se sim, como (email/password, OAuth, etc.)? | Define como passar a sessão para o Pacelkin (token, cookie partilhado, etc.). |

Com estas respostas consegues escolher um dos cenários abaixo e seguir os passos correspondentes.

---

## 2. Cenários de integração

### Cenário A — Link simples (mais rápido)

**Ideia:** No closerpace.com existe um botão/link do tipo “Aceder ao Pacelkin” ou “Otimização LinkedIn 360Brew” que abre a aplicação Pacelkin noutra aba ou na mesma.

**No closerpace.com:**
- Adicionar link para o URL onde o Pacelkin está em produção, por exemplo:
  - `https://app.closerpace.com` ou
  - `https://pacelkin.closerpace.com` ou
  - `https://otimizador.closerpace.com`

**No Pacelkin (este módulo):**
- Garantir que está em produção nesse URL (ver secção 4).
- Opcional: na landing do Pacelkin, referir “Uma ferramenta CloserPace” e link de volta para closerpace.com.

**Vantagens:** Simples, sem alterar autenticação.  
**Desvantagens:** O utilizador faz login separado no Pacelkin (email/password já existente nesta app).

---

### Cenário B — Subdomínio + mesma marca

**Ideia:** O Pacelkin corre num subdomínio do mesmo domínio do CloserPace (ex.: `app.closerpace.com` ou `pacelkin.closerpace.com`), com header/rodapé ou estilo alinhado ao closerpace.com.

**No closerpace.com / DNS:**
- Criar subdomínio (ex.: `app.closerpace.com` ou `pacelkin.closerpace.com`) e apontar para o servidor onde o Pacelkin está (IP ou CNAME para o host do Pacelkin).

**No Pacelkin:**
- Configurar a aplicação para aceitar esse host (e HTTPS).
- Opcional: alterar templates (ex.: `base.html`) para usar logo/nome “CloserPace” e link “Voltar a closerpace.com”.
- Opcional: ficheiro de configuração ou variável de ambiente `BRANDING_SITE_URL = "https://closerpace.com"` para gerar links de volta.

**Cookies:** Como o domínio é diferente (subdomínio), o cookie de sessão do Pacelkin é `app.closerpace.com`. Não partilha cookies com `closerpace.com` a menos que se use um domínio comum (ex.: `.closerpace.com`) — isso já é abordado no SSO abaixo.

**Vantagens:** Experiência “tudo sob o mesmo domínio” e marca única.  
**Desvantagens:** Continua a ser um login separado no Pacelkin, a menos que se implemente SSO.

---

### Cenário C — Single Sign-On (SSO) com closerpace.com

**Ideia:** O utilizador faz login **no closerpace.com**. O CloserPace, após validar o login, redireciona para o Pacelkin com um **token assinado** (ex.: JWT ou HMAC). O Pacelkin valida o token e cria uma sessão local (cookie) para esse utilizador, sem pedir password outra vez.

**Fluxo resumido:**
1. Utilizador está no closerpace.com e clica “Aceder ao Pacelkin”.
2. closerpace.com gera um token (ex.: JWT com `user_id`, `email`, `exp`) assinado com um **segredo partilhado**.
3. Redireciona para:  
   `https://app.closerpace.com/sso?token=TOKEN` (ou POST).
4. O Pacelkin recebe o token, verifica a assinatura e a expiração.
5. Se o utilizador já existir na base do Pacelkin (por email), associa a sessão a esse user_id; se não existir, pode criar um utilizador “à la carte” (só email e nome) e depois criar a sessão.
6. Redireciona para `/backoffice` ou `/` e o utilizador fica logado.

**No closerpace.com (a implementar no vosso lado):**
- Após login bem-sucedido, ao clicar “Aceder ao Pacelkin”:
  - Gerar token (ex.: JWT com payload `{ "user_id": "id-interno-closerpace", "email": "...", "name": "...", "exp": ... }`).
  - Assinar com um segredo partilhado (ex.: `CLOSERSPACE_PACELKIN_SSO_SECRET`).
  - Redirecionar o browser para:  
    `https://[url-do-pacelkin]/sso?token=TOKEN`
- Guardar o segredo num env var e partilhá-lo com o Pacelkin (em produção, de forma segura).

**No Pacelkin (este módulo):**
- Adicionar rota `GET /sso?token=...` (ou POST se preferirem não passar token na URL).
- Validar o token (assinatura + expiração).
- Obter ou criar utilizador por email; criar sessão com `create_session_cookie(user_id)` e devolver o cookie na resposta.
- Redirecionar para `/backoffice` ou `/`.

**Segredo partilhado:**  
Ambos (closerpace.com e Pacelkin) usam a mesma variável de ambiente (ex.: `CLOSERSPACE_PACELKIN_SSO_SECRET`). O closerpace.com usa para assinar; o Pacelkin usa para verificar.

**Vantagens:** Um único login no CloserPace; experiência integrada.  
**Desvantagens:** Exige desenvolvimento em ambos os lados (gerar token no CloserPace, consumir no Pacelkin).

---

### Cenário D — Pacelkin dentro do closerpace.com (iframe)

**Ideia:** Uma página do closerpace.com (ex.: “Ferramentas” ou “Pacelkin”) mostra o Pacelkin dentro de um **iframe** (`src="https://app.closerpace.com"`).

**Problema:** Se o Pacelkin estiver noutro domínio (ex.: `app.closerpace.com`), os cookies de sessão são de terceiros. Browsers modernos bloqueiam cookies third-party em iframes em muitos casos (SameSite, Safari ITP, etc.). Por isso o login dentro do iframe pode falhar.

**Soluções:**
- **Recomendado:** O Pacelkin ser servido **no mesmo domínio** que o closerpace.com, por exemplo:
  - `https://closerpace.com/pacelkin/` — o reverse proxy (Nginx, Cloudflare, etc.) encaminha `/pacelkin/` para a aplicação Pacelkin. Assim os cookies são first-party (`closerpace.com`).
- **Alternativa:** Não usar iframe; usar o **link** (Cenário A) ou **redirecionamento** para o subdomínio (Cenário B). O utilizador abre o Pacelkin numa nova aba ou na mesma.

**Se usarem mesmo domínio + iframe:**
- No Pacelkin: configurar a app para um “path prefix” (ex.: `/pacelkin`) se for preciso (FastAPI suporta com `root_path` ou montagem atrás do proxy).
- No reverse proxy: encaminhar `https://closerpace.com/pacelkin` para o processo/serviço do Pacelkin.

---

### Cenário E — closerpace.com como frontend e Pacelkin como API

**Ideia:** O closerpace.com é a única interface; não há UI do Pacelkin visível para o utilizador. O closerpace.com chama **APIs REST** do Pacelkin (análise de perfil, KPIs, chat, etc.) e mostra os dados nas suas próprias páginas.

**No Pacelkin:**
- Expor endpoints de API (ex.: `/api/profile-analysis`, `/api/kpis`, `/api/chat`) com autenticação por token (API key ou JWT emitido pelo closerpace.com).
- Opcional: manter a UI do Pacelkin para uso direto ou admin; a integração “total” seria só via API.

**No closerpace.com:**
- Após login, obter ou gerar um token para o Pacelkin (ex.: JWT com `user_id`/email).
- Nas páginas relevantes, fazer pedidos HTTP ao Pacelkin com esse token no header (ex.: `Authorization: Bearer TOKEN`).
- Renderizar resultados (relatórios, KPIs, etc.) no design do closerpace.com.

**Vantagens:** Experiência 100% dentro do closerpace.com; um único produto visível.  
**Desvantagens:** Mais desenvolvimento (APIs + frontend no CloserPace); pode ser faseado (primeiro link/SSO, depois API para funcionalidades específicas).

---

## 3. Resumo: o que fazer em cada cenário

| Cenário | No closerpace.com | No Pacelkin (este repo) |
|--------|--------------------|---------------------------|
| **A – Link** | Link/botão para URL do Pacelkin | Deploy em URL público; opcional branding |
| **B – Subdomínio** | DNS para app.closerpace.com (ou similar) | Configurar host; opcional header/logo CloserPace |
| **C – SSO** | Gerar token assinado e redirecionar para `/sso?token=...` | Nova rota `/sso`, validar token, criar/criar sessão |
| **D – Iframe** | Página com iframe; idealmente mesmo domínio (proxy) | Servir sob path do closerpace.com (ex.: /pacelkin) |
| **E – API** | Frontend que chama APIs do Pacelkin com token | Endpoints `/api/...` + auth por token |

---

## 4. Deploy do Pacelkin para uso com closerpace.com

Para qualquer cenário em que o utilizador acede ao Pacelkin por browser (A, B, C ou D), é preciso:

1. **Servidor** (VPS, cloud ou PaaS) com Python 3.9+.
2. **Domínio/subdomínio** (ex.: `app.closerpace.com`) apontando para esse servidor (A record ou CNAME).
3. **HTTPS** (ex.: Let’s Encrypt) — obrigatório para cookies seguros e SSO em produção.
4. **Processo em produção:** por exemplo:
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Atrás de um reverse proxy (Nginx, Caddy, etc.) que termina HTTPS e encaminha para `localhost:8000`.
5. **Variáveis de ambiente:**  
   `APP_SECRET` (e, para SSO, `CLOSERSPACE_PACELKIN_SSO_SECRET` ou o nome que usarem) definidas no servidor, nunca em código.

Se quiseres, no próximo passo posso detalhar **apenas o Cenário C (SSO)** com exemplo de código para:
- Rota `/sso` no Pacelkin (validar token e criar sessão).
- Exemplo de payload e assinatura JWT/HMAC que o closerpace.com deve gerar.

---

## 5. Próximo passo recomendado

1. **Decidir** qual cenário se aplica (A a E) em função das respostas à secção 1.  
2. **Se for SSO (C):** dizer como o closerpace.com faz login hoje (tecnologia e se já emitem algum token). Com isso dá para desenhar o formato exato do token e o código da rota `/sso` no Pacelkin.  
3. **Se for apenas link (A) ou subdomínio (B):** basta configurar o URL de produção e, no CloserPace, colocar o link ou o DNS.

Se indicares o cenário que queres (e, no caso de SSO, a stack do closerpace.com), posso propor o código concreto para este repositório (Pacelkin) e os passos exatos para o lado do closerpace.com.
