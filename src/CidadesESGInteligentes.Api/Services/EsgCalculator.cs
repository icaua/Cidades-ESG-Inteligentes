using CidadesESGInteligentes.Api.Models;

namespace CidadesESGInteligentes.Api.Services;

/// <summary>
/// Regra de negocio central do projeto: transforma os indicadores brutos de uma cidade
/// em uma pontuacao ESG de 0 a 100 e na respectiva classificacao.
///
/// E uma classe estatica e sem dependencias externas (nao conhece banco, HTTP ou DI)
/// justamente para ser 100% testavel por testes unitarios rapidos.
/// </summary>
public static class EsgCalculator
{
    /// <summary>
    /// Numero de projetos sociais que ja garante nota maxima nesse criterio.
    /// Serve para normalizar uma contagem (0..N) em um percentual (0..100).
    /// </summary>
    public const int MetaProjetosSociais = 20;

    // Pesos de cada indicador. A soma e exatamente 100, entao a pontuacao final
    // ja nasce na escala 0..100 sem nenhuma normalizacao extra.
    public const double PesoColetaSeletiva = 20;
    public const double PesoEnergiaRenovavel = 20;
    public const double PesoAreaVerde = 15;
    public const double PesoSaneamento = 20;
    public const double PesoIndicadorSocial = 15;
    public const double PesoProjetosSociais = 10;

    /// <summary>
    /// Calcula a pontuacao ESG (0 a 100) como media ponderada dos indicadores da cidade.
    /// </summary>
    public static double CalcularPontuacao(Cidade cidade)
    {
        ArgumentNullException.ThrowIfNull(cidade);

        var notaProjetosSociais = NormalizarProjetosSociais(cidade.QuantidadeProjetosSociais);

        var pontuacao =
            (Limitar(cidade.PercentualColetaSeletiva) * PesoColetaSeletiva +
             Limitar(cidade.PercentualEnergiaRenovavel) * PesoEnergiaRenovavel +
             Limitar(cidade.PercentualAreaVerde) * PesoAreaVerde +
             Limitar(cidade.IndiceSaneamento) * PesoSaneamento +
             Limitar(cidade.IndicadorSocial) * PesoIndicadorSocial +
             notaProjetosSociais * PesoProjetosSociais) / 100d;

        return Math.Round(pontuacao, 2, MidpointRounding.AwayFromZero);
    }

    /// <summary>
    /// Converte a pontuacao ESG na faixa de classificacao correspondente.
    /// 0-39 Critico | 40-59 Regular | 60-79 Bom | 80-100 Excelente
    /// </summary>
    public static string Classificar(double pontuacao)
    {
        var valor = Limitar(pontuacao);

        return valor switch
        {
            >= 80 => "Excelente",
            >= 60 => "Bom",
            >= 40 => "Regular",
            _ => "Critico"
        };
    }

    /// <summary>
    /// Atalho usado pelos endpoints: calcula pontuacao e classificacao de uma vez.
    /// </summary>
    public static (double Pontuacao, string Classificacao) Avaliar(Cidade cidade)
    {
        var pontuacao = CalcularPontuacao(cidade);
        return (pontuacao, Classificar(pontuacao));
    }

    /// <summary>
    /// Transforma a quantidade de projetos sociais em uma nota de 0 a 100.
    /// Ex.: 0 projetos = 0 | 10 projetos = 50 | 20 ou mais projetos = 100.
    /// </summary>
    private static double NormalizarProjetosSociais(int quantidade)
    {
        if (quantidade <= 0)
        {
            return 0;
        }

        return Math.Min(quantidade, MetaProjetosSociais) * 100d / MetaProjetosSociais;
    }

    /// <summary>
    /// Protege o calculo contra valores fora da escala 0..100.
    /// </summary>
    private static double Limitar(double valor) => Math.Clamp(valor, 0, 100);
}
