using System.ComponentModel.DataAnnotations;

namespace CidadesESGInteligentes.Api.Models;

/// <summary>
/// Entidade persistida no banco. Representa uma cidade e seus indicadores ESG brutos.
/// A pontuacao e a classificacao NAO sao gravadas: sao calculadas sob demanda
/// pelo <see cref="Services.EsgCalculator"/>, o que evita dados desatualizados no banco.
/// </summary>
public class Cidade
{
    public int Id { get; set; }

    [Required]
    [StringLength(120, MinimumLength = 2)]
    public string Nome { get; set; } = string.Empty;

    [Required]
    [StringLength(2, MinimumLength = 2)]
    public string Estado { get; set; } = string.Empty;

    [Range(1, int.MaxValue)]
    public int Populacao { get; set; }

    [Range(0, 100)]
    public double PercentualColetaSeletiva { get; set; }

    [Range(0, 100)]
    public double PercentualEnergiaRenovavel { get; set; }

    [Range(0, 100)]
    public double PercentualAreaVerde { get; set; }

    [Range(0, 100)]
    public double IndiceSaneamento { get; set; }

    [Range(0, 100)]
    public double IndicadorSocial { get; set; }

    [Range(0, int.MaxValue)]
    public int QuantidadeProjetosSociais { get; set; }

    public DateTime CriadoEm { get; set; } = DateTime.UtcNow;

    public DateTime AtualizadoEm { get; set; } = DateTime.UtcNow;
}
