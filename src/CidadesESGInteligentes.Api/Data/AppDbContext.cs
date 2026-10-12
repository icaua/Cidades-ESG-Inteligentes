using CidadesESGInteligentes.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace CidadesESGInteligentes.Api.Data;

/// <summary>
/// Contexto do Entity Framework Core. O projeto tem uma unica tabela,
/// entao o mapeamento e propositalmente minimo.
/// </summary>
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Cidade> Cidades => Set<Cidade>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var cidade = modelBuilder.Entity<Cidade>();

        cidade.ToTable("cidades");
        cidade.HasKey(c => c.Id);
        cidade.Property(c => c.Nome).HasMaxLength(120).IsRequired();
        cidade.Property(c => c.Estado).HasMaxLength(2).IsRequired();

        // Evita duas cidades com o mesmo nome no mesmo estado.
        cidade.HasIndex(c => new { c.Nome, c.Estado }).IsUnique();
    }
}
