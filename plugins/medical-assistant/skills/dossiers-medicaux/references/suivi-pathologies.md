# Référence — Gestion du suivi des pathologies

Fichier de référence de la skill `dossiers-medicaux`. Il décrit en détail la gestion du **suivi des pathologies déclarées** d'un patient : déport, nommage, structure, lecture à la demande, archivage, ce que `synthese.md` conserve, et la procédure de nettoyage par pertinence.

**Chargement à la demande** : `SKILL.md` ne contient qu'un résumé et renvoie ici. Charger ce fichier uniquement quand c'est nécessaire — déclaration d'une pathologie, recherche d'information détaillée, mise à jour d'un `suivi.md`, raisonnement clinique sur un axe, préparation d'un export ou d'une revue de pathologie.

> ⚕️ **Consultatif — validation médicale requise.** Tous les éléments restent consultatifs ; aucun ne constitue un diagnostic définitif.

## Principe

Dès qu'une maladie/pathologie est **déclarée** pour un patient, son suivi détaillé est **déporté** dans un fichier dédié `pathologies/<slug>/suivi.md`, **source de vérité** de cette pathologie. Le dossier médical (`synthese.md`) ne conserve que les **derniers éléments pertinents / en cours** et renvoie à ce fichier. Même logique de déport que pour le laboratoire (`laboratoire/`) et les examens (`examens/`).

## Lecture à la demande

Les fichiers `pathologies/<slug>/suivi.md` ne sont **pas lus systématiquement**. Le travail courant s'appuie sur `synthese.md` (vue consolidée). On n'ouvre un `suivi.md` **que lorsque c'est nécessaire** :

- recherche d'une information détaillée sur la pathologie (historique, antériorité, traitement passé) ;
- mise à jour du suivi de cette pathologie (ajout d'une poussée, d'un traitement, clôture d'un axe) ;
- raisonnement clinique portant spécifiquement sur cet axe ;
- préparation d'un export ou d'une revue approfondie de la pathologie.

En dehors de ces cas, ne pas charger ces fichiers : s'en tenir à `synthese.md` et à ses renvois.

## Emplacement et nommage

- Chaque pathologie a son sous-répertoire sous le dossier du patient : `"$ROOT_DIRECTORY"/<patient>/pathologies/<slug-de-la-pathologie>/`.
- Le suivi détaillé vit dans `pathologies/<slug-de-la-pathologie>/suivi.md`.
  - Exemple : `pathologies/sclerose-en-plaque/suivi.md`.
- Si le répertoire n'existe pas, le créer (y compris les répertoires parents) avant d'y écrire.

### Règle du slug (`<slug-de-la-pathologie>`)

- Dérivé du nom de la pathologie, normalisé en slug sûr pour un système de fichiers : minuscules, sans accents ni caractères spéciaux, espaces et séparateurs remplacés par des tirets `-` (`[a-z0-9-]`).
  - Ex. « Sclérose en plaques » → `sclerose-en-plaque` ; « Diabète de type 2 » → `diabete-type-2`.
- Rester cohérent dans le temps pour une même pathologie (une pathologie = un seul slug, un seul répertoire).
- Indiquer le code CIM-10 quand il est disponible (dans le `suivi.md` et dans la ligne de `synthese.md`), sans l'utiliser comme nom de répertoire.

## Contenu de `suivi.md` — source de vérité

`suivi.md` est la **source de vérité** de la pathologie : il conserve l'historique complet, même les éléments anciens ou terminés (jamais effacés). Il est créé et tenu à partir du gabarit `gabarits/gabarit-suivi-pathologie.md`, **structure de référence** (Identification, Historique, Traitements, Suivi spécialisé, Éléments en cours / archivés, Points de vigilance, Questions ouvertes).

- **Archivage avant modification** : avant toute modification de `suivi.md`, archiver la copie précédente dans `pathologies/<slug>/archives/` sous `<date-du-jour>-suivi.md` (format `yyyy-MM-dd_hh-mm`), même approche que `synthese.md`.
- **Contenu clinique uniquement** (règle d'or n°2 de la skill) : aucun méta-commentaire de process (relecture, rectificatif, mise en forme, document reçu, rapport ajouté ensuite…) ; seuls les faits cliniques et leur historique y figurent.
- **Axes clos** : prose réduite au strict nécessaire (voir « Évaluation de pertinence » ci-dessous).

## Ce que `synthese.md` conserve

- Dans `synthese.md`, chaque pathologie déclarée figure dans « Problèmes actifs » (ou « Problèmes résolus » si résolue) avec **uniquement les derniers éléments pertinents / en cours** : statut actuel, dernière poussée/épisode, traitement de fond en cours, prochaine échéance notable, points de vigilance.
- Toujours renvoyer au fichier détaillé : `pathologies/<slug>/suivi.md`.
- Ne jamais recopier l'historique complet dans `synthese.md` : il reste dans `suivi.md`.
- **Axe clos** : prose réduite au maximum dans `synthese.md`, supprimée si elle devient inutile ; conservée réduite dans `suivi.md`.

## Évaluation de pertinence à chaque révision — nettoyage

À **chaque révision** du dossier (étape d'archivage comprise, voir « Mise à jour et exportation du dossier » dans `SKILL.md`) :

1. Pour chaque pathologie, relire les éléments présents dans `synthese.md` et évaluer leur **pertinence actuelle**.
2. Retirer de `synthese.md` tout élément qui n'est plus en cours ou plus pertinent, après s'être assuré qu'il est bien consigné dans `suivi.md` (le déplacer vers « Éléments archivés / historiques » si besoin).
3. **Supprimer les doublons.** Un même fait (poussée, résultat, décision, traitement) ne figure qu'une seule fois : fusionner les mentions redondantes et garder la formulation la plus récente et la plus complète.
4. **Retirer les mentions devenues obsolètes de données manquantes.** Toute mention du type « rapport manquant », « examen en attente », « document non reçu » qui a depuis été **comblée** (le rapport/examen a été ajouté ensuite) est supprimée de `synthese.md` : on ne garde pas la trace d'un manque résolu. Le détail et l'historique restent dans `suivi.md` (et dans les skills `analyse-laboratoire` / `analyse-examens` pour les résultats).
5. **Ne conserver que les derniers faits réels.** En cas de versions successives d'un même constat, garder uniquement l'état effectivement constaté le plus récent (le fait réel actuel) ; les états antérieurs ou provisoires sont retirés de la synthèse et conservés dans `suivi.md`.
6. **Axe clos → prose réduite au maximum, voire supprimée.** Dès qu'un axe est **clos** (problème résolu, poussée/épisode terminé, question ouverte comblée, pathologie en rémission ou stabilisée), réduire au maximum la prose correspondante dans `synthese.md` : la ramener à une ligne factuelle (statut + date), et la **supprimer entièrement si elle devient inutile** (déjà portée par la section « Problèmes résolus », par un `suivi.md`, ou sans valeur clinique actuelle). La prose n'est pas perdue : elle est **conservée dans le `suivi.md` de la pathologie, réduite au strict nécessaire**.
7. Ne conserver dans `synthese.md` que le **strict nécessaire** : l'état en cours et ce qui doit rester sous les yeux du clinicien.
8. L'archive horodatée de `synthese.md` (règle des 3 étapes) conserve la trace de l'état antérieur ; aucune donnée n'est perdue.

> **Distinction avec les règles d'or n°3 et n°4 :** un élément *invalidé* est retiré du dossier (sa trace vit dans l'archive) ; un problème *résolu* passe en « Problèmes résolus ». Ici, le nettoyage par pertinence déplace le **détail en cours** vers `suivi.md` tout en gardant la pathologie visible dans `synthese.md` tant qu'elle est active.
