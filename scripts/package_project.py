"""Empacota fontes e entregaveis; exclui segredos e artefatos temporarios."""
import hashlib
import json
import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
PDF = OUT / "pdf/Documentacao-tecnica.pdf"
if not PDF.is_file():
    raise SystemExit("Gere primeiro scripts/generate_documentation.py")
parser = argparse.ArgumentParser()
parser.add_argument("--final", action="store_true", help="Exige comprovacao de todos os requisitos")
args = parser.parse_args()
status_file = ROOT / "docs/evidencias/2026-10-13/validacao.json"
status = json.loads(status_file.read_text(encoding="utf-8")) if status_file.exists() else {}
ready = status.get("ready_for_submission") is True
if args.final and not ready:
    raise SystemExit("Entrega definitiva bloqueada: faltam evidencias reais. Consulte docs/STATUS-ENTREGA.md")

files = []
for name in ["Dockerfile", "docker-compose.yml", "CidadesESGInteligentes.sln", "README.md",
             ".dockerignore", ".gitignore", ".env.example", ".env.staging.example", ".env.production.example"]:
    files.append((ROOT / name, name))
excluded = {"bin", "obj", "__pycache__", ".git", "TestResults"}
for directory in ["src", "tests", ".github", "scripts", "docs"]:
    for path in sorted((ROOT / directory).rglob("*")):
        relative = path.relative_to(ROOT)
        if not path.is_file() or excluded.intersection(relative.parts):
            continue
        if path.name.startswith(".env") and not path.name.endswith(".example"):
            continue
        if path.suffix.lower() in {".zip", ".pyc"}:
            continue
        files.append((path, relative.as_posix()))
files.append((PDF, "docs/Documentacao-tecnica.pdf"))
archive = OUT / ("CidadesESGInteligentes-entrega.zip" if ready else "CidadesESGInteligentes-revisao-pendente.zip")
manifest = {}
prefix = "CidadesESGInteligentes/"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for path, name in files:
        data = path.read_bytes()
        z.writestr(prefix + name, data)
        manifest[name] = hashlib.sha256(data).hexdigest()
    z.writestr(prefix + "MANIFEST-SHA256.json", json.dumps(manifest, indent=2, ensure_ascii=False))
with ZipFile(archive) as z:
    assert z.testzip() is None
    names = z.namelist()
    for required in ["Dockerfile", "docker-compose.yml", "README.md", ".env.example",
                     ".github/workflows/ci-cd.yml", "src/CidadesESGInteligentes.Api/Program.cs",
                     "docs/Documentacao-tecnica.pdf"]:
        assert prefix + required in names, required
    assert not any("/tmp/" in name or "/bin/" in name or "/obj/" in name for name in names)
    assert len(names) == len(set(names))
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(OUT / (archive.name + ".sha256")).write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
print(f"ZIP verificado: {archive}\nArquivos: {len(names)}\nSHA256: {digest}")
