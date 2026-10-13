# Registro de evidências

Isaac Cauã Mourão da Silva - RM 564071. Atualizado em 13/10/2026.

- `2026-10-13/validacao.json`: estado consolidado atual; entrega completa false.
- `2026-10-13/github-actions.jpg`: captura real do run aprovado em develop.
- `2026-10-13/render-staging.jpg`: captura real de staging live e Deploy Hook.
- `2026-10-13/render-deploys.json`: resposta do Render com IDs, digest, trigger e status.
- `2026-10-13/staging-confirmado.json`: /health e ranking após conclusão do deploy automático.
- `2026-10-12/github-38323935914/`: run, jobs, logs e artifacts remotos.
- `deploy-staging-11801636843/staging.json`: artifact de staging aprovado na tentativa 2.
- `deploy-staging-11780455497/staging.json` e `deploy-staging/staging.json`: falha histórica da tentativa 1, sem hook/URL.
- `integracao-docker/ci-compose.json`: prova real de rede, volume, containers saudáveis e persistência.
- `2026-10-12/`: build e testes locais; validacao.json desse dia é histórico anterior à conclusão remota.
- Demais logs na raiz: histórico de 04/10, não substituem as evidências atuais.

Artifacts repetidos são mantidos em diretórios com ID para evitar sobrescrever
sucesso com falha antiga. O rerun reaproveitou jobs aprovados de build e imagem.
O CI de develop não implanta produção: job skipped não significa deploy aprovado.
Produção ficou pendente pela decisão expressa de custo zero após o limite gratuito do Render.

O navegador integrado bloqueou a URL pública do endpoint; não existe captura
fabricada de /health. As respostas HTTP reais estão no JSON e os prints mostram
Actions e Dashboard Render. Hooks e conexões secretas não fazem parte dos artefatos.

Para concluir: prover banco independente para produção, configurar o serviço e
os secrets/variables correspondentes, executar main, comprovar ambos os ambientes
e regerar a documentação e o pacote. Ver `../STATUS-ENTREGA.md`.
