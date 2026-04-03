# Video 17: Configuracao de Ambiente e Acesso Inicial

**Duracao:** ~1:17
**Categoria:** Setup do Cliente / Onboarding
**Pre-requisitos:** Plataforma deployada e acessivel (Videos 01-16 concluidos)
**Resultado esperado:** .env configurado, plataforma acessivel, novo aluno/cliente criado

---

## Resumo

Primeiro video da serie de demonstracao. Mostra o fluxo de onboarding de um novo cliente/aluno: renomear .env.example, preencher variaveis de ambiente (IDs de localizacao e aluno), acessar a tela de login e criar um novo usuario na plataforma GrowthAI.

---

## Timeline Detalhada

### Etapa 1: Configurar .env (0:00 - 0:45)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Abertura no editor de codigo |
| 0:00 | Arquivo `env.example` e renomeado para `.env` |
| 0:00 | Variaveis de ambiente sao preenchidas (IDs de localizacao e aluno) |

**Variaveis preenchidas:**
```env
GHL_LOCATION_ID=<id_do_cliente>
IDGHL_ALUNO=<identificador_do_aluno>
```

### Etapa 2: Acesso inicial e criacao de usuario (0:45 - 1:17)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:45 | Mostra a tela de login da plataforma GrowthAI |
| 1:00 | Um novo aluno/cliente e criado para receber credenciais de acesso |
| 1:17 | Credenciais criadas com sucesso. FIM |

**Fluxo de onboarding:**
```
1. Configurar .env com dados do cliente
2. Acessar plataforma (https://seudominio.com)
3. Criar usuario para o cliente
4. Compartilhar credenciais
```

---

## Checklist de Verificacao

- [ ] `.env` renomeado e configurado com dados do cliente
- [ ] Plataforma acessivel via navegador
- [ ] Tela de login carrega corretamente
- [ ] Novo usuario criado com sucesso
- [ ] Credenciais anotadas para compartilhar com o cliente

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Tela de login nao carrega | Frontend nao esta rodando | `docker ps` para verificar container frontend |
| Erro ao criar usuario | Backend nao conecta ao banco | Verificar PostgreSQL: `docker logs postgres-db` |
| "Invalid credentials" ao fazer login | Senha ou usuario incorretos | Resetar via Django admin ou `python manage.py createsuperuser` |

---

## Documentacao Relacionada

- Video 04 — configuracao inicial de variaveis
- Video 12 — validacao dos containers
- Video 18 — proximo passo: integracoes da plataforma
