"""Dispara o deploy de uma imagem por digest, sem revelar o hook secreto."""
import argparse
import os
import json
import re
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from smoke_test import verify, save_evidence


def trigger(hook, image):
    parsed = urlsplit(hook)
    if (parsed.scheme != "https" or parsed.hostname != "api.render.com"
            or not parsed.path.startswith("/deploy/srv-")
            or not dict(parse_qsl(parsed.query)).get("key")
            or parsed.username or parsed.password):
        raise ValueError("Use o deploy hook HTTPS fornecido pelo Render")
    if not re.fullmatch(r"ghcr\.io/[a-z0-9._/-]+@sha256:[a-f0-9]{64}", image):
        raise ValueError("O deploy exige uma imagem com digest sha256")
    query = [(k, v) for k, v in parse_qsl(parsed.query) if k != "imgURL"]
    query.append(("imgURL", image))
    endpoint = urlunsplit(parsed._replace(query=urlencode(query)))
    try:
        with urlopen(Request(endpoint, method="POST", data=b""), timeout=30) as response:
            if response.status not in (200, 202):
                raise RuntimeError("Resposta inesperada do provedor")
            payload = json.load(response) if response.status == 200 else {}
            # Guardar apenas o ID publico; a resposta completa pode conter outros campos.
            return {"hook_status": response.status,
                    "deploy_id": payload.get("deploy", {}).get("id") or payload.get("id")}
    except Exception:
        raise RuntimeError("Falha ao disparar deploy; verifique o hook e a imagem no Render") from None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    hook = os.environ.get("DEPLOY_HOOK", "")
    url = os.environ.get("URL_BASE", "")
    image = os.environ.get("IMAGE_REF", "")
    evidence = {"success": False, "environment": args.environment,
                "expected_version": args.version, "image_ref": image,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "run_id": os.environ.get("GITHUB_RUN_ID"),
                "run_url": (f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/"
                            f"{os.environ['GITHUB_RUN_ID']}") if os.environ.get("GITHUB_RUN_ID") else None}
    try:
        if not all((hook, url, image)):
            raise ValueError("Configure o hook secreto e a URL do ambiente no GitHub")
        parsed_url = urlsplit(url)
        if (parsed_url.scheme != "https" or not parsed_url.hostname or parsed_url.username
                or parsed_url.password or parsed_url.query or parsed_url.fragment):
            raise ValueError("URL_BASE deve ser HTTPS, sem credenciais, query ou fragmento")
        evidence.update(trigger(hook, image))
        evidence = verify(url, args.environment, args.version, args.output, metadata=evidence)
    except Exception as error:
        evidence["error_type"] = type(error).__name__
        save_evidence(args.output, evidence)
        raise SystemExit("Deploy nao aprovado. Verifique configuracao, provedor e evidencia JSON.") from None
