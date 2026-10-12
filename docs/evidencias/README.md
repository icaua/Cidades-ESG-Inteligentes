# Registro de evidências

Autor: Isaac Cauã Mourão da Silva, RM 564071. Atualizado em 12/10/2026.

Os resultados atuais estão em `2026-10-12/`: build sem erros/avisos, 26 testes
xUnit, 9 testes Python e validação actionlint. Os demais logs são o histórico
de 04/10. Consulte `2026-10-12/validacao.json` e `../STATUS-ENTREGA.md`.

Os logs locais e o TRX desta pasta foram obtidos por execução real do build e dos
testes. Os testes Python usam mocks. Nenhum arquivo desta pasta comprova execução
do GitHub Actions, Docker, staging ou produção neste momento.

## Coleta no GitHub Actions

1. Execute o workflow em develop e em main depois de configurar GitHub/GHCR/Render.
2. Guarde os links das duas execuções e seus SHAs no README principal.
3. Capture a visão geral dos jobs e os detalhes de build, testes e deploy.
4. Baixe os artifacts resultados-testes, integracao-docker, deploy-staging e
   deploy-production; copie os logs, TRX e JSON relevantes para esta pasta.
5. Verifique success=true e SHA/ambiente nos JSONs dos deploys.

## Coleta dos ambientes

Capture com URL visível: Swagger, /health e /api/cidades/ranking em cada ambiente.
O campo versao deve ser igual ao SHA da execução e ambiente deve ser Staging ou
Production. Sugestões de nomes: pipeline-staging.png, pipeline-production.png,
staging-health.png, production-health.png, staging-ranking.png e production-ranking.png.
Não capture hooks, tokens ou DATABASE_URL. Evidência de tela deve representar
o sistema realmente executando, sem montagem ou simulação.

## Finalização

Insira os links e imagens reais no README e no gerador scripts/generate_documentation.py.
Regenere o PDF, revise todas as páginas e só então marque os itens comprovados no
checklist. Execute scripts/package_project.py e abra o ZIP para verificar .github,
src, Dockerfile, Compose e PDF. Envie o ZIP e o PDF na plataforma da atividade.
