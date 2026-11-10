# Sensors de vérification (script Python)

Script : `scripts/check_sportif.py` (stdlib uniquement). Verdicts `conforme | ecart | indisponible` ; sortie JSON `sensors_resultats` ; code de sortie 0 / 1 / 2. Le verdict n'est jamais réinterprété : `indisponible` n'est pas `conforme`.

```bash
S="$ROOT_DIRECTORY/<patient>/sport"
python3 scripts/check_sportif.py suivi   "$S"             # format de suivi-sportif.md
python3 scripts/check_sportif.py archive "$S" --modified  # archive de l'ancienne version après modification
python3 scripts/check_sportif.py all     "$S" --modified
```

## Quand les lancer

- `suivi` : après chaque ajout au journal `suivi-sportif.md`, et avant la revue du dimanche.
- `archive --modified` : après l'application d'un programme validé (étape 4 du versionnage), avant l'export PDF et la remise à l'humain.
- Un `ecart` bloque : corriger puis relancer, ne jamais livrer avec un écart.

## Ce que vérifie `suivi`

Format exact de `suivi-sportif.md` (voir `suivi-et-progression.md`) : titre, séances à date valide, ordre chronologique, pas de doublon de date, `Séance confirmée par patient|humain`, RPE et EVA entre 0 et 10, tableau d'exercices avec charge `N kg` ou `poids du corps`, lignes optionnelles (fatigue du lendemain, symptômes, retours) valides, aucune ligne hors format.

## Ce que vérifie `archive`

Noms d'archives conformes `yyyy-MM-dd_hh-mm.programme-sportif.md` à date valide ; avec `--modified` : une archive de l'ancienne version existe, différente du programme actuel et antérieure à sa modification ; le PDF existant n'est pas plus ancien que le programme.
