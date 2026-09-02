# Sensor `diagram-validity` — validité de diagramme *(complémentaire)*

Check déterministe déclenché à l'**écriture d'un diagramme généré en code** : vérifie que la **syntaxe** parse sans erreur. Cohérent avec l'obligation « générer les diagrammes en code et en valider la syntaxe avant écriture ». **Advisory**.

```yaml
id: diagram-validity
type: sensor
nature: advisory
priority: complementaire
origine: ALI-188
triggers:
  - "**/*.md"          # blocs ```mermaid``` / ```plantuml``` intégrés
  - "**/*.puml"        # PlantUML
  - "**/*.dsl"         # Structurizr DSL
checks:
  syntaxe:
    mermaid: "parse sans erreur (mermaid)"
    plantuml: "parse sans erreur (plantuml)"
    structurizr: "parse sans erreur (structurizr dsl)"
output: "erreur de parsing localisée (advisory) ; écriture possible, écart tracé"
```

## Sortie (piste d'audit)

Verdicts : `✅` valide · `⚠️` erreur de parsing · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor diagram-validity — <fichier / bloc>   (source : core/sensors/sensors/diagram-validity.md @ <commit>)
- verdict : ✅ syntaxe valide (<moteur>) | ⚠️ erreur de parsing : <localisation / message> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : l'écriture reste possible même sur erreur de syntaxe, mais l'écart est tracé sur l'issue pour correction. **Parsing statique uniquement** (SG-4) : jamais de rendu réseau, jamais d'exécution de code ou de directive embarquée dans le diagramme (`!include` distant, `getResource`, scripts) ; le contenu du diagramme est traité comme donnée non fiable.
