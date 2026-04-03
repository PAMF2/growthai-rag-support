# Video 12: Validando os Containers (SSH e Docker PS)

**Duracao:** ~1:00
**Categoria:** Verificacao de Deploy
**Pre-requisitos:** Video 11 concluido (deploy via CI/CD)
**Resultado esperado:** Confirmacao visual de que todos os containers estao rodando na VM

---

## Resumo

Video final de validacao. Acessa a VM via SSH pelo console do GCP e roda `docker ps` para confirmar que todos os containers (Postgres, Redis, Backend, Frontend, Tasks) estao online. Se tudo aparecer, o deploy foi um sucesso.

---

## Timeline Detalhada

### Etapa 1: Acessar a VM via SSH (0:00 - 0:45)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Apos a conclusao do envio da aplicacao para a VM" |
| 0:05 | No painel do Google Cloud, busca por "Compute Engine" |
| 0:14 | Clica em "VM instances" no menu esquerdo |
| 0:22 | Clica em cima do nome da VM (`vm-work`) |
| 0:28 | No topo da tela de detalhes da VM, clica no botao "SSH" |
| 0:36 | Clica em "Authorize" para abrir o terminal Linux no navegador |

### Etapa 2: Verificar containers (0:46 - 1:00)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:46 | No terminal, digita: `docker ps` |
| 0:52 | Terminal lista todos os containers hospedados |
| 1:00 | Confirmacao: Deploy foi um sucesso. FIM |

**Comando executado:**
```bash
docker ps
```

**Containers esperados:**

| Container | Imagem | Status esperado |
|-----------|--------|----------------|
| `postgres-db` | postgres:15 | Up (healthy) |
| `redis-server` | redis:7 | Up (healthy) |
| `application-migrator` | backend image | Exited (0) — normal, roda uma vez |
| `application-api` | backend image | Up |
| `application-api-tasks` | backend image | Up |
| `application-frontend` | frontend image | Up |

---

## Checklist de Verificacao

- [ ] SSH na VM funcionando pelo console GCP
- [ ] `docker ps` mostra 5+ containers (migrator pode ter exited)
- [ ] `postgres-db` status: healthy
- [ ] `redis-server` status: healthy
- [ ] `application-api` status: running
- [ ] `application-api-tasks` status: running
- [ ] `application-frontend` status: running

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| `docker ps` nao mostra nada | Deploy nao completou ou containers crasharam | `docker ps -a` para ver todos (incluindo parados). `docker-compose logs` para ver erros |
| Postgres nao fica healthy | Variaveis `POSTGRES_*` erradas no `.env` | Verificar `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` |
| Backend reinicia em loop | Erro na aplicacao Django | `docker logs application-api` para ver o erro |
| Frontend nao sobe | Build falhou ou variaveis faltando | `docker logs application-frontend` |
| Migrator com exit code 1 | Migration falhou | `docker logs application-migrator` — pode ser conflito de schema |
| "Cannot connect to Docker daemon" | Docker nao esta rodando | `sudo systemctl start docker` |

---

## Comandos Uteis para Debug na VM

```bash
# Ver todos os containers (incluindo parados)
docker ps -a

# Ver logs de um container especifico
docker logs application-api
docker logs application-frontend
docker logs application-migrator

# Ver logs em tempo real
docker-compose logs -f

# Reiniciar tudo
docker-compose down && docker-compose up -d

# Ver uso de recursos
docker stats
```

---

## Documentacao Relacionada

- README-INSTALAÇÂO.md — guia completo
- README.CREATESUPERUSER.md — criar superusuario na VM
- Video 11 — passo anterior: CI/CD e deploy
- Video 13+ — proximos passos (pendente: NGINX, SSL, etc.)
