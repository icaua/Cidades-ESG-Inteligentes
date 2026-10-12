"""Valida a revisao implantada, o ambiente e uma consulta real ao banco."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


def get_json(url):
    request = Request(url, headers={"Cache-Control": "no-cache"})
    with urlopen(request, timeout=8) as response:
        return json.load(response)


def validate_health(health, environment, version):
    if not isinstance(health, dict) or health.get("status") != "ok":
        raise ValueError("API ou banco indisponivel")
    if health.get("ambiente") != environment:
        raise ValueError("Ambiente diferente do esperado")
    if health.get("versao") != version:
        raise ValueError("A revisao esperada ainda nao esta em execucao")


def save_evidence(output, evidence):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")


def verify(url, environment, version, output, attempts=40, interval=10, metadata=None):
    evidence = {**(metadata or {}), "url": url, "environment": environment, "expected_version": version,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(), "success": False}
    for attempt in range(1, attempts + 1):
        try:
            health = get_json(url.rstrip("/") + "/health")
            validate_health(health, environment, version)
            ranking = get_json(url.rstrip("/") + "/api/cidades/ranking")
            if not isinstance(ranking, list):
                raise ValueError("Ranking nao retornou uma lista JSON")
            evidence.update(success=True, health=health, ranking=ranking, attempt=attempt,
                            verified_at_utc=datetime.now(timezone.utc).isoformat())
            save_evidence(output, evidence)
            print(f"OK: {environment}, revisao {version}, ranking com {len(ranking)} cidades")
            return evidence
        except Exception as error:
            # Nao imprime URLs de excecoes: podem conter credenciais.
            evidence["last_error_type"] = type(error).__name__
            print(f"Tentativa {attempt}/{attempts}: aguardando API, banco e revisao esperada.")
            if attempt < attempts:
                time.sleep(interval)
    save_evidence(output, evidence)
    raise RuntimeError("Verificacao falhou; consulte o provedor e a evidencia JSON")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--attempts", type=int, default=40)
    args = parser.parse_args()
    verify(args.url, args.environment, args.version, args.output, args.attempts)
