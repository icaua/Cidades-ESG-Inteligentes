"""Gera a documentacao a partir dos resultados locais reais. Requer reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted

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
story.append(Spacer(1, 24))
add("Cidades ESG<br/>Inteligentes", "TitleESG")
add("Automação de build, testes e deploy de uma API em C#", "SubESG")
story.append(Spacer(1, 18))
add("<b>Isaac Cauã Mourão da Silva</b><br/>RM 564071<br/>12 de outubro de 2026")
story.append(Spacer(1, 20))
add("O projeto cadastra cidades e calcula uma pontuação ESG a partir de indicadores ambientais e sociais. A API oferece CRUD, classificação e ranking; Swagger funciona como interface de demonstração. Os dados iniciais são fictícios.")
add("Esta documentação descreve a implementação DevOps, os comandos para reprodução e o estado das evidências da atividade. O código existente foi preservado e as configurações de entrega foram ajustadas para verificar a revisão implantada e isolar ambientes.")
table([["Validação realizada", "Resultado"],
       ["Build Release .NET 8", "Aprovado: zero erros e zero avisos"],
       ["Testes automatizados locais", "26 casos xUnit + 9 casos Python aprovados"],
       ["Arquivos YAML", "Sintaxe validada; não equivale a executar Docker"],
       ["Docker, GitHub Actions e deploys", "Execução ainda pendente"]], [245, 266])
note("<b>Documento parcial para finalização da entrega.</b> Repositório informado: icaua/Cidades-ESG-Inteligentes. A escrita retornou HTTP 403; Docker está ausente e Render aguarda login. As evidências locais são reais; não há comprovação de pipeline remoto ou deploy neste PDF.")

page()
heading("01", "Pipeline CI/CD")
add("A automação usa GitHub Actions, Docker Buildx, GHCR e Render. O workflow fica em <b>.github/workflows/ci-cd.yml</b>. Um erro em build, testes ou integração impede o deploy.")
table([["Etapa", "Execução e critério de sucesso"],
       ["1. Build e testes", "Restore NuGet, build Release, xUnit e testes do verificador. Publica relatórios TRX como artifacts."],
       ["2. Imagem e integração", "Build multi-stage, APP_VERSION com SHA completo, imagem no GHCR e execução da API com PostgreSQL no Compose. Consulta /health e /api/cidades/ranking."],
       ["3. Deploy por ambiente", "Hook Render recebe a imagem por digest sha256. O serviço deve ser baseado em imagem existente do registry."],
       ["4. Validação e evidência", "A resposta deve informar ambiente e SHA esperados; o ranking deve responder. O resultado é salvo em JSON e anexado à execução."]], [127, 384])
add("Gatilhos e branches", "SubESG")
table([["Gatilho", "Destino"],
       ["Pull request para develop/main", "Build, testes e integração; sem publicação ou deploy"],
       ["Push em develop", "Publicação de imagem e deploy em staging"],
       ["Push em main", "Staging validado e depois produção, com o mesmo digest"],
       ["Execução manual", "Develop: staging; main: staging e depois produção"]], [230, 281])
add("Os deploys são serializados entre as branches. Em main, produção depende explicitamente de staging aprovado na mesma execução. O digest é preservado na promoção. Falha em staging bloqueia produção. Em develop, o fluxo termina após staging.")
add("A imagem recebe a tag SHA completo. O deploy usa o digest retornado pelo build, evitando ambiguidade de tags. A publicação ocorre antes do teste de integração; se esse teste falhar, a imagem pode existir no registry, mas não será implantada.")
add("O verificador faz até 40 tentativas, com pausa de 10 segundos e timeout de 8 segundos por chamada. Resposta da versão anterior não conclui o deploy. Não há rollback automático.")

page()
heading("02", "Docker e arquitetura")
table([["Acesso HTTP", "Aplicação", "Persistência"],
       ["Navegador / Swagger<br/>Porta do host: 8080", "API ASP.NET Core 8<br/>Porta interna: 8080<br/>Usuário: app", "PostgreSQL 16<br/>DNS: db:5432<br/>Volume: postgres-data"]], [145, 180, 186])
add("A API e o banco compartilham uma rede bridge do Compose. O banco não expõe porta no host. O volume persiste quando os containers são removidos com down, e o healthcheck do PostgreSQL condiciona a inicialização da API.")
add("Estratégia de imagem", "SubESG")
add("Os comandos multilinha abaixo usam Bash. No PowerShell, use as linhas únicas do README.", "SmallESG")
add("O Dockerfile usa <b>mcr.microsoft.com/dotnet/sdk:8.0</b> para restore/publish e <b>mcr.microsoft.com/dotnet/aspnet:8.0</b> para execução. Apenas o conteúdo publicado entra na imagem final. O usuário app não tem privilégios de root; curl executa o healthcheck. O Dockerfile completo está no README e no ZIP.")
code("docker build --build-arg APP_VERSION=local \\\n  -t cidades-esg-api:local .\ndocker compose config --quiet\ndocker compose up -d --build --wait --wait-timeout 180\ndocker compose ps\ndocker compose logs --tail 100 api\ndocker compose down")
add("Antes de subir, copie .env.example para .env e defina DB_PASSWORD. DATABASE_URL tem prioridade sobre DB_*. A API cria o schema fixo com EnsureCreated e insere dados de demonstração no primeiro início.")
add("Dois ambientes locais isolados", "SubESG")
code("docker compose --env-file .env.staging -p cidades-staging \\\n  up -d --build --wait --wait-timeout 180\ndocker compose --env-file .env.production -p cidades-production \\\n  up -d --build --wait --wait-timeout 180")
add("Copie antes os respectivos arquivos .example. Staging responde em localhost:8081; produção, em localhost:8082. Cada projeto recebe sua rede e volume. Estes comandos ainda precisam ser executados com Docker disponível.")
note("<b>Persistência:</b> down preserva os dados; down -v apaga o volume. Uma senha alterada no .env não reconfigura automaticamente um banco já inicializado.")

page()
heading("03", "Evidências locais verificadas")
add("Os trechos abaixo vêm dos logs reais gravados em 12/10/2026. São registros de terminal local, não capturas de GitHub Actions ou de ambientes hospedados. O SDK temporário usado para validação foi o .NET 8.0.425.")
add("Build Release", "SubESG")
build = (ROOT / "docs/evidencias/2026-10-12/build.log").read_text(encoding="utf-8-sig")
code("\n".join(build.strip().splitlines()[-6:]))
add("Execução dos testes xUnit", "SubESG")
tests = (ROOT / "docs/evidencias/2026-10-12/xunit.log").read_text(encoding="utf-8-sig")
code("\n".join(tests.strip().splitlines()[-4:]))
add("Os 26 casos cobrem cálculo da pontuação, pesos, arredondamento, classificação, faixas de fronteira e validação dos dados de cadastro. O relatório completo resultado-testes.trx está em docs/evidencias/2026-10-12/testes/.")
add("Verificador de deploy", "SubESG")
code("9 testes Python aprovados\nRejeita SHA antigo e ambiente incorreto\nRejeita health com banco indisponivel\nEspera nova revisao antes de consultar o ranking\nGrava evidencia de falha quando o ranking e invalido")
add("Esses nove testes usam mocks. Eles verificam a lógica do script e não demonstram acesso a staging ou produção. O log integral está em 2026-10-12/python.log; os quatro novos testes validam hook, digest, ID de deploy e ocultação do segredo em erros.")
add("Arquivos de evidência no ZIP", "SubESG")
table([["Arquivo em docs/evidencias/", "Conteúdo"],
       ["2026-10-12/build.log", "Compilação real da revisão atual"],
       ["2026-10-12/xunit.log e testes/*.trx", "Resultados xUnit da revisão atual"],
       ["2026-10-12/python.log", "Nove testes de automação aprovados"],
       ["2026-10-12/actionlint.log e config.log", "Actionlint 1.7.12 e validação YAML"]], [295, 216])

page()
heading("04", "Deploy e evidências a completar")
add("Configuração dos serviços", "SubESG")
add("O repositório icaua/Cidades-ESG-Inteligentes foi informado, mas a integração recusou gravação (403). Conecte o GitHub pelo plugin e autorize esse repositório; então execute o workflow para criar a primeira imagem GHCR. O deploy inicial falhará enquanto os serviços não estiverem configurados. Crie dois Web Services Render com Existing Image e dois bancos PostgreSQL separados. Para GHCR privado, configure credenciais de leitura no Render.")
table([["Item", "Staging / Produção"],
       ["ASPNETCORE_ENVIRONMENT", "Staging / Production"],
       ["PORT e ASPNETCORE_HTTP_PORTS", "8080 em ambos os serviços"],
       ["DATABASE_URL", "Conexão do banco exclusivo de cada ambiente"],
       ["Health check path", "/health"],
       ["GitHub Secrets", "RENDER_DEPLOY_HOOK_STAGING<br/>RENDER_DEPLOY_HOOK_PRODUCTION"],
       ["GitHub Variables", "STAGING_URL / PRODUCTION_URL (HTTPS)"]], [190, 321])
add("Não sobrescreva APP_VERSION no provedor. O hook recebe imgURL com digest imutável do mesmo pacote configurado no serviço. Defina os valores de staging e valide develop. Só depois configure produção e execute main, que revalida staging antes de promover o mesmo digest.")
add("Registro obrigatório antes de enviar a atividade", "SubESG")
table([["Evidência solicitada", "Estado atual / captura necessária"],
       ["Pipeline: build, testes e deploy", "Pendente. Capturar jobs, SHA e URL das execuções develop/main."],
       ["Staging funcionando", "Pendente. Capturar Swagger, health e ranking com URL visível."],
       ["Produção funcionando", "Pendente. Capturar Swagger, health e ranking com URL visível."],
       ["Resultados dos deploys", "Pendente. Baixar artifacts deploy-staging e deploy-production."]], [190, 321])
note("<b>Não há prints de deploy neste documento.</b> Insira as capturas reais e os links correspondentes, atualize o checklist e gere novamente o PDF e o ZIP antes da entrega definitiva.")
add('Referências: <link href="https://render.com/docs/deploy-hooks" color="#087F8C">Render - Deploy Hooks</link>; <link href="https://docs.github.com/en/actions" color="#087F8C">GitHub Actions</link>; <link href="https://docs.docker.com/compose/" color="#087F8C">Docker Compose</link>.', "SmallESG")

page()
heading("05", "Desafios e checklist de entrega")
table([["Desafio", "Solução"],
       ["Conflito entre ambientes Compose", "Remoção de nomes globais; isolamento com -p."],
       ["Resposta de versão antiga no deploy", "SHA incorporado à imagem e comparado no health."],
       ["Health sem validação do banco", "Verificação de conectividade; HTTP 503 em falha."],
       ["Imagem implantada sem rastreabilidade", "Hook recebe o digest do build aprovado."],
       ["Ausência de SDK local", "SDK temporário, build e testes registrados."],
       ["Sem Docker, escrita GitHub e login Render", "Configuração preparada; aguardando acesso externo."]], [220, 291])
add("Limites da simulação de produção", "SubESG")
add("CRUD e Swagger estão públicos, sem autenticação. O schema é fixo, sem migrações incrementais; rollback e backup não são automatizados. DATABASE_URL usa SSL Prefer e não interpreta query parameters. Antes de operar dados reais, implemente autenticação, migrações e política TLS/backup adequada ao provedor.")
add("Checklist obrigatório", "SubESG")
add("OK indica item comprovado no escopo descrito. Parcial ou pendente permanece sem marcação. Situação em 12/10/2026.", "SmallESG")
table([["Item", "OK", "Situação"],
       ["Projeto compactado em ZIP", "Sim", "Pacote de revisão; envio definitivo bloqueado"],
       ["Dockerfile funcional", "Não", "Build Docker ainda não executado"],
       ["Compose ou Kubernetes", "Não", "Sintaxe validada; execução real pendente"],
       ["Pipeline build, teste e deploy", "Não", "Análise estática aprovada; execução pendente"],
       ["README com instruções e prints", "Não", "Instruções e logs; faltam prints remotos"],
       ["Documentação técnica com evidências", "Não", "PDF com logs locais; faltam provas de deploy"],
       ["Deploy staging e produção", "Não", "Ainda não comprovado"]], [225, 38, 248])
add("Não envie a revisão parcial como entrega definitiva. Consulte docs/STATUS-ENTREGA.md e docs/CONFIGURACAO-RENDER.md; conclua os deploys e regenere os artefatos com as evidências reais.", "SmallESG")


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

