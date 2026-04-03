# Video 15: Configuracao Cloudflare com Hostinger

**Duracao:** ~3:11
**Categoria:** CDN / Protecao / DNS
**Pre-requisitos:** Video 14 (DNS configurado na Hostinger), conta no Cloudflare
**Resultado esperado:** Cloudflare gerenciando o DNS do dominio (nameservers atualizados)

---

## Resumo

Migra o gerenciamento DNS da Hostinger para o Cloudflare. Isso adiciona: protecao DDoS, CDN global, certificado SSL automatico, cache, analytics e firewall. O Cloudflare passa a ser o intermediario entre o usuario e o servidor.

---

## Timeline Detalhada

### Etapa 1: Adicionar site no Cloudflare (0:00 - 1:15)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Abre o site da Cloudflare, faz login |
| 0:20 | Clica no botao azul "Adicionar" (site) |
| 0:20 | Responde questionario rapido: Profissional > Marketing > Tamanho da empresa > Proteja aplicativos e usuarios > Sites publicos |
| 0:49 | Insere o dominio (ex: `accelera360.co`) e clica "Continuar" |
| 1:16 | Rola para baixo, seleciona Plano **Free** ($0) e clica "Continuar" |

### Etapa 2: Verificar registros DNS importados (1:16 - 1:42)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:29 | Cloudflare faz varredura no DNS |
| 1:29 | Tela exibe os registros DNS importados (os IPs da Hostinger) |
| 1:42 | Clica "Continuar" |

**Verificar:** Os dois registros A (@ e www) apontando para o IP da VM devem aparecer. Se nao aparecerem, adicionar manualmente.

### Etapa 3: Trocar nameservers na Hostinger (1:43 - 2:41)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:43 | Cloudflare exibe dois nameservers (ex: `ns1.cloudflare.com`, `ns2.cloudflare.com`) |
| 1:43 | Volta para a aba da Hostinger |
| 1:43 | Na secao "DNS / Nameservers", clica em "Alterar nameservers" |
| 1:43 | Apaga os nameservers da Hostinger |
| 1:43 | Cola os dois nameservers do Cloudflare |
| 2:41 | Salva |

**Nameservers a substituir:**
```
# REMOVER (nameservers da Hostinger):
ns1.dns-parking.com
ns2.dns-parking.com

# ADICIONAR (nameservers do Cloudflare — os seus serao diferentes):
ns1.cloudflare.com
ns2.cloudflare.com
```

**IMPORTANTE:** Os nameservers do Cloudflare sao UNICOS por conta. Copie exatamente os que aparecem no SEU painel Cloudflare.

### Etapa 4: Confirmar no Cloudflare (2:42 - 3:11)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:42 | Volta para o Cloudflare |
| 2:42 | Clica "Atualizei meus servidores de nomes" |
| 3:11 | Mensagem: "Aguardando que seu registrador propague...". Cloudflare agora gerencia o dominio. FIM |

**Propagacao:** Pode levar de minutos a 24h para os nameservers propagarem globalmente.

---

## O que o Cloudflare adiciona

| Feature | Beneficio |
|---------|-----------|
| CDN | Cache global, carregamento mais rapido |
| DDoS Protection | Protecao contra ataques |
| SSL/TLS | Certificado HTTPS automatico |
| Firewall | Regras de bloqueio por IP/pais |
| Analytics | Metricas de trafego |
| Bot Protection | Bloqueio de bots maliciosos |
| Always Online | Cache offline se o servidor cair |

---

## Checklist de Verificacao

- [ ] Conta Cloudflare criada e logada
- [ ] Site adicionado no Cloudflare com o dominio correto
- [ ] Plano Free selecionado
- [ ] Registros DNS importados corretamente (2 registros A: @ e www)
- [ ] Nameservers do Cloudflare copiados
- [ ] Nameservers da Hostinger substituidos pelos do Cloudflare
- [ ] Alteracao salva na Hostinger
- [ ] "Atualizei meus servidores de nomes" clicado no Cloudflare
- [ ] Aguardando propagacao (verificar status no painel Cloudflare)

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| "Pending nameserver update" por mais de 24h | Nameservers nao foram trocados corretamente | Verificar na Hostinger que APENAS os do Cloudflare estao la |
| Site para de funcionar apos trocar nameservers | Registros DNS nao foram importados pelo Cloudflare | Adicionar manualmente os registros A no painel DNS do Cloudflare |
| SSL nao funciona apos Cloudflare | Modo SSL do Cloudflare em "Off" | Cloudflare > SSL/TLS > mudar para "Full" ou "Full (Strict)" |
| "Too many redirects" | Conflito SSL entre Cloudflare e NGINX | Cloudflare SSL = "Full". Nao usar "Flexible" se o server ja tem SSL |
| Webhooks do WhatsApp param de chegar | Cloudflare bloqueando requests da Z-API | Criar regra no Firewall: permitir requests para `/webhooks/*` |

---

## Notas Tecnicas

- Apos Cloudflare ativo, o DNS e gerenciado APENAS no Cloudflare (nao mais na Hostinger).
- Qualquer alteracao DNS futura deve ser feita no painel Cloudflare.
- O Cloudflare proxy (nuvem laranja) esconde o IP real do servidor. Requests chegam pelo IP do Cloudflare.
- Para o NGINX + Certbot (Video 16), o SSL do Cloudflare deve estar em modo "Full" ou "Full (Strict)".

---

## Documentacao Relacionada

- Video 14 — passo anterior: DNS na Hostinger
- Video 16 — proximo passo: NGINX + SSL
