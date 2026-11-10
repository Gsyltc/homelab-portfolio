# Suivi des séances et progression

## `sport/suivi-sportif.md`

Journal chronologique, non versionné. Chaque séance effectuée est **confirmée par le patient ou l'humain** et retranscrite avec sa date. Pour chaque exercice réalisé, consigner la **charge utilisée** (kg, ou « poids du corps »). La dernière charge enregistrée par exercice alimente « Dernière séance » dans `programme-sportif.md`.

**Format imposé** (vérifié par le sensor `scripts/check_sportif.py suivi`, voir `sensors.md`), séances en ordre chronologique croissant :

```markdown
# Suivi sportif — <patient>

## 2026-09-13 — Séance confirmée par patient
- RPE séance : 6/10
- Douleur (EVA) : 2/10
- Fatigue lendemain : aucune
- Symptômes : RAS
- Retours : facile sur le stepper, banc un peu dur

| Exercice | Charge | Séries × répétitions |
|---|---|---|
| Stepper | poids du corps | 1 × 15 min |
| Développé couché (banc) | 12,5 kg | 3 × 10 |
```

- Obligatoires : en-tête de séance (`patient` ou `humain`), RPE (0-10), EVA (0-10), tableau avec au moins un exercice.
- Optionnels : `Fatigue lendemain` (aucune | légère | marquée), `Symptômes` (SEP : voir `adaptation-sep.md`), `Retours` (difficulté, facilité, ressenti).

## Progression

- Ne jamais augmenter charge ET volume simultanément ; progression max. ~**10 % par semaine**.
- Progresser seulement si les séances sont tolérées (RPE stable, pas de douleur croissante).
- En cas de gêne, de fatigue marquée ou de séance manquée : appliquer la **régression** de l'exercice ou stabiliser.

## Douleur

- **Gêne acceptable** : < 3/10, décroissante et revenue à l'état initial sous 24 h.
- **Signal d'alarme** : douleur croissante, œdème, perte de fonction → arrêter l'exercice, revoir le plan et alerter le médecin (« 🚨 À vérifier auprès du médecin avant tout exercice : … »).

## Prévention

Travail de contrôle neuromusculaire, gainage, mobilité et renforcement des groupes musculaires sollicités, limité au matériel disponible et au poids du corps.
