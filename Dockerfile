# =========================================================
# Estagio 1 - build: compila e publica a aplicacao.
# Usa a imagem do SDK, que e grande (~800 MB) e nao vai para producao.
# =========================================================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

# Copiar primeiro apenas os arquivos de projeto permite que o Docker reaproveite
# o cache do restore enquanto nenhuma dependencia NuGet mudar.
COPY CidadesESGInteligentes.sln ./
COPY src/CidadesESGInteligentes.Api/CidadesESGInteligentes.Api.csproj src/CidadesESGInteligentes.Api/
COPY tests/CidadesESGInteligentes.Tests/CidadesESGInteligentes.Tests.csproj tests/CidadesESGInteligentes.Tests/
RUN dotnet restore

COPY . .
RUN dotnet publish src/CidadesESGInteligentes.Api/CidadesESGInteligentes.Api.csproj \
    --configuration Release \
    --no-restore \
    --output /app/publish

# =========================================================
# Estagio 2 - runtime: apenas o necessario para executar.
# A imagem final exclui o SDK e os arquivos de desenvolvimento.
# =========================================================
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# curl e usado pelo HEALTHCHECK abaixo; a imagem base nao traz nenhum cliente HTTP.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/publish .

ENV ASPNETCORE_HTTP_PORTS=8080
ARG APP_VERSION=local
ENV APP_VERSION=$APP_VERSION
LABEL org.opencontainers.image.revision=$APP_VERSION
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:8080/health || exit 1

# Usuario sem privilegios ja incluido nas imagens oficiais do .NET 8.
USER app

ENTRYPOINT ["dotnet", "CidadesESGInteligentes.Api.dll"]
