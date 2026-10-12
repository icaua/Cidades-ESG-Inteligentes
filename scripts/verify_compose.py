"""Verificacao real de rede, health e persistencia no projeto descartavel 'ci'."""
import argparse
import json
import os
import subprocess
import uuid
from pathlib import Path
from smoke_test import verify, save_evidence

COMPOSE = ["docker", "compose", "-p", "ci"]


def run(*args):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def inspect_service(service):
    container_id = run(*COMPOSE, "ps", "-q", service)
    if not container_id:
        raise RuntimeError(f"Servico {service} ausente")
    data = json.loads(run("docker", "inspect", container_id))[0]
    # Nao salvar Config.Env: contem a senha do banco.
    return {"id": container_id, "image_id": data["Image"],
            "health": data["State"].get("Health", {}).get("Status"),
            "networks": sorted(data["NetworkSettings"]["Networks"]),
            "volumes": [m["Name"] for m in data["Mounts"] if m["Type"] == "volume"]}


def sql(statement):
    return run(*COMPOSE, "exec", "-T", "db", "psql", "-v", "ON_ERROR_STOP=1",
               "-U", os.environ.get("DB_USER", "postgres"),
               "-d", os.environ.get("DB_NAME", "cidades_esg"), "-tAc", statement)


def main(version):
    output = "docs/evidencias/ci-compose.json"
    evidence = {"success": False, "project": "ci", "version": version}
    try:
        before = {s: inspect_service(s) for s in ("api", "db")}
        assert all(s["health"] == "healthy" for s in before.values())
        common = set(before["api"]["networks"]) & set(before["db"]["networks"])
        assert common, "API e banco sem rede compartilhada"
        assert before["db"]["volumes"], "Banco sem volume nomeado"
        marker = uuid.uuid4().hex
        sql("CREATE TABLE IF NOT EXISTS devops_volume_probe (value text PRIMARY KEY);")
        sql(f"INSERT INTO devops_volume_probe VALUES ('{marker}');")
        # Somente o projeto ci e recriado. Sem -v: dados devem sobreviver.
        run(*COMPOSE, "down")
        run(*COMPOSE, "up", "-d", "--no-build", "--wait", "--wait-timeout", "180")
        after = {s: inspect_service(s) for s in ("api", "db")}
        assert before["db"]["id"] != after["db"]["id"], "Banco nao foi recriado"
        assert before["db"]["volumes"] == after["db"]["volumes"], "Volume alterado"
        assert sql(f"SELECT count(*) FROM devops_volume_probe WHERE value='{marker}';") == "1"
        sql("DROP TABLE devops_volume_probe;")
        verify("http://localhost:" + os.environ.get("API_PORT", "8080"),
               "Staging", version, "docs/evidencias/ci-smoke-after-recreate.json", 3)
        evidence.update(success=True, before=before, after=after,
                        persistence_verified=True, shared_networks=sorted(common))
    except Exception as error:
        evidence["error_type"] = type(error).__name__
        raise
    finally:
        save_evidence(output, evidence)
    print("Compose validado: API, PostgreSQL, healthchecks, rede e persistencia apos recriacao.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    main(parser.parse_args().version)
