# Video 01: Clonando o Repositorio

**Duracao:** ~2:33
**Categoria:** Setup Inicial
**Pre-requisitos:** Git instalado, conta no GitLab, acesso ao repositorio original
**Resultado esperado:** Projeto clonado localmente com remote apontando para o GitLab do aluno

---

## Resumo

Este video ensina como clonar o repositorio GrowthAI do GitLab do professor, remover o remote original e configurar o remote para o repositorio proprio do aluno. E o primeiro passo obrigatorio antes de qualquer configuracao.

---

## Timeline Detalhada

### Abertura (0:00 - 0:07)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Tela preta com logomarca roxa "Accelera 360 - business acceleration" |
| 0:02 | Titulo do video: "Como clonar um repositorio e configurar a origem para o seu proprio GitLab" |

### Etapa 1: Acessar o repositorio no GitLab (0:08 - 0:23)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:08 | Tela de transicao. Abre o navegador no GitLab, mostrando o projeto original `growth-ai-agents` |
| 0:10 | Texto na tela informa que o usuario recebera o link de acesso ao repositorio |

**O que o aluno precisa ter:** O link do repositorio original fornecido pelo professor/Accelera.

### Etapa 2: Criar pasta e abrir terminal (0:24 - 0:39)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:24 | Area de Trabalho do Windows. Mouse clica com botao direito para criar "Nova pasta" |
| 0:28 | Texto instrui a criar uma pasta com o nome de sua preferencia |
| 0:34 | Pasta aberta. Mouse clica com botao direito dentro dela e seleciona "Abrir no terminal" (Terminal Linux/Ubuntu) |

**Comando equivalente:**
```bash
mkdir minha-pasta
cd minha-pasta
```

### Etapa 3: Clonar o repositorio (0:40 - 1:22)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:40 | Volta para o GitLab. Mouse clica no botao azul "Code" (ou Clone) e copia a URL em "Clone with HTTPS" |
| 0:48 | Volta para o terminal escuro. Instrucao diz para digitar `git clone` e colar o link |
| 0:53 | Texto avisa que o terminal vai pedir usuario e senha |
| 1:00 | Dica visual apontando para a foto de perfil no canto superior direito do GitLab para descobrir o @Username exato |
| 1:08 | No terminal, usuario digita o Username e aperta Enter |
| 1:12 | Usuario digita o Password (senha fica invisivel no terminal) e aperta Enter |
| 1:18 | Processo de "Downloading objects: 100%" e concluido no terminal |

**Comando executado:**
```bash
git clone https://gitlab.com/accelera3601/growth-ai-agents.git
# Terminal pede:
# Username: seu_usuario_gitlab
# Password: sua_senha (invisivel)
```

**Dica importante:** Se o aluno usa autenticacao de dois fatores (2FA), precisa usar um Personal Access Token em vez da senha. Gerar em: GitLab > Settings > Access Tokens.

### Etapa 4: Entrar na pasta do projeto (1:23 - 1:41)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:23 | Tela de transicao para a proxima etapa |
| 1:33 | No terminal, e digitado o comando para entrar na pasta baixada |

**Comando executado:**
```bash
cd growth-ai-agents/
```

### Etapa 5: Remover remote original (1:42 - 1:59)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 1:42 | Digitado o comando para remover o link com o repositorio do professor |
| 1:50 | Mensagem na tela confirma que a origem foi removida com sucesso |

**Comando executado:**
```bash
git remote remove origin
```

**Por que fazer isso:** O projeto veio com o `origin` apontando para o repo do professor. Se nao remover, o aluno faria push para o repo errado.

### Etapa 6: Adicionar novo remote (2:00 - 2:33)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 2:00 | Texto: "Agora vamos adicionar a nova origem, que sera o repositorio criado pelo usuario" |
| 2:07 | Mostra o GitLab do aluno (projeto vazio recem-criado). Mouse copia a segunda linha de comando da tela |
| 2:14 | Comando colado no terminal, usuario aperta Enter |
| 2:22 | Para conferir, digita-se `git remote -v` |
| 2:33 | Terminal exibe os dois links (fetch e push) apontando para o GitLab correto do aluno. FIM |

**Comandos executados:**
```bash
git remote add origin https://gitlab.com/aluno/seu-projeto.git
git remote -v
# Deve mostrar:
# origin  https://gitlab.com/aluno/seu-projeto.git (fetch)
# origin  https://gitlab.com/aluno/seu-projeto.git (push)
```

---

## Checklist de Verificacao

- [ ] Pasta criada no computador
- [ ] `git clone` executado com sucesso (100% downloaded)
- [ ] `cd growth-ai-agents/` executado
- [ ] `git remote remove origin` executado
- [ ] Novo repositorio criado no GitLab do aluno
- [ ] `git remote add origin <URL_DO_ALUNO>` executado
- [ ] `git remote -v` mostra fetch e push para o repo correto

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| "Authentication failed" ao clonar | Usuario/senha errados ou 2FA ativado | Verificar @Username no GitLab. Se tem 2FA, usar Personal Access Token |
| "fatal: repository not found" | URL errada ou sem permissao | Verificar se tem acesso ao repo original. Pedir link atualizado |
| Pasta `growth-ai-agents` nao aparece apos clone | Clone falhou silenciosamente | Rolar o terminal para cima e verificar erros. Tentar novamente |
| `git remote -v` mostra o repo do professor | Esqueceu de executar `git remote remove origin` | Executar `git remote remove origin` e depois `git remote add origin <URL>` |
| "fatal: remote origin already exists" | Tentou adicionar origin sem remover o antigo | Executar `git remote remove origin` primeiro |

---

## Documentacao Relacionada

- README-CLONAR.md (no repo) — guia escrito equivalente
- Video 02 — proximo passo: renomear .env
