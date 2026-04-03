# GrowthAI Support Skill

**An AI-powered technical support system for the GrowthAI platform, built as a Claude Code skill with RAG (Retrieval-Augmented Generation).**

When a support question comes in, Claude Code automatically searches a local vector database of 1,110+ indexed chunks across 61 files, finds the most relevant documentation, and answers with exact sources and video timestamps.

---

## What is GrowthAI?

GrowthAI is a multi-tenant SaaS platform by [Accelera 360](https://accelera360.com.br) that automates the full sales lead pipeline via WhatsApp using AI agents (Google Gemini via ADK).

```
Lead enters (Google Forms / CRM / Inbound WhatsApp)
  -> AI Agent contacts lead via WhatsApp (Z-API)
  -> Conducts qualifying conversation (BANT / GPCT)
  -> Scores lead 0-10
  -> Routes to CRM pipeline (GoHighLevel)
  -> Schedules meeting on Google Calendar
  -> Sends confirmation email via SMTP
```

**Stack:** Python/Django + Next.js + Google ADK (Gemini) + PostgreSQL + Redis + Docker + GCP

---

## What This Repo Contains

```
growthai-support-skill/
|
|-- SKILL.md                    # Main knowledge base (700+ lines)
|                                 Architecture, setup, deploy, env vars,
|                                 troubleshooting, API routes, qualification
|                                 rules, and the video index with quick
|                                 reference tables.
|
|-- videos/                     # 21 detailed video guides
|   |-- 01-clonando-repositorio.md
|   |-- 02-arquivo-env.md
|   |-- 03-missao-identidade.md
|   |-- 04-frontend-variaveis.md
|   |-- 05-rodando-local-docker-ngrok.md
|   |-- 06-configuracao-ghl.md
|   |-- 07-google-ai-studio-gemini.md
|   |-- 08-configuracao-zapi.md
|   |-- 09-gcp-firewall-vm-serviceaccount.md
|   |-- 10-ip-estatico-gcp.md
|   |-- 11-cicd-deploy-gitlab.md
|   |-- 12-validando-containers-ssh.md
|   |-- 13-comprar-dominio.md
|   |-- 14-dns-hostinger-ip-estatico.md
|   |-- 15-cloudflare-hostinger.md
|   |-- 16-nginx-ssl-certbot.md
|   |-- 17-config-ambiente-acesso.md
|   |-- 18-integracoes-plataforma.md
|   |-- 19-demo-agente-acao.md
|   |-- 20-ghl-variaveis-detalhado.md
|   |-- 21-google-cloud-oauth-calendar.md
|
|-- rag/                        # RAG system (semantic search)
|   |-- index_knowledge.py        # Indexes all .md files into ChromaDB
|   |-- query_knowledge.py        # Queries the vector DB
|   |-- chroma_db/                # (generated, gitignored)
|
|-- README.md                   # This file
```

---

## How It Works

### 1. Knowledge Base (`SKILL.md` + `videos/`)

Every training video from the Accelera Drive was transcribed second-by-second and converted into structured markdown files. Each file contains:

- **Timeline tables** with exact timestamps for every action
- **Exact commands** (copy-pasteable)
- **Verification checklists** to confirm each step was done
- **Common problems + solutions** table
- **Technical notes** for advanced support
- **Cross-references** to related videos and repo docs

### 2. RAG Engine (`rag/`)

All documentation (skill files + GrowthAI repo docs + `.env.example` + policies) is chunked by markdown headers and indexed into a local ChromaDB vector database using `all-MiniLM-L6-v2` sentence embeddings.

**Stats:**
- 1,110 semantic chunks
- 61 source files
- ~3,700 lines of documentation
- Searches in < 1 second (after model warm-up)

### 3. Claude Code Integration

When the `/recall-growthai` command is invoked in Claude Code:

1. The `SKILL.md` is loaded into context (architecture, troubleshooting, quick references)
2. The embedding model is pre-loaded (warm-up query)
3. For every subsequent question, Claude automatically runs:
   ```bash
   python rag/query_knowledge.py "the user's question"
   ```
4. The top 5 results (ranked HIGH/MED/LOW) are returned with source + section
5. Claude answers using the retrieved context, citing exact sources and video timestamps

**The user never runs Python manually.** Claude does it automatically via Bash tool.

---

## Setup

### Prerequisites

- Python 3.10+
- [Claude Code](https://claude.ai/code) CLI installed

### Install

```bash
# Clone this repo into the Claude Code skills directory
git clone https://github.com/PAMF2/growthai-support-skill.git \
  ~/.claude/skills/recall-growthai

# Install Python dependencies
pip install chromadb sentence-transformers

# Index the knowledge base (first time only, ~30s)
cd ~/.claude/skills/recall-growthai/rag
python index_knowledge.py
```

### If you also have the GrowthAI repo

The indexer automatically includes docs from `~/Desktop/growth-ai-agents/` if it exists. To index after cloning the GrowthAI repo:

```bash
cd ~/.claude/skills/recall-growthai/rag
python index_knowledge.py
# This will index skill files + repo docs + .env.example + policies
```

### Create the Claude Code command

Create `~/.claude/commands/recall-growthai.md`:

```markdown
---
description: /recall-growthai - Load GrowthAI platform context + RAG search
---

Load the GrowthAI platform context by reading the skill file at
`~/.claude/skills/recall-growthai/SKILL.md`.

After loading, warm up the RAG engine by running:
python ~/.claude/skills/recall-growthai/rag/query_knowledge.py "growthai overview"

For EVERY question about GrowthAI, ALWAYS run this before answering:
python ~/.claude/skills/recall-growthai/rag/query_knowledge.py "THE QUESTION"
```

---

## Usage

### In Claude Code

```
> /recall-growthai
GrowthAI context loaded.
- RAG: 1,110 chunks indexed from 61 files
Ask me anything about GrowthAI.

> como resolvo redirect_uri_mismatch no oauth?
[Claude automatically queries RAG, finds Video 21 timestamp 1:25]

The redirect URI must be EXACTLY:
  https://seudominio.com/api/calendar/oauth/callback/
With the trailing slash. Without it, Google returns redirect_uri_mismatch.
(Source: Video 21 - Google Cloud OAuth, timestamp 1:25)
```

### Standalone (without Claude Code)

```bash
# Query the knowledge base directly
python rag/query_knowledge.py "como configuro o webhook da z-api"

# Output:
# [HIGH] videos/08-configuracao-zapi.md | Etapa 4: Configurar Webhook
# Volta no site da Z-API. Clica em "Instancias Web", abre sua instancia
# e clica na aba "Webhook e configuracoes gerais"...
```

---

## Video Index

| # | Title | Duration | Category |
|---|-------|----------|----------|
| 01 | Cloning the Repository | ~2:33 | Initial Setup |
| 02 | .env File | ~0:19 | Initial Setup |
| 03 | Mission & Brand Identity | ~0:58 | Branding |
| 04 | Frontend & Environment Variables | ~2:30 | Configuration |
| 05 | Running Locally (Docker + Ngrok) | ~3:26 | Local Dev |
| 06 | GHL Configuration (CRM) | ~2:47 | Integration |
| 07 | Google AI Studio (Gemini Key) | ~1:23 | Integration |
| 08 | Z-API Configuration (WhatsApp) | ~1:19 | Integration |
| 09 | GCP: Firewall + VM + Service Account | ~6:44 | GCP Infra |
| 10 | Static IP on VM | ~1:45 | GCP Infra |
| 11 | CI/CD and Deploy (GitLab) | ~3:13 | CI/CD |
| 12 | Validating Containers (SSH) | ~1:00 | Verification |
| 13 | Buying a Domain | ~4:39 | Domain/DNS |
| 14 | DNS: Point Domain to IP | ~1:34 | Domain/DNS |
| 15 | Cloudflare with Hostinger | ~3:11 | CDN/Protection |
| 16 | NGINX + SSL (Certbot) | ~3:10 | Web Server |
| 17 | Environment Config + Initial Access | ~1:17 | Onboarding |
| 18 | Platform Integrations (Frontend) | ~2:59 | Integrations |
| 19 | Demo: Agent in Action | ~3:09 | Demo |
| 20 | GHL Variables (Detailed) | ~2:30 | Integration |
| 21 | Google Cloud OAuth + Calendar | ~3:28 | Integration |

---

## Adding New Videos

1. Create a new file in `videos/` following the existing format:
   - Timeline tables with timestamps
   - Commands section
   - Checklist
   - Problems + solutions table
   - Technical notes

2. Update the video index table in `SKILL.md`

3. Re-index:
   ```bash
   cd rag && python index_knowledge.py
   ```

---

## Architecture

```
User asks question
       |
       v
Claude Code reads SKILL.md (loaded by /recall-growthai)
       |
       v
Claude runs: python rag/query_knowledge.py "question"
       |
       v
ChromaDB semantic search (all-MiniLM-L6-v2 embeddings)
       |
       v
Top 5 results returned with relevance score + source + section
       |
       v
Claude synthesizes answer citing sources and video timestamps
```

---

## License

Private. Internal use only for Accelera 360 technical support.
