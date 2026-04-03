# Video 18: Integracoes e Configuracoes da Plataforma

**Duracao:** ~2:59 (01:17 - 04:16 no compilado)
**Categoria:** Integracoes / Configuracao via Frontend
**Pre-requisitos:** Video 17 (acesso a plataforma), credenciais de Google Calendar, Gemini, GHL, SMTP, WhatsApp
**Resultado esperado:** Todas as integracoes conectadas e checklist verde no frontend

---

## Resumo

Video mais completo de integracao. Configura TUDO pelo frontend: Google Calendar (OAuth), Gemini API key, GoHighLevel (tokens + pipeline), Email SMTP (Gmail app password), horarios de expediente, perfil do agente e WhatsApp (Z-API). Ao final, o checklist da plataforma fica todo verde.

---

## Timeline Detalhada

### Etapa 1: Google Calendar (01:17 - 01:55)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:17 | Na plataforma, acessa secao de integracoes |
| 1:17 | Clica em "Conectar Google Calendar" |
| 1:55 | Fluxo OAuth: autoriza acesso ao calendario. Conexao confirmada |

**Fluxo:** Botao "Conectar" → Redirect Google → Login → Autorizar escopos → Callback → Status "Conectado"

**Endpoint envolvido:** `GET /api/calendar/oauth/start` → Google OAuth → `GET /api/calendar/oauth/callback`

### Etapa 2: Inteligencia Artificial — Gemini API Key (01:55 - 02:04)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:55 | Secao de configuracao de IA |
| 2:04 | Insere a chave de API do Google Gemini (criada no Video 07) |

**Campo:** Google API Key (chave Gemini)

**IMPORTANTE:** Cada tenant precisa da SUA propria key. Sem ela: `GEMINI_NOT_CONFIGURED`.

### Etapa 3: GoHighLevel (02:04 - 02:21)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:04 | Secao de configuracao GHL |
| 2:04 | Insere tokens e IDs: Location ID, PIT, Pipeline ID, Calendar ID |
| 2:21 | Configuracao GHL salva |

**Campos preenchidos (mesmo do Video 06, mas agora via frontend):**
- GHL Location ID
- GHL PIT (Private Integration Token)
- GHL Pipeline ID
- GHL Calendar ID

### Etapa 4: Email / SMTP (02:21 - 02:50)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:21 | Secao de configuracao de Email/SMTP |
| 2:21 | Mostra o processo de gerar uma senha de aplicativo no Google |
| 2:50 | Campos SMTP preenchidos e salvos |

**Campos preenchidos:**
```
SMTP Host: smtp.gmail.com
SMTP Port: 587
SMTP User: email@gmail.com
SMTP Password: xxxx xxxx xxxx xxxx (app password sem espacos)
From Email: email@gmail.com
```

**Como gerar App Password:**
1. https://myaccount.google.com/security → 2FA ativado
2. https://myaccount.google.com/apppasswords → "Growth AI" → Gerar
3. Copiar senha (16 caracteres, remover espacos)

### Etapa 5: Horarios e Localizacao (02:50 - 03:16)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:50 | Ajuste dos horarios de expediente |
| 2:50 | Configuracao da localizacao (UF/estado) |
| 3:16 | Checklist verde — todas as integracoes OK |

**Campos:**
```
Business Hours Start: 9
Business Hours End: 18
Estado: SC (ou UF do cliente)
Feriado Estadual: True/False
```

**Checklist verde:** Todos os modulos (Calendar, Gemini, GHL, SMTP, WhatsApp) mostram status "OK" ou "Conectado".

### Etapa 6: Perfil do Agente + WhatsApp (03:16 - 04:16)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 3:16 | Configuracao do perfil do agente (descricao da missao, nomes) |
| 3:16 | Integracao final com WhatsApp usando tokens da instancia Z-API |
| 4:16 | Todas as integracoes completas. FIM |

**Perfil do agente:**
- Nome do atendente
- Descricao/missao da empresa
- Tom de comunicacao

**WhatsApp (Z-API) — mesmos campos do Video 08:**
- Instance ID
- Instance Token
- Client Token

---

## Ordem das Integracoes (recomendada)

```
1. Google Calendar (OAuth)
2. Gemini API Key
3. GoHighLevel (Location, PIT, Pipeline, Calendar)
4. Email/SMTP (Gmail app password)
5. Horarios + Localizacao
6. Perfil do Agente
7. WhatsApp (Z-API tokens)
→ Checklist verde = pronto para operar
```

---

## Checklist de Verificacao

- [ ] Google Calendar conectado (status "Conectado" no frontend)
- [ ] Gemini API Key inserida
- [ ] GHL: Location ID, PIT, Pipeline ID, Calendar ID preenchidos
- [ ] SMTP configurado e testado
- [ ] Horarios de expediente definidos
- [ ] Estado/UF selecionado
- [ ] Perfil do agente preenchido (nome, missao)
- [ ] WhatsApp (Z-API) conectado
- [ ] Checklist da plataforma TODO VERDE

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Google Calendar nao conecta | OAuth credentials nao configuradas no backend | Verificar `key/oauth-client-credentials.json` e `GOOGLE_OAUTH_*` no `.env` |
| Checklist mostra item vermelho | Uma integracao faltando ou com erro | Clicar no item para ver detalhes. Endpoint: `GET /api/v1/tenant/health` |
| SMTP "Authentication failed" | App password errada ou 2FA desativado | Gerar nova app password em myaccount.google.com/apppasswords |
| WhatsApp "Desconectado" | Instancia Z-API nao esta online | Verificar no painel Z-API se o QR Code foi escaneado |
| Gemini "Not configured" | Key nao foi salva | Reinserir key e salvar. Verificar logs: `[GEMINI]` |

---

## Nota Tecnica

Este video mostra que TODAS as integracoes sao configuradas pelo FRONTEND (nao pelo `.env`). Em producao multi-tenant:
- Cada cliente configura suas proprias credenciais em `/perfil/configuracoes`
- O `ConfigResolver` resolve as credenciais do banco (`TenantSettings`)
- O `.env` e usado apenas como fallback do owner/dev
- Campos sensiveis sao armazenados criptografados (Fernet AES-128)

---

## Documentacao Relacionada

- docs/GA-004-profile-settings-api.md — API de configuracoes do tenant
- docs/GA-007-README.md — Gemini multi-tenant
- docs/OAUTH-CALENDAR-FASE0-DECISOES.md — decisoes OAuth Calendar
- Video 06 — GHL via .env (equivalente manual)
- Video 07 — Gemini via .env (equivalente manual)
- Video 08 — Z-API via .env (equivalente manual)
- Video 17 — passo anterior: acesso inicial
- Video 19 — proximo passo: demonstracao pratica
