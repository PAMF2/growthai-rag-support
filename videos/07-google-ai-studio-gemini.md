# Video 07: Google AI Studio (API Key do Gemini)

**Duracao:** ~1:23
**Categoria:** Integracao AI
**Pre-requisitos:** Conta Google com projeto no Google Cloud Console
**Resultado esperado:** Chave da API Gemini criada e configurada no `.env`

---

## Resumo

Cria a chave de API do Google Gemini atraves do Google AI Studio. Esta chave e essencial — sem ela, os agentes AI nao funcionam. O video mostra como importar um projeto GCP existente no AI Studio e gerar a key.

---

## Timeline Detalhada

### Abertura (0:00 - 0:07)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Como criar uma chave de API no Google AI Studio" |

### Etapa 1: Acessar Google Cloud Console (0:08 - 0:22)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:08 | Acessa o Google Cloud Console (console.cloud.google.com) |
| 0:17 | Clica em "Select a project" (Selecionar projeto) no topo e escolhe um projeto existente |

**Por que:** O AI Studio precisa de um projeto GCP associado para criar a API key. Selecionar o projeto primeiro garante que a key fica vinculada ao projeto correto.

### Etapa 2: Acessar Google AI Studio (0:23 - 0:41)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:23 | Abre uma nova aba e pesquisa por "Google AI Studio" |
| 0:30 | Acessa a pagina oficial e clica no botao "Get started" |
| 0:37 | Aceita os Termos de Servico e clica em "Continuar" |

**URL direta:** https://aistudio.google.com/

### Etapa 3: Criar API Key (0:42 - 1:23)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:42 | No menu da esquerda, clica em "Get API key" |
| 0:46 | Clica no botao "Create API key" |
| 0:55 | Aparece um popup. Clica no botao "Importar projeto" |
| 1:01 | Seleciona o projeto do Google Cloud que voce escolheu no começo e clica em "Importar" |
| 1:07 | Com o projeto importado selecionado, clica no botao "Create key" |
| 1:12 | A chave (API Key) e gerada |
| 1:17 | Clica nela e copia a longa string de caracteres |
| 1:23 | Vai para o VS Code (`.env`), acha a variavel `GOOGLE_API_KEY` e cola a chave la. FIM |

**Caminho no AI Studio:** Menu esquerdo > Get API key > Create API key > Importar projeto > Create key

**Variavel no `.env`:**
```env
GOOGLE_API_KEY=AIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Fluxo Resumido

```
1. Google Cloud Console → selecionar projeto
2. Google AI Studio → Get started → aceitar termos
3. Get API key → Create API key
4. Importar projeto GCP → Create key
5. Copiar key → colar no .env em GOOGLE_API_KEY
```

---

## Checklist de Verificacao

- [ ] Projeto existente no Google Cloud Console selecionado
- [ ] Google AI Studio acessado e termos aceitos
- [ ] Projeto importado no AI Studio
- [ ] API Key criada com sucesso
- [ ] Key copiada e colada em `GOOGLE_API_KEY` no `.env`
- [ ] Key guardada em local seguro (nao sera exibida novamente no AI Studio)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Nao aparece opcao de importar projeto | Conta Google nao tem projetos no GCP | Criar um projeto primeiro em console.cloud.google.com |
| "Quota exceeded" apos configurar | Key correta mas free tier esgotou | Verificar quotas em console.cloud.google.com > APIs > Quotas. Considerar habilitar billing |
| Agente nao inicia: `GEMINI_NOT_CONFIGURED` | `GOOGLE_API_KEY` vazia ou errada no `.env` | Verificar variavel. Testar key: `curl "https://generativelanguage.googleapis.com/v1/models?key=SUA_KEY"` |
| "API key not valid" nos logs | Key expirada, deletada ou projeto errado | Recriar key no AI Studio. Verificar que o projeto e o mesmo |
| Erro 403 "Permission denied" | API "Generative Language API" nao habilitada no projeto | No Google Cloud Console: APIs & Services > Library > buscar "Generative Language API" > Enable |

---

## Notas Tecnicas

- Em multi-tenant (GA-007), cada tenant deve ter sua PROPRIA key. A key do `.env` e fallback do owner/dev.
- Logs do backend mostram `source=tenant` (key do banco) ou `source=env` (key do `.env`). Em producao, `source=env` e um red flag — significa que o tenant nao configurou sua key.
- Para validar todas as keys dos tenants: `python scripts/validar_gemini_keys.py`
- O modelo padrao e `gemini-2.5-flash` com fallback para `gemini-2.5-pro` em erros 503.
- A key criada no AI Studio funciona tanto para a API GenAI direta quanto para o Google ADK.

---

## Documentacao Relacionada

- docs/GA-007-README.md — Gemini multi-tenant (keys por tenant)
- docs/GA-007-RESUMO.md — resumo executivo da feature
- README_ENV.md secao "GOOGLE AI / VERTEX / GENAI"
- Video 06 — passo anterior: configuracao do GHL
- Video 08 — proximo passo: configuracao da Z-API (WhatsApp)
