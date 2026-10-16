---
doc_id: das-16-questions-decisions
theme: Questions en attente et décisions attendues
domaine: [affaires, solution, logiciel, data, infrastructure, securite, transverse]
sujets:
  - Invariants hérités
  - Questions en attente
  - Logiciel
  - Sécurité
  - Données
  - Infrastructure
  - Décisions attendues
  - Logiciel
  - Sécurité
  - Données
  - Infrastructure
types_presentation: [technique, entreprise]
sensibilite: interne
togaf_layer: null
ordre_presentation: 16
---
<!--
FICHIER « DERNIER DE LA LISTE ». Ce gabarit regroupe, dans un **seul et même fichier**, les
**questions en attente** et les **décisions attendues** du projet. Il porte **toujours le
numéro le plus élevé** de la DAS : si un nouveau fichier est ajouté au DAS avec un numéro
supérieur, ce fichier **doit être renommé** pour reprendre le numéro le plus élevé et rester
le dernier de la liste.

Deux grandes sections obligatoires :
  1. Questions en attente — points à clarifier, en attente d'une réponse d'une partie prenante.
  2. Décisions attendues — choix structurants à trancher (candidats ADR), en attente d'arbitrage.

Une section de cadrage **« Invariants hérités »** précède ces deux sections : elle rappelle les
invariants non contournables hérités des couches supérieures (gouvernance, plancher sécurité,
règles de niveau supérieur, ADR acceptés) qui **bornent** les questions et les décisions. Aucune
question ni décision de ce fichier ne peut affaiblir un invariant hérité ; en cas de tension, c'est
l'invariant qui prime et l'arbitrage humain est requis.

Chaque grande section est déclinée en **sous-sections par domaine** : Logiciel, Sécurité,
Données, Infrastructure. Ajouter une sous-section de domaine supplémentaire (ex. Affaires,
Transverse) uniquement si le projet le requiert, en conservant l'ordre Logiciel → Sécurité →
Données → Infrastructure en tête.

Conventions :
  - Identifiants codés : invariants hérités `INV-001`, questions `Q-001`, décisions `DEC-001`
    (numérotation séquentielle, continue, globale au fichier par type, indépendante du domaine).
  - Une question tranchée ou une décision prise sort de ce fichier : la question est close
    (statut `Résolue` avec renvoi), la décision devient un ADR (`decisions/ADR-NNN-…`) et est
    référencée en colonne « Décision / lien ».
  - Statuts suggérés : question → `Ouverte`, `En attente`, `Résolue` ; décision → `À trancher`,
    `En discussion`, `Tranchée` (ADR). Toute décision tranchée pointe vers son ADR.
  - Garder la cohérence avec la matrice de suivi du `02-objectifs.md` et l'historique du `001`.
-->
## Invariants hérités

<!--
Rappeler ici les **invariants non contournables hérités** des couches supérieures qui s'imposent
au projet et **bornent** les questions en attente et les décisions attendues : invariants de
**gouvernance** (validation humaine granulaire, décision structurante tracée en ADR, piste
d'audit), **plancher de sécurité** (contrôle OWASP/STRIDE systématique, aucun secret, aucune
action à impact sans validation humaine, rollback validé avant action destructive), **règles de
niveau supérieur** (workspace / organisation) et **ADR déjà acceptés** du projet. Source de
référence : `core/common/protocols/governance-security.md` (§ « Invariants non contournables »)
et le registre des décisions (`decisions/`).

Règle : **aucune** question ni décision de ce fichier ne peut affaiblir, restreindre ou
conditionner un invariant hérité. En cas de tension entre une décision attendue et un invariant,
l'invariant **prime** et la situation relève de l'**arbitrage humain**. Chaque invariant porte un
identifiant `INV-NNN` et renvoie à sa source (protocole, règle de couche supérieure, ADR).
-->

| ID | Invariant hérité | Origine (couche / source) | Référence | Portée (domaines) |
| --- | --- | --- | --- | --- |
| INV-001 | Validation humaine granulaire : chaque choix validé / rejeté séparément | Gouvernance | `governance-security.md` § Invariants non contournables | Tous |
| INV-002 | Décision structurante tracée dans le registre de décisions (ADR) | Gouvernance | `governance-security.md` ; `decisions/` | Tous |
| INV-003 | Contrôle de sécurité minimal OWASP / STRIDE, systématique ; aucun secret dans les livrables | Plancher sécurité | `governance-security.md` | Sécurité, Tous |
| INV-004 | Aucune action à impact sans validation humaine ; rollback validé avant action destructive | Gouvernance / sécurité | `governance-security.md` | Infrastructure, Tous |

## Questions en attente

<!--
Lister les **questions ouvertes** nécessitant une réponse d'une partie prenante (métier,
sécurité, données, exploitation, fournisseur, etc.) avant de pouvoir avancer ou trancher.
Une question close est marquée `Résolue` avec le renvoi vers la réponse (section du DAS, ADR,
comité). Chaque question porte un identifiant `Q-NNN` unique et continu dans tout le fichier.
-->

### Logiciel

<!-- Questions ouvertes relevant de l'architecture logicielle (composants, intégration, API, séquences, dépendances applicatives). -->

| ID | Question | Posée par | Destinataire attendu | Statut | Date | Décision / lien |
| --- | --- | --- | --- | --- | --- | --- |
| Q-001 | <Formuler la question logicielle en attente> | <auteur> | <partie prenante> | Ouverte | AAAA-MM-JJ | — |

### Sécurité

<!-- Questions ouvertes relevant de la sécurité (GIA, conformité, chiffrement, modélisation des menaces, exigences réglementaires). -->

| ID | Question | Posée par | Destinataire attendu | Statut | Date | Décision / lien |
| --- | --- | --- | --- | --- | --- | --- |
| Q-002 | <Formuler la question de sécurité en attente> | <auteur> | <partie prenante> | Ouverte | AAAA-MM-JJ | — |

### Données

<!-- Questions ouvertes relevant de l'architecture de données (modèles, flux, cycle de vie, gouvernance, qualité, volumétrie). -->

| ID | Question | Posée par | Destinataire attendu | Statut | Date | Décision / lien |
| --- | --- | --- | --- | --- | --- | --- |
| Q-003 | <Formuler la question de données en attente> | <auteur> | <partie prenante> | Ouverte | AAAA-MM-JJ | — |

### Infrastructure

<!-- Questions ouvertes relevant de l'infrastructure (réseau, calcul, stockage, déploiement, DevSecOps, résilience). -->

| ID | Question | Posée par | Destinataire attendu | Statut | Date | Décision / lien |
| --- | --- | --- | --- | --- | --- | --- |
| Q-004 | <Formuler la question d'infrastructure en attente> | <auteur> | <partie prenante> | Ouverte | AAAA-MM-JJ | — |

## Décisions attendues

<!--
Lister les **décisions structurantes à trancher** (candidats ADR) en attente d'arbitrage :
choix de solution, de technologie, de patron, de structure d'intégration. Une décision tranchée
devient un **ADR** (`decisions/ADR-NNN-…`, voir la skill `create-architecture-decision-record`)
et est référencée en colonne « Décision / lien » avec le statut `Tranchée`. Chaque décision
porte un identifiant `DEC-NNN` unique et continu dans tout le fichier.
-->

### Logiciel

<!-- Décisions logicielles à trancher (framework, découpage en composants, patron d'intégration, choix d'API/protocole). -->

| ID | Décision à trancher | Options envisagées | Impact | Décideur attendu | Statut | Date | ADR / lien |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | <Décrire la décision logicielle attendue> | <option A ; option B> | <impact> | <décideur> | À trancher | AAAA-MM-JJ | — |

### Sécurité

<!-- Décisions de sécurité à trancher (GIA, chiffrement, contrôles, conformité, zonage réseau sécurité). -->

| ID | Décision à trancher | Options envisagées | Impact | Décideur attendu | Statut | Date | ADR / lien |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-002 | <Décrire la décision de sécurité attendue> | <option A ; option B> | <impact> | <décideur> | À trancher | AAAA-MM-JJ | — |

### Données

<!-- Décisions de données à trancher (choix de stockage, modèle, stratégie de persistance, gouvernance, rétention). -->

| ID | Décision à trancher | Options envisagées | Impact | Décideur attendu | Statut | Date | ADR / lien |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-003 | <Décrire la décision de données attendue> | <option A ; option B> | <impact> | <décideur> | À trancher | AAAA-MM-JJ | — |

### Infrastructure

<!-- Décisions d'infrastructure à trancher (plateforme, réseau, calcul, stockage, modèle de déploiement, DevSecOps). -->

| ID | Décision à trancher | Options envisagées | Impact | Décideur attendu | Statut | Date | ADR / lien |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-004 | <Décrire la décision d'infrastructure attendue> | <option A ; option B> | <impact> | <décideur> | À trancher | AAAA-MM-JJ | — |
