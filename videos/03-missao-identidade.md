# Video 03: Missao e Identidade

**Duracao:** ~0:58
**Categoria:** Configuracao de Branding
**Pre-requisitos:** Videos 01 e 02 concluidos (repo clonado, `.env` renomeado)
**Resultado esperado:** Missao da empresa definida e variaveis de identidade visual preenchidas

---

## Resumo

Configura dois elementos fundamentais: o texto de missao da empresa (usado pelo agente AI para contexto) e as variaveis de identidade visual que aparecem no frontend e nas mensagens do WhatsApp. Se o aluno pular este video, o bot vai se identificar como "Accelera" em vez do nome da empresa dele.

---

## Timeline Detalhada

### Abertura (0:00 - 0:05)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Configurando a missao e identidade da operacao" |

### Etapa 1: Configurar a missao da empresa (0:06 - 0:24)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:06 | No VS Code, mouse clica na pasta `business_mission` na barra lateral |
| 0:11 | Dentro dela, clica no arquivo `MISSION.md` |
| 0:16 | Tela mostra o texto padrao: "Accelera 360 acelera a transformacao..." |
| 0:18 | Instrucao pede para apagar o texto padrao e descrever a missao da SUA empresa em no maximo 10 linhas |

**Arquivo:** `business_mission/MISSION.md`

**Conteudo padrao (apagar):**
```
Accelera 360 acelera a transformacao digital de empresas na America Latina,
implementando estrategicamente Fluxos de Agentes de IA nas operacoes dos clientes.
Transformamos empresas em referencia no uso de Agentes de IA,
com fluxos inteligentes, ferramentas avancadas e foco em resultado real.
```

**O que colocar:** A missao da empresa do aluno. Maximo 10 linhas. Exemplo:
```
A [Nome da Empresa] ajuda pequenas e medias empresas a automatizar
seu processo de vendas usando inteligencia artificial.
Nosso foco e qualificacao de leads e agendamento automatico
para que sua equipe comercial foque no que importa: fechar negocios.
```

**Por que isso importa:** O agente AI usa este texto como contexto para entender a empresa. Afeta como o bot se apresenta e responde no WhatsApp.

### Etapa 2: Configurar variaveis de identidade visual (0:25 - 0:58)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:25 | Usuario clica no arquivo `.env` (renomeado no video anterior) |
| 0:30 | Codigo rola para baixo ate a linha ~93, na aba `# INTERFACE / IDENTIDADE VISUAL` |
| 0:35 | Seta vermelha aponta para `TITULO_MENU` — nome que aparece no menu do frontend |
| 0:37 | Seta aponta para `TITULO_PAGE_AGENTES` — titulo da pagina de agentes |
| 0:39 | Seta aponta para `NAME_ATENDENTE_CHAT` — nome do atendente virtual no WhatsApp |
| 0:41 | Seta aponta para `CORPORATE_NAME` — nome corporativo da empresa |
| 0:43 | Seta aponta para `LINK_PROJETO` — URL do site da empresa |
| 0:46 | Texto explica que essas informacoes aparecem no Frontend e nas mensagens do WhatsApp do robo |
| 0:58 | Aviso: "Essa configuracao e extremamente importante pois define a identidade visual". FIM |

**Variaveis no `.env` (linha ~93):**

```env
#########################################################
# CONFIGURACOES DE INTERFACE (FRONTEND)
#########################################################

TITULO_MENU="Nome da Empresa"
TITULO_PAGE_AGENTES="Nome da Empresa - Agents"
NAME_ATENDENTE_CHAT="Nome do Atendente"
CORPORATE_NAME="NOME CORPORATIVO"
LINK_PROJETO="https://seusite.com.br/"
```

**Onde cada variavel aparece:**

| Variavel | Onde aparece | Exemplo |
|----------|-------------|---------|
| `TITULO_MENU` | Menu lateral do frontend (sidebar) | "MegaVendas" |
| `TITULO_PAGE_AGENTES` | Titulo da aba do navegador na pagina de agentes | "MegaVendas - Agents" |
| `NAME_ATENDENTE_CHAT` | Nome do bot nas mensagens do WhatsApp | "Julia" |
| `CORPORATE_NAME` | Assinatura em emails e mensagens corporativas | "MEGAVENDAS LTDA" |
| `LINK_PROJETO` | Link institucional no footer e emails | "https://megavendas.com.br/" |

---

## Checklist de Verificacao

- [ ] `business_mission/MISSION.md` editado com a missao da empresa (max 10 linhas)
- [ ] `TITULO_MENU` preenchido no `.env`
- [ ] `TITULO_PAGE_AGENTES` preenchido no `.env`
- [ ] `NAME_ATENDENTE_CHAT` preenchido no `.env`
- [ ] `CORPORATE_NAME` preenchido no `.env`
- [ ] `LINK_PROJETO` preenchido no `.env`

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Bot se apresenta como "Kelvin" ou "Accelera" no WhatsApp | `NAME_ATENDENTE_CHAT` e/ou `CORPORATE_NAME` nao foram alterados | Editar as variaveis no `.env` e reiniciar os containers |
| Frontend mostra "Accelera" no menu | `TITULO_MENU` nao foi alterado | Editar no `.env`, rebuild do frontend necessario |
| Link no email aponta para accelera360.com.br | `LINK_PROJETO` nao foi alterado | Editar no `.env` |
| Agente AI nao sabe descrever a empresa | `MISSION.md` nao foi editado ou esta vazio | Escrever a missao da empresa no arquivo |

---

## Nota Tecnica

- As variaveis de identidade sao lidas pelo frontend em tempo de build (Next.js). Em producao, apos alterar, e necessario rebuild do frontend.
- Em dev local com `docker-compose.dev.yml`, as variaveis sao lidas via hot-reload (nao precisa rebuild).
- O `MISSION.md` e lido pelo backend para dar contexto ao agente. Alteracoes sao refletidas apos restart do container backend.

---

## Documentacao Relacionada

- `.env.example` linhas 93-120 — template das variaveis
- README_ENV.md — referencia completa
- Video 02 — passo anterior: renomear .env
- Video 04 — proximo passo: configurar frontend e dominio
