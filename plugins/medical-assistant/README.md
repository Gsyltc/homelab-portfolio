# medical-assistant

Plugin conforme à **Agent Plugins v1.0.0** regroupant les skills de la clinique
**Biboumed**. Il permet à un agent d'accompagner le suivi médical et para-médical
d'un patient : interprétation des dossiers médicaux, analyses de laboratoire et
d'examens, suivi de la morphologie et des dossiers sportifs, planification de
repas équilibrés (recherche de recettes par appareil de cuisine) et ajout des
repas au **calendrier Home Assistant** via son serveur MCP.

> **Avertissement médical.** Toutes les analyses et interprétations produites par
> ces skills sont **consultatives** et ne remplacent pas l'avis d'un
> professionnel de santé diplômé. Aucun diagnostic n'est présenté comme
> définitif ; l'incertitude et les valeurs critiques sont signalées
> explicitement.

## Structure (Agent Plugins v1.0.0)

```text
plugins/medical-assistant/
├── plugin.json          # manifeste racine ($schema + name, schéma fermé)
├── mcp.json             # config MCP (serveur home-assistant — voir « MCP » ci-dessous)
├── CHANGELOG.md
├── README.md
├── sensors/             # manifestes des sensors de clôture (contrat + verdict attendu)
├── scripts/sensors/     # scripts Python des sensors (bibliothèque standard)
└── skills/
    ├── analyse-examens/              # SKILL.md
    ├── analyse-laboratoire/          # SKILL.md
    ├── dossiers-medicaux/            # SKILL.md + gabarits/ + references/
    ├── home-assistant-calendrier/    # SKILL.md
    ├── recherche-repas/              # SKILL.md + appareils/
    ├── sportif-dossiers/             # SKILL.md + references/ + scripts/
    └── suivi-morphologie/            # SKILL.md
```

Chaque dossier immédiat sous `skills/` contient un `SKILL.md` conforme à la
spécification [Agent Skills](https://agentskills.io/specification) (frontmatter
`name` + `description`, puis corps Markdown). Le champ `name` du frontmatter
correspond au nom du dossier. La conformité est vérifiée par le validateur
officiel `skills-ref` — `scripts/validate_skills.sh` à la racine du dépôt,
également exécuté par le hook `pre-commit` et la CI GitHub Actions.

## Skills exportés (mapping)

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `dossiers-medicaux` | Clinicien — interprétation des dossiers médicaux (OCR, FHIR, notes), synthèse clinique, interactions médicamenteuses, conseil UI | `gabarits/` (suivi pathologie, export dossier), `references/` (suivi des pathologies) |
| `analyse-laboratoire` | Biologiste clinicien — analyse et archivage des bilans de biologie médicale, comparaison aux références et à l'historique, synthèse pour les médecins | — |
| `analyse-examens` | Clinicien — analyse et archivage des examens cliniques et d'imagerie (hors biologie), synthèse tableau | — |
| `suivi-morphologie` | Clinicien — suivi de la composition corporelle (poids, IMC, IMG, IGC, tours, ratios, métabolisme de base), archivage horodaté et synthèse | — |
| `sportif-dossiers` | Coach sportif — programmes d'entraînement adaptés, versionnage, planification sur 2 semaines, suivi des séances, export PDF | — |
| `recherche-repas` | Planification nutritionnelle — registre extensible des appareils de cuisine et **format** des fichiers de données ; la diversification randomisée des sources et les règles métier sont portées par l'agent | `appareils/` (registre extensible : 1 fichier de référence par appareil, livres embarqués) |
| `home-assistant-calendrier` | Intégration domotique — ajout des repas planifiés au **calendrier Home Assistant** via le serveur MCP de HA (repli REST documenté) : repas **19h–20h** avec ingrédients en puces + créneau du lendemain **12h–13h** sans description | — |

## Sensors de clôture (Python)

Trois contrôles déterministes, lancés par l'agent chef cuisinier **à la clôture** — manifestes dans
`sensors/`, scripts dans `scripts/sensors/` (bibliothèque standard uniquement) :

| Sensor | Vérifie | Sévérité |
|---|---|---|
| `repas-calendrier-agenda` | Chaque repas retenu à venir existe dans `calendar.repas` : repas **19h–20h** avec ingrédients en puces + créneau du lendemain **12h–13h** sans description | advisory |
| `historique-repas-30j` | Aucune entrée de `repas-retenus.md` plus ancienne que 30 jours glissants | **bloquant** |
| `fichiers-repas-conformes` | `repas-retenus.md`, `repas-exclus.md` et `ingredients-refuses.md` conformes (front matter, `count`, bornes, tableau, listes) | advisory |

Verdicts `✅` conforme / `⚠️` écart / `⛔` indisponible — un `⛔` n'est jamais lu comme un vert. Les
scripts ne modifient aucune donnée et n'affichent aucun secret. Tests :
`python3 -m unittest discover -s plugins/medical-assistant/sensors/tests`.

## MCP

`mcp.json` déclare un serveur MCP **`home-assistant`** au format v1.0.0
(`streamable-http`), utilisé par la skill `home-assistant-calendrier` pour créer
les évènements de repas dans le calendrier Home Assistant :

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "home-assistant": {
      "type": "streamable-http",
      "url": "${HOMEASSISTANT_URL}/api/mcp",
      "headers": {
        "Authorization": "Bearer ${HOMEASSISTANT_TOKEN}"
      }
    }
  }
}
```

Conformément à la spec v1.0.0 (§7.2.1 / §9.2), **aucun secret n'est committé** :
l'adresse et le jeton sont référencés par les variables d'environnement
`HOMEASSISTANT_URL` et `HOMEASSISTANT_TOKEN`, jamais par leurs valeurs.

## Sécurité (dépôt public)

- Aucun secret en clair n'est committé. Les accès Home Assistant sont référencés
  via des variables d'environnement documentées (`HOMEASSISTANT_URL`,
  `HOMEASSISTANT_TOKEN`), jamais leurs valeurs.
- Les données médicales manipulées par ces skills sont des **données de santé
  sensibles** : elles ne sont jamais committées dans ce dépôt public. Les skills
  décrivent **comment** traiter et archiver ces données dans l'espace privé du
  patient, pas les données elles-mêmes.
- Les analyses sont **consultatives** : aucune décision clinique n'est posée sans
  la validation d'un médecin diplômé (voir l'avertissement en tête de ce
  document).
