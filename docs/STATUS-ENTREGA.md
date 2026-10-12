# Estado da entrega FIAP - 12/10/2026

**Isaac Cauã Mourão da Silva - RM 564071**

**Ainda não apto para envio definitivo.** O build e os testes locais foram
aprovados, mas o critério de conclusão exige os dois deploys reais.

| Requisito | Estado | Evidência |
| --- | --- | --- |
| Build ASP.NET Core 8 | Aprovado | 2026-10-12/build.log: 0 erros, 0 avisos |
| Testes xUnit | Aprovado | 26/26; relatório TRX da execução atual |
| Testes Python | Aprovado | 9/9; testes unitários com mocks |
| Workflow revisado | Aprovado na análise estática | actionlint 1.7.12; sem shellcheck/pyflakes |
| Compose, rede e volume | Sintaxe validada; execução pendente | config.log; engine Docker ausente |
| Dockerfile funcional | Pendente de build Docker | Não confundir build .NET com build de imagem |
| Publicação GHCR | Não executada | Nenhum pipeline remoto iniciado |
| Deploy staging | Não executado | Sem URL/run ID comprovados |
| Deploy produção | Não executado | Bloqueado até staging aprovado |
| README/PDF | Atualizados com evidência local | Faltam evidências remotas |
| ZIP | Pacote de revisão | Não é o ZIP definitivo para envio |

Os logs e os hashes da revisão avaliada estão em
[evidencias/2026-10-12/validacao.json](evidencias/2026-10-12/validacao.json).
Os registros de 04/10 foram preservados como histórico e não comprovam a revisão atual.

## Correções de infraestrutura

- Produção passou a depender explicitamente de staging na mesma execução.
- Deploys de main/develop compartilham controle de concorrência, protegendo a promoção.
- O mesmo digest aprovado em staging é promovido para produção.
- A integração Compose ganhou prova de persistência após recriação de containers.
- O hook valida host, caminho, chave e digest; mensagens de erro não expõem o segredo.
- A evidência de deploy registra run ID, imagem, ID do deploy quando disponível,
  ambiente, SHA e horário da verificação. Falhas também geram JSON.
- As funcionalidades e a arquitetura ASP.NET Core/PostgreSQL foram preservadas.

## Bloqueios observados e ações necessárias

1. **GitHub:** consulta ao repositório funcionou, mas a primeira tentativa de criar
   README retornou HTTP 403, `Resource not accessible by integration`. Nenhum arquivo
   foi publicado. A lista de instalações também retornou vazia. Conecte/autorize
   a conta pelo plugin GitHub do aplicativo, selecionando este repositório.
   Repositório: https://github.com/icaua/Cidades-ESG-Inteligentes.
2. **Render:** o navegador disponível abriu na tela de login. Entre na conta pelo
   painel aberto nesta conversa. Não envie credenciais ou hooks em mensagens.
3. **Docker local:** CLI/Engine não encontrados. Inicie Docker Desktop com containers
   Linux. Como alternativa, o runner Ubuntu fará essa validação quando GitHub for liberado.

Configuração campo a campo: [CONFIGURACAO-RENDER.md](CONFIGURACAO-RENDER.md).
Após liberar o acesso: publicar fontes, executar CI/Compose, configurar e validar
staging, preparar produção, executar a promoção, coletar artifacts/prints e regerar
PDF/ZIP. Nenhuma URL, captura, run ID ou aprovação remota foi inventada.
