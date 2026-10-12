using System.ComponentModel.DataAnnotations;
using CidadesESGInteligentes.Api.Dtos;
using Xunit;

namespace CidadesESGInteligentes.Tests;

/// <summary>
/// Testes das regras de validacao aplicadas no cadastro de uma cidade.
/// Sao as mesmas regras que o ASP.NET Core executa antes de chegar no controller,
/// entao aqui elas sao verificadas diretamente, sem subir a aplicacao nem o banco.
/// </summary>
public class CidadeCadastroTests
{
    [Fact]
    public void Cadastro_ComDadosValidos_NaoDeveApresentarErros()
    {
        var requisicao = CriarRequisicaoValida();

        Assert.Empty(Validar(requisicao));
    }

    [Fact]
    public void Cadastro_SemNome_DeveSerRejeitado()
    {
        var requisicao = CriarRequisicaoValida();
        requisicao.Nome = string.Empty;

        var erros = Validar(requisicao);

        Assert.Contains(erros, e => e.MemberNames.Contains(nameof(CidadeRequest.Nome)));
    }

    [Theory]
    [InlineData(-10)]
    [InlineData(150)]
    public void Cadastro_ComPercentualForaDaEscala_DeveSerRejeitado(double percentualInvalido)
    {
        var requisicao = CriarRequisicaoValida();
        requisicao.PercentualColetaSeletiva = percentualInvalido;

        var erros = Validar(requisicao);

        Assert.Contains(erros, e => e.MemberNames.Contains(nameof(CidadeRequest.PercentualColetaSeletiva)));
    }

    [Fact]
    public void Cadastro_ComPopulacaoZerada_DeveSerRejeitado()
    {
        var requisicao = CriarRequisicaoValida();
        requisicao.Populacao = 0;

        var erros = Validar(requisicao);

        Assert.Contains(erros, e => e.MemberNames.Contains(nameof(CidadeRequest.Populacao)));
    }

    [Fact]
    public void Cadastro_DeveNormalizarNomeEEstadoAoGerarAEntidade()
    {
        var requisicao = CriarRequisicaoValida();
        requisicao.Nome = "  Curitiba  ";
        requisicao.Estado = "pr";

        var cidade = requisicao.ParaEntidade();

        Assert.Equal("Curitiba", cidade.Nome);
        Assert.Equal("PR", cidade.Estado);
    }

    private static CidadeRequest CriarRequisicaoValida() => new()
    {
        Nome = "Florianopolis",
        Estado = "SC",
        Populacao = 540000,
        PercentualColetaSeletiva = 62.5,
        PercentualEnergiaRenovavel = 48,
        PercentualAreaVerde = 35,
        IndiceSaneamento = 88,
        IndicadorSocial = 72,
        QuantidadeProjetosSociais = 14
    };

    private static IList<ValidationResult> Validar(object modelo)
    {
        var contexto = new ValidationContext(modelo);
        var resultados = new List<ValidationResult>();

        Validator.TryValidateObject(modelo, contexto, resultados, validateAllProperties: true);

        return resultados;
    }
}
