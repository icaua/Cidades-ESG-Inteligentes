using CidadesESGInteligentes.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace CidadesESGInteligentes.Api.Data;

/// <summary>
/// Cria o schema no startup e popula alguns registros de exemplo.
///
/// Usamos EnsureCreated em vez de Migrations porque o schema deste projeto academico
/// e fixo (uma tabela) e assim o "docker compose up --build" funciona sem nenhum
/// passo manual de migration.
///
/// O retry existe porque, mesmo com healthcheck no compose, o container do PostgreSQL pode
/// levar alguns segundos a mais para aceitar conexoes do que para responder ao pg_isready.
/// </summary>
public static class DatabaseInitializer
{
    private const int MaxTentativas = 12;
    private static readonly TimeSpan EsperaEntreTentativas = TimeSpan.FromSeconds(5);

    public static async Task InicializarAsync(WebApplication app)
    {
        using var scope = app.Services.CreateScope();
        var contexto = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var logger = scope.ServiceProvider.GetRequiredService<ILoggerFactory>()
            .CreateLogger(nameof(DatabaseInitializer));

        for (var tentativa = 1; tentativa <= MaxTentativas; tentativa++)
        {
            try
            {
                await contexto.Database.EnsureCreatedAsync();
                await PopularDadosIniciaisAsync(contexto);
                logger.LogInformation("Banco de dados pronto (tentativa {Tentativa}).", tentativa);
                return;
            }
            catch (Exception ex) when (tentativa < MaxTentativas)
            {
                logger.LogWarning(
                    "Banco indisponivel na tentativa {Tentativa}/{Max}: {Mensagem}. Nova tentativa em {Segundos}s.",
                    tentativa, MaxTentativas, ex.Message, EsperaEntreTentativas.TotalSeconds);

                await Task.Delay(EsperaEntreTentativas);
            }
        }

        throw new InvalidOperationException(
            $"Nao foi possivel conectar ao banco de dados apos {MaxTentativas} tentativas.");
    }

    /// <summary>
    /// Insere cidades de exemplo apenas quando a tabela esta vazia,
    /// para que o Swagger e o endpoint de ranking ja tenham dados na demonstracao.
    /// </summary>
    private static async Task PopularDadosIniciaisAsync(AppDbContext contexto)
    {
        if (await contexto.Cidades.AnyAsync())
        {
            return;
        }

        contexto.Cidades.AddRange(
            new Cidade
            {
                Nome = "Curitiba",
                Estado = "PR",
                Populacao = 1830000,
                PercentualColetaSeletiva = 85,
                PercentualEnergiaRenovavel = 70,
                PercentualAreaVerde = 78,
                IndiceSaneamento = 95,
                IndicadorSocial = 80,
                QuantidadeProjetosSociais = 18
            },
            new Cidade
            {
                Nome = "Sao Paulo",
                Estado = "SP",
                Populacao = 11450000,
                PercentualColetaSeletiva = 45,
                PercentualEnergiaRenovavel = 38,
                PercentualAreaVerde = 30,
                IndiceSaneamento = 88,
                IndicadorSocial = 65,
                QuantidadeProjetosSociais = 12
            },
            new Cidade
            {
                Nome = "Recife",
                Estado = "PE",
                Populacao = 1650000,
                PercentualColetaSeletiva = 32,
                PercentualEnergiaRenovavel = 41,
                PercentualAreaVerde = 25,
                IndiceSaneamento = 52,
                IndicadorSocial = 48,
                QuantidadeProjetosSociais = 7
            },
            new Cidade
            {
                Nome = "Manaus",
                Estado = "AM",
                Populacao = 2250000,
                PercentualColetaSeletiva = 18,
                PercentualEnergiaRenovavel = 22,
                PercentualAreaVerde = 40,
                IndiceSaneamento = 30,
                IndicadorSocial = 35,
                QuantidadeProjetosSociais = 4
            });

        await contexto.SaveChangesAsync();
    }
}
