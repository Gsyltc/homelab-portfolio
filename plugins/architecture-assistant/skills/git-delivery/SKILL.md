---
name: git-delivery
description: >
    Capacité technique de mise à disposition par Git : commiter des fichiers et ouvrir une Pull Request vers une branche cible donnée, via `gh` (GitHub) ou l'outil adapté au type de dépôt (GitLab `glab`, Bitbucket). Utiliser lorsqu'un commit + PR est explicitement demandé et que la branche cible est déjà fournie. Déclencheurs : « commit + PR », « ouvrir une PR », « pousser la branche d'issue », « mise à disposition par Git ».
---

# Mise à disposition par Git (commit + PR)

Cette skill fournit **uniquement la capacité technique** d'exécuter un commit et une Pull Request. Elle **ne porte aucune logique de workflow** : la décision de faire la PR, la demande d'accord humain et la résolution de la branche cible sont décidées en amont par le coordinateur (voir [`core/common/stages/construction/delivery-handoff.md`](../../../../core/common/stages/construction/delivery-handoff.md)). Tu reçois une **tâche déjà cadrée** : les fichiers à commiter, la branche d'issue source et la **branche cible résolue**. Tu exécutes, tu remontes le résultat.

## Prérequis fournis par le coordinateur

Avant de commencer, tu dois disposer de ces éléments (le coordinateur les fournit ; **ne les devine jamais**) :

- **Branche source** : la branche d'issue `feature/<id-issue>-<slug-court>` créée en Initialization.
- **Branche cible** : déjà résolue par le coordinateur (description du projet → README → `integration`). **Tu ne résous pas la branche cible toi-même.**
- **Périmètre des fichiers** : tous les fichiers liés à la tâche **et à l'ensemble de ses sous-tâches**.
- **Accord humain explicite** : confirmé en amont. Sans cet accord transmis, **ne commite pas et n'ouvre pas de PR** — signale-le sur l'issue et arrête-toi.
- **Séquencement — seulement après la réalisation ET la revue** : tu n'archives et ne commites **jamais** avant que les livrables aient été **réalisés** puis **revus** (revue de cohérence, puis revue de sécurité) et **validés par l'humain**. La mise à disposition est un acte de **fin de cycle** ; elle ne porte que sur des livrables produits, revus et validés.

## Détection du type de dépôt

Déterminer l'outil adapté avant d'agir :

```bash
git remote get-url origin
```

- URL `github.com` → utiliser **`gh`** (GitHub CLI).
- URL `gitlab` → utiliser **`glab`** (GitLab CLI) ou l'API MR.
- URL `bitbucket.org` → utiliser l'intégration Bitbucket (API PR / pipeline du dépôt).

Si l'outil adapté n'est pas disponible, signaler le blocage sur l'issue plutôt que de contourner.

## Procédure — GitHub (`gh`)

```bash
# 1. Se placer sur la branche d'issue source (fournie)
git checkout "<branche-source>"

# 2. Vérifier l'intégrité des fichiers du périmètre (existence, contenu non vide)
git status

# 3. Stager explicitement les fichiers de la tâche + sous-tâches (éviter `git add .`
#    si des fichiers hors périmètre sont présents)
git add <fichiers-de-la-tache-et-sous-taches>

# 4. Commiter avec un message clair
git commit -m "<type>(<scope>): <résumé de la mise à disposition>"

# 5. Pousser la branche source avec suivi distant
git push -u origin "<branche-source>"

# 6. Ouvrir la PR vers la branche cible fournie
gh pr create \
  --base "<branche-cible>" \
  --head "<branche-source>" \
  --title "<titre concis>" \
  --body "<résumé des livrables mis à disposition>"
```

## Procédure — autres dépôts

- **GitLab** : `glab mr create --source-branch <source> --target-branch <cible> --title "..." --description "..."` après `git push -u origin <source>`.
- **Bitbucket** : pousser la branche puis créer la PR via l'intégration/API du dépôt vers la branche cible fournie.

## Règles

- **Aucun commit, push ou PR sans l'accord humain explicite** transmis par le coordinateur.
- **Ne jamais résoudre la branche cible** ni décider s'il faut faire la PR : ces décisions appartiennent au workflow (coordinateur).
- **Ne pas pousser sur `main`/`master`** ni fusionner la PR : la PR est le livrable, la fusion reste humaine.
- Préférer un stage explicite des fichiers du périmètre à `git add .` pour ne pas emporter de fichiers hors tâche.
- Ne jamais inclure de secret dans un commit (clé, `.env`, token).
- **Ne pas attendre la CI** : une fois la PR ouverte, remonter le lien ; la CI/le gate de fusion ne sont pas des critères d'acceptation de ta tâche.

## Remontée

Après exécution, remonter sur l'issue : le **lien de la PR**, la branche source, la branche cible, la liste des fichiers commités et le statut. En cas d'anomalie (outil manquant, accord non transmis, conflit), signaler le blocage sur l'issue sans contourner.
