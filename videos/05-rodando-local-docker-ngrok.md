# Video 05: Rodando o Projeto Localmente do Zero (Docker + Ngrok)

**Duracao:** ~3:26
**Categoria:** Setup Local / Dev Environment
**Pre-requisitos:** Videos 01-04 concluidos, Docker instalado, conta no ngrok.com
**Resultado esperado:** Aplicacao rodando local com containers Docker + tunel publico via Ngrok

---

## Resumo

Este video ensina a rodar o GrowthAI inteiramente local usando Docker. Inclui: build das imagens backend e frontend, configuracao das tags no `.env`, criacao de tunel publico com Ngrok (necessario para webhooks do WhatsApp) e subida dos containers com `docker-compose up`. Ao final, o frontend esta acessivel em `localhost:3000`.

---

## Timeline Detalhada

### Abertura (0:00 - 0:06)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Como rodar o projeto localmente do zero..." |

### Etapa 1: Clonar e abrir o projeto (0:07 - 0:38)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:07 | Abre o terminal. Texto instrui a clonar o repositorio |
| 0:10 | Executa no terminal: `git clone https://gitlab.com/accelera3601/growth-ai-agents.git` |
| 0:25 | Apos baixar, abre o projeto no VS Code: `code growth-ai-agents/` |

**Comandos executados:**
```bash
git clone https://gitlab.com/accelera3601/growth-ai-agents.git
code growth-ai-agents/
```

### Etapa 2: Verificar Docker e fazer build das imagens (0:39 - 1:02)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:39 | No terminal dentro do VS Code, digita `docker ps` para confirmar que nenhum container esta rodando |
| 0:43 | Digita o comando de build da imagem do Backend |
| 0:49 | Digita o comando de build da imagem do Frontend |
| 0:58 | Verifica se as imagens foram criadas: `docker images \| grep registry` |

**Comandos executados:**
```bash
# Verificar que Docker esta limpo
docker ps

# Build da imagem do Backend
docker build -t registry.gitlab.com/accelera3601/growth-ai.backend.v1-local backend/

# Build da imagem do Frontend
docker build -t registry.gitlab.com/accelera3601/growth-ai.frontend.v1-local frontend/docker/frontend/

# Verificar imagens criadas
docker images | grep registry
```

**IMPORTANTE:** Os nomes das imagens seguem o padrao `registry.gitlab.com/accelera3601/growth-ai.<tipo>.v1-local`. O sufixo `-local` diferencia das imagens de producao.

### Etapa 3: Configurar tags no .env (1:03 - 1:27)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:03 | Abre o arquivo `.env` |
| 1:11 | Vai nas linhas 309 a 313. Configura as variaveis `CI_REGISTRY_NAMESPACE`, `CI_BACKEND_TAG` e `CI_FRONTEND_TAG` para apontarem para as imagens `.v1-local` que acabaram de ser criadas |

**Variaveis a configurar no `.env` (~linhas 309-313):**
```env
CI_REGISTRY_NAMESPACE=accelera3601/growth-ai
CI_BACKEND_TAG=backend.v1-local
CI_FRONTEND_TAG=frontend.v1-local
```

**Por que:** O `docker-compose.yml` monta o nome da imagem assim: `${CI_REGISTRY}/${CI_REGISTRY_NAMESPACE}:${CI_BACKEND_TAG}`. Essas variaveis precisam bater com os nomes usados no `docker build -t`.

### Etapa 4: Configurar Ngrok (1:28 - 2:51)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:28 | Abre o navegador no site do ngrok (ngrok.com) para criar um tunel publico |
| 1:36 | Clica em Sign up, preenche Nome, E-mail, Senha |
| 2:04 | No painel do Ngrok, mostra a secao de instalacao e seleciona o sistema operacional Linux |
| 2:19 | Copia os comandos de instalacao do Ngrok via terminal e os executa no VS Code |
| 2:43 | Roda o comando `ngrok http 8081` no terminal para abrir o tunel e gerar o link HTTPS |
| 2:49 | Copia o link publico gerado (Ex: `https://abcd-123.ngrok-free.app`) |

**Comandos executados:**
```bash
# Instalar ngrok (seguir instrucoes do painel ngrok.com para seu OS)
# Autenticar
ngrok config add-authtoken <SEU_TOKEN>

# Criar tunel para a porta do backend (8081)
ngrok http 8081
```

**O que o Ngrok faz:** Cria um URL publico HTTPS (ex: `https://abcd-123.ngrok-free.app`) que aponta para seu `localhost:8081`. Isso e necessario porque o Z-API (WhatsApp) precisa de uma URL publica para enviar webhooks.

**IMPORTANTE:** O link do Ngrok muda toda vez que voce reinicia. Precisa atualizar no `.env` e no painel da Z-API.

### Etapa 5: Configurar URLs do Ngrok no .env (2:52 - 3:05)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:52 | Volta no `.env`. Cola o link (SEM o "https://") na variavel `ALLOWED_HOSTS` (linha 253) |
| 2:52 | Cola o link inteiro (COM "https://") nas variaveis `WEBHOOK_URL` e `DJANGO_WEBHOOK_URL` (linhas 258 e 259) |

**Variaveis a configurar no `.env`:**
```env
# Linha 253 — SEM https://, so o dominio
ALLOWED_HOSTS=abcd-123.ngrok-free.app,backend,application-api,0.0.0.0,localhost,127.0.0.1,host.docker.internal

# Linha 258 — COM https:// e path do webhook
WEBHOOK_URL=https://abcd-123.ngrok-free.app/webhooks/whatsapp

# Linha 259 — idem
DJANGO_WEBHOOK_URL=https://abcd-123.ngrok-free.app/webhooks/whatsapp
```

**ATENCAO:**
- `ALLOWED_HOSTS`: SEM `https://`, so o hostname. Separado por virgula dos outros hosts.
- `WEBHOOK_URL` e `DJANGO_WEBHOOK_URL`: COM `https://` e com o path `/webhooks/whatsapp`.

### Etapa 6: Subir containers e verificar (3:06 - 3:26)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 3:06 | Roda `docker-compose up` no terminal |
| 3:11 | Tela mostra os logs subindo. Texto avisa que as mensagens ja estao sendo enviadas aos leads no WhatsApp |
| 3:21 | Digita `docker ps` para ver todos os containers online |
| 3:26 | Abre o navegador, acessa `localhost:3000` e a tela de login do GrowthAI carrega com sucesso. FIM |

**Comandos executados:**
```bash
# Subir todos os servicos
docker-compose up

# Em outro terminal, verificar containers
docker ps
```

**Containers que devem aparecer:**
| Container | Status esperado |
|-----------|----------------|
| `postgres-db` | healthy |
| `redis-server` | healthy |
| `application-migrator` | exited (0) — roda uma vez e morre |
| `application-api` | running |
| `application-api-tasks` | running |
| `application-frontend` | running |

---

## Fluxo Completo Resumido

```
1. git clone → code .
2. docker build backend + frontend (tags .v1-local)
3. .env → CI_BACKEND_TAG=backend.v1-local, CI_FRONTEND_TAG=frontend.v1-local
4. ngrok http 8081 → copiar URL publica
5. .env → ALLOWED_HOSTS (sem https), WEBHOOK_URL + DJANGO_WEBHOOK_URL (com https)
6. docker-compose up
7. Abrir localhost:3000
```

---

## Checklist de Verificacao

- [ ] Docker instalado e rodando (`docker ps` funciona)
- [ ] Imagem backend buildada com tag `.v1-local`
- [ ] Imagem frontend buildada com tag `.v1-local`
- [ ] `docker images | grep registry` mostra as 2 imagens
- [ ] `.env` com `CI_BACKEND_TAG` e `CI_FRONTEND_TAG` apontando para `.v1-local`
- [ ] Conta no ngrok.com criada e autenticada
- [ ] `ngrok http 8081` rodando e gerando URL publica
- [ ] `ALLOWED_HOSTS` no `.env` com hostname do ngrok (sem https)
- [ ] `WEBHOOK_URL` no `.env` com URL completa do ngrok (com https + /webhooks/whatsapp)
- [ ] `docker-compose up` executado sem erros
- [ ] `docker ps` mostra todos os containers healthy/running
- [ ] `localhost:3000` carrega a tela de login

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| `docker build` falha com erro de rede | Docker sem internet ou proxy | Verificar conexao. Se usa proxy: configurar Docker daemon |
| `docker-compose up` falha com "image not found" | Tags no `.env` nao batem com os nomes do `docker build` | Verificar que `CI_BACKEND_TAG` e `CI_FRONTEND_TAG` sao exatamente `backend.v1-local` e `frontend.v1-local` |
| Ngrok fecha sozinho | Terminal foi fechado ou sessao gratuita expirou | Reabrir ngrok. Na versao gratuita, o tunel dura ate fechar o terminal |
| Webhook do WhatsApp nao chega | URL do ngrok nao configurada no `.env` ou na Z-API | Verificar WEBHOOK_URL no `.env` E no painel Z-API (Video 08) |
| `localhost:3000` nao carrega | Container frontend nao subiu | `docker ps` para verificar. `docker-compose logs frontend` para ver erros |
| Postgres nao fica healthy | Porta 5432 ja em uso por outro PostgreSQL local | Parar outro PostgreSQL: `sudo systemctl stop postgresql` |
| Redis nao fica healthy | Porta 6380 em uso | Verificar com `netstat -tlnp | grep 6380` |
| "DisallowedHost" no Django | Hostname do ngrok nao esta no `ALLOWED_HOSTS` | Adicionar o hostname (sem https://) no `ALLOWED_HOSTS` |

---

## Notas Tecnicas

- O `docker-compose.yml` da raiz usa imagens pre-buildadas (do registry). Por isso o build local precisa das tags certas no `.env`.
- Para dev com hot-reload, use `docker-compose.dev.yml` em vez do `docker-compose.yml` (nao precisa build manual, monta volumes).
- O Ngrok e necessario apenas se voce quer testar webhooks do WhatsApp localmente. Se so quer ver o frontend/backend, pode pular o ngrok.
- Na versao gratuita do Ngrok, o URL muda a cada reinicio. Em producao, use dominio fixo com NGINX + SSL.

---

## Documentacao Relacionada

- `docker-compose.yml` — configuracao de producao
- `docker-compose.dev.yml` — configuracao de desenvolvimento (hot-reload)
- `Dockerfile` — build do backend
- `frontend/Dockerfile.dev` — build do frontend em dev
- README-DOCKER_COMPOSE.md — guia Docker
- Video 04 — passo anterior: frontend e variaveis
- Video 06 — proximo passo: configuracao do GHL
