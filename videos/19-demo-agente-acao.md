# Video 19: Demonstracao Pratica do Agente em Acao

**Duracao:** ~3:09 (04:16 - 07:25 no compilado)
**Categoria:** Demonstracao / Resultado Final
**Pre-requisitos:** Videos 17-18 (plataforma configurada com todas as integracoes)
**Resultado esperado:** Agente AI funcionando end-to-end: conversa WhatsApp → qualificacao → agendamento → email → metricas

---

## Resumo

O "show reel" da plataforma. Mostra o agente AI em acao real: um lead envia mensagem no WhatsApp, o bot responde (inclusive com audios), qualifica o lead usando BANT/GPCT, identifica demanda e capacidade de investimento, oferece horarios disponiveis, agenda a reuniao automaticamente, envia email de confirmacao e atualiza as metricas no painel.

---

## Timeline Detalhada

### Etapa 1: Teste no WhatsApp — Conversa com o Lead (04:16 - 06:42)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 4:16 | Inicia teste pratico do robo no WhatsApp |
| 4:16 | Lead envia uma mensagem |
| 4:30 | Agente de IA responde (inclusive com audios) |
| 5:00 | Agente faz qualificacao do lead |
| 5:00 | Identifica a demanda do lead |
| 5:20 | Identifica disponibilidade de capital/investimento |
| 5:40 | Agente oferece horarios disponiveis para reuniao |
| 6:00 | Lead confirma horario |
| 6:20 | Agente conclui o agendamento de forma autonoma |
| 6:30 | Email de confirmacao do agendamento e mostrado na tela |
| 6:42 | Conversa encerrada com sucesso |

**Fluxo completo demonstrado:**
```
Lead: "Oi, tenho interesse no servico"
  ↓
Bot: Apresenta-se, pergunta sobre necessidades
  ↓
Lead: Descreve sua demanda
  ↓
Bot: Qualifica (BANT/GPCT) — pergunta sobre orcamento, timeline
  ↓
Lead: Responde sobre capital disponivel
  ↓
Bot: Score calculado → lead classificado como "hot"
  ↓
Bot: "Tenho esses horarios disponiveis: [lista]"
  ↓
Lead: "Pode ser amanha as 14h"
  ↓
Bot: Agenda no Google Calendar + registra no GHL
  ↓
Bot: "Reuniao confirmada! Voce recebera um email de confirmacao"
  ↓
Email enviado automaticamente via SMTP
```

**Capacidades demonstradas:**
| Feature | Evidencia |
|---------|-----------|
| Resposta em texto | Bot responde mensagens de texto |
| Resposta em audio | Bot processa e responde com audio |
| Qualificacao BANT | Pergunta sobre budget, authority, need, timeline |
| Scoring automatico | Lead classificado por pontuacao |
| Agendamento | Horarios oferecidos e reuniao criada |
| Email automatico | Confirmacao enviada via SMTP |
| Integracao Calendar | Evento criado no Google Calendar |
| Integracao GHL | Lead registrado no pipeline do CRM |

### Etapa 2: Metricas e Calendar (06:42 - 07:25)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 6:42 | Retorna a plataforma GrowthAI |
| 6:42 | Abre o painel de "Metricas" |
| 7:00 | Dados do funil atualizados automaticamente |
| 7:00 | Mostra: leads totais, respondidos, agendados |
| 7:15 | Abre o Google Calendar |
| 7:25 | Reuniao aparece inserida corretamente no calendario. FIM |

**Metricas mostradas no painel:**
| Metrica | Descricao |
|---------|-----------|
| Leads totais | Quantidade total de leads processados |
| Leads respondidos | Leads que receberam primeira mensagem |
| Leads agendados | Leads com reuniao marcada |
| Taxa de conversao | % de leads que agendaram |

**Endpoints de metricas:** `GET /api/metricas/`, `GET /api/agents/metrics`

---

## O que esse video prova

Este video e a **prova de conceito** completa da plataforma. Mostra que:

1. **O agente funciona autonomamente** — nao precisa de intervencao humana
2. **Multimodal** — processa texto E audio
3. **Qualificacao inteligente** — usa frameworks de vendas (BANT/GPCT)
4. **Integracoes funcionam** — Calendar, GHL, SMTP, WhatsApp conectados
5. **Metricas atualizadas** — painel reflete dados em tempo real
6. **End-to-end** — do primeiro contato ao agendamento confirmado

**Use este video para mostrar a clientes o que a plataforma faz.**

---

## Checklist de Verificacao (para replicar a demo)

- [ ] Todas as integracoes verdes (Video 18)
- [ ] Numero de WhatsApp conectado na Z-API
- [ ] Google Calendar com horarios disponiveis
- [ ] Pipeline GHL configurada
- [ ] SMTP funcionando (email de teste)
- [ ] Lead de teste com numero real de WhatsApp
- [ ] Enviar mensagem de teste e aguardar resposta do bot
- [ ] Verificar agendamento no Calendar
- [ ] Verificar email de confirmacao
- [ ] Verificar metricas no painel

---

## Problemas Comuns na Demo

| Problema | Causa | Solucao |
|----------|-------|---------|
| Bot nao responde | Gemini key invalida ou worker parado | Verificar logs: `docker logs application-api-tasks`. Checar `[GEMINI]` |
| Bot responde mas nao agenda | Calendar nao conectado ou sem horarios | Verificar `/api/calendar/oauth/status`. Checar horarios de expediente |
| Email nao chega | SMTP nao configurado | Verificar app password do Gmail. Testar SMTP |
| Metricas nao atualizam | Background tasks paradas | `docker ps` → verificar `application-api-tasks` |
| Bot repete a saudacao | Sessao ADK foi perdida (Redis) | Verificar Redis memory. `python manage.py whatsapp_session_inspect` |
| Audio nao e processado | Transcription model nao configurado | Verificar `GEMINI_TRANSCRIPTION_MODEL` no `.env` |

---

## Documentacao Relacionada

- docs/checklist_manual_whatsapp_sdr.md — checklist de teste detalhado
- docs/feature_audio_input/GUIA_IMPLEMENTACAO_AUDIO.md — como audio funciona
- policies/qualification.yaml — regras de scoring
- policies/cadence.yaml — cadencia de follow-up
- Video 18 — passo anterior: integracoes
