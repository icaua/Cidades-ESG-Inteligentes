using CidadesESGInteligentes.Api.Models;
using CidadesESGInteligentes.Api.Services;
using Xunit;

namespace CidadesESGInteligentes.Tests;

/// <summary>
/// Testes da regra de negocio central do projeto: pontuacao e classificacao ESG.
/// </summary>
public class EsgCalculatorTests
{
    /// <summary>
    /// Casas decimais consideradas na comparacao de pontuacoes.
    /// Comparar double com igualdade exata deixaria os testes sujeitos
    /// a diferencas de arredondamento binario.
    /// </summary>
    private const int Precisao = 2;

    // ---------------------------------------------------------------
    // Classificacao: 0-39 Critico | 40-59 Regular | 60-79 Bom | 80-100 Excelente
    // ---------------------------------------------------------------

    [Theory]
    [InlineData(85, "Excelente")]
    [InlineData(65, "Bom")]
    [InlineData(50, "Regular")]
    [InlineData(30, "Critico")]
    public void Classificar_DeveRetornarAFaixaCorrespondenteAPontuacao(double pontuacao, string esperado)
    {
        Assert.Equal(esperado, EsgCalculator.Classificar(pontuacao));
    }

    [Theory]
    [InlineData(0, "Critico")]
    [InlineData(39.99, "Critico")]
    [InlineData(40, "Regular")]
    [InlineData(59.99, "Regular")]
    [InlineData(60, "Bom")]
    [InlineData(79.99, "Bom")]
    [InlineData(80, "Excelente")]
    [InlineData(100, "Excelente")]
    public void Classificar_DeveTratarCorretamenteOsLimitesDeCadaFaixa(double pontuacao, string esperado)
    {
        Assert.Equal(esperado, EsgCalculator.Classificar(pontuacao));
    }

    // ---------------------------------------------------------------
    // Calculo da pontuacao
    // ---------------------------------------------------------------

    [Fact]
    public void CalcularPontuacao_ComTodosOsIndicadoresNoMaximo_DeveRetornar100()
    {
        var cidade = CriarCidade(
            coletaSeletiva: 100,
            energiaRenovavel: 100,
            areaVerde: 100,
            saneamento: 100,
            indicadorSocial: 100,
            projetosSociais: EsgCalculator.MetaProjetosSociais);

        Assert.Equal(100d, EsgCalculator.CalcularPontuacao(cidade), Precisao);
        Assert.Equal("Excelente", EsgCalculator.Classificar(EsgCalculator.CalcularPontuacao(cidade)));
    }

    [Fact]
    public void CalcularPontuacao_ComTodosOsIndicadoresZerados_DeveRetornar0()
    {
        var cidade = CriarCidade(0, 0, 0, 0, 0, 0);

        Assert.Equal(0d, EsgCalculator.CalcularPontuacao(cidade), Precisao);
        Assert.Equal("Critico", EsgCalculator.Classificar(EsgCalculator.CalcularPontuacao(cidade)));
    }

    [Fact]
    public void CalcularPontuacao_ComTodosOsIndicadoresIguais_DeveRetornarOMesmoValor()
    {
        // Como a soma dos pesos e 100, uma cidade com todos os indicadores em 60
        // (e 12 projetos sociais, que equivalem a 60 na escala normalizada) pontua exatamente 60.
        var cidade = CriarCidade(60, 60, 60, 60, 60, projetosSociais: 12);

        Assert.Equal(60d, EsgCalculator.CalcularPontuacao(cidade), Precisao);
        Assert.Equal("Bom", EsgCalculator.Classificar(60));
    }

    [Fact]
    public void CalcularPontuacao_DeveRespeitarOPesoDeCadaIndicador()
    {
        // Apenas a coleta seletiva no maximo: 100 * peso 20 / 100 = 20 pontos.
        var cidade = CriarCidade(coletaSeletiva: 100, 0, 0, 0, 0, 0);

        Assert.Equal(EsgCalculator.PesoColetaSeletiva, EsgCalculator.CalcularPontuacao(cidade), Precisao);
    }

    [Fact]
    public void CalcularPontuacao_AcimaDaMetaDeProjetosSociais_NaoDevePontuarAlemDoTeto()
    {
        var cidadeNaMeta = CriarCidade(0, 0, 0, 0, 0, projetosSociais: EsgCalculator.MetaProjetosSociais);
        var cidadeAcimaDaMeta = CriarCidade(0, 0, 0, 0, 0, projetosSociais: 500);

        Assert.Equal(EsgCalculator.PesoProjetosSociais, EsgCalculator.CalcularPontuacao(cidadeNaMeta), Precisao);
        Assert.Equal(
            EsgCalculator.CalcularPontuacao(cidadeNaMeta),
            EsgCalculator.CalcularPontuacao(cidadeAcimaDaMeta),
            Precisao);
    }

    [Fact]
    public void CalcularPontuacao_DeveArredondarParaDuasCasasDecimais()
    {
        // 33.33 * 20 / 100 = 6.666 -> 6.67
        var cidade = CriarCidade(coletaSeletiva: 33.33, 0, 0, 0, 0, 0);

        Assert.Equal(6.67, EsgCalculator.CalcularPontuacao(cidade), Precisao);
    }

    [Fact]
    public void CalcularPontuacao_DeveSempreFicarEntre0E100()
    {
        var cidade = CriarCidade(
            coletaSeletiva: 85,
            energiaRenovavel: 70,
            areaVerde: 78,
            saneamento: 95,
            indicadorSocial: 80,
            projetosSociais: 18);

        var pontuacao = EsgCalculator.CalcularPontuacao(cidade);

        Assert.InRange(pontuacao, 0, 100);
        Assert.Equal(82.7, pontuacao, Precisao);
        Assert.Equal("Excelente", EsgCalculator.Classificar(pontuacao));
    }

    [Fact]
    public void Avaliar_DeveDevolverPontuacaoEClassificacaoConsistentes()
    {
        var cidade = CriarCidade(50, 50, 50, 50, 50, projetosSociais: 10);

        var (pontuacao, classificacao) = EsgCalculator.Avaliar(cidade);

        Assert.Equal(50d, pontuacao, Precisao);
        Assert.Equal("Regular", classificacao);
    }

    private static Cidade CriarCidade(
        double coletaSeletiva,
        double energiaRenovavel,
        double areaVerde,
        double saneamento,
        double indicadorSocial,
        int projetosSociais) => new()
        {
            Nome = "Cidade Teste",
            Estado = "SP",
            Populacao = 100000,
            PercentualColetaSeletiva = coletaSeletiva,
            PercentualEnergiaRenovavel = energiaRenovavel,
            PercentualAreaVerde = areaVerde,
            IndiceSaneamento = saneamento,
            IndicadorSocial = indicadorSocial,
            QuantidadeProjetosSociais = projetosSociais
        };
}
