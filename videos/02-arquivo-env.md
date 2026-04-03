# Video 02: Arquivo .env

**Duracao:** ~0:19
**Categoria:** Setup Inicial
**Pre-requisitos:** Video 01 concluido (repositorio clonado)
**Resultado esperado:** Arquivo `.env` pronto para configuracao

---

## Resumo

Video curto e direto. Ensina a renomear o arquivo `env.example` para `.env`. Sem esse passo, a aplicacao nao tem nenhuma configuracao e nao inicia.

---

## Timeline Detalhada

### Etapa unica: Renomear env.example para .env (0:00 - 0:19)

| Timestamp | O que acontece na tela |
|-----------|----------------------|
| 0:00 | Abre o VS Code (Visual Studio Code) |
| 0:02 | Texto na tela explica que apos clonar, o projeto vem com um arquivo de exemplo chamado `env.example` |
| 0:10 | Mouse vai na barra lateral esquerda (Explorer) e localiza o arquivo `env.example` |
| 0:12 | Instrucao pede para clicar com o botao direito no arquivo ou apertar F2 |
| 0:19 | Usuario apaga a palavra "example" e o ponto, deixando o nome do arquivo exatamente como `.env`. FIM |

**Acao no VS Code:**
1. Abrir o projeto no VS Code
2. Na barra lateral (Explorer), encontrar `env.example`
3. Botao direito → Rename (ou selecionar e apertar F2)
4. Apagar `.example` do nome → resultado final: `.env`

**Comando equivalente (terminal):**
```bash
# Na raiz do projeto growth-ai-agents/
mv env.example .env
# ou
cp env.example .env   # se quiser manter o original como backup
```

---

## Checklist de Verificacao

- [ ] VS Code aberto com o projeto
- [ ] Arquivo `env.example` localizado na raiz do projeto
- [ ] Arquivo renomeado para `.env` (sem a palavra "example")
- [ ] Arquivo `.env` visivel na barra lateral do VS Code

---

## Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Nao encontra `env.example` no Explorer | Arquivo pode estar oculto ou VS Code abriu a pasta errada | Verificar se abriu a pasta `growth-ai-agents/` (nao a pasta pai). No terminal: `ls -la` para ver arquivos ocultos |
| Arquivo `.env` nao aparece no Explorer apos renomear | VS Code pode filtrar arquivos dotfiles | Verificar em Settings > Files: Exclude se `.env` esta excluido. Ou verificar no terminal: `ls -la .env` |
| App nao inicia mesmo com `.env` | Arquivo foi renomeado mas esta vazio ou corrompido | Verificar conteudo: `cat .env`. Deve ter ~450 linhas de configuracao |
| Renomeou para `env` sem o ponto | Nome errado — Django procura `.env` (com ponto) | Renomear novamente: botao direito → Rename → adicionar o ponto no inicio |

---

## Nota Tecnica

O arquivo `.env` contem TODAS as variaveis de ambiente do projeto:
- Credenciais de banco (PostgreSQL)
- Credenciais Redis
- Chaves de API (Gemini, Z-API, GHL)
- Configuracoes de frontend (dominio, branding)
- Configuracoes de CI/CD (GitLab, GCP)
- Superusuario do sistema

**NUNCA commitar o `.env` no Git.** Ele ja esta no `.gitignore` por padrao.

O `env.example` e mantido no repo como template — contem os nomes das variaveis com valores de exemplo, sem dados sensiveis.

---

## Documentacao Relacionada

- README_ENV.md (no repo) — referencia completa de todas as variaveis
- Video 01 — passo anterior: clonar repositorio
- Video 03 — proximo passo: configurar missao e identidade
