# Scopes Homelab et axes Depth / Stratégie de vérification

---
auteurs: Mika (agent)
accepté par : Sylvain G.
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

Le workflow `docs/homelab-workflow.md` — piloté par le Tech Lead Homelab — énonçait le principe « le workflow s'adapte au travail », mais ne l'outillait qu'avec une **grille binaire** « traitement allégé vs traitement complet ». Cette grille est un premier pas vers les scopes, mais reste **à deux niveaux** : pas de routage nommé, pas d'auto-détection par mots-clés, pas de matrice stage × scope, et aucune séparation entre le **détail des artefacts** produits et l'**intensité de la vérification** (QA Docker).

L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-200, cadrage ALI-201, ADR de cadrage 0013) a validé une refonte complète en miroir de `core/`. Ce Stage 2 (ALI-202) traite le plus gros gain d'alignement : transformer la grille binaire en scopes nommés et introduire les deux axes.

Le modèle `core/` (ADR-0003, ADR-0010) définit 8 scopes génériques (`standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`) et deux axes (Depth / vérification), avec un fichier par scope sous `core/scopes/`. Le contexte Homelab est différent : livrables docker-compose Swarm / Terraform / n8n / Home Assistant, pas de documentation d'architecture générique. Les scopes doivent être **spécifiques au Homelab**.

Le modèle de scopes et la nomenclature ont été soumis à l'humain sur ALI-201 (§4 du cadrage) et validés (« 1. ok, 2. ok »).

## Décision

**Formaliser un mécanisme de scopes Homelab et deux axes d'exécution indépendants**, en miroir de `core/scopes/` (forme déclarative, un fichier par scope), dans le respect des garde-fous absolus du workflow Homelab.

**Table de 7 scopes** (validée sur ALI-201) — noms conservés du cadrage :

- `stack-update` *(défaut)* — modification d'une stack existante ;
- `new-stack` — création complète d'une nouvelle stack ;
- `config-change` — modification d'une variable existante sans impact sécurité (héritier de l'ancien « allégé ») ;
- `security-patch` — tout impact sécurité (auth, réseau, exposition, secrets, hardening, permissions, Traefik) ;
- `infra-terraform` — infra Terraform / Proxmox ;
- `n8n` — branche autonome, délégation immédiate (règle absolue §1.1) ;
- `home-assistant` — branche autonome.

**Scope par défaut** : `stack-update`, en l'absence de mot-clé détecté — aucune régression par rapport au parcours Homelab historique.

**Deux axes indépendants**, distincts et pilotables séparément :

- **Depth** (détail des artefacts) : `minimal` / `standard` / `comprehensive`.
- **Stratégie de vérification** (intensité du QA Docker) : `advisory` (syntaxe seule) / `standard` (hardening standard + Swarm + Traefik) / `renforcé` (audit sécurité approfondi : secrets `_FILE`, exposition, permissions, absence de `${SNI}`, durcissement).

Valeurs par défaut par scope portées dans chaque fichier `homelab/scopes/<name>.md` (source d'identité) : `config-change` = minimal/advisory ; `stack-update` / `infra-terraform` / `n8n` / `home-assistant` = standard/standard ; `new-stack` / `security-patch` = comprehensive/renforcé.

**Auto-détection & désambiguïsation** : détection par mots-clés FR / EN (champ `keywords:`), confirmation explicite avant démarrage, règle « le niveau le plus élevé l'emporte » (héritée de la règle de départage), ordre : `n8n` = `home-assistant` > `security-patch` > `new-stack` > `infra-terraform` > `stack-update` > `config-change`. **Le doute ne bascule jamais vers `config-change`.**

**Structure des artefacts** : `homelab/scopes/` (miroir de `core/scopes/`) — un `README.md` (contrat, schéma de front-matter, axes, garde-fous, désambiguïsation) + un fichier par scope. La **matrice scope × phase** (vue lisible) est ajoutée à la section « Scopes et axes d'exécution » de `docs/homelab-workflow.md`, **remplaçant** la grille binaire. L'appartenance sera transposée sur le champ `scopes:` des fiches de stage au Stage 7.

**Garde-fous absolus préservés (aucun scope ne les désactive)** :

- **Règle absolue n8n (§1.1)** : le scope `n8n` déclenche la délégation immédiate à l'Expert N8n, pas même l'analyse par le Tech Lead.
- **Sélection automatique du type d'authentification (§1.4)** (`oidc → saml → ldap → forwardauth → local`) inchangée ; en cas de doute → humain.
- **Validation humaine granulaire** avant toute action à impact ; **Terraform ne déploie jamais** ; **aucun secret en clair** ; **jamais `${SNI}`** en Terraform ; **un seul traitement par stack** (verrou `active_step`).
- Sur `security-patch` / `new-stack` : `depth` ≥ `standard` et `verification` ≥ `renforcé` non abaissables ; auto-détection = plancher (monter oui, descendre sans trace non).

**Tooling amont écarté** (cohérent avec le cadrage) : pas de `scope-grid.json`, pas de moteur TypeScript ; l'exécution passe par Multica (mentions UUID, `trigger_outcomes`, statut d'issue, verrou metadata, piste d'audit). On adopte la seule forme déclarative.

## Conséquences

### Positives

- **POS-001** : Adaptativité réellement outillée — routage déterministe et auditable par scope, à la place d'une grille binaire subjective.
- **POS-002** : Depth et vérification pilotables séparément (ex. `security-patch` = produire peu, vérifier fort).
- **POS-003** : Axe de vérification adapté au Homelab (intensité du QA Docker) tout en restant compatible avec le sens AI-DLC.
- **POS-004** : Garde-fou explicite empêchant l'abaissement des niveaux de sécurité par override.
- **POS-005** : Base pour les Verification gates et Sensors du Stage 4 (le niveau `renforcé` les préfigure) et pour la transposition sur les fiches de stage (Stage 7).
- **POS-006** : Cohérence structurelle avec `core/scopes/` (même forme déclarative) sans perte du vocabulaire métier Homelab.

### Négatives

- **NEG-001** : Table de scopes, matrice et mots-clés à maintenir à jour à mesure que le workflow évolue.
- **NEG-002** : Effort de cadrage supplémentaire au démarrage (détection + confirmation du scope, choix des axes).
- **NEG-003** : La matrice scope × phase est adossée aux 3 phases actuelles ; elle devra être re-projetée sur les 5 phases au Stage 5, puis transposée sur les fiches de stage au Stage 7 (double maintenance temporaire, assumée).

## Alternatives étudiées

### ALT-001 - Reprise des 8 scopes génériques de `core/`

Adopter tels quels `standard`, `feature`, `infra`, `mvp`, `poc`, `express`, `enterprise`, `security-patch`.

**Raison du rejet** : plusieurs scopes sont orientés architecture documentaire (`mvp`, `poc`, `enterprise`, `feature`) et peu pertinents pour un workflow d'opérations Homelab (stacks Docker / Terraform / n8n / HA). Sélection de 7 scopes spécifiques au Homelab (validée sur ALI-201).

### ALT-002 - Conserver la grille binaire, l'enrichir sans scopes nommés

Garder « allégé / complet » et ajouter seulement les deux axes.

**Raison du rejet** : sans routage nommé ni auto-détection, on perd la traçabilité et l'affectation déterministe des agents (branches n8n / HA autonomes, accent Terraform). Le gain d'alignement AI-DLC visé par le Stage 2 ne serait pas atteint.

### ALT-003 - Un seul axe combiné (Depth = vérification)

Fusionner détail des artefacts et intensité du QA.

**Raison du rejet** : un patch de sécurité produit peu (Depth minimal/standard) mais exige une vérification renforcée. Un axe unique empêcherait ce couplage. Deux axes indépendants sont retenus, alignés sur AI-DLC / ADR-0003.

## Notes d'implémentation

- **IMP-001** : Artefacts sous `homelab/scopes/` (`README.md` + 7 fichiers de scope). Section « Scopes et axes d'exécution » de `docs/homelab-workflow.md` remplaçant la grille binaire.
- **IMP-002** : Les Verification gates et Sensors déterministes sont introduits au Stage 4 (ALI-204) ; le niveau `renforcé` en pose le cadre.
- **IMP-003** : Le passage aux 5 phases est traité au Stage 5 (ALI-205) ; la matrice sera re-projetée sur la nouvelle ossature.
- **IMP-004** : La transposition de l'appartenance sur le champ `scopes:` des fiches de stage est traitée au Stage 7 (ALI-207).
- **IMP-005** : Décision `Proposed` — passe `Accepted` après validation humaine granulaire sur ALI-202.

## Références

- **REF-001** : ADR-0013 - Cadrage de la refonte homelab-workflow.md sur AI-DLC (Stage 1, ALI-201) *(livré via PR #75)*
- **REF-002** : [ADR-0003 - Scopes et axes Depth / vérification des livrables (core)](0003-scopes-et-axes-depth-verification.md)
- **REF-003** : [ADR-0010 - Scopes : un fichier par scope et axes / review_cap (core)](0010-scopes-fichiers-par-scope-et-axes-review-cap.md)
- **REF-004** : [ADR-0002 - Stratégie de compatibilité et terminologie (core)](0002-strategie-compatibilite-et-terminologie.md)
- **REF-005** : [AI-DLC workflows (awslabs) — core/scopes](https://github.com/awslabs/aidlc-workflows/tree/main/core/scopes)
