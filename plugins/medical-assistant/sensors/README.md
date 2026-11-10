# Sensors du plugin `medical-assistant` — contrôles déterministes de clôture

Ce répertoire porte les **manifestes déclaratifs** des sensors Python du domaine repas, et les
scripts associés vivent sous [`../scripts/sensors/`](../scripts/sensors/). Ils reprennent la
convention des sensors du workflow `core` (manifeste = contrat, script = exécution déterministe,
sortie = piste d'audit), à portée du plugin.

| Sensor | Rôle | Sévérité par défaut | Script |
| --- | --- | --- | --- |
| [`repas-calendrier-agenda`](repas-calendrier-agenda.md) | Chaque repas retenu à venir existe dans le calendrier HA (`calendar.repas`) : évènement repas 19h–20h avec ingrédients en puces + créneau du lendemain 12h–13h sans description. | advisory | `repas_calendrier_agenda.py` |
| [`historique-repas-30j`](historique-repas-30j.md) | Aucun repas de `repas-retenus.md` plus ancien que 30 jours glissants — sinon **FAILED**. | **blocking** | `historique_repas_30j.py` |
| [`fichiers-repas-conformes`](fichiers-repas-conformes.md) | Les trois fichiers de données sont à jour et conformes (front matter, `count`, `oldest`/`newest`, tableau 4 colonnes, listes à puces sans doublon). | advisory | `fichiers_repas_conformes.py` |

## Exécution (lancement à la clôture)

Les scripts ne dépendent que de la bibliothèque standard (Python ≥ 3.9) et **ne modifient jamais
les données** : ils constatent et rendent un verdict.

```bash
DATA=/nfs/workspace/datas/repas
python3 plugins/medical-assistant/scripts/sensors/repas_calendrier_agenda.py --data-dir "$DATA"
python3 plugins/medical-assistant/scripts/sensors/historique_repas_30j.py    --data-dir "$DATA"
python3 plugins/medical-assistant/scripts/sensors/fichiers_repas_conformes.py --data-dir "$DATA"
```

Options communes : `--date AAAA-MM-JJ` (date de référence, défaut : aujourd'hui), `--format json`,
`--strict` (code retour 1 en cas d'écart, pour la CI). Le sensor `historique-repas-30j` est
**bloquant** : il renvoie déjà 1 en cas d'échec, sans `--strict`.

## Verdicts

`✅` conforme · `⚠️` écart (détail des écarts) · `⛔` indisponible (Home Assistant injoignable,
variable d'environnement absente, fichier illisible). **Un `⛔` n'est jamais lu comme un vert** : la
clôture n'est pas présentée comme conforme et l'humain est informé du motif.

Aucun secret n'est affiché : ni `HOMEASSISTANT_URL` ni `HOMEASSISTANT_TOKEN` ne sortent des
scripts (seul le code HTTP est cité en cas d'erreur).

## Tests

```bash
python3 -m unittest discover -s plugins/medical-assistant/sensors/tests
```

Les tests n'ont besoin d'aucun accès réseau ni des données réelles (fixtures en répertoire
temporaire) ; la corrélation calendrier est testée via la fonction pure `correler`.
