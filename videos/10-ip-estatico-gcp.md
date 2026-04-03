# Video 10: Como Configurar um IP Estatico na VM

**Duracao:** ~1:45
**Categoria:** Infraestrutura GCP
**Pre-requisitos:** Video 09 concluido (VM criada no GCP)
**Resultado esperado:** IP externo da VM mudado de Ephemeral para Static

---

## Resumo

Video curto. Reserva um IP estatico no Google Cloud e associa a VM. Sem isso, o IP muda toda vez que a VM reinicia, quebrando DNS, NGINX, webhooks e tudo que depende do endereco fixo.

---

## Timeline Detalhada

### Abertura (0:00 - 0:04)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Titulo: "Como configurar um IP estatico na VM do Google Cloud" |

### Etapa 1: Acessar a tela de IPs (0:05 - 0:21)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:05 | Na busca do Google Cloud, digita e acessa "VPC network" |
| 0:14 | No menu da esquerda, clica em "IP addresses" |
| 0:22 | Mostra a lista de IPs e aponta para o "External IP" provisorio da VM |

### Etapa 2: Reservar IP estatico (1:03 - 1:31)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:03 | No topo da pagina, clica em "Reserve external static IP address" |
| 1:10 | Preenche o campo Name (ex: `ip-vm-work`) |
| 1:15 | No campo "Attached to", abre a caixa suspensa e seleciona a VM recem-criada |
| 1:21 | Clica no botao "Reserve" |
| 1:31 | Tela de IPs recarrega e mostra que o campo "Type" mudou de "Ephemeral" para "Static" |

**Caminho no GCP:** VPC Network > IP addresses > Reserve external static IP address

**Configuracao:**
```
Name:        ip-vm-work (ou nome de preferencia)
Type:        External
Version:     IPv4
Region:      mesma regiao da VM
Attached to: [sua VM]
```

### Encerramento (1:31 - 1:45)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:45 | Instrucao final: "Anote e guarde o numero desse IP Estatico, pois ele sera usado no VS Code". FIM |

**IMPORTANTE:** Anotar o IP. Ele sera usado em:
- `GCP_VM_HOST` no `.env` (Video 11)
- Configuracao DNS do dominio
- `ALLOWED_HOSTS` no `.env`

---

## Checklist de Verificacao

- [ ] IP estatico reservado no GCP
- [ ] IP associado a VM correta
- [ ] Coluna "Type" mostra "Static" (nao "Ephemeral")
- [ ] IP anotado para uso posterior

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| "Quota 'STATIC_ADDRESSES' exceeded" | Limite de IPs estaticos na regiao | Liberar IPs nao usados ou solicitar aumento de cota |
| VM nao aparece no dropdown "Attached to" | VM esta em regiao diferente do IP | Criar o IP na mesma regiao da VM |
| IP mudou mesmo sendo estatico | IP foi desassociado acidentalmente | Reassociar em IP addresses > editar |
| Cobranca por IP nao usado | IP reservado sem VM associada e cobrado | Sempre associar a uma VM ou deletar se nao usar |

---

## Nota Tecnica

- IPs estaticos no GCP sao gratuitos ENQUANTO estao associados a uma VM rodando.
- Se a VM estiver parada ou o IP nao estiver associado, o GCP cobra ~$0.01/hora.
- O IP estatico persiste mesmo se a VM for deletada — precisa liberar manualmente.

---

## Documentacao Relacionada

- README-IP.md — guia escrito equivalente
- Video 09 — passo anterior: firewall + VM + service account
- Video 11 — proximo passo: CI/CD e deploy
