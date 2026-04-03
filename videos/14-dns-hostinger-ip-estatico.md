# Video 14: Configurando o IP Estatico na Hostinger (DNS)

**Duracao:** ~1:34
**Categoria:** Dominio e DNS
**Pre-requisitos:** Video 13 (dominio comprado), Video 10 (IP estatico reservado no GCP)
**Resultado esperado:** Dominio apontando para o IP da VM via registros DNS tipo A

---

## Resumo

Aponta o dominio comprado para o IP estatico da VM no Google Cloud. Cria dois registros DNS tipo A (@ e www) na Hostinger para que tanto `seudominio.com` quanto `www.seudominio.com` levem ao servidor.

---

## Timeline Detalhada

### Setup (0:00 - 0:14)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Tela dividida: Google Cloud (VM Instances) na esquerda e Hostinger (Dominios) na direita |
| 0:00 | Objetivo: apontar o dominio para o IP da VM |

### Etapa 1: Editar registro A principal (@) (0:15 - 0:49)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:15 | Na Hostinger: "Dominios" > "Meus dominios" > "Gerenciar" > "DNS / Nameservers" |
| 0:31 | Localiza o registro tipo A com nome `@` |
| 0:31 | Clica em "Editar" |
| 0:31 | No campo "Apontar para", cola o IP Externo Estatico da VM do Google Cloud |
| 0:49 | Clica em "Atualizar" |

**Registro editado:**
```
Tipo: A
Nome: @
Apontar para: 35.xxx.xxx.xxx (IP estatico da VM)
```

### Etapa 2: Remover CNAME www existente (0:50 - 1:00)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:50 | Localiza registro existente tipo CNAME com nome `www` |
| 1:00 | Exclui esse registro |

**Por que:** O CNAME www antigo provavelmente aponta para o hosting padrao da Hostinger. Precisa ser substituido por um registro A apontando para a VM.

### Etapa 3: Criar registro A para www (1:01 - 1:23)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:01 | Sobe a pagina e cria um novo registro |
| 1:01 | Tipo: `A` |
| 1:01 | Nome: `www` |
| 1:01 | Apontar para: IP externo da VM (mesmo IP) |
| 1:01 | TTL: `300` |
| 1:23 | Clica em "Adicionar registro" |

**Registro criado:**
```
Tipo: A
Nome: www
Apontar para: 35.xxx.xxx.xxx (mesmo IP estatico)
TTL: 300
```

### Verificacao final (1:24 - 1:34)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:24 | Mostra a lista final de DNS |
| 1:34 | Dois registros tipo A (@ e www), ambos apontando para o IP do Google Cloud. FIM |

**Estado final do DNS:**
```
Tipo    Nome    Apontar para         TTL
A       @       35.xxx.xxx.xxx       300
A       www     35.xxx.xxx.xxx       300
```

---

## Checklist de Verificacao

- [ ] Registro A com nome `@` editado para o IP da VM
- [ ] Registro CNAME `www` antigo excluido
- [ ] Novo registro A com nome `www` criado apontando para o IP da VM
- [ ] Ambos os registros mostram o mesmo IP
- [ ] Propagacao DNS iniciada (pode levar ate 48h, geralmente minutos)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Site nao abre apos configurar DNS | Propagacao DNS ainda nao completou | Aguardar 5-30 min. Testar com `nslookup seudominio.com` |
| "This site can't be reached" | IP errado ou VM parada | Verificar IP no GCP e que a VM esta running |
| www funciona mas dominio sem www nao | Registro `@` nao foi editado | Verificar que ambos os registros A existem |
| Dominio sem www funciona mas www nao | Registro `www` nao foi criado | Criar registro A para `www` |

**Teste rapido (terminal):**
```bash
nslookup seudominio.com
# Deve retornar o IP da VM

nslookup www.seudominio.com
# Deve retornar o mesmo IP
```

---

## Documentacao Relacionada

- README-IP.md — guia de IP estatico
- Video 10 — IP estatico no GCP
- Video 13 — passo anterior: comprar dominio
- Video 15 — proximo passo: Cloudflare
