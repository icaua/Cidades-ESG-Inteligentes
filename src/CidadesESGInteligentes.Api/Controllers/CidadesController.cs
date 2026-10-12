using CidadesESGInteligentes.Api.Data;
using CidadesESGInteligentes.Api.Dtos;
using CidadesESGInteligentes.Api.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CidadesESGInteligentes.Api.Controllers;

/// <summary>
/// CRUD de cidades e consultas de pontuacao, classificacao e ranking ESG.
/// </summary>
[ApiController]
[Route("api/cidades")]
[Produces("application/json")]
public class CidadesController : ControllerBase
{
    private readonly AppDbContext _contexto;

    public CidadesController(AppDbContext contexto)
    {
        _contexto = contexto;
    }

    /// <summary>Lista todas as cidades cadastradas com sua pontuacao ESG.</summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<CidadeResponse>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<CidadeResponse>>> Listar()
    {
        var cidades = await _contexto.Cidades
            .AsNoTracking()
            .OrderBy(c => c.Nome)
            .ToListAsync();

        return Ok(cidades.Select(CidadeResponse.DeEntidade));
    }

    /// <summary>
    /// Ranking das cidades da maior para a menor pontuacao ESG.
    /// </summary>
    /// <remarks>
    /// A ordenacao e feita em memoria porque a pontuacao e calculada pela aplicacao
    /// e nao fica armazenada no banco. O volume de dados deste projeto torna isso irrelevante.
    /// </remarks>
    [HttpGet("ranking")]
    [ProducesResponseType(typeof(IEnumerable<RankingItemResponse>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<RankingItemResponse>>> Ranking()
    {
        var cidades = await _contexto.Cidades.AsNoTracking().ToListAsync();

        var ranking = cidades
            .OrderByDescending(EsgCalculator.CalcularPontuacao)
            .ThenBy(c => c.Nome)
            .Select((cidade, indice) => RankingItemResponse.DeEntidade(cidade, indice + 1));

        return Ok(ranking);
    }

    /// <summary>Busca uma cidade pelo identificador.</summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(CidadeResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<CidadeResponse>> BuscarPorId(int id)
    {
        var cidade = await _contexto.Cidades.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);

        if (cidade is null)
        {
            return NotFound(new { mensagem = $"Cidade {id} nao encontrada." });
        }

        return Ok(CidadeResponse.DeEntidade(cidade));
    }

    /// <summary>Retorna apenas a pontuacao ESG calculada da cidade.</summary>
    [HttpGet("{id:int}/pontuacao")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Pontuacao(int id)
    {
        var cidade = await _contexto.Cidades.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);

        if (cidade is null)
        {
            return NotFound(new { mensagem = $"Cidade {id} nao encontrada." });
        }

        return Ok(new
        {
            id = cidade.Id,
            nome = cidade.Nome,
            pontuacaoEsg = EsgCalculator.CalcularPontuacao(cidade)
        });
    }

    /// <summary>Retorna a pontuacao e a classificacao ESG da cidade.</summary>
    [HttpGet("{id:int}/classificacao")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Classificacao(int id)
    {
        var cidade = await _contexto.Cidades.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);

        if (cidade is null)
        {
            return NotFound(new { mensagem = $"Cidade {id} nao encontrada." });
        }

        var (pontuacao, classificacao) = EsgCalculator.Avaliar(cidade);

        return Ok(new
        {
            id = cidade.Id,
            nome = cidade.Nome,
            pontuacaoEsg = pontuacao,
            classificacaoEsg = classificacao
        });
    }

    /// <summary>Cadastra uma nova cidade.</summary>
    [HttpPost]
    [ProducesResponseType(typeof(CidadeResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<CidadeResponse>> Cadastrar([FromBody] CidadeRequest requisicao)
    {
        var nome = requisicao.Nome.Trim();
        var estado = requisicao.Estado.Trim().ToUpperInvariant();

        var jaExiste = await _contexto.Cidades.AnyAsync(c => c.Nome == nome && c.Estado == estado);

        if (jaExiste)
        {
            return Conflict(new { mensagem = $"A cidade {nome}/{estado} ja esta cadastrada." });
        }

        var cidade = requisicao.ParaEntidade();
        cidade.CriadoEm = DateTime.UtcNow;

        _contexto.Cidades.Add(cidade);
        await _contexto.SaveChangesAsync();

        return CreatedAtAction(
            nameof(BuscarPorId),
            new { id = cidade.Id },
            CidadeResponse.DeEntidade(cidade));
    }

    /// <summary>Atualiza os dados de uma cidade existente.</summary>
    [HttpPut("{id:int}")]
    [ProducesResponseType(typeof(CidadeResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<CidadeResponse>> Atualizar(int id, [FromBody] CidadeRequest requisicao)
    {
        var cidade = await _contexto.Cidades.FirstOrDefaultAsync(c => c.Id == id);

        if (cidade is null)
        {
            return NotFound(new { mensagem = $"Cidade {id} nao encontrada." });
        }

        requisicao.AplicarEm(cidade);
        await _contexto.SaveChangesAsync();

        return Ok(CidadeResponse.DeEntidade(cidade));
    }

    /// <summary>Exclui uma cidade.</summary>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Excluir(int id)
    {
        var cidade = await _contexto.Cidades.FirstOrDefaultAsync(c => c.Id == id);

        if (cidade is null)
        {
            return NotFound(new { mensagem = $"Cidade {id} nao encontrada." });
        }

        _contexto.Cidades.Remove(cidade);
        await _contexto.SaveChangesAsync();

        return NoContent();
    }
}
