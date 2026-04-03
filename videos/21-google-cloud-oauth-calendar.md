# Video 21: Configuracao do Google Cloud Console (OAuth + Calendar)

**Duracao:** ~3:28
**Categoria:** Integracao Google / OAuth
**Pre-requisitos:** Projeto no Google Cloud Console, dominio com HTTPS configurado
**Resultado esperado:** OAuth consent screen configurado, credenciais OAuth criadas, JSON na pasta key, app publicado

---

## Resumo

Configura o fluxo OAuth completo no Google Cloud Console para integracao com Google Calendar. Diferente do Video 07 (que so cria a API key do Gemini), este video configura o OAuth consent screen, cria credenciais tipo "Web application" com redirect URIs, adiciona escopos do Calendar, publica o app e salva o JSON no projeto.

---

## Timeline Detalhada

### Etapa 1: OAuth Consent Screen (0:00 - 0:56)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Acessa o Google Cloud Console |
| 0:00 | Navega ate "API e Servicos" > "Tela de consentimento OAuth" (OAuth consent screen) |
| 0:15 | Escolhe a opcao "External" |
| 0:25 | Preenche o nome do app |
| 0:35 | Preenche os emails de suporte |
| 0:57 | Finaliza a criacao da consent screen |

**Caminho:** Google Cloud Console > APIs & Services > OAuth consent screen

**Campos:**
```
User type: External
App name: [Nome da empresa]
User support email: [email da empresa]
Developer contact: [email da empresa]
```

### Etapa 2: Criar credenciais OAuth (0:57 - 1:46)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:57 | Clica em "Create OAuth client" |
| 1:05 | Seleciona tipo: "Web application" |
| 1:10 | Define um nome para o client |
| 1:15 | Em "Authorized JavaScript origins", adiciona a URL base do dominio |
| 1:25 | Em "Authorized redirect URIs", adiciona a URL completa de callback |
| 1:40 | Finaliza a criacao |
| 1:47 | Faz download do arquivo JSON gerado |

**Campos da credencial:**

```
Application type: Web application
Name: [Nome do projeto]

Authorized JavaScript origins:
  https://seudominio.com

Authorized redirect URIs:
  https://seudominio.com/api/calendar/oauth/callback/
```

**IMPORTANTE:** A redirect URI deve ser EXATAMENTE:
```
https://seudominio.com/api/calendar/oauth/callback/
```
Com barra no final. Se errar, o OAuth falha com "redirect_uri_mismatch".

### Etapa 3: Configurar escopos (Data Access) (1:47 - 2:30)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:47 | Acessa "Data Access" |
| 1:55 | Adiciona os 3 escopos padrao (userinfo, email, profile) |
| 2:10 | Adiciona manualmente os escopos do Google Calendar |
| 2:25 | Insere os links da API na caixa de texto |
| 2:31 | Salva as alteracoes |

**Escopos adicionados:**

Padrao:
```
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

Google Calendar (adicionar manualmente):
```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

### Etapa 4: Publicar o app (2:31 - 2:45)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:31 | Na aba "Audience" |
| 2:35 | Altera o status de "Testing" para "In production" |
| 2:40 | Clica em "Publish app" |
| 2:46 | Confirma a acao |

**Por que publicar:** Em modo "Testing", apenas usuarios de teste (max 100) podem usar o OAuth. Em "In production", qualquer usuario Google pode autorizar. Necessario para multi-tenant.

**ATENCAO:** Se o app usa escopos sensiveis, o Google pode pedir verificacao. Para escopos do Calendar, geralmente nao e necessario.

### Etapa 5: Configurar .env e salvar JSON (2:46 - 3:28)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:46 | No editor de codigo, abre o arquivo `.env` |
| 2:59 | Preenche `GOOGLE_OAUTH_BASE_URL` com o dominio |
| 2:59 | Renomeia o arquivo JSON baixado para `oauth-client-credentials.json` |
| 3:15 | Arrasta o arquivo para dentro da pasta `key` no projeto |
| 3:28 | Integracao finalizada. FIM |

**Variavel no `.env`:**
```env
GOOGLE_OAUTH_BASE_URL=https://seudominio.com
GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH=key/oauth-client-credentials.json
GOOGLE_OAUTH_REDIRECT_PATH=/api/calendar/oauth/callback/
```

**Arquivo:** `key/oauth-client-credentials.json` (renomear o JSON baixado do Google)

**NUNCA commitar esse arquivo no Git.** Ja esta no `.gitignore`.

---

## Diferenca entre Video 07 e Video 21

| | Video 07 | Video 21 |
|---|---------|---------|
| **O que cria** | API Key (Gemini) | OAuth Client (Calendar) |
| **Usado para** | Agentes AI (Gemini) | Google Calendar OAuth |
| **Tipo** | Chave simples | OAuth 2.0 Web Application |
| **Arquivo** | Nenhum (so a string da key) | `oauth-client-credentials.json` |
| **Variavel .env** | `GOOGLE_API_KEY` | `GOOGLE_OAUTH_BASE_URL` + `GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH` |

---

## Checklist de Verificacao

- [ ] OAuth consent screen criado (tipo External)
- [ ] Nome do app e emails preenchidos
- [ ] Credencial OAuth tipo "Web application" criada
- [ ] "Authorized JavaScript origins" com dominio correto
- [ ] "Authorized redirect URIs" com URL completa de callback (com `/` no final)
- [ ] Escopos padrao adicionados (userinfo, email, profile)
- [ ] Escopos do Calendar adicionados manualmente
- [ ] App publicado (status "In production")
- [ ] `GOOGLE_OAUTH_BASE_URL` preenchido no `.env`
- [ ] JSON baixado, renomeado para `oauth-client-credentials.json` e salvo em `key/`

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| "redirect_uri_mismatch" | URI de callback errada ou sem barra no final | Verificar que e exatamente `https://dominio/api/calendar/oauth/callback/` |
| "Access blocked: app not verified" | App ainda em modo Testing | Publicar o app (Audience > Publish) |
| "invalid_client" | JSON errado ou corrompido | Re-baixar o JSON do Google Cloud Console |
| OAuth funciona em dev mas nao em producao | `GOOGLE_OAUTH_BASE_URL` com localhost | Trocar para dominio real com HTTPS |
| "File not found: oauth-client-credentials.json" | Arquivo nao esta na pasta `key/` ou nome errado | Verificar nome exato e localizacao |
| Escopos do Calendar nao aparecem na tela de autorizacao | Escopos nao foram adicionados em Data Access | Adicionar manualmente os links da API do Calendar |

---

## Notas Tecnicas

- Este OAuth e do tipo "Web application" (diferente do Video original do README que usa "Desktop app"). Web application e necessario para o fluxo de redirect no browser.
- O `GOOGLE_OAUTH_APP_SECRET` no `.env` e usado para assinar o state do OAuth (prevencao CSRF). Gerar com: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Em multi-tenant, cada tenant faz seu proprio fluxo OAuth pelo frontend (botao "Conectar Google Calendar"). O token e armazenado criptografado em `TenantSettings`.
- Logs de OAuth usam prefixo `[CALENDAR_OAUTH]`.

---

## Documentacao Relacionada

- README.md secao "Configuracao Completa do Google" — guia original
- README-CALENDAR.md — guia Calendar especifico
- docs/OAUTH-CALENDAR-FASE0-DECISOES.md — decisoes arquiteturais
- docs/OAUTH-CALENDAR-FASE7-OBSERVABILIDADE.md — logs e metricas
- Video 07 — Gemini API Key (diferente!)
- Video 18 — integracao Calendar via frontend
- Video 20 — passo anterior: GHL
