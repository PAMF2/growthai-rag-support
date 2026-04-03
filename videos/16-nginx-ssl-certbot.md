# Video 16: Instalacao e Configuracao do NGINX e SSL

**Duracao:** ~3:10
**Categoria:** Web Server / SSL
**Pre-requisitos:** Videos 09-15 (VM rodando, dominio apontando para IP, Cloudflare configurado)
**Resultado esperado:** NGINX configurado como reverse proxy + certificado SSL (HTTPS) ativo

---

## Resumo

Instala NGINX na VM, configura como reverse proxy (frontend na porta 3000, backend na 8000, webhooks com timeouts longos), gera certificado SSL com Certbot. Ao final, o site esta acessivel via HTTPS no dominio proprio.

---

## Timeline Detalhada

### Etapa 1: Acessar VM e instalar NGINX (0:00 - 0:44)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Google Cloud > Compute Engine > VM instances. Clica "SSH" na VM |
| 0:28 | No terminal: `sudo apt update` |
| 0:28 | `sudo apt install nginx -y` |

**Comandos:**
```bash
sudo apt update
sudo apt install nginx -y
```

### Etapa 2: Criar arquivo de configuracao (0:45 - 1:32)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:45 | Cria/abre o arquivo de configuracao: `sudo vim /etc/nginx/sites-available/accelera360.co` |
| 1:04 | Cola o bloco de configuracao do NGINX |
| 1:04 | Na linha `server_name`, apaga o exemplo e escreve o dominio real: `server_name accelera360.co www.accelera360.co;` |
| 1:32 | Pressiona ESC, digita `:wq` e Enter para salvar |

**Comando:**
```bash
sudo vim /etc/nginx/sites-available/seudominio.com
```

**Bloco de configuracao NGINX (copiar inteiro):**
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    # FRONTEND (Next.js)
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # BACKEND API
    location /api/ {
        proxy_pass http://127.0.0.1:8081/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
    }

    # WEBHOOKS (timeouts longos para processamento de agentes IA)
    location /webhooks/ {
        proxy_pass http://127.0.0.1:8081/webhooks/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_buffering off;
    }
}
```

**IMPORTANTE:** Substituir `seudominio.com` e `www.seudominio.com` pelo dominio real em `server_name`.

**Mapeamento de portas:**
| Location | Proxy para | Servico |
|----------|-----------|---------|
| `/` | `127.0.0.1:3000` | Frontend (Next.js) |
| `/api/` | `127.0.0.1:8081/api/` | Backend (Django) |
| `/webhooks/` | `127.0.0.1:8081/webhooks/` | Webhooks (Z-API → Django) |

**Por que 300s de timeout nos webhooks:** O agente AI pode levar ate 180s para processar uma mensagem complexa (ADK_AGENT_EXECUTION_TIMEOUT_SECONDS=180). O timeout de 300s no NGINX garante que a conexao nao cai durante o processamento.

### Etapa 3: Ativar site e testar (1:33 - 2:10)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:33 | Cria link simbolico para ativar o site |
| 1:57 | Testa configuracao: `sudo nginx -t` → "syntax is ok" + "test is successful" |
| 1:57 | Recarrega NGINX: `sudo systemctl reload nginx` |

**Comandos:**
```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/seudominio.com /etc/nginx/sites-enabled/seudominio.com

# Testar configuracao
sudo nginx -t

# Recarregar
sudo systemctl reload nginx
```

### Etapa 4: Instalar Certbot e gerar SSL (2:11 - 3:10)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:11 | Instala Certbot: `sudo apt install certbot python3-certbot-nginx -y` |
| 2:35 | Gera certificado: `sudo certbot --nginx -d accelera360.co -d www.accelera360.co` |
| 2:35 | Terminal pede email → digita email |
| 2:35 | Aceitar termos → digita `y` |
| 2:35 | Receber emails da EFF → digita `n` |
| 3:10 | Mensagem final confirma: certificado emitido com sucesso! FIM |

**Comandos:**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Gerar certificado SSL
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

**Prompts do Certbot:**
| Prompt | Resposta |
|--------|----------|
| Enter email address | Seu email real (para avisos de expiracao) |
| Agree to terms? | `Y` |
| Share email with EFF? | `N` |

---

## Checklist de Verificacao

- [ ] NGINX instalado (`nginx -v` retorna versao)
- [ ] Arquivo de configuracao criado em `/etc/nginx/sites-available/seudominio`
- [ ] `server_name` com dominio correto (com e sem www)
- [ ] Link simbolico criado em `sites-enabled`
- [ ] `sudo nginx -t` retorna "syntax is ok"
- [ ] NGINX recarregado
- [ ] Certbot instalado
- [ ] Certificado SSL gerado com sucesso
- [ ] Site acessivel via `https://seudominio.com`
- [ ] Cadeado verde aparece no navegador

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| `nginx -t` falha com "syntax error" | Erro no bloco de configuracao (faltou `;` ou `}`) | Verificar o arquivo. Cada diretiva termina com `;`, cada bloco com `}` |
| Certbot falha: "Could not find a valid DNS record" | Dominio nao aponta para o IP da VM | Verificar DNS (Video 14). `nslookup seudominio.com` deve retornar IP da VM |
| Certbot falha: "Connection refused" | Porta 80 bloqueada | Verificar regra de firewall `allow-http` (Video 09) |
| "502 Bad Gateway" | Backend ou frontend nao esta rodando | `docker ps` para verificar containers |
| "504 Gateway Timeout" | Processamento do agente excede timeout | Aumentar `proxy_read_timeout` no NGINX |
| "Too many redirects" com Cloudflare | Conflito SSL Cloudflare + Certbot | Cloudflare SSL → "Full (Strict)". Nao usar "Flexible" |
| Site HTTP funciona mas HTTPS nao | Certbot nao conseguiu configurar | Rodar `sudo certbot --nginx` novamente |
| Certificado expira | Nao renovou automaticamente | `sudo certbot renew --dry-run` para testar. Certbot cria cron automatico |

---

## Notas Tecnicas

- O Certbot configura automaticamente o NGINX para redirecionar HTTP → HTTPS.
- O certificado Let's Encrypt expira a cada 90 dias. O Certbot instala um cron que renova automaticamente.
- Se usar Cloudflare com proxy ativo (nuvem laranja), o SSL do Cloudflare ja encripta ate o edge. O Certbot encripta do edge ate a VM (end-to-end).
- Para usar Cloudflare + Certbot: SSL mode = "Full (Strict)" no Cloudflare.
- O `proxy_buffering off` nos webhooks garante que a resposta e enviada imediatamente, sem buffer.

---

## Documentacao Relacionada

- README-NGINX.md — guia escrito com o mesmo conteudo
- Video 15 — passo anterior: Cloudflare
- Video 17+ — proximos passos (pendente)
