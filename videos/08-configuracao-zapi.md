# Video 08: Configuracao da Z-API (WhatsApp)

**Duracao:** ~1:19
**Categoria:** Integracao WhatsApp
**Pre-requisitos:** Conta na Z-API com instancia Web criada, `.env` configurado, `WEBHOOK_URL` definida (Video 05)
**Resultado esperado:** 3 tokens Z-API no `.env` + webhook configurado no painel Z-API

---

## Resumo

Configura a integracao com o WhatsApp via Z-API. O video mostra como copiar 3 credenciais do painel Z-API para o `.env` e como configurar o webhook para que mensagens recebidas no WhatsApp cheguem ao backend. E o ultimo passo antes do sistema poder enviar/receber mensagens.

---

## Timeline Detalhada

### Abertura (0:00 - 0:04)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Apos finalizar a criacao das instancias" |

### Etapa 1: Copiar Client Token (0:05 - 0:21)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:05 | Acessa o site da Z-API. No menu lateral, clica em "Seguranca" |
| 0:10 | Vai em "Token de seguranca da conta", clica em gerar e copia o token |
| 0:14 | No VS Code (`.env`), cola esse token em `Z_API_CLIENT_TOKEN` (linha 274) |

**Caminho na Z-API:** Menu lateral > Seguranca > Token de seguranca da conta > Gerar > Copiar

**Variavel no `.env`:**
```env
Z_API_CLIENT_TOKEN=seu_client_token_aqui
```

### Etapa 2: Copiar Instance Token (0:22 - 0:38)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:22 | Volta na Z-API, clica em "Instancias Web" no menu lateral e depois em "Web Instance Data" |
| 0:30 | Copia o Token da Instancia (Instance Token) |
| 0:33 | Vai no VS Code e cola o valor em `Z_API_TOKEN` (linha 271) |

**Caminho na Z-API:** Menu lateral > Instancias Web > [sua instancia] > Web Instance Data > Token da Instancia

**Variavel no `.env`:**
```env
Z_API_TOKEN=seu_instance_token_aqui
```

### Etapa 3: Copiar Instance ID (0:39 - 0:53)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:39 | Retorna ao site da Z-API, ainda na tela de Web Instance Data |
| 0:44 | Copia a ID da instancia (Instance ID) |
| 0:49 | Vai no VS Code e cola esse valor em `Z_API_INSTANCE_ID` (linha 268) |

**Caminho na Z-API:** Menu lateral > Instancias Web > [sua instancia] > Web Instance Data > ID da Instancia

**Variavel no `.env`:**
```env
Z_API_INSTANCE_ID=seu_instance_id_aqui
```

### Etapa 4: Configurar Webhook na Z-API (0:54 - 1:19)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:54 | Volta no site da Z-API. Clica em "Instancias Web", abre sua instancia e clica na aba "Webhook e configuracoes gerais" |
| 1:06 | Vai no VS Code e copia o valor da variavel `WEBHOOK_URL` (linha 258) |
| 1:11 | Volta no painel da Z-API e cola esse link do webhook no campo "Ao receber" |
| 1:19 | Rola a pagina da Z-API para baixo e clica no botao verde "Salvar". FIM |

**Caminho na Z-API:** Instancias Web > [sua instancia] > Webhook e configuracoes gerais > Campo "Ao receber"

**Valor a colar no campo "Ao receber":**
```
https://seudominio.com/webhooks/whatsapp
```
(ou o link do Ngrok se estiver rodando local: `https://abcd-123.ngrok-free.app/webhooks/whatsapp`)

**IMPORTANTE:** Este e o mesmo valor da variavel `WEBHOOK_URL` no `.env`. Deve ser identico nos dois lugares.

---

## Resumo das 3 Credenciais + Webhook

| Variavel | Onde encontrar na Z-API | Linha no .env |
|----------|------------------------|---------------|
| `Z_API_CLIENT_TOKEN` | Seguranca > Token de seguranca da conta | ~274 |
| `Z_API_TOKEN` | Instancias Web > Web Instance Data > Token da Instancia | ~271 |
| `Z_API_INSTANCE_ID` | Instancias Web > Web Instance Data > ID da Instancia | ~268 |
| Webhook "Ao receber" | Instancias Web > Webhook e config gerais | (no painel Z-API, nao no .env) |

---

## Checklist de Verificacao

- [ ] `Z_API_CLIENT_TOKEN` preenchido no `.env`
- [ ] `Z_API_TOKEN` preenchido no `.env`
- [ ] `Z_API_INSTANCE_ID` preenchido no `.env`
- [ ] Webhook configurado no painel Z-API com a mesma URL do `WEBHOOK_URL` do `.env`
- [ ] Botao "Salvar" clicado no painel Z-API
- [ ] Instancia Z-API conectada a um numero de WhatsApp (QR Code escaneado)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Mensagens nao sao enviadas | `Z_API_TOKEN` ou `Z_API_INSTANCE_ID` errados | Verificar no painel Z-API que os valores batem |
| Mensagens sao enviadas mas respostas nao chegam | Webhook nao configurado ou URL errada | Verificar campo "Ao receber" no painel Z-API. Testar a URL no navegador |
| "401 Unauthorized" nos logs | `Z_API_CLIENT_TOKEN` invalido | Gerar novo token em Seguranca > Token de seguranca |
| Webhook chega mas backend nao processa | URL do webhook sem `/webhooks/whatsapp` no final | Adicionar o path completo: `https://dominio/webhooks/whatsapp` |
| Funciona local mas para apos reiniciar Ngrok | URL do Ngrok mudou | Atualizar no `.env` (WEBHOOK_URL, DJANGO_WEBHOOK_URL, ALLOWED_HOSTS) E no painel Z-API |
| Instancia Z-API desconectada | WhatsApp deslogou ou numero mudou | Reconectar no painel Z-API escaneando QR Code novamente |
| "Connection refused" no webhook | Backend nao esta rodando ou porta errada | Verificar `docker ps`. Backend deve estar na porta 8081 |

---

## Fluxo de uma Mensagem WhatsApp

```
Lead envia mensagem no WhatsApp
    |
    v
Z-API recebe a mensagem
    |
    v
Z-API faz POST para WEBHOOK_URL (configurado no painel)
    |
    v
Ngrok (dev) ou NGINX (prod) roteia para localhost:8081
    |
    v
Django recebe em /webhooks/whatsapp/
    |
    v
Background task e criada → ADK session resumida do Redis
    |
    v
Agente AI processa e responde via Z-API
```

---

## Notas Tecnicas

- Cada tenant pode ter sua propria instancia Z-API. Em multi-tenant, as credenciais ficam em `TenantSettings` no banco, nao no `.env`.
- O `.env` com credenciais Z-API e usado apenas pelo owner/dev.
- O webhook aceita multiplos paths aliases (ver `config/urls.py`): `/webhook/whatsapp/`, `/webhooks/whatsapp/`, etc.
- Para debug de webhooks, verificar a tabela `WebhookEvent` no Django admin.
- Status da conexao WhatsApp: `GET /api/whatsapp/status`

---

## Documentacao Relacionada

- README_ENV.md secao "Z-API (Integracao WhatsApp)"
- docs/checklist_manual_whatsapp_sdr.md — checklist de teste do fluxo WhatsApp
- web/views/processing.py — onde o webhook e processado
- Video 05 — configuracao do Ngrok (WEBHOOK_URL)
- Video 07 — passo anterior: Google AI Studio
- Video 09+ — proximos passos (pendente)
