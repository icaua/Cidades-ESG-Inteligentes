using CidadesESGInteligentes.Api.Models;
using CidadesESGInteligentes.Api.Services;

namespace CidadesESGInteligentes.Api.Dtos;

/// <summary>
/// Representacao de uma cidade devolvida pela API, ja com a pontuacao
/// e a classificacao ESG calculadas.
/// </summary>
public class CidadeResponse
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public int Populacao { get; set; }
    public double PercentualColetaSeletiva { get; set; }
    public double PercentualEnergiaRenovavel { get; set; }
    public double PercentualAreaVerde { get; set; }
    public double IndiceSaneamento { get; set; }
    public double IndicadorSocial { get; set; }
    public int QuantidadeProjetosSociais { get; set; }

    /// <summary>Pontuacao ESG calculada, de 0 a 100.</summary>
    public double PontuacaoEsg { get; set; }

    /// <summary>Faixa correspondente a pontuacao: Critico, Regular, Bom ou Excelente.</summary>
    public string ClassificacaoEsg { get; set; } = string.Empty;

    public DateTime CriadoEm { get; set; }
    public DateTime AtualizadoEm { get; set; }

    public static CidadeResponse DeEntidade(Cidade cidade)
    {
        var (pontuacao, classificacao) = EsgCalculator.Avaliar(cidade);

        return new CidadeResponse
        {
            Id = cidade.Id,
            Nome = cidade.Nome,
            Estado = cidade.Estado,
            Populacao = cidade.Populacao,
            PercentualColetaSeletiva = cidade.PercentualColetaSeletiva,
            PercentualEnergiaRenovavel = cidade.PercentualEnergiaRenovavel,
            PercentualAreaVerde = cidade.PercentualAreaVerde,
            IndiceSaneamento = cidade.IndiceSaneamento,
            IndicadorSocial = cidade.IndicadorSocial,
            QuantidadeProjetosSociais = cidade.QuantidadeProjetosSociais,
            PontuacaoEsg = pontuacao,
            ClassificacaoEsg = classificacao,
            CriadoEm = cidade.CriadoEm,
            AtualizadoEm = cidade.AtualizadoEm
        };
    }
}
