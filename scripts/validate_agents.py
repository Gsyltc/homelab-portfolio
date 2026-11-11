#!/usr/bin/env python3
"""Valide les fiches d'agents (<workflow>/agents/*.md) : front-matter + bonnes pratiques Multica / AI-DLC.

Règles (ADR-0008, ADR-0019) :
  - front-matter YAML présent, délimité par '---' ;
  - name == stem du fichier, kebab-case, 1–64 car. ;
  - display_name et description non vides (description <= 1024 car.) ;
  - disallowedTools inclut 'Task' ;
  - tier dans {judgment, balanced, templated} ;
  - skills (optionnel) : liste de noms kebab-case ;
  - champs interdits : allowedTools, model (jamais de model brut en source) ;
  - aucun secret apparent ; corps Markdown non vide.

Usage : validate_agents.py [fichier.md ...]   (sans argument : tous les agents du dépôt)
Code de sortie non nul si une fiche échoue.
"""
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("ERROR: PyYAML requis (pip install pyyaml).")

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
TIERS = {"judgment", "balanced", "templated"}
FORBIDDEN = {"allowedTools", "model"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET = re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{16,}")


def agent_files():
    return sorted(
        p for p in ROOT.glob("*/agents/*.md") if p.name.lower() != "readme.md"
    )


def validate(path: Path):
    errs = []
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return ["front-matter YAML absent ou mal délimité (---)"]
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return [f"front-matter YAML invalide : {e}"]
    if not isinstance(fm, dict):
        return ["front-matter n'est pas un mapping YAML"]
    body = m.group(2)

    name = fm.get("name")
    if name != path.stem:
        errs.append(f"name ({name!r}) doit égaler le nom de fichier ({path.stem!r})")
    if isinstance(name, str) and not (KEBAB.match(name) and len(name) <= 64):
        errs.append("name doit être kebab-case (a-z, 0-9, '-'), 64 car. max")
    for key in ("display_name", "description"):
        v = fm.get(key)
        if not isinstance(v, str) or not v.strip():
            errs.append(f"{key} requis (chaîne non vide)")
    d = fm.get("description")
    if isinstance(d, str) and len(d.strip()) > 1024:
        errs.append(f"description trop longue ({len(d.strip())} > 1024 car.)")
    dt = fm.get("disallowedTools")
    dt_list = dt if isinstance(dt, list) else [t.strip() for t in str(dt or "").split(",")]
    if "Task" not in dt_list:
        errs.append("disallowedTools doit inclure 'Task' (pas d'auto-délégation)")
    if fm.get("tier") not in TIERS:
        errs.append(f"tier doit être l'un de {sorted(TIERS)} (reçu {fm.get('tier')!r})")
    skills = fm.get("skills")
    if skills is not None:
        if not isinstance(skills, list) or not all(isinstance(s, str) and KEBAB.match(s) for s in skills):
            errs.append("skills doit être une liste de noms kebab-case")
        elif len(set(skills)) != len(skills):
            errs.append("skills contient des doublons")
    for k in sorted(FORBIDDEN & fm.keys()):
        errs.append(f"champ interdit : {k} (cf. ADR-0008 ; pas de model brut / allowedTools)")
    if not body.strip():
        errs.append("corps Markdown vide")
    if SECRET.search(text):
        errs.append("secret apparent détecté (aucun secret dans une fiche d'agent)")
    return errs


def main(argv):
    files = [Path(a).resolve() for a in argv] if argv else agent_files()
    if not files:
        print("Aucune fiche d'agent trouvée.")
        return 0
    failed = 0
    for f in files:
        errs = validate(f)
        rel = f.relative_to(ROOT)
        if errs:
            failed += 1
            print(f"FAIL  {rel}")
            for e in errs:
                print(f"      - {e}")
    print("-" * 40)
    print(f"Agent definitions validation: {len(files) - failed} passed, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
