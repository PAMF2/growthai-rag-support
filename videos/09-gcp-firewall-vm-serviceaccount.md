# Video 09: Criando Regras de Firewall, VM e Service Account (Google Cloud)

**Duracao:** ~6:44
**Categoria:** Infraestrutura GCP
**Pre-requisitos:** Conta no Google Cloud com projeto criado, billing ativado
**Resultado esperado:** 5 regras de firewall, VM rodando com Docker, Service Account com chave JSON

---

## Resumo

Video mais longo e denso da serie. Configura toda a infraestrutura no Google Cloud: cria 5 regras de firewall (SSH, HTTP, HTTPS, backend, frontend), provisiona uma VM e2-medium com Ubuntu, cria uma Service Account com 3 roles para o CI/CD, exporta a chave JSON, acessa a VM via SSH e instala Docker + Docker Compose.

---

## Timeline Detalhada

### Etapa 1: Criar regras de firewall (0:00 - 3:01)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Painel inicial do Google Cloud Platform (Projeto "deploy tutorial") |
| 0:09 | Na barra de pesquisa superior, digita e acessa "VPC network" |
| 0:16 | No menu esquerdo, clica em "Firewall" |

**Regra 1 — SSH (0:21 - 0:52)**

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:21 | Clica em "Create Firewall Rule" |
| 0:21 | Nome: `allow-ssh` |
| 0:21 | Targets: "All instances in the network" |
| 0:21 | Source IPv4 ranges: `0.0.0.0/0` |
| 0:21 | Marca TCP, porta: `22` |
| 0:52 | Clica em "Create" |

**Regra 2 — HTTP (0:53 - 1:25)**

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:53 | Clica em "Create Firewall Rule" |
| 0:53 | Nome: `allow-http` |
| 0:53 | Targets: "All instances in the network" |
| 0:53 | Source IPv4 ranges: `0.0.0.0/0` |
| 0:53 | Marca TCP, porta: `80` |
| 1:26 | Clica em "Create" |

**Regra 3 — HTTPS (1:26 - 1:56)**

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:26 | Clica em "Create Firewall Rule" |
| 1:26 | Nome: `allow-https` |
| 1:26 | Targets: "All instances in the network" |
| 1:26 | Source IPv4 ranges: `0.0.0.0/0` |
| 1:26 | Marca TCP, porta: `443` |
| 1:57 | Clica em "Create" |

**Regra 4 — Backend (1:57 - 2:27)**

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:57 | Clica em "Create Firewall Rule" |
| 1:57 | Nome: `allow-backend-8000` |
| 1:57 | Targets: "All instances in the network" |
| 1:57 | Source IPv4 ranges: `0.0.0.0/0` |
| 1:57 | Marca TCP, porta: `8000` |
| 2:28 | Clica em "Create" |

**Regra 5 — Frontend (2:28 - 3:01)**

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:28 | Clica em "Create Firewall Rule" |
| 2:28 | Nome: `allow-frontend-3000` |
| 2:28 | Targets: "All instances in the network" |
| 2:28 | Source IPv4 ranges: `0.0.0.0/0` |
| 2:28 | Marca TCP, porta: `3000` |
| 3:01 | Clica em "Create" |

**Resumo das 5 regras:**

| Nome | Protocolo | Porta | Finalidade |
|------|-----------|-------|-----------|
| `allow-ssh` | TCP | 22 | Acesso SSH a VM |
| `allow-http` | TCP | 80 | Trafego HTTP (NGINX) |
| `allow-https` | TCP | 443 | Trafego HTTPS (SSL) |
| `allow-backend-8000` | TCP | 8000 | Django API |
| `allow-frontend-3000` | TCP | 3000 | Next.js frontend |

**Todas as regras usam:** Direction: Ingress, Targets: All instances, Source: 0.0.0.0/0

### Etapa 2: Criar a VM (3:02 - 3:56)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 3:02 | Barra de pesquisa → busca "Compute Engine" e clica |
| 3:12 | Clica em "Create Instance" |
| 3:16 | Define nome da VM (ex: `vm-work`) e seleciona a Zona desejada |
| 3:25 | Desce ate "Boot disk", clica em "Change". Altera tamanho do disco para 50 GB. Clica "Select" |
| 3:37 | Na secao Firewall (Networking), marca: "Allow HTTP traffic" e "Allow HTTPS traffic" |
| 3:48 | Clica em "Create" no final da pagina |

**Configuracao da VM:**
```
Nome:          vm-work (ou nome de preferencia)
Zona:          ex: us-central1-c
Machine type:  e2-medium (padrao)
Boot disk:     Ubuntu 22.04 LTS, 50 GB
Firewall:      ☑ Allow HTTP  ☑ Allow HTTPS
```

### Etapa 3: Criar Service Account (3:57 - 5:09)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 3:57 | Barra de pesquisa → digita "IAM" e clica em "IAM & Admin" |
| 4:05 | Menu lateral → "Service Accounts" → "Create service account" |
| 4:13 | Nome: `gitlab-ci-deploy`. Clica "Create and Continue" |
| 4:20 | Adiciona 3 Roles clicando em "Add another role" |
| 4:20 | Role 1: `Compute Instance Admin (v1)` |
| 4:20 | Role 2: `Service Account User` |
| 4:20 | Role 3: `Compute Viewer` |
| 4:43 | Clica "Continue" → "Done" |
| 4:43 | Clica na Service Account criada → aba "Keys" → "Add Key" → "Create new key" |
| 4:53 | Formato: JSON → "Create". Arquivo da chave e baixado |

**Roles necessarios:**
```
roles/compute.instanceAdmin.v1   — gerenciar VMs
roles/iam.serviceAccountUser     — usar service accounts
roles/compute.viewer             — visualizar recursos
```

**IMPORTANTE:** O arquivo JSON baixado sera usado no Video 11 (CI/CD). Guardar com seguranca.

### Etapa 4: Acessar VM e instalar Docker (5:10 - 6:44)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 5:10 | Retorna ao Compute Engine > VM instances. Clica no botao "SSH" da VM |
| 5:31 | Clica em "Authorize" para abrir o terminal |
| 5:43 | No terminal: `sudo apt update` |
| 5:53 | `sudo apt install -y docker.io git curl wget` |
| 6:02 | `sudo apt install -y docker-compose` |
| 6:15 | `sudo systemctl enable docker` |
| 6:15 | `sudo systemctl start docker` |
| 6:15 | `sudo usermod -aG docker $USER` |
| 6:24 | `docker --version` e `docker-compose --version` |
| 6:44 | `sudo mkdir -p /opt/app` e `sudo chown -R $USER:$USER /opt/app`. FIM |

**Comandos completos (copiar e colar):**
```bash
# 1. Atualizar sistema
sudo apt update

# 2. Instalar Docker e ferramentas
sudo apt install -y docker.io git curl wget

# 3. Instalar Docker Compose
sudo apt install -y docker-compose

# 4. Ativar Docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# 5. Verificar instalacao
docker --version
docker-compose --version

# 6. Criar pasta do app
sudo mkdir -p /opt/app
sudo chown -R $USER:$USER /opt/app
```

---

## Checklist de Verificacao

- [ ] 5 regras de firewall criadas (allow-ssh, allow-http, allow-https, allow-backend-8000, allow-frontend-3000)
- [ ] VM criada com Ubuntu 22.04, 50GB disco, HTTP+HTTPS habilitados
- [ ] Service Account `gitlab-ci-deploy` criada com 3 roles
- [ ] Chave JSON da Service Account baixada e guardada
- [ ] SSH na VM funcionando
- [ ] `docker --version` retorna versao
- [ ] `docker-compose --version` retorna versao
- [ ] `/opt/app` criada com permissoes do usuario

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| "You don't have permission to create firewall rules" | Conta sem role de Network Admin | Pedir ao admin do projeto para adicionar role `Compute Network Admin` |
| VM nao cria: "Quota exceeded" | Cota de CPUs ou IPs esgotada na regiao | Trocar zona ou solicitar aumento de cota |
| SSH nao conecta | Regra `allow-ssh` nao criada ou porta 22 bloqueada | Verificar regra de firewall. Tentar SSH pelo console web |
| `docker: command not found` | Docker nao instalou | Rodar `sudo apt install -y docker.io` novamente |
| `docker-compose: command not found` | Compose nao instalou | `sudo apt install -y docker-compose` |
| `permission denied` ao rodar docker | Usuario nao esta no grupo docker | `sudo usermod -aG docker $USER` + deslogar e logar novamente |

---

## Documentacao Relacionada

- README-INSTALAÇÂO.md — guia completo de instalacao GCP
- README-IP.md — configuracao de IP estatico (Video 10)
- Video 08 — passo anterior: Z-API
- Video 10 — proximo passo: IP estatico
