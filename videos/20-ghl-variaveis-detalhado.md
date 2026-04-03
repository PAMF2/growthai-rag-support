# Video 20: Configuracao Detalhada das Variaveis GHL

**Duracao:** ~2:30
**Categoria:** Integracao CRM
**Pre-requisitos:** Conta no GoHighLevel com acesso admin
**Resultado esperado:** 3 variaveis GHL preenchidas no `.env` (Location ID, PIT, Pipeline ID)

---

## Resumo

Video focado e detalhado mostrando como preencher as 3 variaveis principais do GoHighLevel no `.env`. Similar ao Video 06, mas com foco no editor de codigo e no fluxo passo a passo de cada variavel.

---

## Timeline Detalhada

### Etapa 1: Identificar variaveis no .env (0:00 - 0:25)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Video inicia no editor de codigo |
| 0:00 | Destaca 3 variaveis do GoHighLevel que precisam ser preenchidas: `GHL_LOCATION_ID`, `GHL_PIT` e `GHL_PIPELINE_ID` |

### Etapa 2: Copiar Location ID (0:26 - 0:55)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:26 | Acessa o dashboard do GoHighLevel |
| 0:26 | Navega ate "Configuracoes" > "Perfil da empresa" |
| 0:46 | Copia o "ID de Localizacao" |
| 0:46 | Retorna ao editor de codigo |
| 0:56 | Cola o valor copiado na variavel `GHL_LOCATION_ID` |

**Caminho:** GHL > Configuracoes > Perfil da Empresa > ID de Localizacao

```env
GHL_LOCATION_ID=loc_xxxxxxxxxxxxxxxx
```

### Etapa 3: Criar PIT e copiar token (0:56 - 1:37)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:56 | De volta ao GHL, acessa a aba "Integracoes Privado" |
| 1:04 | Cria uma nova integracao (nome: "PIT Teste") |
| 1:15 | Seleciona TODOS os escopos disponiveis |
| 1:22 | Confirma a criacao |
| 1:28 | Copia o token gerado |
| 1:32 | Cola o token na variavel `GHL_PIT` no editor |

**Caminho:** GHL > Configuracoes > Integracoes > Privado > Criar nova integracao

**Passos:**
1. Nome: "PIT Teste" (ou nome descritivo)
2. Escopos: **Selecionar tudo**
3. Criar > Confirmar
4. Copiar token

```env
GHL_PIT=pit_xxxxxxxxxxxxxxxxxxxxxxxx
```

**IMPORTANTE:** O token so aparece uma vez. Se perder, criar outro.

### Etapa 4: Extrair Pipeline ID (1:38 - 2:30)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:38 | No GHL, acessa "Leads" > "Pipelines" |
| 1:45 | Clica em "Gerenciar permissoes" na pipeline de vendas desejada |
| 1:56 | Copia o link da pipeline |
| 2:06 | Cola o link num bloco de notas para ler inteiro |
| 2:10 | Seleciona e copia apenas o ID no final da URL (apos `/pipeline/`) |
| 2:18 | Cola o ID na variavel `GHL_PIPELINE_ID` no editor |
| 2:30 | Configuracao do GHL concluida. FIM |

**Como extrair o Pipeline ID:**
```
URL completa: https://app.gohighlevel.com/v2/location/xxx/pipeline/ABC123DEF456
                                                                     ^^^^^^^^^^^
Pipeline ID: ABC123DEF456 (tudo depois de /pipeline/)
```

```env
GHL_PIPELINE_ID=ABC123DEF456
```

---

## Resumo das 3 Variaveis

| Variavel | Onde no GHL | Como copiar |
|----------|-------------|-------------|
| `GHL_LOCATION_ID` | Configuracoes > Perfil da Empresa | Copiar direto do campo |
| `GHL_PIT` | Integracoes > Privado > Criar | Token gerado na criacao |
| `GHL_PIPELINE_ID` | Leads > Pipelines > Copiar link | Extrair ID do final da URL |

---

## Checklist de Verificacao

- [ ] `GHL_LOCATION_ID` preenchido
- [ ] Integracao privada criada com todos os escopos
- [ ] `GHL_PIT` preenchido (token guardado)
- [ ] `GHL_PIPELINE_ID` preenchido (ID extraido da URL)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Nao encontra "Integracoes Privado" | Sem permissao admin | Pedir acesso admin |
| Pipeline ID copiado errado | Copiou URL inteira | Extrair so o trecho apos `/pipeline/` |
| "GHL connection failed" | PIT sem todos os escopos | Recriar com "Selecionar tudo" |

---

## Documentacao Relacionada

- Video 06 — versao anterior (com Calendar ID tambem)
- Video 18 — configuracao GHL via frontend
- Video 21 — proximo: Google Cloud OAuth
