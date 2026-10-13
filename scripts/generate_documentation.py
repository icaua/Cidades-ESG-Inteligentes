"""Gera a documentacao a partir dos resultados locais e remotos reais. Requer reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/Documentacao-tecnica.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor("#123347")
TEAL = colors.HexColor("#087F8C")
LIGHT = colors.HexColor("#EAF4F4")
INK = colors.HexColor("#20333E")
AMBER = colors.HexColor("#FFF1D9")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyESG", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="SmallESG", parent=styles["BodyESG"], fontSize=8, leading=11, spaceAfter=5))
styles.add(ParagraphStyle(name="TitleESG", fontName="Helvetica-Bold", fontSize=31, leading=35, textColor=NAVY, spaceAfter=18))
styles.add(ParagraphStyle(name="HeadingESG", fontName="Helvetica-Bold", fontSize=19, leading=24, textColor=NAVY, spaceAfter=14))
styles.add(ParagraphStyle(name="SubESG", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=TEAL, spaceBefore=9, spaceAfter=7))
styles.add(ParagraphStyle(name="CodeESG", fontName="Courier", fontSize=8, leading=11, textColor=INK, backColor=LIGHT, borderPadding=9, spaceAfter=12))
story = []


def p(text, style="BodyESG"):
    return Paragraph(text, styles[style])


def add(text, style="BodyESG"):
    story.append(p(text, style))


def heading(number, title):
    add(f"{number} / DOCUMENTAÇÃO TÉCNICA", "SmallESG")
    add(title, "HeadingESG")


def table(rows, widths, header=True):
    cells = [[p(str(cell), "SmallESG") for cell in row] for row in rows]
    t = Table(cells, colWidths=widths, hAlign="LEFT")
    rules = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 9),
             ("RIGHTPADDING", (0, 0), (-1, -1), 9),
             ("TOPPADDING", (0, 0), (-1, -1), 8),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
             ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#CADDDD"))]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(rules))
    story.append(t)
    story.append(Spacer(1, 12))


def note(text):
    t = Table([[p(text)]], colWidths=[511])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AMBER),
                          ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5C17B")),
                          ("LEFTPADDING", (0, 0), (-1, -1), 12),
                          ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                          ("TOPPADDING", (0, 0), (-1, -1), 11),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t)
    story.append(Spacer(1, 12))


def code(text):
    story.append(Preformatted(text, styles["CodeESG"], maxLineLength=90))


def page():
    story.append(PageBreak())


add("NAVEGANDO PELO MUNDO DEVOPS", "SubESG")
story.append(Spacer(1, 22))
add("Cidades ESG<br/>Inteligentes", "TitleESG")
add("Infraestrutura executada e evidências de CI/CD", "SubESG")
add("<b>Isaac Cauã Mourão da Silva</b><br/>RM 564071<br/>13 de outubro de 2026")
story.append(Spacer(1, 15))
add("API acadêmica ASP.NET Core 8 com PostgreSQL 16. Permite cadastrar cidades, calcular pontuações ESG e consultar um ranking. Os registros iniciais são fictícios; Swagger oferece a interface de demonstração. A arquitetura e as funcionalidades existentes foram preservadas.")
table([["Validação", "Resultado comprovado"],
 ["Build e testes", "Build Release aprovado; 26 testes xUnit e 9 testes Python aprovados localmente e no CI."],
 ["Containerização", "Dockerfile construído, imagem publicada no GHCR e executada com PostgreSQL no Compose."],
 ["Orquestração", "Rede, volume, healthchecks e persistência após recriação dos containers comprovados no runner Ubuntu."],
 ["Deploy staging", "GitHub Actions aprovado; deploy por hook live no Render; health e ranking validados."],
 ["Deploy produção", "Pendente por decisão do titular de manter custo zero."]], [150,361])
note("<b>Entrega parcial, com pendência explícita.</b> O Render recusou o segundo banco PostgreSQL gratuito. A opção paga de US$ 6,30/mês não foi autorizada; o formulário foi cancelado. Não há deploy ou evidência de produção. O pacote não satisfaz integralmente o requisito de dois ambientes.")
add('Repositório: <link href="https://github.com/icaua/Cidades-ESG-Inteligentes" color="#087F8C">github.com/icaua/Cidades-ESG-Inteligentes</link>', "SmallESG")

page()
heading("01", "Pipeline CI/CD e rastreabilidade")
add("Ferramentas: GitHub Actions, Docker Buildx, GitHub Container Registry e Render. O arquivo .github/workflows/ci-cd.yml contém os jobs abaixo. Erros no build, testes ou integração impedem o deploy.")
table([["Etapa", "Lógica e critério"],
 ["Build e testes", "Restore NuGet, compilação Release, xUnit e unittest Python. Relatórios TRX e logs são publicados como artifacts."],
 ["Imagem e integração", "Build multi-stage com APP_VERSION=SHA. Publicação no GHCR. Compose sobe API e PostgreSQL, verifica health, ranking, rede e persistência do volume."],
 ["Deploy staging", "O hook Render recebe imgURL com digest imutável. Smoke test exige ambiente Staging, SHA esperado e ranking JSON."],
 ["Deploy produção", "Somente na branch main, após staging aprovado na mesma execução. Promove o mesmo digest e verifica Production. Ainda não executado."]], [122,389])
table([["Gatilho", "Comportamento"],
 ["Pull request para develop/main", "Build, testes e integração; sem publicação nem deploy."],
 ["Push ou execução manual em develop", "Build, testes, GHCR, integração e staging."],
 ["Push ou execução manual em main", "Mesmo fluxo, com produção após staging."]], [225,286])
add("A concorrência é serializada entre main e develop. O verificador compara o SHA completo de /health, rejeita ambiente incorreto e consulta o banco pelo ranking. Há até 40 tentativas, intervalo de 10 segundos e timeout de 8 segundos por requisição. Rollback é manual.")
add("Execução real", "SubESG")
add('<link href="https://github.com/icaua/Cidades-ESG-Inteligentes/actions/runs/38323935914" color="#087F8C">Run 38323935914 - tentativa 2 - success - develop</link>')
code("Commit: fdd1db6f2313336c3355ba6cf7b06b7ba746d314\nImagem: ghcr.io/icaua/cidades-esg-inteligentes\nDigest: sha256: d84b32f2e169f2af00375547705489963\n                4bbed0e4107f104c2ff8807aaf7c4b4")
add("O digest acima foi dividido somente para diagramação; use a referência contínua do README. A tentativa 1 falhou no deploy por ausência do hook/URL. Após configurar staging, a tentativa 2 reaproveitou os jobs aprovados e concluiu o deploy. Produção aparece skipped, como esperado para develop.", "SmallESG")

page()
heading("02", "Docker e persistência comprovada")
table([["Entrada", "Aplicação", "Banco"],
 ["HTTP / Swagger\nHost: 8080", "ASP.NET Core 8\nContainer: 8080\nUsuário app", "PostgreSQL 16\nDNS db:5432\nVolume postgres-data"]], [145,180,186])
add("O Dockerfile usa SDK .NET 8 para restore/publish e ASP.NET Runtime 8 para execução. A imagem final contém somente a publicação e curl para healthcheck; roda sem root. APP_VERSION é incorporada no build. O Dockerfile completo está no README e no ZIP.")
add("No Compose, API e banco compartilham rede bridge. A porta do banco não é publicada no host; a dependência exige PostgreSQL saudável. A configuração usa variáveis de ambiente e volume nomeado. DATABASE_URL tem prioridade sobre as variáveis DB_*.")
add("Execução local - PowerShell", "SubESG")
code("Copy-Item .env.example .env\n# Defina DB_PASSWORD no arquivo .env.\ndocker compose config --quiet\ndocker compose up -d --build --wait --wait-timeout 180\ndocker compose ps\ncurl.exe --fail http://localhost:8080/health\ncurl.exe --fail http://localhost:8080/api/cidades/ranking\ndocker compose down")
add("down preserva os dados; down -v remove o volume. Staging e produção locais podem usar projetos Compose distintos (-p cidades-staging e -p cidades-production) e os exemplos .env correspondentes, com portas 8081 e 8082. Esses exemplos não representam deploy remoto de produção.")
add("Prova real no GitHub Actions", "SubESG")
add("A imagem publicada foi carregada no runner e executada com PostgreSQL. scripts/verify_compose.py gravou um marcador no banco descartável ci, executou down sem -v, recriou os containers, confirmou novos IDs de containers e o mesmo volume, consultou o marcador e o removeu. Um novo smoke test aprovou API, banco e revisão após a recriação.")
table([["Verificação", "Resultado"],
 ["Rede compartilhada", "ci_cidades-esg-net"],
 ["Volume persistente", "ci_postgres-data"],
 ["Containers antes/depois", "API e db healthy; IDs distintos após recriação"],
 ["Persistência", "persistence_verified: true"]], [210,301])
add("Fonte: docs/evidencias/2026-10-12/github-38323935914/integracao-docker/ci-compose.json. Docker não estava instalado no Windows; a validação foi realizada no runner Ubuntu.", "SmallESG")

page()
heading("03", "Evidências do pipeline e testes")
add("Captura real do GitHub Actions em 13/10/2026. Build, integração e staging aparecem aprovados; produção está skipped. Não há montagem de resultados.")
im=Image(str(ROOT/'docs/evidencias/2026-10-13/github-actions.jpg')); im._restrictSize(511,295); story.append(im)
story.append(Spacer(1,10))
add("Resultados dos testes", "SubESG")
table([["Execução", "Resultado e alcance"],
 ["Build local Release", "SDK 8.0.425; zero erros, zero avisos."],
 ["xUnit local e CI", "26 aprovados. Cálculo, pesos, arredondamento, classificação e validação de cadastro. Não são testes de integração dos controllers."],
 ["Python local e CI", "9 aprovados. Usa mocks para testar verificação de ambiente/SHA, falhas e segurança do hook."],
 ["Integração real", "Compose com API/PostgreSQL, health, ranking e persistência. Complementa os testes unitários."],
 ["Análise estática", "Actionlint 1.7.12 e YAML aprovados. Shellcheck/pyflakes não executados."]], [145,366])
add("Os logs, resultados TRX, run.json e jobs.json estão no ZIP. O diretório github-38323935914 contém a primeira execução e o rerun. Artifacts de staging com IDs diferentes preservam a falha inicial e o sucesso posterior. Os testes Python isoladamente não comprovam deploy.", "SmallESG")

page()
heading("04", "Staging no Render")
add('<link href="https://cidades-esg-staging-l9tl.onrender.com" color="#087F8C">https://cidades-esg-staging-l9tl.onrender.com</link>')
im=Image(str(ROOT/'docs/evidencias/2026-10-13/render-staging.jpg')); im._restrictSize(511,295); story.append(im)
story.append(Spacer(1,10))
add("A captura real mostra o serviço no plano Free, a imagem por digest e o deploy acionado por Deploy Hook. O Render confirmou o status live do deploy automatizado.")
code("Servico: srv-db6vh2l9fdbs73eh7h3g\nDeploy: dep-db6vibs9v7es739vje50\nTrigger: deploy_hook\nStatus: live\nConcluido: 2026-10-13 09:26:31 UTC")
add("Configuração validada", "SubESG")
table([["Campo", "Valor / uso"],
 ["Região / runtime", "Ohio / imagem existente do GHCR"],
 ["ASPNETCORE_ENVIRONMENT", "Staging"],
 ["PORT / ASPNETCORE_HTTP_PORTS", "8080 / 8080 (este último definido na imagem)"],
 ["DATABASE_URL", "Conexão interna do banco staging; valor secreto omitido"],
 ["Healthcheck", "/health"],
 ["GitHub", "RENDER_DEPLOY_HOOK_STAGING e STAGING_URL configurados"]], [200,311])
add("O PostgreSQL staging gratuito expira em 11/11/2026. O serviço pode hibernar por inatividade. O projeto padrão do Dashboard usa o rótulo Production; isso não representa deploy de produção da API, cujo ambiente é Staging.", "SmallESG")

page()
heading("05", "Endpoints e pendência de produção")
add("Após o Render confirmar o deploy por hook como live, o script consultou novamente /health e /api/cidades/ranking em 13/10/2026, às 09:28 UTC. A evidência completa está em docs/evidencias/2026-10-13/staging-confirmado.json.")
import json
verified=json.loads((ROOT/'docs/evidencias/2026-10-13/staging-confirmado.json').read_text(encoding='utf-8'))
code(json.dumps(verified['health'],indent=2,ensure_ascii=False))
table([["Posição", "Cidade", "UF", "Pontuação ESG", "Classificação"]]+[[r['posicao'],r['nome'],r['estado'],r['pontuacaoEsg'],r['classificacaoEsg']] for r in verified['ranking']], [55,155,40,115,146])
add("Os dados acima são a resposta real do endpoint, não uma captura de tela. O navegador integrado bloqueou a abertura direta da URL; a consulta HTTP pelo script funcionou. As imagens das páginas anteriores são capturas reais do Actions e do Dashboard Render.", "SmallESG")
add("Produção: configuração preparada, deploy pendente", "SubESG")
note("O Render retornou: <b>cannot have more than one active free tier database</b>. O segundo banco gratuito não foi criado. A alternativa preparada era PostgreSQL 16, 1 GB, sem autoscaling, por US$ 6,30/mês. O titular escolheu manter custo zero e deixar produção pendente; a contratação foi cancelada.")
add("Para concluir, disponibilizar PostgreSQL separado para produção e criar outro Web Service de imagem, com ASPNETCORE_ENVIRONMENT=Production, DATABASE_URL própria e /health. Configurar RENDER_DEPLOY_HOOK_PRODUCTION e PRODUCTION_URL no GitHub. Publicar main e executar o workflow, que valida staging antes de promover o mesmo digest.")
add("Não há URL, banco, serviço, secret ou evidência de produção neste pacote. O critério acadêmico de dois ambientes ainda não foi atendido. Regerar PDF e ZIP após essa validação futura.")
add("Tecnologias utilizadas", "SubESG")
add("C#; .NET 8; ASP.NET Core; Entity Framework Core 8; Npgsql; PostgreSQL 16; Swagger/Swashbuckle; xUnit; Docker/Compose; GitHub Actions; GHCR; Render; Python 3; ReportLab.")

page()
heading("06", "Desafios e checklist FIAP")
table([["Desafio", "Resolução / estado"],
 ["SDK e Docker ausentes no Windows", "SDK temporário para testes locais; Docker executado no runner Ubuntu."],
 ["Conector GitHub retornou 403", "Publicação com Git Credential Manager já autenticado pelo titular."],
 ["Hook/URL ausentes na primeira execução", "Secret e variável de staging configurados; rerun aprovado."],
 ["Risco de promover imagem diferente", "Deploy por digest; produção depende de staging; concorrência serializada."],
 ["Volume precisava de prova real", "Marcador persistiu após recriar os containers no CI."],
 ["Limite de banco gratuito", "Produção mantida pendente por decisão de custo zero."]], [218,293])
add("Limites da simulação", "SubESG")
add("CRUD e Swagger públicos, dados fictícios, schema fixo via EnsureCreated, sem migrações incrementais e sem rollback/backup automatizado. O parser de DATABASE_URL usa SSL Prefer. Este é um cenário acadêmico, sem operação de dados sensíveis.")
add("Checklist obrigatório - 13/10/2026", "SubESG")
table([["Item", "OK", "Situação"],
 ["Projeto compactado em ZIP", "Sim", "Pacote de revisão organizado com fontes, configurações, evidências e PDF."],
 ["Dockerfile funcional", "Sim", "Build e execução comprovados."],
 ["Compose ou Kubernetes", "Sim", "Compose, rede, volume e healthchecks comprovados."],
 ["Pipeline build, teste e deploy", "Não", "Comprovado até staging; falta produção."],
 ["README com instruções e prints", "Sim", "Instruções e capturas reais incluídas."],
 ["Documentação com evidências", "Não", "PDF atualizado, mas falta evidência de produção."],
 ["Deploy staging e produção", "Não", "Apenas staging executado e validado."]], [215,36,260])
add("O ZIP é identificado como revisao-pendente. O comando package_project.py --final bloqueia uma entrega definitiva enquanto ready_for_submission for false. As alterações posteriores à revisão implantada restringem-se à documentação, evidências e empacotamento.", "SmallESG")
add('Referências: <link href="https://render.com/docs/deploy-hooks" color="#087F8C">Render Deploy Hooks</link>; <link href="https://docs.github.com/en/actions" color="#087F8C">GitHub Actions</link>; <link href="https://docs.docker.com/compose/" color="#087F8C">Docker Compose</link>.', "SmallESG")

def footer(canvas, doc):
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(2)
    canvas.line(42, 807, 553, 807)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(42, 23, "Cidades ESG Inteligentes | Isaac Cauã Mourão da Silva | RM 564071")
    canvas.drawRightString(553, 23, f"{doc.page}")


doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=42, leftMargin=42,
                        topMargin=52, bottomMargin=42, title="Cidades ESG Inteligentes - Documentação DevOps",
                        author="Isaac Cauã Mourão da Silva - RM 564071")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)

