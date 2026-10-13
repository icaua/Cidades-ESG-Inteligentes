# Estado da entrega FIAP - 13/10/2026

**Isaac Cauã Mourão da Silva - RM 564071**

**Entrega parcial: produção pendente por decisão de manter custo zero.**
O Render permite apenas um PostgreSQL gratuito ativo no workspace. O segundo
banco gratuito foi recusado; a opção paga de US$ 6,30/mês não foi autorizada.
O formulário pago foi cancelado. Não foi criado serviço ou banco de produção.

| Requisito | Estado | Evidência |
| --- | --- | --- |
| Build .NET 8 | Aprovado local e CI | 0 erros e 0 avisos no build local; job de CI aprovado |
| Testes xUnit | Aprovados | 26/26, TRX local e artifact remoto |
| Testes Python | Aprovados | 9/9; testes unitários com mocks |
| Dockerfile e GHCR | Aprovados | Imagem construída, publicada e executada |
| Compose, rede, volume e healthchecks | Aprovados no runner Ubuntu | ci-compose.json: persistence_verified=true; containers saudáveis |
| Pipeline em develop | Aprovado | Run 38323935914, tentativa 2, success |
| Deploy staging | Aprovado | Deploy Hook, dep-db6vibs9v7es739vje50, live |
| Health e ranking staging | Aprovados | SHA esperado, ambiente Staging e 4 cidades |
| Deploy produção | Pendente | Não executado; sem URL ou secret de produção |
| README e PDF | Atualizados | Capturas reais e resultados; falta evidência de produção |
| ZIP | Revisão com pendência | Estrutura e integridade verificadas; não é entrega completa |

## Execução comprovada

- Pipeline: https://github.com/icaua/Cidades-ESG-Inteligentes/actions/runs/38323935914
- Revisão implantada: `fdd1db6f2313336c3355ba6cf7b06b7ba746d314`.
- Imagem: `ghcr.io/icaua/cidades-esg-inteligentes@sha256:d84b32f2e169f2af003755477054899634bbed0e4107f104c2ff8807aaf7c4b4`.
- Staging: https://cidades-esg-staging-l9tl.onrender.com
- Endpoints: `/health` e `/api/cidades/ranking`, verificados em 13/10/2026, 09:28 UTC.
- Deploy Render: https://dashboard.render.com/web/srv-db6vh2l9fdbs73eh7h3g/deploys/dep-db6vibs9v7es739vje50

A tentativa 1 falhou somente no deploy por falta do hook/URL. Após configurar
`RENDER_DEPLOY_HOOK_STAGING` como secret e `STAGING_URL` como variável, a tentativa 2
concluiu staging. Os jobs de build e imagem foram reaproveitados da execução aprovada.
O job de produção está `skipped`, conforme a regra da branch develop; isso não
comprova execução de produção. O deploy por hook também foi confirmado como live
no Render e os endpoints foram consultados novamente após essa conclusão.

O banco staging é PostgreSQL 16, gratuito, na região Ohio, com expiração informada
pelo Render em **11/11/2026**. O serviço gratuito pode hibernar por inatividade.
O nome Production no projeto padrão do painel foi criado no onboarding; não é
evidência de ambiente de produção da aplicação. A API usa Staging e banco staging.

## Para concluir futuramente

1. Disponibilizar outro PostgreSQL independente, dentro de um orçamento autorizado.
2. Criar Web Service de produção com o mesmo pacote GHCR e `ASPNETCORE_ENVIRONMENT=Production`.
3. Configurar `DATABASE_URL`, healthcheck `/health`, secret `RENDER_DEPLOY_HOOK_PRODUCTION`
   e variável `PRODUCTION_URL`; não reutilizar o banco staging.
4. Criar/publicar main e executar CI/CD: staging deve passar antes da promoção do mesmo digest.
5. Coletar JSON, logs, URLs e capturas de produção; atualizar checklist, PDF e ZIP.

## Desafios resolvidos

- SDK ausente: SDK .NET 8 temporário usado para build e testes locais.
- Integração GitHub sem escrita (403): publicação realizada com Git Credential Manager
  já autenticado pelo titular; não é necessário reconectar o plugin para este fluxo.
- Docker ausente no Windows: integração real executada no runner Ubuntu do Actions.
- Hook/URL ausentes: configurados sem incluir valores secretos no repositório ou ZIP.
- Promoção insegura: produção depende explicitamente de staging, com concorrência
  serializada e referência imutável por digest.
- Artifact repetido após rerun: cópias preservadas em diretórios com ID do artifact.

As mudanças finais em documentação e empacotamento não alteram o código de aplicação
ou o workflow da revisão comprovada. Consulte [evidências](evidencias/README.md).
