# Video 04: Frontend e Variaveis de Ambiente

**Duracao:** ~2:30
**Categoria:** Configuracao de Ambiente
**Pre-requisitos:** Videos 01-03 concluidos (repo clonado, `.env` renomeado e branding configurado)
**Resultado esperado:** Dominio da API configurado em 3 lugares + superusuario definido

---

## Resumo

Este video configura o dominio da API em tres arquivos diferentes e define as credenciais do superusuario. E o video mais critico para erros: se o aluno esquecer de alterar o dominio em qualquer um dos 3 lugares, a aplicacao quebra em producao.

---

## Timeline Detalhada

### Abertura (0:00 - 0:23)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Configuracao do Frontend e variaveis de ambiente" |
| 0:08 | Tela de boas-vindas do VS Code |
| 0:17 | Novo titulo: "Configuracao do dominio da API no projeto Frontend e Docker Compose" |
| 0:24 | Mostra a lista de pastas do projeto no canto esquerdo |

### Etapa 1: Configurar dominio em `frontend/config/api.ts` (0:28 - 0:54)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:28 | Mouse clica para abrir a pasta `frontend` |
| 0:31 | Dentro de `frontend`, abre a pasta `config` |
| 0:34 | Clica no arquivo `api.ts` |
| 0:38 | Codigo abre. Seta vermelha aponta para a linha 4 |
| 0:45 | Texto instrui a apagar `localhost:8081` e colocar o dominio. Exemplo: `https://seudominio.com` |
| 0:51 | Instrucao: Salve e feche este arquivo |

**Arquivo:** `frontend/config/api.ts`

**Linha a alterar (linha 4):**
```typescript
// ANTES (dev):
process.env.NEXT_PUBLIC_API_BASE_PATH || 'http://localhost:8081'

// DEPOIS (producao):
process.env.NEXT_PUBLIC_API_BASE_PATH || 'https://seudominio.com'
```

**IMPORTANTE:** Para desenvolvimento local, MANTER `localhost:8081`. So alterar para producao.

### Etapa 2: Configurar dominio em `frontend/.env` (0:55 - 1:17)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:55 | Ainda dentro da pasta `frontend`, mouse abre subpasta de env |
| 0:59 | Abre o arquivo `.env` que esta dentro de `frontend/` |
| 1:01 | Seta aponta para a linha 1: `NEXT_PUBLIC_API_URL=http://localhost:8081` |
| 1:08 | Instrucao: Remova o endereco atual e insira seu dominio com HTTPS |
| 1:13 | Instrucao para salvar e fechar o arquivo |

**Arquivo:** `frontend/.env`

**Conteudo a alterar:**
```env
# ANTES (dev):
NEXT_PUBLIC_API_URL=http://localhost:8081

# DEPOIS (producao):
NEXT_PUBLIC_API_URL=https://seudominio.com
```

**IMPORTANTE:** Sem `/api` no final. Apenas o dominio base.

### Etapa 3: Configurar dominio em `docker-compose.yml` (1:18 - 1:46)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:18 | Mouse fecha a pasta frontend, vai para a raiz do projeto e abre `docker-compose.yml` |
| 1:24 | Rola o codigo ate la embaixo (linha 180+), na secao do servico `frontend:` |
| 1:28 | Seta aponta para `NEXT_PUBLIC_API_URL` debaixo da palavra `environment:` |
| 1:34 | Texto pede para trocar a URL pelo dominio real |
| 1:42 | Salve e feche o arquivo `docker-compose.yml` |

**Arquivo:** `docker-compose.yml` (raiz do projeto)

**Secao a alterar (~linha 107):**
```yaml
frontend:
    # ...
    environment:
      # ANTES:
      NEXT_PUBLIC_API_URL: https://seudominio.com  #https://accelera360.ai
      # DEPOIS:
      NEXT_PUBLIC_API_URL: https://seudominiomesmo.com
```

### Etapa 4: Configurar superusuario (1:47 - 2:30)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:47 | Abre de novo o arquivo `.env` principal (raiz do projeto) |
| 1:54 | Rola ate a ultima linha, na secao `# SUPER USUARIO DO SISTEMA` |
| 2:00 | Seta vermelha em `APP_USERNAME=`. Usuario escreve seu username de login |
| 2:08 | Seta em `APP_PASSWORD=`. Usuario digita a senha escolhida |
| 2:13 | Seta em `APP_EMAIL=`. Usuario preenche seu e-mail |
| 2:18 | Texto: "Apos subir a aplicacao, essas credenciais serao utilizadas para criar o super usuario responsavel pelo acesso administrativo ao frontend da plataforma" |
| 2:30 | Ultima mensagem: "Guarde essas informacoes com seguranca". FIM |

**Arquivo:** `.env` (raiz do projeto)

**Secao a preencher (ultimas linhas):**
```env
#########################################################
# SUPER USUARIO DO SISTEMA
#########################################################

APP_USERNAME="seu_usuario"
APP_PASSWORD=sua_senha_segura
APP_EMAIL="seu@email.com"
```

**IMPORTANTE:** Essas credenciais sao usadas pelo comando `bootstrap_app` para criar o superusuario Django automaticamente no primeiro deploy. Sao as credenciais de login no frontend.

---

## Resumo dos 3 Lugares do Dominio

Este e o ponto mais critico do video. O dominio da API deve ser configurado em EXATAMENTE 3 arquivos:

| # | Arquivo | Variavel | Usado por |
|---|---------|----------|-----------|
| 1 | `frontend/config/api.ts` | Fallback hardcoded na linha 4 | Client-side JS (fallback quando env var nao existe) |
| 2 | `frontend/.env` | `NEXT_PUBLIC_API_URL` | Next.js durante build e dev mode |
| 3 | `docker-compose.yml` | `NEXT_PUBLIC_API_URL` (em environment) | Container Docker em producao |

**Regra:**
- **Dev local:** manter `http://localhost:8081` em todos
- **Producao:** trocar para `https://seudominio.com` em todos (sem `/api`)

---

## Checklist de Verificacao

- [ ] `frontend/config/api.ts` — dominio atualizado na linha 4
- [ ] `frontend/.env` — `NEXT_PUBLIC_API_URL` atualizado
- [ ] `docker-compose.yml` — `NEXT_PUBLIC_API_URL` no servico frontend atualizado
- [ ] Os 3 dominios sao IDENTICOS (mesmo protocolo, mesmo dominio, sem barra no final)
- [ ] `.env` raiz — `APP_USERNAME` preenchido
- [ ] `.env` raiz — `APP_PASSWORD` preenchido
- [ ] `.env` raiz — `APP_EMAIL` preenchido
- [ ] Credenciais do superusuario anotadas em lugar seguro

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Frontend carrega mas nao conecta na API | Dominio diferente em um dos 3 arquivos | Verificar que os 3 lugares tem o MESMO dominio |
| "ERR_CONNECTION_REFUSED" em producao | Ainda esta como `localhost:8081` em algum dos 3 | Buscar `localhost:8081` em todos os 3 arquivos e trocar |
| Login nao funciona apos deploy | `APP_USERNAME`/`APP_PASSWORD` nao preenchidos ou `bootstrap_app` nao rodou | Verificar `.env`, depois rodar: `docker exec application-api python manage.py bootstrap_app` |
| "NEXT_PUBLIC_API_URL is undefined" | Variavel nao foi setada corretamente no docker-compose | Verificar indentacao YAML (espacos, nao tabs) e que a variavel esta sob `environment:` |
| API funciona em dev mas nao em Docker | Alterou `frontend/.env` mas nao `docker-compose.yml` | Docker usa as variaveis do `docker-compose.yml`, nao do `frontend/.env` |
| Mixed content (HTTP/HTTPS) no browser | Dominio sem `https://` ou dominio com `http://` em producao | Sempre usar `https://` em producao. Certificar que o SSL esta configurado (Video de NGINX+SSL) |

---

## Nota Tecnica

- `NEXT_PUBLIC_*` variaveis sao embutidas no build do Next.js (client-side). Alterar apos o build nao surte efeito — precisa rebuild.
- Em dev mode (`pnpm dev` ou `docker-compose.dev.yml`), as variaveis sao lidas em tempo real.
- O `API_INTERNAL_URL` (dentro do `docker-compose.yml`) e diferente: e usado para SSR (server-side rendering) e aponta para o container interno (`http://application-api:8000`). Este **NAO** deve ser alterado.
- O superusuario e criado pelo management command `bootstrap_app` que roda automaticamente no `entrypoint.sh` durante o primeiro deploy.

---

## Documentacao Relacionada

- `frontend/config/api.ts` — arquivo de configuracao da API
- `frontend/.env` / `frontend/.env.example` — variaveis do frontend
- `docker-compose.yml` / `docker-compose.dev.yml` — configuracao Docker
- README_ENV.md — referencia completa de variaveis
- README.CREATESUPERUSER.md — criacao manual de superusuario
- Video 03 — passo anterior: missao e identidade
- Video 05+ — proximos passos (pendente: Google Cloud, etc.)
