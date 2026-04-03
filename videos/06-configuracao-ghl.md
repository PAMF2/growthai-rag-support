# Video 06: Configuracao do GHL (GoHighLevel)

**Duracao:** ~2:47
**Categoria:** Integracao CRM
**Pre-requisitos:** Conta no GoHighLevel com acesso admin, `.env` configurado (Videos 01-04)
**Resultado esperado:** 4 variaveis GHL preenchidas no `.env` (Location ID, PIT, Pipeline ID, Calendar ID)

---

## Resumo

Configura a integracao com o GoHighLevel (CRM). O video mostra como encontrar e copiar 4 credenciais do painel GHL e cola-las no `.env`. Essas credenciais permitem que o agente AI registre leads nos pipelines, faca agendamentos e consulte dados do CRM.

---

## Timeline Detalhada

### Abertura (0:00 - 0:26)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Configuracao das variaveis GHL..." |

### Etapa 1: Copiar Location ID (0:27 - 0:52)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:27 | Acessa o dashboard do GoHighLevel (GHL) no navegador |
| 0:33 | Clica em "Configuracoes" no menu lateral inferior esquerdo |
| 0:38 | Na pagina de Perfil da Empresa, localiza o campo "ID de localizacao" |
| 0:44 | Copia o ID de localizacao |
| 0:47 | No VS Code, abre o `.env` e cola na variavel `GHL_LOCATION_ID` (linha 241) |

**Caminho no GHL:** Menu lateral > Configuracoes > Perfil da Empresa > ID de localizacao

**Variavel no `.env`:**
```env
GHL_LOCATION_ID=seu_location_id_aqui
```

### Etapa 2: Criar e copiar PIT (Private Integration Token) (0:53 - 1:39)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:53 | Volta ao GHL. No menu lateral, desce e clica em "Integracoes Privado" |
| 1:04 | Clica no botao "Criar nova integracao" |
| 1:08 | Preenche "Nome" (ex: PIT Teste), "Descricao" e clica em Proximo |
| 1:15 | No campo Escopos, clica em "Selecionar tudo" |
| 1:22 | Clica em "Criar", confirma o aviso de risco de seguranca e a integracao e gerada |
| 1:28 | Copia o Token (PIT) gerado na tela |
| 1:33 | Vai no VS Code e cola na variavel `GHL_PIT` (linha 238) |

**Caminho no GHL:** Menu lateral > Configuracoes > Integracoes > Privado > Criar nova integracao

**Passos detalhados:**
1. Nome: qualquer nome descritivo (ex: "GrowthAI Integration")
2. Descricao: opcional
3. Escopos: **Selecionar tudo** (importante!)
4. Criar > Confirmar aviso de seguranca
5. Copiar o token gerado

**Variavel no `.env`:**
```env
GHL_PIT=pit_xxxxxxxxxxxxxxxxxxxxxxxx
```

**IMPORTANTE:** O PIT so e exibido uma vez. Se perder, precisa criar outro.

### Etapa 3: Copiar Pipeline ID (1:40 - 2:23)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:40 | Volta ao GHL e clica em "Leads" (Oportunidades) no menu lateral |
| 1:45 | No menu superior, clica na aba "Pipelines" |
| 1:56 | Na pipeline desejada, clica no icone de engrenagem/ferramentas e depois em "Copiar link" |
| 2:06 | Cola esse link num bloco de notas para conseguir ler inteiro |
| 2:10 | Seleciona e copia apenas o codigo que vem depois da palavra `/pipeline/` na URL |
| 2:19 | Vai no VS Code e cola o codigo copiado na variavel `GHL_PIPELINE_ID` (linha 244) |

**Caminho no GHL:** Menu lateral > Leads/Oportunidades > Pipelines > [sua pipeline] > Engrenagem > Copiar link

**Como extrair o Pipeline ID da URL:**
```
URL completa: https://app.gohighlevel.com/v2/location/xxx/pipeline/ABC123DEF456
Pipeline ID:  ABC123DEF456  (tudo depois de /pipeline/)
```

**Variavel no `.env`:**
```env
GHL_PIPELINE_ID=ABC123DEF456
```

### Etapa 4: Copiar Calendar ID (2:24 - 2:47)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:24 | Volta no GHL, acessa o menu "Calendarios" e clica em "Configuracoes de Calendario" |
| 2:41 | Na lista, copia o ID do calendario desejado clicando no icone de copia |
| 2:47 | Vai no VS Code e cola esse ID na variavel `GHL_CALENDAR_ID` (linha 235). FIM |

**Caminho no GHL:** Menu lateral > Calendarios > Configuracoes de Calendario > [seu calendario] > Icone de copia

**Variavel no `.env`:**
```env
GHL_CALENDAR_ID=seu_calendar_id_aqui
```

---

## Resumo das 4 Variaveis

| Variavel | Onde encontrar no GHL | Linha no .env |
|----------|----------------------|---------------|
| `GHL_LOCATION_ID` | Configuracoes > Perfil da Empresa > ID de localizacao | ~241 |
| `GHL_PIT` | Configuracoes > Integracoes > Privado > Criar nova | ~238 |
| `GHL_PIPELINE_ID` | Leads > Pipelines > Engrenagem > Copiar link > extrair ID | ~244 |
| `GHL_CALENDAR_ID` | Calendarios > Configuracoes > Icone de copia | ~235 |

---

## Checklist de Verificacao

- [ ] `GHL_LOCATION_ID` preenchido no `.env`
- [ ] Integracao privada criada no GHL com TODOS os escopos
- [ ] `GHL_PIT` preenchido no `.env` (token copiado e guardado)
- [ ] Pipeline identificada e `GHL_PIPELINE_ID` preenchido no `.env`
- [ ] Calendario identificado e `GHL_CALENDAR_ID` preenchido no `.env`
- [ ] `USE_GHL_API=true` no `.env` (ja vem como padrao)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Nao encontra "Integracoes Privado" no GHL | Conta sem permissao de admin | Pedir acesso admin ao dono da conta GHL |
| PIT nao aparece apos criar | Pagina nao atualizou ou popup foi fechado | Criar nova integracao. O token so aparece uma vez |
| Pipeline ID copiado errado | Copiou a URL inteira em vez de so o ID | Extrair apenas o trecho apos `/pipeline/` |
| "GHL connection failed" no log do backend | PIT expirado ou escopos incompletos | Recriar a integracao com "Selecionar tudo" nos escopos |
| Leads nao aparecem no pipeline | `GHL_PIPELINE_ID` errado | Verificar que o ID corresponde a pipeline correta |
| Agendamentos nao funcionam | `GHL_CALENDAR_ID` errado ou calendario desativado | Verificar no GHL que o calendario esta ativo |

---

## Notas Tecnicas

- O GHL_PIT (Private Integration Token) e equivalente a uma chave de API. Tem acesso total se todos os escopos foram selecionados.
- Em multi-tenant, cada tenant tem seus proprios valores de GHL. Eles sao armazenados criptografados em `TenantSettings` no banco (nao no `.env`).
- O `.env` com credenciais GHL e usado apenas pelo owner/dev. Tenants configuram via frontend em `/perfil/configuracoes`.
- A variavel `GHL_MCP_URL=https://services.leadconnectorhq.com/mcp/` ja vem preenchida e NAO deve ser alterada.

---

## Documentacao Relacionada

- README_ENV.md secao "GOHIGHLEVEL" — referencia das variaveis
- docs/GA-002-tenant-settings.md — configuracao multi-tenant
- Video 05 — passo anterior: rodando local com Docker
- Video 07 — proximo passo: Google AI Studio (Gemini API Key)
