# Agents — temporaires (à validater avant migration)

Définitions **conformes** (front-matter YAML + corps Markdown, même format que [`core/agents/`](../../core/agents/) et [`homelab/agents/`](../../homelab/agents/)) des agents du workspace encore dans `temporaire/agents/`, en attente de validation / migration vers leur emplacement définitif.

## Agents présents

| Agent | Fichier | Objet |
|---|---|---|
| Hector - Leader Analyses Financières | [hector-leader-analyses-financieres.md](hector-leader-analyses-financieres.md) | Leader de l'équipe d'analyse financière : coordonne Leo, Nestor et Victor, synthétise et produit des rapports pour investisseur intermédiaire. |
| Leo - Data Provider | [leo-data-provider.md](leo-data-provider.md) | Collecte les données de marché et fondamentales des titres canadiens (sources gratuites), livrables `<TICKER>.json` + `synthese.json`. |
| Nestor - Analyse Technique | [nestor-analyse-technique.md](nestor-analyse-technique.md) | Expert en analyse technique : indicateurs (MM, RSI, MACD, Bollinger), tendances 1J/1S/1M, risques et avis. |
| Victor - Analyse Fondamentale | [victor-analyse-fondamentale.md](victor-analyse-fondamentale.md) | Expert en analyse fondamentale : news, tendances marché et géopolitiques, santé de l'entreprise, risques et points positifs 1J/1S/1M. |
| Mika | [mika.md](mika.md) | Chief of Staff du workspace : objectifs → issues, coordination des agents, construction de workflows réutilisables. |
| Eric - Chef de la clinique Biboumed | [eric-chef-clinique-biboumed.md](eric-chef-clinique-biboumed.md) | Médecin généraliste, chef de la clinique médicale : analyse des dossiers médicaux, recherche et réponses aux patients. |

## Notes

- Les agents conformés migrés vers leur emplacement définitif (Homelab, core, notifications) ne sont **plus** dupliqués ici : leur définition unique vit dans [`core/agents/`](../../core/agents/) ou [`homelab/agents/`](../../homelab/agents/).
- Aucun secret (clés d'environnement, credentials) n'est exporté dans ces définitions.
