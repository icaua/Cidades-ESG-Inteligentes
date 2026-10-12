using CidadesESGInteligentes.Api.Models;
using CidadesESGInteligentes.Api.Services;

namespace CidadesESGInteligentes.Api.Dtos;

/// <summary>
/// Linha do ranking ESG: versao enxuta da cidade, com a posicao na classificacao geral.
/// </summary>
public class RankingItemResponse
{
    public int Posicao { get; set; }
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public string Estado { get; set; } = string.Empty;
    public double PontuacaoEsg { get; set; }
    public string ClassificacaoEsg { get; set; } = string.Empty;

    public static RankingItemResponse DeEntidade(Cidade cidade, int posicao)
    {
        var (pontuacao, classificacao) = EsgCalculator.Avaliar(cidade);

        return new RankingItemResponse
        {
            Posicao = posicao,
            Id = cidade.Id,
            Nome = cidade.Nome,
            Estado = cidade.Estado,
            PontuacaoEsg = pontuacao,
            ClassificacaoEsg = classificacao
        };
    }
}
