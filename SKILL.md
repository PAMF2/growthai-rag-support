---
name: recall-growthai
description: Load complete GrowthAI platform context — architecture, setup, deployment, troubleshooting, and support knowledge base
user_invocable: true
trigger: /recall-growthai
---

# /recall-growthai — GrowthAI Support Knowledge Base

When this skill is invoked, load the following context into the conversation and confirm readiness.

---

## WHAT IS GROWTHAI

GrowthAI is a **multi-tenant SaaS platform** by Accelera 360 that automates the full sales lead pipeline via WhatsApp using AI agents (Google Gemini via ADK).

**Flow:**
```
Lead enters (Google Forms / CRM / Inbound WhatsApp)
  → Stored in Google Cloud Storage
  → AI Agent contacts lead via WhatsApp (Z-API)
  → Conducts qualifying conversation (BANT or GPCT_LIGHT)
  → Scores lead 0-10 → hot / warm / cold / not_qualified
  → Routes to CRM pipeline (GoHighLevel)
  → Schedules meeting on Google Calendar
  → Sends confirmation email via SMTP
```

**Mission:** Accelera 360 accelerates digital transformation in Latin America by implementing AI Agent Flows in client operations.

---

## TECH STACK

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django 5.2, DRF, ASGI (Gunicorn + Uvicorn) |
| AI/Agents | Google ADK 1.18.0, Gemini 2.5 Flash (fallback: Gemini 2.5 Pro) |
| Frontend | Next.js 15, React 19, TypeScript 5, Tailwind, shadcn/ui, pnpm |
| Database | PostgreSQL 15 (prod) / SQLite (dev fallback) |
| Cache/Sessions | Redis 7 (ADK sessions stored here) |
| WhatsApp | Z-API (instances per tenant) |
| CRM | GoHighLevel (GHL) via MCP toolset |
| Calendar | Google Calendar API (OAuth per tenant) |
| Storage | Google Cloud Storage (lead files) |
| Email | Gmail SMTP (app password) |
| Infra | Docker Compose, GCP VM (e2-medium), NGINX + Certbot SSL |
| CI/CD | GitLab CI (.gitlab-ci.yml) |
| Observability | OpenTelemetry + GCP exporters |
| ML extras | scikit-learn, faiss-cpu, pandas |

---

## ARCHITECTURE

### Docker Services (docker-compose.yml)

```
postgres-db        ← PostgreSQL 15 (port 5432)
redis-server       ← Redis 7 (internal 6379, external 6380)
migrator           ← One-shot: makemigrations + migrate + bootstrap_app
application-api    ← Django ASGI API (port 8081→8000, WORK=false)
application-api-tasks ← Django background worker (WORK=true, ENABLE_SCHEDULER=true)
application-frontend  ← Next.js (port 3000→80)
```

### Agent Orchestration (Google ADK)

```
root_agent (gemini-2.5-flash)
│   Tools: consultar_lead, send_whatsapp_message, detect_lead_response,
│          update_context_crm, calendar_tool, lead_locking, atualizar_lead, ghl_mcp
│
├── Score_Classifier    ← BANT/GPCT scoring (0-10)
├── Segregator_Register ← CRM pipeline placement (GHL)
└── SDR_Whats          ← WhatsApp conversation driver
```

Each call to `build_root_agent()` creates a **fresh isolated agent instance** (no race conditions).

### Multi-Tenancy

Each user (tenant) has isolated:
- Gemini API key (stored encrypted in DB, resolved by ConfigResolver)
- GHL credentials (location_id, pipeline_id, private_key)
- WhatsApp instance (Z-API instance_id + token)
- Google Calendar OAuth token
- SMTP credentials
- GCS bucket prefix

**ConfigResolver priority:** TenantSettings (DB) → global defaults → .env (infra fallback only)

### Key Django Models (web/models.py)

- `CustomUser` — AUTH_USER_MODEL, tenant identity
- `TenantSettings` — 30+ fields, encrypted secrets (Fernet AES-128), auto-created via signal
- `WhatsAppMessage` — full audit trail per lead per user
- `ProcessedLead` — idempotency + runner state tracking
- `AgentSession` — shared session state across processes
- `ProfileSettings` — per-tenant UI and corporate config
- `CalendarOAuthAuditEvent` — Google Calendar OAuth audit log
- `WebhookEvent` — webhook debugging

### Request Flow (Webhook → Agent)

```
WhatsApp reply → POST /webhook/whatsapp/ → web/views.py
  → background task dispatched
  → ADK session resumed from Redis
  → ConfigResolver resolves tenant credentials
  → agent continues conversation
```

### Inbound Unknown Numbers

When a number contacts without existing lead record:
- Tagged with `[INBOUND_DESCONHECIDO]` in prompt
- SDR switches to welcoming mode (no outbound pitch)
- Distinct from `[SESSAO_RETOMADA]` (existing lead, new ADK session)

---

## KEY DIRECTORIES

```
app/                        ← Core AI application
  agent.py                  ← Root orchestrator agent factory
  sub_agents/               ← score_classifier/, sdr_whats/, segregator_register/
  tools/                    ← 20+ tool functions (calendar, whatsapp, lead, GHL, scoring, locking)
  jobs/                     ← Background jobs (process_new_leads_whatsapp, update_lead_bucket)
  config/                   ← JSON configs (fallback_rules, lead_mapping, tags)
  gemini_client.py          ← Per-tenant Gemini key resolution
  audio_transcription.py    ← Gemini Files API transcription (audio→text middleware)

web/                        ← Django app
  models.py                 ← All models (CustomUser, TenantSettings, WhatsAppMessage, etc.)
  views/                    ← Views including processing.py (webhook handler, retry logic)
  config_resolver.py        ← Multi-tenant config resolution
  crypto_utils.py           ← Fernet encryption for secrets
  services/                 ← Calendar OAuth, credentials, audit log
  signals.py                ← Auto-create TenantSettings on user creation
  management/commands/       ← whatsapp_session_clear, inspect, history, calendar_oauth_metrics

config/                     ← Django project config
  settings.py               ← All settings including 20+ ADK_* tuning knobs
  urls.py                   ← URL routes
  asgi.py / wsgi.py

frontend/                   ← Next.js 15 app
  pages/                    ← Next.js pages
  components/               ← React components (chat, sidebar, agents UI, settings)
  lib/translations/         ← pt-BR and en-US

policies/                   ← YAML-driven qualification rules
  qualification.yaml        ← BANT/GPCT thresholds (hot>=8, warm>=6, cold>=4)
  cadence.yaml              ← Segment→pipeline mapping (vip>=8.5, priority>=7, nurture>=5)

observability/              ← OpenTelemetry / GCP module
oraicle/                    ← Legacy compatibility shim (oraicle.tools → app.tools)
key/                        ← Google OAuth credentials (gitignored)
auth-calendar-master/       ← Standalone Google Calendar OAuth portal
scripts/                    ← Utility scripts (validar_gemini_keys.py)
tests/                      ← Test suite
```

---

## HOW TO SET UP — LOCAL (Dev)

### Prerequisites
- Docker + Docker Compose installed
- `.env` file configured (see ENV VARS section)
- `key/credentials.json` (Google OAuth)
- `key/mvp-agentes-accelera.json` (GCS service account) — optional for local

### Steps

```bash
# 1. Clone
git clone https://gitlab.com/accelera3601/growth-ai-agents.git
cd growth-ai-agents

# 2. Create .env from template (see README_ENV.md for all vars)
cp .env.example .env  # or create manually

# 3. Start dev environment
docker-compose -f docker-compose.dev.yml up

# This starts:
# - PostgreSQL 15 (port 5432)
# - Redis 7 (port 6380)
# - Backend Django with hot-reload (port 8081)
# - Frontend Next.js dev mode (port 3000)
# - Background tasks worker

# 4. Create superuser
docker exec -it application-api-dev python manage.py createsuperuser

# 5. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8081
# Django Admin: http://localhost:8081/admin
```

### Dev Docker Compose differences
- Builds from local Dockerfile (not registry images)
- Volumes mounted for hot-reload (backend: `.:/app`, frontend: `./frontend:/app`)
- Frontend runs `pnpm dev` instead of production build
- Worker has `RUN_DB_SETUP=false` to avoid migration race conditions

---

## HOW TO DEPLOY — GCP (Production)

### Infrastructure Setup (one-time)

1. **Create GCP Project** — Console → New Project

2. **Firewall Rules** (5 rules, all Ingress, All instances, 0.0.0.0/0):
   - `allow-ssh` → tcp:22
   - `allow-http` → tcp:80
   - `allow-https` → tcp:443
   - `allow-backend-8000` → tcp:8000
   - `allow-frontend-3000` → tcp:3000

3. **Create VM**:
   - Machine: `e2-medium` (minimum)
   - OS: Ubuntu 22.04 or 24.04 LTS
   - Check: Allow HTTP + HTTPS traffic

4. **Static IP**:
   - VPC Network → IP Addresses → Reserve Static Address
   - Associate to VM (change from Ephemeral to Static)

5. **Service Account** (`gitlab-ci-deploy`):
   - Roles: Compute Instance Admin (v1), Service Account User, Compute Viewer
   - Create JSON key → save as `key/gcp-key-work.json`

6. **Install Docker on VM**:
   ```bash
   sudo apt update && sudo apt install -y docker.io git curl wget docker-compose
   sudo systemctl enable docker && sudo systemctl start docker
   sudo usermod -aG docker $USER && newgrp docker
   sudo mkdir -p /opt/app && sudo chown -R $USER:$USER /opt/app
   ```

### CI/CD Pipeline (.gitlab-ci.yml)

**Stages:** build_frontend → build_backend → deploy

**Gate:** Only runs on `CI_DEPLOY_BRANCH` (set in .env)

**Deploy process:**
1. Authenticates with GCP via service account JSON
2. SCPs `docker-compose.yml` + `.env` to VM at `/opt/app`
3. Pulls new images, runs `docker compose up -d --force-recreate`
4. Healthcheck: polls 12x (5s each) for all containers healthy/running
5. **Auto-rollback** on failure: restores `docker-compose.rollback.yml`

**Required CI .env vars:**
```env
CI_DEPLOY_BRANCH=feature/ci-cd    # Branch that triggers deploy
CI_REGISTRY_NAMESPACE=accelera3601/growth-ai
CI_FRONTEND_TAG=frontend.v1
CI_BACKEND_TAG=backend.v1
GCP_VM_INSTANCE_NAME=vm-work
GCP_VM_ZONE=us-central1-c
GCP_VM_HOST=<static-ip>
GCP_VM_USER=<vm-username>
GCP_PROJECT_ID=<gcp-project-id>
```

### NGINX + SSL (on VM)

```bash
# Install
sudo apt install nginx -y

# Create site config
sudo vim /etc/nginx/sites-available/yourdomain

# Content: proxy / → localhost:3000, /api/ → localhost:8081, /webhooks/ → localhost:8081
# (with long timeouts for webhook/agent processing: 300s read/send timeout)

# Enable + test
sudo ln -s /etc/nginx/sites-available/yourdomain /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL with Certbot
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain -d www.yourdomain
```

---

## ENV VARS — COMPLETE REFERENCE

### Fixed (don't change)
```env
POLLING_INTERVAL_SECONDS=300
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
POSTGRES_HOST=postgres-db       # Docker service name
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CI_REGISTRY=registry.gitlab.com
CI_REGISTRY_IMAGE=registry.gitlab.com/accelera360
ADK_APP_NAME=growth-ai-whatsapp
DEPLOY_PATH=/opt/app
```

### Configurable per client/environment
```env
# Django
DJANGO_SECRET_KEY=<generate-unique>
DEBUG=False                      # MUST be False in production
LOG_LEVEL=INFO

# Database
POSTGRES_DB=growthai
POSTGRES_USER=accelera-user
POSTGRES_PASSWORD=<secure-password>

# Encryption
SETTINGS_CRYPTO_KEY=<fernet-key>  # python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'

# Frontend
FRONTEND_DOMAIN=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com   # In docker-compose.yml line ~107

# Email/SMTP
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=<gmail-app-password>     # No spaces!
DEFAULT_FROM_EMAIL=email@gmail.com

# Google Calendar
GOOGLE_CALENDAR_ID=primary
GOOGLE_CREDENTIALS_PATH=key/credentials.json
TIMEZONE=America/Sao_Paulo

# Google Cloud Storage
USE_GCS_LEADS=true
GCS_BUCKET_NAME=lead_contacts
GCS_PROJECT_ID=<gcp-project-id>
GOOGLE_APPLICATION_CREDENTIALS=key/mvp-agentes-accelera.json

# WhatsApp (Z-API) — per tenant
Z_API_INSTANCE_ID=<instance>
Z_API_TOKEN=<token>
Z_API_CLIENT_TOKEN=<client-token>

# GoHighLevel — per tenant
USE_GHL_API=true
GHL_MCP_URL=https://services.leadconnectorhq.com/mcp/
GHL_LOCATION_ID=<location>
GHL_CALENDAR_ID=<calendar>
GHL_PIPELINE_ID=<pipeline>
GHL_PIT=<pit>
GHL_PRIVATE_KEY=<private-key>

# Business
ESTADO_ALUNO=SC                  # State for holiday rules (2-letter code)
BUSINESS_HOURS_START=9
BUSINESS_HOURS_END=18
FERIADO_ESTADUAL=True

# Branding
TITULO_MENU="Accelera"
NAME_ATENDENTE_CHAT="Kelvin"
CORPORATE_NAME="ACCELERA360"
LINK_PROJETO="https://accelera360.com.br/"
```

### ADK Tuning Knobs (advanced)
```env
ADK_MAX_CONCURRENT_CALLS=50
ADK_MIN_REQUEST_INTERVAL_SECONDS=0.5
ADK_AGENT_EXECUTION_TIMEOUT_SECONDS=180
ADK_503_MAX_ATTEMPTS=5
ADK_503_RETRY_DELAY_SECONDS=3.0
ADK_503_BACKOFF_MULT=2.0
ADK_503_MAX_DELAY_SECONDS=30.0
ADK_503_JITTER_SECONDS=1.0
ADK_503_FALLBACK_MODEL=gemini-2.5-pro
ADK_RESOURCE_EXHAUSTED_MAX_ATTEMPTS=4
ADK_RESOURCE_EXHAUSTED_RETRY_DELAY_SECONDS=2.0
ADK_RESOURCE_EXHAUSTED_BACKOFF_MULT=1.5
ADK_RESOURCE_EXHAUSTED_MAX_DELAY_SECONDS=30.0
ADK_APPOINTMENT_EARLY_FINALIZE_SECONDS=12
```

---

## GOOGLE SETUP (Calendar + SMTP)

### Google Cloud Console (https://console.cloud.google.com/)
1. Create/select project
2. Enable APIs: **Google Calendar API** + **Google Drive API**
3. OAuth Consent Screen: External, add company email as test user
4. Create OAuth credentials: Desktop app → download `credentials.json` → save to `key/credentials.json`
5. First run: browser opens, login with test user, authorize → creates `key/token.json`

### Gmail SMTP
1. Enable 2FA: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords → "Growth AI"
3. Use generated password (remove spaces) in `EMAIL_HOST_PASSWORD`

### Per-Tenant Gemini Keys (GA-007)
- Each tenant MUST have their own Gemini API key in profile settings
- Without it: `GEMINI_NOT_CONFIGURED` / `SetupPendingError`
- Get key: https://aistudio.google.com/app/apikey
- Validate: `python scripts/validar_gemini_keys.py`
- Logs: `source=tenant` = correct; `source=env` = missing key (red flag in prod)

---

## TROUBLESHOOTING

### Agent not responding
1. Check container is running: `docker ps`
2. Check logs: `docker compose logs -f application-api`
3. Check Redis: `docker exec redis-server redis-cli ping`
4. Check Gemini key: `GET /api/v1/tenant/settings` → `google_api_key_configured: true`?
5. Check ADK session: `python manage.py whatsapp_session_inspect --phone <number> --user-id <id>`

### Webhook not receiving
1. Check NGINX config: `sudo nginx -t`
2. Check webhook URL in Z-API points to `https://yourdomain/webhook/whatsapp/`
3. Check SSL: `sudo certbot certificates`
4. Check container: `docker logs application-api -f --tail=100`
5. Check WebhookEvent table in Django admin

### Agent repeats greeting / loses context
1. Session may have been recreated: check for `[SESSAO_RETOMADA]` in logs
2. Redis may have evicted session: check Redis memory (`docker exec redis-server redis-cli info memory`)
3. Clear and restart: `python manage.py whatsapp_session_clear --phone <number> --user-id <id>`

### 503 errors / Gemini overloaded
1. Check logs for `[503_RETRY]`, `[503_FALLBACK]`, `[503_FINAL]`
2. Tune: `ADK_503_MAX_ATTEMPTS`, `ADK_503_RETRY_DELAY_SECONDS`
3. Fallback model: `ADK_503_FALLBACK_MODEL=gemini-2.5-pro`
4. Consider: user might need higher Vertex quota

### Calendar not working
1. Check OAuth: `GET /api/calendar/oauth/status`
2. Check credentials: `key/credentials.json` exists, `key/token.json` generated
3. Check logs: filter by `[CALENDAR_OAUTH]`
4. Metrics: `python manage.py calendar_oauth_metrics --days 7`
5. `invalid_grant` = token expired, need re-auth

### Deploy failed
1. Check GitLab CI pipeline logs
2. Verify `.env` CI vars (CI_DEPLOY_BRANCH matches pushed branch)
3. Check `key/gcp-key-work.json` exists and SA has correct roles
4. SSH to VM: `gcloud compute ssh <user>@<vm> --zone <zone>`
5. On VM: `docker compose logs`, `docker ps -a`

### Database issues
1. Check migrations: `docker exec application-api python manage.py showmigrations`
2. Force migrate: `docker exec application-api python manage.py migrate`
3. Check connection: `docker exec postgres-db pg_isready`

---

## MANAGEMENT COMMANDS

```bash
# WhatsApp session management
python manage.py whatsapp_session_clear --phone <number> --user-id <id>
python manage.py whatsapp_session_inspect --phone <number> --user-id <id>
python manage.py whatsapp_session_history --phone <number> --user-id <id> --limit 20

# Calendar OAuth metrics
python manage.py calendar_oauth_metrics --days 7

# Validate Gemini keys across tenants
python scripts/validar_gemini_keys.py

# Create superuser
python manage.py createsuperuser

# Bootstrap app (creates default data)
python manage.py bootstrap_app

# Generate encryption key
python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'

# Test calendar connection
python -c "from app.tools.calendar_tool import check_calendar_availability; print(check_calendar_availability())"
```

---

## QUALIFICATION & CADENCE

### Scoring Frameworks
- **BANT:** Budget (25pts) + Authority (25pts) + Need (25pts) + Timeline (25pts) = 100 → normalized to 0-10
- **GPCT_LIGHT (simplified):** Interesse (50pts) + Capacidade (50pts) = 100 → normalized to 0-10

### Thresholds
| Score | Label | Action |
|-------|-------|--------|
| >= 8.0 | hot | Immediate handoff |
| 6.0-7.9 | warm | Active follow-up |
| 4.0-5.9 | cold | Controlled nurturing |
| < 4.0 | not_qualified | Long-term |

### Cadence Mapping
| Score | Segment | Pipeline | Frequency |
|-------|---------|----------|-----------|
| 8.5-10.0 | vip | vip_pipeline | Daily |
| 7.0-8.4 | priority | priority_pipeline | 2x/week |
| 5.0-6.9 | nurture | nurture_program | Weekly |
| 0-4.9 | long_term | segmentation_pending | Monthly |

---

## API ROUTES (key endpoints)

```
# Auth
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/forgot-password
POST /api/auth/reset-password

# Profile & Settings
GET|PATCH /api/v1/tenant/settings        ← tenant config (masked secrets)
GET /api/v1/tenant/health                ← per-module health status
GET|PATCH /api/profile/settings

# Calendar OAuth
GET /api/calendar/oauth/start            ← initiates OAuth flow
GET /api/calendar/oauth/callback         ← OAuth redirect
GET /api/calendar/oauth/status           ← connection status
POST /api/calendar/oauth/disconnect

# WhatsApp
GET /api/whatsapp/status
POST /api/whatsapp/connect
POST /api/whatsapp/disconnect

# Agents
GET /api/agents/status
GET /api/agents/metrics
GET /api/agents/sessions
GET /api/agents/conversations/active

# Webhooks
POST /webhook/whatsapp/                  ← Z-API webhook (multiple alias paths)

# Metrics
GET /api/metricas/
```

---

## RELEASE NOTES (Latest: 2026-03-27)

Key features in current release:
- **Audio input support** — agent receives audio + text, always responds in text
- **Inbound unknown numbers** — `[INBOUND_DESCONHECIDO]` tag for first-contact leads not in DB
- **GHL + Google Calendar** integration for automatic scheduling
- **Per-tenant Gemini keys** (GA-007) — each client uses their own API key
- **503 retry with fallback** — exponential backoff + model fallback on Gemini overload
- **Frontend-driven config** — Calendar, SMTP settings all via UI, not .env

---

## TRAINING VIDEOS (from Accelera Drive)

Videos are stored on Google Drive. Each video has a dedicated .md file in `videos/` with full timestamps, commands, checklists, and troubleshooting.

### Video Index

| # | Titulo | Duracao | Categoria | Arquivo |
|---|--------|---------|-----------|---------|
| 01 | Clonando o Repositorio | ~2:33 | Setup Inicial | [videos/01-clonando-repositorio.md](videos/01-clonando-repositorio.md) |
| 02 | Arquivo .env | ~0:19 | Setup Inicial | [videos/02-arquivo-env.md](videos/02-arquivo-env.md) |
| 03 | Missao e Identidade | ~0:58 | Branding | [videos/03-missao-identidade.md](videos/03-missao-identidade.md) |
| 04 | Frontend e Variaveis | ~2:30 | Configuracao | [videos/04-frontend-variaveis.md](videos/04-frontend-variaveis.md) |
| 05 | Rodando Local (Docker + Ngrok) | ~3:26 | Setup Local | [videos/05-rodando-local-docker-ngrok.md](videos/05-rodando-local-docker-ngrok.md) |
| 06 | Configuracao do GHL | ~2:47 | Integracao CRM | [videos/06-configuracao-ghl.md](videos/06-configuracao-ghl.md) |
| 07 | Google AI Studio (Gemini Key) | ~1:23 | Integracao AI | [videos/07-google-ai-studio-gemini.md](videos/07-google-ai-studio-gemini.md) |
| 08 | Configuracao da Z-API | ~1:19 | Integracao WhatsApp | [videos/08-configuracao-zapi.md](videos/08-configuracao-zapi.md) |
| 09 | GCP: Firewall + VM + Service Account | ~6:44 | Infraestrutura GCP | [videos/09-gcp-firewall-vm-serviceaccount.md](videos/09-gcp-firewall-vm-serviceaccount.md) |
| 10 | IP Estatico na VM | ~1:45 | Infraestrutura GCP | [videos/10-ip-estatico-gcp.md](videos/10-ip-estatico-gcp.md) |
| 11 | CI/CD e Deploy (GitLab) | ~3:13 | CI/CD e Deploy | [videos/11-cicd-deploy-gitlab.md](videos/11-cicd-deploy-gitlab.md) |
| 12 | Validando Containers (SSH) | ~1:00 | Verificacao | [videos/12-validando-containers-ssh.md](videos/12-validando-containers-ssh.md) |
| 13 | Como Comprar seu Dominio | ~4:39 | Dominio/DNS | [videos/13-comprar-dominio.md](videos/13-comprar-dominio.md) |
| 14 | DNS: Apontar Dominio para IP | ~1:34 | Dominio/DNS | [videos/14-dns-hostinger-ip-estatico.md](videos/14-dns-hostinger-ip-estatico.md) |
| 15 | Cloudflare com Hostinger | ~3:11 | CDN/Protecao | [videos/15-cloudflare-hostinger.md](videos/15-cloudflare-hostinger.md) |
| 16 | NGINX + SSL (Certbot) | ~3:10 | Web Server/SSL | [videos/16-nginx-ssl-certbot.md](videos/16-nginx-ssl-certbot.md) |
| 17 | Config Ambiente + Acesso Inicial | ~1:17 | Onboarding | [videos/17-config-ambiente-acesso.md](videos/17-config-ambiente-acesso.md) |
| 18 | Integracoes da Plataforma (Frontend) | ~2:59 | Integracoes | [videos/18-integracoes-plataforma.md](videos/18-integracoes-plataforma.md) |
| 19 | Demo: Agente em Acao (WhatsApp → Agenda) | ~3:09 | Demonstracao | [videos/19-demo-agente-acao.md](videos/19-demo-agente-acao.md) |
| 20 | GHL Variaveis (Detalhado) | ~2:30 | Integracao CRM | [videos/20-ghl-variaveis-detalhado.md](videos/20-ghl-variaveis-detalhado.md) |
| 21 | Google Cloud OAuth + Calendar | ~3:28 | Integracao Google | [videos/21-google-cloud-oauth-calendar.md](videos/21-google-cloud-oauth-calendar.md) |

### Quick Reference — Common Support Questions → Video

| Pergunta do cliente | Video | Timestamp |
|--------------------|-------|-----------|
| "Como clono o repositorio?" | 01 | 0:40 |
| "Qual meu username do GitLab?" | 01 | 1:00 |
| "Como configuro o remote?" | 01 | 2:00 |
| "Cadê o arquivo .env?" | 02 | 0:10 |
| "Como renomear env.example?" | 02 | 0:12 |
| "Como mudo o nome do bot no WhatsApp?" | 03 | 0:39 (NAME_ATENDENTE_CHAT) |
| "Como mudo o nome da empresa?" | 03 | 0:41 (CORPORATE_NAME) |
| "Onde configuro o dominio?" | 04 | 0:28 (api.ts), 0:55 (.env), 1:18 (docker-compose) |
| "Como crio o superusuario?" | 04 | 1:54 |
| "Frontend nao conecta na API" | 04 | Checar os 3 arquivos de dominio |
| "Como rodo local com Docker?" | 05 | 0:39 (docker build) → 3:06 (docker-compose up) |
| "Como configuro o Ngrok?" | 05 | 1:28 (signup) → 2:43 (ngrok http 8081) |
| "Onde coloco o link do Ngrok?" | 05 | 2:52 (ALLOWED_HOSTS + WEBHOOK_URL) |
| "Como pego o Location ID do GHL?" | 06 | 0:33 (Configuracoes > Perfil) |
| "Como crio o PIT no GHL?" | 06 | 0:53 (Integracoes > Privado > Criar) |
| "Como pego o Pipeline ID?" | 06 | 1:40 (Leads > Pipelines > Copiar link > extrair ID) |
| "Como pego o Calendar ID do GHL?" | 06 | 2:24 (Calendarios > Configuracoes) |
| "Como crio a API Key do Gemini?" | 07 | 0:42 (Get API key > Create) |
| "Onde configuro a Z-API?" | 08 | 0:05 (Client Token) → 0:22 (Instance Token) → 0:39 (Instance ID) |
| "Como configuro o webhook na Z-API?" | 08 | 0:54 (Webhook > Ao receber > colar URL) |
| "Como crio as regras de firewall no GCP?" | 09 | 0:16 (Firewall > Create) — 5 regras |
| "Como crio a VM no GCP?" | 09 | 3:02 (Compute Engine > Create Instance) |
| "Como crio a Service Account?" | 09 | 3:57 (IAM > Service Accounts > Create) |
| "Como instalo Docker na VM?" | 09 | 5:43 (sudo apt install docker.io) |
| "Como configuro IP estatico?" | 10 | 1:03 (Reserve external static IP) |
| "Como configuro o CI/CD?" | 11 | 0:30 (variaveis no .env) → 2:07 (git push) |
| "Onde coloco a chave JSON do GCP?" | 11 | 0:06 (pasta key > gcp-key-work.json) |
| "Como vejo se o deploy funcionou?" | 12 | 0:46 (SSH > docker ps) |
| "Onde compro dominio?" | 13 | 0:20 (Hostinger) ou 1:01 (Registro.br) |
| "Como aponto dominio para a VM?" | 14 | 0:31 (registro A com IP) |
| "Como configuro Cloudflare?" | 15 | 0:20 (adicionar site) → 1:43 (trocar nameservers) |
| "Como instalo NGINX?" | 16 | 0:28 (apt install nginx) |
| "Como configuro SSL/HTTPS?" | 16 | 2:35 (certbot --nginx) |
| "Qual o bloco do NGINX?" | 16 | 1:04 (config com proxy para 3000/8081) |
| "Como configuro integracoes pelo frontend?" | 18 | 1:17 (Calendar) → 2:04 (GHL) → 2:21 (SMTP) → 3:16 (WhatsApp) |
| "Checklist nao fica verde" | 18 | 3:16 (verificar cada integracao) |
| "Como mostro a demo pro cliente?" | 19 | 4:16 (teste WhatsApp completo) |
| "Bot nao responde no WhatsApp" | 19 | Checar Gemini key + worker + Z-API |
| "Como preencho GHL no .env passo a passo?" | 20 | 0:26 (Location) → 0:56 (PIT) → 1:38 (Pipeline) |
| "Como configuro OAuth do Calendar no GCP?" | 21 | 0:00 (consent screen) → 0:57 (credentials) → 2:31 (publish) |
| "redirect_uri_mismatch no OAuth" | 21 | 1:25 (URI deve ter `/` no final) |
| "Onde coloco o JSON do OAuth?" | 21 | 2:59 (key/oauth-client-credentials.json) |

### Erros Mais Comuns por Video

| Video | Erro | Causa raiz |
|-------|------|-----------|
| 01 | "Authentication failed" | 2FA ativado no GitLab, precisa de Personal Access Token |
| 01 | Push vai pro repo errado | Esqueceu `git remote remove origin` |
| 02 | App nao inicia | Esqueceu de renomear `env.example` → `.env` |
| 03 | Bot se apresenta como "Accelera" | `NAME_ATENDENTE_CHAT` / `CORPORATE_NAME` nao alterados |
| 04 | ERR_CONNECTION_REFUSED em producao | Dominio alterado em 1 ou 2 dos 3 lugares, mas nao nos 3 |
| 04 | Login nao funciona | `APP_USERNAME`/`APP_PASSWORD` vazios no `.env` |
| 05 | "image not found" no docker-compose | Tags no `.env` nao batem com nomes do `docker build` |
| 05 | "DisallowedHost" no Django | Hostname do ngrok nao esta no `ALLOWED_HOSTS` |
| 06 | "GHL connection failed" | PIT expirado ou escopos incompletos — recriar integracao |
| 06 | Leads nao aparecem no pipeline | `GHL_PIPELINE_ID` errado — extrair so o ID da URL |
| 07 | `GEMINI_NOT_CONFIGURED` | `GOOGLE_API_KEY` vazia ou errada no `.env` |
| 07 | "Permission denied" 403 | "Generative Language API" nao habilitada no projeto GCP |
| 08 | Mensagens enviadas mas respostas nao chegam | Webhook nao configurado no painel Z-API |
| 08 | Funciona local mas para apos reiniciar | URL do Ngrok mudou — atualizar `.env` + painel Z-API |
| 09 | "Quota exceeded" ao criar VM | Cota de CPUs esgotada — trocar zona ou pedir aumento |
| 09 | SSH nao conecta na VM | Regra `allow-ssh` nao criada — verificar firewall |
| 09 | `docker: command not found` na VM | Docker nao instalou — rodar `sudo apt install docker.io` |
| 10 | IP muda apos reiniciar VM | IP nao foi convertido para Static — Video 10 |
| 11 | Pipeline nao inicia no GitLab | Branch nao bate com `CI_DEPLOY_BRANCH` |
| 11 | Deploy falha "Permission denied" | Service Account sem roles corretos — Video 09 |
| 11 | Deploy falha "key file not found" | `gcp-key-work.json` faltando na pasta `key/` |
| 12 | `docker ps` nao mostra nada | Deploy falhou — `docker ps -a` + `docker-compose logs` |
| 14 | Site nao abre apos DNS | Propagacao DNS leva ate 48h — `nslookup seudominio.com` |
| 15 | "Pending nameserver update" 24h+ | Nameservers na Hostinger nao foram trocados corretamente |
| 15 | "Too many redirects" com Cloudflare | SSL mode deve ser "Full", nao "Flexible" |
| 16 | `nginx -t` syntax error | Faltou `;` ou `}` no bloco de config |
| 16 | Certbot "could not find DNS record" | Dominio nao aponta para IP da VM — checar Video 14 |
| 16 | "502 Bad Gateway" | Containers nao estao rodando — `docker ps` |

### Cada arquivo de video contem:

- Resumo do que o video ensina
- Timeline detalhada segundo a segundo
- Comandos exatos executados (copiaveis)
- Checklist de verificacao pos-video
- Tabela de problemas comuns + solucoes
- Notas tecnicas para suporte avancado
- Links para documentacao relacionada

> Para suporte: identifique o problema → encontre o video na tabela acima → abra o .md → va direto ao timestamp + solucao.

---

## SUPPORT WORKFLOW

When providing technical support to Accelera clients:

1. **Identify the issue category** — setup, deployment, runtime, integration
2. **Check the relevant section** above
3. **Use management commands** to diagnose (session inspect, metrics, validate keys)
4. **Check logs** with appropriate prefixes: `[GEMINI]`, `[CALENDAR_OAUTH]`, `[503_RETRY]`, `[INBOUND_DESCONHECIDO]`
5. **Reference training videos** from Drive for step-by-step visual guidance
6. **Escalate** if: database corruption, security incident, or Gemini API quota/billing issues

---

## RAG — BUSCA SEMANTICA AUTOMATICA

**INSTRUCAO CRITICA PARA O CLAUDE:** Quando esta skill estiver carregada e o usuario fizer QUALQUER pergunta sobre GrowthAI, SEMPRE execute este comando Bash ANTES de responder:

```bash
python C:/Users/Pichau/.claude/skills/recall-growthai/rag/query_knowledge.py "PERGUNTA_AQUI"
```

Substitua `PERGUNTA_AQUI` pela pergunta do usuario (em portugues ou ingles). Use timeout de 30000ms pois o modelo de embeddings demora ~10s no primeiro load.

**Base:** 1,110 chunks de 61 arquivos (21 videos + repo docs + .env.example + policies + release notes).

**Regras:**
1. SEMPRE rode a query antes de responder perguntas tecnicas sobre GrowthAI
2. Use os resultados HIGH como base da resposta
3. Cite o source (video + timestamp ou doc) na resposta
4. Se nenhum resultado e HIGH, diga que nao tem certeza e sugira onde procurar
5. Se o comando demorar, nao desista — o primeiro load do modelo leva ~15s, depois fica rapido
6. Para re-indexar apos novos videos: `python C:/Users/Pichau/.claude/skills/recall-growthai/rag/index_knowledge.py`

---

*Context loaded. Ready for GrowthAI support.*
