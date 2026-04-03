# Video 11: Configuracao do CI/CD e Deploy (VS Code e GitLab)

**Duracao:** ~3:13
**Categoria:** CI/CD e Deploy
**Pre-requisitos:** Videos 09 e 10 concluidos (VM + IP estatico), chave JSON da Service Account
**Resultado esperado:** Pipeline GitLab CI rodando com sucesso, imagens buildadas e deploy na VM

---

## Resumo

Conecta tudo: coloca a chave JSON da Service Account no projeto, preenche as variaveis de CI/CD no `.env`, faz push para o GitLab e acompanha o pipeline de 3 estagios (build frontend, build backend, deploy). Ao final, a aplicacao esta rodando na VM na nuvem.

---

## Timeline Detalhada

### Etapa 1: Colocar chave JSON no projeto (0:00 - 0:29)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Tutorial configuracao do CI/CD e deploy da aplicacao" |
| 0:06 | Abre o VS Code. Localiza a pasta `key` na raiz do projeto |
| 0:11 | Arrasta o arquivo `.json` (baixado no Video 09) para dentro da pasta `key` |
| 0:19 | Renomeia o arquivo para `gcp-key-work.json` |

**IMPORTANTE:** O nome DEVE ser exatamente `gcp-key-work.json`. O pipeline depende desse nome.

### Etapa 2: Preencher variaveis de CI/CD no .env (0:30 - 1:44)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:30 | Abre o arquivo `.env` principal |
| 0:33 | `CI_REGISTRY_NAMESPACE=` → coloca usuario GitLab / nome do projeto |
| 0:48 | `CI_DEPLOY_BRANCH=` → coloca `feature/tutorial-deploy` |
| 0:56 | `GCP_VM_INSTANCE_NAME=` → cola o nome exato da VM do Google Cloud |
| 1:05 | `GCP_VM_ZONE=` → cola a zona da VM (ex: `us-central1-c`) |
| 1:11 | `GCP_VM_HOST=` → cola o numero do IP Estatico (do Video 10) |
| 1:25 | `GCP_VM_USER=` → coloca o nome de usuario do Gmail (tudo antes do @) |
| 1:33 | `GCP_PROJECT_ID=` → copia o ID do projeto no painel GCP e cola |

**Variaveis no `.env`:**
```env
# CI/CD GitLab
CI_REGISTRY_NAMESPACE=seu-usuario/growth-ai
CI_DEPLOY_BRANCH=feature/tutorial-deploy

# GCP VM
GCP_VM_INSTANCE_NAME=vm-work
GCP_VM_ZONE=us-central1-c
GCP_VM_HOST=35.xxx.xxx.xxx          # IP estatico do Video 10
GCP_VM_USER=seunome                  # parte antes do @ do Gmail
GCP_PROJECT_ID=deploy-tutorial-xxxxx # ID do projeto no GCP
```

**Como encontrar cada valor:**

| Variavel | Onde encontrar |
|----------|---------------|
| `CI_REGISTRY_NAMESPACE` | GitLab > seu projeto > URL (ex: `accelera3601/growth-ai`) |
| `CI_DEPLOY_BRANCH` | Nome da branch que voce vai criar (qualquer nome) |
| `GCP_VM_INSTANCE_NAME` | GCP > Compute Engine > VM instances > coluna "Name" |
| `GCP_VM_ZONE` | GCP > Compute Engine > VM instances > coluna "Zone" |
| `GCP_VM_HOST` | GCP > VPC Network > IP addresses > coluna "External Address" |
| `GCP_VM_USER` | Seu email Gmail sem o @gmail.com (ex: `joaosilva`) |
| `GCP_PROJECT_ID` | GCP > Dashboard > Project ID (nao confundir com Project Name) |

### Etapa 3: Push para GitLab (1:45 - 2:13)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:45 | Abre o terminal no VS Code. Digita `git status` |
| 1:49 | `git checkout -b feature/tutorial-deploy` |
| 1:58 | `git add .` |
| 2:02 | `git commit -m "enviando app para vm"` |
| 2:07 | `git push -u origin feature/tutorial-deploy` |

**Comandos executados:**
```bash
git status
git checkout -b feature/tutorial-deploy
git add .
git commit -m "enviando app para vm"
git push -u origin feature/tutorial-deploy
```

### Etapa 4: Acompanhar pipeline no GitLab (2:14 - 3:13)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:14 | Abre o site do GitLab, muda para a branch enviada |
| 2:21 | Clica no icone azul "Running" para abrir o Pipeline de CI/CD |
| 2:26 | Mostra o diagrama com 3 etapas: `build_frontend`, `build_backend` e `deploy` |
| 2:34 | Clica em `build_frontend` — mostra o codigo carregando ate "Job succeeded" |
| 2:49 | Clica em `build_backend` — mostra o final do carregamento |
| 3:01 | Menu esquerdo → Deploy > Container Registry → confere as imagens docker geradas |
| 3:13 | Volta no Pipeline e clica no job `deploy`. Mostra o codigo finalizando o envio pra VM. FIM |

**Pipeline stages:**
```
build_frontend → build_backend → deploy
     |                |              |
  Builda imagem   Builda imagem   SCP + docker-compose up
  do Next.js      do Django       na VM via Service Account
```

---

## Checklist de Verificacao

- [ ] `key/gcp-key-work.json` no projeto (nome exato)
- [ ] `CI_REGISTRY_NAMESPACE` preenchido no `.env`
- [ ] `CI_DEPLOY_BRANCH` preenchido no `.env`
- [ ] `GCP_VM_INSTANCE_NAME` preenchido no `.env`
- [ ] `GCP_VM_ZONE` preenchido no `.env`
- [ ] `GCP_VM_HOST` preenchido com IP estatico
- [ ] `GCP_VM_USER` preenchido no `.env`
- [ ] `GCP_PROJECT_ID` preenchido no `.env`
- [ ] Branch criada e push feito para o GitLab
- [ ] Pipeline `build_frontend` succeeded
- [ ] Pipeline `build_backend` succeeded
- [ ] Pipeline `deploy` succeeded
- [ ] Imagens visiveis no Container Registry do GitLab

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Pipeline nao inicia | Branch nao bate com `CI_DEPLOY_BRANCH` | Verificar que o nome da branch e identico ao valor no `.env` |
| `build_frontend` falha | Erro no Dockerfile do frontend ou dependencias | Checar logs do job. Comum: falta de `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` |
| `build_backend` falha | Erro no Dockerfile ou requirements.txt | Checar logs. Comum: pacote Python nao encontrado |
| `deploy` falha com "Permission denied" | Service Account sem roles corretos | Verificar os 3 roles do Video 09 (Compute Instance Admin, SA User, Compute Viewer) |
| `deploy` falha com "Could not connect" | IP da VM errado ou VM parada | Verificar `GCP_VM_HOST` e que a VM esta running |
| `deploy` falha com "key file not found" | `gcp-key-work.json` nao esta na pasta `key/` ou nome errado | Verificar nome exato e localizacao |
| Imagens nao aparecem no Container Registry | Push falhou silenciosamente | Verificar credenciais do registry: `CI_REGISTRY_USER` e `CI_REGISTRY_PASSWORD` |

---

## Notas Tecnicas

- O pipeline usa `google/cloud-sdk` image para autenticar no GCP via Service Account JSON.
- O deploy faz `gcloud compute scp` para copiar `docker-compose.yml` e `.env` para a VM.
- Apos copiar, executa `docker compose up -d --force-recreate --remove-orphans` na VM.
- Healthcheck: polls 12x (5s cada) verificando containers.
- Auto-rollback: se healthcheck falha, restaura `docker-compose.rollback.yml`.

---

## Documentacao Relacionada

- `.gitlab-ci.yml` — definicao do pipeline
- README-INSTALAÇÂO.md secao "Etapas Finais" — guia escrito
- Video 10 — passo anterior: IP estatico
- Video 12 — proximo passo: validacao dos containers
