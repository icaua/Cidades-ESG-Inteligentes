# Configuração externa para concluir a entrega

Repositório: https://github.com/icaua/Cidades-ESG-Inteligentes

## 1. Estado confirmado em 13/10/2026

GitHub já foi publicado pela autenticação existente do Git Credential Manager.
Não é necessário reconectar a integração que retornou 403 na primeira tentativa.
Build, testes, GHCR, Compose e deploy staging passaram no run 38323935914, tentativa 2.
`RENDER_DEPLOY_HOOK_STAGING` e `STAGING_URL` estão configurados. A URL é
https://cidades-esg-staging-l9tl.onrender.com.

**Produção pendente por opção de custo zero.** O segundo PostgreSQL gratuito foi
recusado (`cannot have more than one active free tier database`). O plano mínimo
preparado custava US$ 6,30/mês com 1 GB; não foi autorizado e a criação foi cancelada.
Não há URL, banco, serviço ou hook de produção. As etapas abaixo descrevem como
reproduzir staging ou preparar produção futuramente, não recursos já existentes.

## 2. Criar staging primeiro

Entre em https://dashboard.render.com no navegador aberto nesta conversa.
Crie um banco PostgreSQL exclusivo para staging e um Web Service com **Existing Image**.
O pacote é `ghcr.io/icaua/cidades-esg-inteligentes`. Use uma tag SHA realmente
publicada pela execução do Actions; não use uma tag fictícia.

| Campo | Staging | Produção (somente após staging validado) |
| --- | --- | --- |
| Nome sugerido | cidades-esg-staging | cidades-esg-production |
| Origem | Existing Image / GHCR | Mesmo pacote GHCR |
| ASPNETCORE_ENVIRONMENT | Staging | Production |
| ASPNETCORE_HTTP_PORTS | 8080 | 8080 |
| PORT | 8080 | 8080 |
| DATABASE_URL | URL interna do banco staging | URL interna de OUTRO banco |
| Health Check Path | /health | /health |
| Instâncias | 1 | 1 |
| APP_VERSION | Não sobrescrever | Não sobrescrever |

Escolha a mesma região para cada serviço e seu banco. Escolha o plano no painel
conforme a disponibilidade da conta; qualquer cobrança deve ser aprovada pelo titular.
Se o GHCR for privado, configure uma credencial de leitura do pacote no Render.
Não coloque a credencial em arquivo versionado. A visibilidade do repositório
GitHub e a do pacote GHCR são configurações distintas.

## 3. Configurar GitHub Actions

Em Settings > Environments, crie `staging` e `production`.
Em Settings > Secrets and variables > Actions, cadastre:

| Tipo | Nome exato | Origem |
| --- | --- | --- |
| Secret | RENDER_DEPLOY_HOOK_STAGING | Settings do Web Service staging |
| Secret | RENDER_DEPLOY_HOOK_PRODUCTION | Settings do Web Service produção |
| Variable | STAGING_URL | URL HTTPS pública de staging, sem /health |
| Variable | PRODUCTION_URL | URL HTTPS pública distinta, sem /health |

As URLs ficam como Variables do repositório. Os hooks podem ser Secrets do
repositório ou do Environment correspondente. Um hook é uma credencial: copie
diretamente do Render para o campo Secret, nunca para README, logs ou mensagens.
O token GITHUB_TOKEN é fornecido pelo próprio Actions; não precisa ser criado.

## 4. Executar e comprovar, em ordem

1. Execute CI/CD em develop para publicar e verificar apenas staging.
2. Confira success=true em staging.json, o SHA em /health e /api/cidades/ranking.
3. Após staging aprovado, configure o serviço/banco de produção e seus valores no GitHub.
4. Execute CI/CD em main. Esse fluxo revalida staging com o digest dessa execução
   e promove exatamente esse digest para produção, somente se staging passar.
5. Baixe artifacts resultados-testes, integracao-docker, deploy-staging e deploy-production.
6. Registre run ID, URLs e SHA; capture as páginas reais sem credenciais.

O pipeline globalmente serializa os deploys entre main e develop para impedir
que staging seja trocado durante a promoção. A ausência de qualquer configuração
necessária gera falha explícita e nunca libera produção.

## 5. Docker local (opcional se validado no runner)

Instale Docker Desktop a partir de https://docs.docker.com/desktop/setup/install/windows-install/
e inicie o engine de containers Linux. Caso seja necessário habilitar WSL2,
virtualização, privilégios administrativos ou reiniciar o computador, conclua
essa etapa no sistema e confirme `docker info` e `docker compose version`.
O runner Ubuntu do Actions executa Compose, rede, volume, healthchecks e teste
de persistência real; essa execução pode ser usada como evidência da atividade.

Referências: [Deploy hooks](https://render.com/docs/deploy-hooks),
[Deploy de imagens](https://render.com/docs/deploying-an-image).
