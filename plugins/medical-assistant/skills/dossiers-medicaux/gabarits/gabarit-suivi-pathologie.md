<!--
Gabarit de SUIVI D'UNE PATHOLOGIE déclarée.
Ce gabarit normalise le fichier `pathologies/<slug-de-la-pathologie>/suivi.md` d'un patient.
`suivi.md` est la SOURCE DE VÉRITÉ de la pathologie : il conserve l'historique complet (jamais effacé).
`synthese.md` ne reprend QUE les derniers éléments pertinents / en cours et renvoie à ce fichier.

Conventions (voir la skill `dossiers-medicaux`, section « Pathologies déclarées — suivi déporté ») :
- Slug du répertoire : minuscules, sans accents ni caractères spéciaux, tirets `-` (`[a-z0-9-]`).
  Ex. « Sclérose en plaques » → `sclerose-en-plaque` ; « Diabète de type 2 » → `diabete-type-2`.
- CONTENU CLINIQUE UNIQUEMENT : aucun méta-commentaire de process (relecture, rectificatif, mise en
  forme, document reçu, rapport ajouté ensuite, synthèse mise à jour…). La trace de ces opérations
  vit dans les archives horodatées, pas dans le contenu.
- Avant toute modification, archiver la copie précédente dans `pathologies/<slug>/archives/` sous
  `<date-du-jour>-suivi.md` (format `yyyy-MM-dd_hh-mm`).
- Lecture À LA DEMANDE : ce fichier n'est ouvert que lorsque c'est nécessaire (recherche
  d'information, mise à jour du suivi, raisonnement clinique sur l'axe, préparation d'export).
- Axe clos : prose réduite au strict nécessaire ici ; dans `synthese.md`, réduite au maximum voire
  supprimée si elle devient inutile.
- Ne jamais inventer de données : laisser vide et signaler la lacune.
AVERTISSEMENT : contenu consultatif — la validation d'un médecin diplômé est requise.
-->

# Suivi de pathologie — [Nom de la pathologie]

> ⚕️ **Consultatif — validation médicale requise.** Tous les éléments de ce fichier sont consultatifs ; aucun ne constitue un diagnostic définitif. L'incertitude est signalée explicitement.

## Identification

<!-- Métadonnées de la pathologie. Le slug sert de nom de répertoire ; le code CIM-10 n'est pas utilisé comme nom de répertoire. -->

| Champ                   | Valeur                                      |
| ----------------------- | ------------------------------------------- |
| **Pathologie**          | [nom clinique de la pathologie]             |
| **Slug (répertoire)**   | `[slug-de-la-pathologie]`                   |
| **Code CIM-10**         | [si disponible]                             |
| **Date de déclaration** | yyyy-MM-dd                                   |
| **Statut actuel**       | [actif / en rémission / stabilisé / résolu] |
| **Médecin référent**    | [spécialiste / service suivant la pathologie] |

---

## Historique

<!--
Événements datés, du plus ancien au plus récent : diagnostic, poussées/épisodes, hospitalisations,
décisions thérapeutiques, changements de statut. Faits cliniques uniquement.
-->

| Date (yyyy-MM-dd) | Événement                         | Détail clinique                       |
| ----------------- | --------------------------------- | ------------------------------------- |
| [date]            | [diagnostic / poussée / décision] | [description factuelle]               |
|                   |                                   |                                       |

---

## Traitements (fond et symptomatiques)

<!-- Nom générique en premier, marque entre parenthèses. Indiquer la période, la réponse et les effets indésirables. Les traitements arrêtés restent listés (période close). -->

| Traitement (générique / marque) | Type (fond / sympt.) | Dose      | Période (début → fin)   | Réponse / Effets indésirables |
| ------------------------------- | -------------------- | --------- | ----------------------- | ----------------------------- |
| [générique (marque)]            | [fond / sympt.]      | [dose]    | [yyyy-MM → yyyy-MM / en cours] | [réponse, effets]        |
|                                 |                      |           |                         |                               |

---

## Suivi spécialisé

<!-- Spécialiste(s), rythme de suivi, prochaines échéances (consultations, examens de contrôle). -->

| Spécialiste / Service | Rythme de suivi | Dernière évaluation | Prochaine échéance |
| --------------------- | --------------- | ------------------- | ------------------ |
| [spécialiste]         | [rythme]        | [yyyy-MM-dd]        | [yyyy-MM-dd]       |
|                       |                 |                     |                    |

---

## Éléments en cours / pertinents (reflétés dans `synthese.md`)

<!--
Ce qui est ACTUELLEMENT reporté dans `synthese.md` pour cette pathologie : doit rester synchronisé.
Statut, dernière poussée/épisode, traitement de fond en cours, prochaine échéance, points de vigilance.
-->

| Élément en cours        | Détail                        | Reporté dans `synthese.md` ? |
| ----------------------- | ----------------------------- | ---------------------------- |
| [statut / épisode / tt] | [description courte]          | Oui / Non                    |
|                         |                               |                              |

---

## Éléments archivés / historiques (hors `synthese.md`)

<!--
Éléments qui ne sont plus en cours, conservés ici pour l'historique (jamais effacés).
Axes clos : prose réduite au strict nécessaire.
Ne PAS confondre avec un élément INVALIDÉ (retiré du dossier, trace dans l'archive horodatée).
-->

| Date de clôture | Élément / axe clos    | Résultat / résolution (court)       |
| --------------- | --------------------- | ----------------------------------- |
| [yyyy-MM]       | [axe clos]            | [résolution courte]                 |
|                 |                       |                                     |

---

## Points de vigilance

<!-- Alertes cliniques actives liées à cette pathologie. Signaler les valeurs critiques : 🚨 CRITIQUE : [élément] nécessite une revue urgente. -->

| Point de vigilance | Niveau (info / 🚨) | Source (labo / examen / clinique) | Date       |
| ------------------ | ------------------ | --------------------------------- | ---------- |
| [élément]          | [info / 🚨]        | [source]                          | [yyyy-MM-dd] |
|                    |                    |                                   |            |

> Détail des analyses : `laboratoire/synthese-bilans.md` (skill `analyse-laboratoire`). Détail des examens : `examens/synthese-examens.md` (skill `analyse-examens`).

---

## Questions ouvertes

<!-- Lacunes, points incertains, examens de contrôle à prévoir pour cette pathologie. -->

| #   | Question ouverte / Lacune            |
| --- | ------------------------------------ |
| 1   | [lacune / point incertain]           |
| 2   |                                      |

---

*⚕️ Consultatif — validation médicale requise. — `pathologies/[slug-de-la-pathologie]/suivi.md` — Source de vérité de la pathologie.*
