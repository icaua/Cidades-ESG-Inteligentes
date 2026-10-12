using System.ComponentModel.DataAnnotations;
using CidadesESGInteligentes.Api.Models;

namespace CidadesESGInteligentes.Api.Dtos;

/// <summary>
/// Dados de entrada para cadastrar ou atualizar uma cidade.
/// Existe separado da entidade para que o cliente nao consiga enviar Id,
/// CriadoEm ou qualquer campo controlado pelo servidor.
/// </summary>
public class CidadeRequest
{
    /// <example>Sao Paulo</example>
    [Required(ErrorMessage = "O nome da cidade e obrigatorio.")]
    [StringLength(120, MinimumLength = 2, ErrorMessage = "O nome deve ter entre 2 e 120 caracteres.")]
    public string Nome { get; set; } = string.Empty;

    /// <example>SP</example>
    [Required(ErrorMessage = "O estado e obrigatorio.")]
    [StringLength(2, MinimumLength = 2, ErrorMessage = "Informe a sigla do estado com 2 letras.")]
    public string Estado { get; set; } = string.Empty;

    /// <example>12300000</example>
    [Range(1, int.MaxValue, ErrorMessage = "A populacao deve ser maior que zero.")]
    public int Populacao { get; set; }

    /// <example>62.5</example>
    [Range(0, 100, ErrorMessage = "O percentual de coleta seletiva deve estar entre 0 e 100.")]
    public double PercentualColetaSeletiva { get; set; }

    /// <example>48</example>
    [Range(0, 100, ErrorMessage = "O percentual de energia renovavel deve estar entre 0 e 100.")]
    public double PercentualEnergiaRenovavel { get; set; }

    /// <example>35</example>
    [Range(0, 100, ErrorMessage = "O percentual de area verde deve estar entre 0 e 100.")]
    public double PercentualAreaVerde { get; set; }

    /// <example>88</example>
    [Range(0, 100, ErrorMessage = "O indice de saneamento deve estar entre 0 e 100.")]
    public double IndiceSaneamento { get; set; }

    /// <example>72</example>
    [Range(0, 100, ErrorMessage = "O indicador social deve estar entre 0 e 100.")]
    public double IndicadorSocial { get; set; }

    /// <example>14</example>
    [Range(0, int.MaxValue, ErrorMessage = "A quantidade de projetos sociais nao pode ser negativa.")]
    public int QuantidadeProjetosSociais { get; set; }

    /// <summary>
    /// Cria uma nova entidade a partir dos dados recebidos.
    /// </summary>
    public Cidade ParaEntidade()
    {
        var cidade = new Cidade();
        AplicarEm(cidade);
        return cidade;
    }

    /// <summary>
    /// Copia os dados recebidos para uma entidade existente (usado no PUT).
    /// </summary>
    public void AplicarEm(Cidade cidade)
    {
        cidade.Nome = Nome.Trim();
        cidade.Estado = Estado.Trim().ToUpperInvariant();
        cidade.Populacao = Populacao;
        cidade.PercentualColetaSeletiva = PercentualColetaSeletiva;
        cidade.PercentualEnergiaRenovavel = PercentualEnergiaRenovavel;
        cidade.PercentualAreaVerde = PercentualAreaVerde;
        cidade.IndiceSaneamento = IndiceSaneamento;
        cidade.IndicadorSocial = IndicadorSocial;
        cidade.QuantidadeProjetosSociais = QuantidadeProjetosSociais;
        cidade.AtualizadoEm = DateTime.UtcNow;
    }
}
