# Guide d'utilisation — Workflow Matching Appels d'Offres ↔ CV

Ce guide explique **comment utiliser au quotidien** le workflow de matching entre appels d'offres (AO) et CV de collaborateurs du dépôt `homelab-portfolio`, orchestré par des agents Multica. Il s'adresse aux humains qui pilotent une demande de matching ; il ne remplace pas la source technique du workflow (`matching-cv-ao/common/conductor.md` et `matching-cv-ao/common/protocols/`), qu'il vulgarise.

---

## 1. Ce qu'est ce workflow

Le workflow transforme un **appel d'offres (PDF)** reçu d'un client en un **classement de profils de collaborateurs** adaptés, avec un **score pondéré**, puis en une **grille d'évaluation client** remplie. Il repose sur trois principes :

- **Orchestration A2A (agent-to-agent)** : un agent **coordinateur** découpe le travail et délègue à des agents spécialisés (analyse de l'AO, extraction des CV, matching) ; il ne produit pas lui-même les livrables.
- **Validation humaine granulaire** : vous validez **chaque profil séparément** — rien n'avance sans votre accord.
- **Tout est tracé sur l'issue Multica** : analyses, décisions, délégations et validations vivent dans les commentaires de l'issue (piste d'audit unique).

> Le workflow **s'adapte à la complexité de l'AO** : un AO simple reçoit un traitement léger (scope *express*), un AO multi-profils le traitement complet (*complex*) — voir `matching-cv-ao/common/protocols/scopes-and-axes.md` et `matching-cv-ao/common/scopes/`.

---

## 2. Choisir le bon workflow (règle de routage)

Le dépôt porte **trois workflows totalement indépendants**. Avant tout, la demande est classée dans **l'un ou l'autre** — jamais plusieurs :

| La demande porte sur… | Workflow | Coordinateur |
| --- | --- | --- |
| Architecture de solution : documentation (DAS), décisions, diagrammes, choix techno, intégration, cybersécurité, AWS, OpenSpec | **Architecture** (guide `docs/guide-utilisation-workflow-architecture.md`) | Architecture Solution & Intégration |
| Homelab : stack Docker/Proxmox, `docker-compose`, Terraform de stack, n8n, Home Assistant, Vault, Traefik | **Homelab** | Tech Lead |
| **Matching AO ↔ CV** : analyse d'un PDF d'appel d'offres, extraction de profils recherchés, croisement avec les CV des collaborateurs, scoring, remplissage d'une grille d'évaluation client | **Matching AO ↔ CV** (ce guide) | **Coordinateur Matching** |

En cas de doute, le coordinateur **vous demande de trancher** avant d'engager quoi que ce soit.

---

## 3. Comment soumettre une demande

1. **Créer une issue Multica** décrivant l'appel d'offres reçu (client, objet, échéance), et **attacher le PDF de l'AO** en pièce jointe.
2. **Fournir les CV sources** (PDF, DOCX) des collaborateurs à analyser **en pièces jointes de l'issue** : c'est ainsi qu'ils sont transmis au Gestionnaire CV. Ils sont analysés puis **supprimés** (non conservés).
3. **Mentionner le Coordinateur Matching** (`[@Coordinateur Matching](mention://agent/<uuid>)`) sur l'issue — ou l'assigner à l'agent Coordinateur.
4. **Prévoir la grille d'évaluation client** (Markdown) lorsque le workflow la demandera — elle vous sera réclamée, jamais inventée.
5. Toute la conversation reste **sur l'issue** : c'est là que vous suivez l'avancement et rendez vos décisions.

> **Une grille d'évaluation n'est jamais inventée** : si le workflow en a besoin et qu'elle est absente, le coordinateur vous la **demande** et **attend** votre réponse (halt-and-ask).

---

## 4. Ce qui se passe ensuite

| # | Étape | Ce qui s'y passe | Gate humain |
| --- | --- | --- | --- |
| 1 | **Réception & vérification** | Vérification de la présence du PDF d'AO, de la grille, de l'accès aux CV | Non (bootstrap déterministe) |
| 2 | **Analyse de l'AO** | L'Analyste RFP parse le PDF, extrait les exigences et les profils recherchés → **résumé Markdown** | Léger (approbation du résumé) |
| 3 | **Chargement & extraction des CV** | Le Gestionnaire CV récupère les CV joints à l'issue, produit les profils structurés, puis supprime la copie de travail | Non |
| 4 | **Matching & scoring** | Le Matcher croise profils ↔ exigences et calcule le **score pondéré** → **classement** | Advisory (commentaires) |
| 5 | **Validation granulaire** | Présentation de **chaque profil séparément** (Keep/Modify/Redo) | **Granulaire** |
| 6 | **Remplissage de la grille** | Remplissage de la grille d'évaluation client (fournie par l'humain, à la demande) | Granulaire |
| 7 | **Mise à jour des CV** *(optionnel)* | Mise à jour des CV sur votre demande | Explicite |
| 8 | **Clôture & livraison** | Livraison finale des résultats | **Explicite** |

---

## 5. Comment vous validez : la boucle Keep / Modify / Redo

À chaque point de validation, le coordinateur présente **chaque profil / élément séparément** (le résultat, sa justification, les points forts et les écarts). Pour chacun, vous répondez :

- **✅ Keep** — l'élément est validé, on avance.
- **💬 Modify** — vous formulez un ajustement ; le coordinateur ajuste **cet élément** et le re-présente.
- **❌ Redo** — vous rejetez ; le coordinateur propose une alternative pour **cet élément**.

Le coordinateur **ne fusionne jamais** les profils en un « tout ou rien », et n'avance jamais sur un profil non validé.

---

## 6. Qui fait quoi (rôles A2A)

| Fonction | Rôle dans le workflow |
| --- | --- |
| **Coordinateur Matching** | Orchestre le flux, délégué, contrôle, sollicite vos validations, traduit les résultats JSON en Markdown |
| **Analyste RFP** | Analyse l'AO (PDF), extrait exigences et profils recherchés |
| **Gestionnaire CV** | Lit et met à jour les CV des collaborateurs |
| **Matcher Profils** | Croise profils ↔ exigences, calcule le **score pondéré**, classe les profils |

La délégation se fait par **mention** sur l'issue ; l'agent sollicité répond sur la même issue.

---

## 7. Où sont stockés les documents

| Élément | Emplacement |
| --- | --- |
| CV sources (PDF, DOCX) | **Pièces jointes de l'issue** — analysés puis **supprimés** (non conservés) |
| Anciennes fiches d'analyse Markdown | `/nfs/workspace/expertise-architecture/<nom-prenom>/cv/archives/` |
| Fiche d'analyse Markdown courante + JSON versionnés | Racine de `/nfs/workspace/expertise-architecture/<nom-prenom>/cv/` |
| Résumés AO | `/nfs/workspace/expertise-architecture/ao/<client>/<titre-ao>/` |
| Grille d'évaluation | Fournie par l'humain — **jamais inventée** |

Ces chemins sont créés **si absents** par l'Analyste RFP, toujours au bon endroit (client = nom du client, titre-ao = slug du titre).

> **CV sources fournis dans l'issue** : joignez les CV des collaborateurs (PDF, DOCX) **en pièces jointes de
> l'issue**. À chaque analyse, le Gestionnaire CV les récupère, produit une fiche Markdown datée **du jour** à la
> racine de `cv/` (les anciennes fiches sont déplacées dans `cv/archives/`) et un JSON d'analyse **versionné**
> (`<nom>-<prenom>-<AAAA-MM-JJ>.json`), **puis supprime la copie de travail** — **les originaux ne sont pas
> conservés** (leur nom est journalisé sur l'issue avant suppression, pour l'audit). Seule la **dernière version
> JSON** est croisée avec un AO ; le fichier retenu et les versions écartées sont journalisés sur l'issue.

---

## 8. Communication et principes

- **Agent ↔ Agent** : JSON uniquement.
- **Agent ↔ Humain** : Markdown uniquement.
- **Comportement « jamais inventer la grille »** : toute grille d'évaluation est fournie par l'humain à chaque fois. En cas d'absence, **halt-and-ask**.
- **Piste d'audit** : chaque étape et décision est tracée sur l'issue.
- **Aucun secret** dans les livrables, commentaires ou notifications.

---

## 9. Scoring pondéré

Le **Matcher Profils** calcule le score pondéré (immuable — seul un changement validé par l'humain peut le modifier) :

| Critère | Poids |
| --- | --- |
| Compétences techniques | 50% |
| Expérience en projets | 35% |
| Études | 10% |
| Disponibilité | 5% |

---

## 10. En résumé — le parcours type

1. Vous **créez l'issue**, **attachez le PDF d'AO** et **mentionnez le Coordinateur Matching**.
2. Le coordinateur **vérifie** les prérequis (PDF, grille si connue, accès CV) — vous fournissez ce qui manque.
3. **Analyse de l'AO** → résumé Markdown → vous **approuvez**.
4. **Chargement des CV, matching, scoring** → classement → vous **commentez**.
5. **Validation granulaire** des profils (Keep/Modify/Redo) — profil par profil.
6. **Remplissage de la grille client** (vous la fournissez à la demande) → **mise à jour des CV** si demandée → **clôture** sous votre validation explicite.

---

*Sources techniques : `matching-cv-ao/common/conductor.md` (instructions du coordinateur), `matching-cv-ao/common/stages/` (fiches de stage), `matching-cv-ao/common/protocols/` (gouvernance & sécurité, reviewer, scopes & axes, définition/protocole de stage), `matching-cv-ao/common/scopes/`, `matching-cv-ao/common/sensors/`, `matching-cv-ao/agents/`. Règle de routage : `AGENTS.md`.*
