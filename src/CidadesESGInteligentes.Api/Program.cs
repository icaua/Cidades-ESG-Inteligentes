using System.Reflection;
using CidadesESGInteligentes.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);

// A string de conexao e montada a partir de variaveis de ambiente (arquivo .env no Docker).
// Os valores padrao servem para rodar a API localmente sem container.
var connectionString = ConstruirStringDeConexao(builder.Configuration);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Cidades ESG Inteligentes",
        Version = "v1",
        Description = "API para cadastro de cidades e calculo de pontuacao e classificacao ESG."
    });

    var arquivoXml = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var caminhoXml = Path.Combine(AppContext.BaseDirectory, arquivoXml);

    if (File.Exists(caminhoXml))
    {
        options.IncludeXmlComments(caminhoXml);
    }
});

var app = builder.Build();

// O Swagger fica ativo em todos os ambientes porque ele e a propria interface
// de demonstracao do projeto em staging e em producao.
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "Cidades ESG Inteligentes v1");
    options.RoutePrefix = string.Empty; // Swagger na raiz: http://localhost:8080/
});

// Readiness: verifica o banco e identifica a revisao que realmente esta em execucao.
app.MapGet("/health", async (AppDbContext db) =>
{
    if (!await db.Database.CanConnectAsync())
        return Results.Json(new { status = "unhealthy" }, statusCode: 503);

    return Results.Ok(new
    {
        status = "ok",
        ambiente = app.Environment.EnvironmentName,
        versao = app.Configuration["APP_VERSION"] ?? "local"
    });
})
.WithTags("Infraestrutura");

app.MapControllers();

await DatabaseInitializer.InicializarAsync(app);

app.Run();

static string ConstruirStringDeConexao(IConfiguration configuracao)
{
    // Provedores gerenciados (Render, Neon, Heroku) entregam o banco em uma unica
    // variavel DATABASE_URL. Quando ela existe, tem prioridade sobre as variaveis DB_*.
    var databaseUrl = configuracao["DATABASE_URL"];

    if (!string.IsNullOrWhiteSpace(databaseUrl))
    {
        return ConverterDatabaseUrl(databaseUrl);
    }

    var host = configuracao["DB_HOST"] ?? "localhost";
    var porta = configuracao["DB_PORT"] ?? "5432";
    var banco = configuracao["DB_NAME"] ?? "cidades_esg";
    var usuario = configuracao["DB_USER"] ?? "postgres";
    var senha = configuracao["DB_PASSWORD"] ?? "postgres";

    return new NpgsqlConnectionStringBuilder
    {
        Host = host, Port = int.Parse(porta), Database = banco,
        Username = usuario, Password = senha
    }.ConnectionString;
}

// Converte postgres://usuario:senha@host:porta/banco para o formato do Npgsql.
static string ConverterDatabaseUrl(string databaseUrl)
{
    var uri = new Uri(databaseUrl);
    var credenciais = uri.UserInfo.Split(':', 2);

    return new NpgsqlConnectionStringBuilder
    {
        Host = uri.Host,
        Port = uri.Port > 0 ? uri.Port : 5432,
        Database = uri.AbsolutePath.TrimStart('/'),
        Username = Uri.UnescapeDataString(credenciais[0]),
        Password = credenciais.Length > 1 ? Uri.UnescapeDataString(credenciais[1]) : string.Empty,
        SslMode = SslMode.Prefer
    }.ConnectionString;
}
