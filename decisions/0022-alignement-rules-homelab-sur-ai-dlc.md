# Alignement du système de règles Homelab sur le contrat AI-DLC « Rules and the Learning Loop »

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — en attente de validation humaine granulaire (invariant : aucun ADR accepté sans validation humaine explicite). Aucune règle n'est ajoutée / modifiée dans `homelab/rules/` par cet ADR : il **vérifie et trace** la conformité de la chaîne de couches déjà scaffoldée en [ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md), et ne procède qu'à **une correction de cohérence structurelle** (ajout du fichier de phase `ideation.md`). Il ne passe pas par la boucle d'apprentissage (capture → confirmation → contrôle de conflit), réservée à l'**écriture de règles** (invariant SEC-5). Aucune posture de sécurité ni garde-fou de gouvernance n'est modifié.

## Contexte

La mémoire de règles multi-couches du Homelab vit sous [`homelab/rules/`](../homelab/rules/README.md), introduite par l'[ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md) (*Accepted*) : quatre couches de précédence `global > stack > phase > scope`, alimentées par une **boucle d'apprentissage** (capture → remontée → confirmation humaine → contrôle de conflit à l'admission → écriture → application au prochain workflow), avec les clauses de sécurité **SEC-1 à SEC-5** et 12 règles `global` seedées (`RULE-GL-001..012`).

Le Stage 4 de l'alignement AI-DLC du harness Homelab (issue ALI-212, parente ALI-208) porte ce système de règles sur le contrat **« Rules and the Learning Loop »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`). C'est le **miroir Homelab** de l'[ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md) (*Accepted*, issue ALI-197), qui a fait ce travail pour `core/rules/`.

Le contrat amont fixe :

- **Cinq couches** résolues au démarrage de chaque workflow : `org → team → project → phase → stage`, fichiers sous `core/memory/` (`org.md`, `team.md`, `project.md`, `phases/<phase>.md`), **portée dérivée du nom de fichier** (pas de champ `scope:`). Les quatre fichiers de phase sont `ideation`, `inception`, `construction`, `operation` (l'`initialization` est **bootstrap-only** et ne livre **aucun** fichier de règles). La cinquième couche — **règles par stage** (`aidlc-stage-<slug>.md`) — est **réservée pour une future version** : on ne peut pas en écrire aujourd'hui.
- **Modèle strict-additif** : toutes les règles applicables coexistent dans le contexte de l'agent ; **aucune couche n'en écrase silencieusement une autre au runtime**. Pas de bloc `overrides:`, pas de mot-clé `enforcement:`.
- **Contrôle de conflit avant écriture, pas au runtime** : une règle qui contredit une couche plus large est traitée **à l'admission** (comparaison au niveau de la rubrique avant l'écriture déterministe) — **revise / skip / escalate** — jamais résolue à l'exécution.
- **Boucle d'apprentissage** : journal → gate présentant les candidats verbatim → confirmation → écriture datée, **portée par défaut la plus étroite**, promotion contrôlée. Application au **prochain** workflow, jamais à celui en cours.

Contrainte de cadrage (ALI-208, miroir d'ALI-193/ALI-197) : adopter la **forme déclarative et les contrats** d'AI-DLC sans importer le tooling amont non applicable (`bun`, hooks `.ts`, `dist/<harness>/`, `core/memory` resolver) ; **préserver** la précédence et le contrôle de conflit à l'admission ; toute divergence assumée est **tracée en décision structurante**.

Cet ADR répond aux inputs et critères d'acceptation de l'issue ALI-212 : (1) chaîne de couches confirmée (emplacement, précédence, modèle additif vs surcharge) ; (2) couche `stage` et couches globales clarifiées ; (3) garde-fous absolus formalisés comme **non surchargeables** ; (4) contrôle de conflit à l'admission documenté ; (5) divergences tracées.

## Décision

La structure établie par l'[ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md) est **vérifiée conforme** au contrat amont (moyennant les divergences assumées ci-dessous) et **conservée**, avec **une seule correction de cohérence structurelle** (§1, ajout de `phases/ideation.md`). La vérification n'a trouvé **aucune non-conformité** hors ce point.

### 1. Chaîne de couches — quatre couches conservées, `stage` différée, `org`/`team` fusionnés dans `global`, `scope` maison conservée

La chaîne **`global > stack > phase > scope`** de l'[ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md) est **conservée** (miroir structurel de la chaîne core `workspace > project > phase > scope`), avec les positions suivantes — mêmes arbitrages que l'[ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md), transposés au nommage métier Homelab :

- **Couche `stage` — NON ajoutée (différée), en miroir de l'amont.** AI-DLC réserve la couche `stage` (`aidlc-stage-<slug>.md`) « pour une future version » et **interdit d'en écrire une aujourd'hui**. Ajouter une couche `stage` maison irait *au-delà* de l'amont. Décision : **rester aligné** en ne créant pas la couche `stage` ; la granularité fine reste couverte par la couche `scope` (les 7 scopes Homelab) et par les fiches de stage elles-mêmes (comportement, non règles apprises). Réévaluable si l'amont ouvre la couche `stage`.
- **`org`/`team` — assumés comme fusion dans `global`.** Le périmètre Homelab n'a pas de frontière org/équipe distincte à modéliser. La couche `global` (toujours chargée, précédence maximale) **tient lieu des deux couches amont `org` + `team`**, et se distingue du `core/rules/workspace.md` (qui couvre le workspace Multica entier). Divergence de nommage assumée : `global` ≡ `org` ⊕ `team`, `global` ≠ `workspace` (périmètre Homelab, pas le workspace entier). Conséquence : la promotion `stack → global`, **parce qu'elle touche la couche des invariants**, reste soumise au **contrôle sécurité systématique** (SEC-4, Architecte de sécurité Homelab) — garde-fou plus strict que le « un clic » amont.
- **Couche `scope` — conservée (divergence maison assumée, déjà tracée ADR-0015).** AI-DLC n'a pas de couche `scope` de règles (le mot « scope » y désigne les *profils de workflow*). Notre couche `scope` est un **pont explicite** avec les 7 scopes Homelab de [`homelab/scopes/`](../homelab/scopes/README.md) (source d'identité, ADR-0014 / ADR-0021) ; elle est **conservée** comme couche de plus faible précédence.

**Correction de cohérence (5 phases) — ajout de `phases/ideation.md`.** L'[ADR-0017](0017-passage-5-phases-et-mode-autonomie-homelab.md) (*Accepted*) a fait passer le workflow Homelab à **5 phases** (`Initialisation → Idéation → Cadrage et Paramètres → Production et Contrôle → Validation et Déploiement`), mais la couche `phase` des règles ne comptait que **trois fichiers** (`cadrage`, `production`, `validation`). L'amont livre **quatre** fichiers de phase (`ideation`, `inception`, `construction`, `operation`) et **aucun** pour `initialization` (bootstrap-only). Décision : **ajouter `homelab/rules/phases/ideation.md`** (couche `phase`, chargement à la demande, format `RULE-PH-NNN`), et **ne pas** créer de fichier `initialisation` — exactement le partitionnement amont, et le miroir de l'[ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md) IMP-002. La couche `phase` passe donc de 3 à **4 fichiers**, cohérente à la fois avec l'amont, avec l'ADR-0011 (core) et avec l'ADR-0017 (5 phases Homelab). C'est la **seule écriture de fichier** de cet ADR ; le fichier ne contient **aucune règle apprise** (structure uniquement).

### 2. Emplacement — `homelab/rules/` conservé (divergence assumée, déjà tranchée ADR-0015)

L'amont place les règles sous `core/memory/`. Le Homelab **conserve `homelab/rules/`** (décision ADR-0015, miroir de `core/rules/`), **confirmée ici** :

- `homelab/rules/` est **cohérent avec les autres surfaces déclaratives Homelab** (`homelab/scopes/`, `homelab/agents/`, `homelab/sensors/`) et **agnostique de méthodologie**, contrairement à `homelab/memory/` (nommage lié au moteur amont).
- Le nom `rules` **dit ce que le répertoire contient** (règles persistantes versionnées) ; `memory` recouvre chez l'amont un espace plus large (space memory, learnings, practices) non répliqué ici.
- Aucun tooling amont (`aidlc-learnings.ts`, résolveur `core/memory`) n'est importé : renommer n'apporterait **aucun bénéfice d'exécution** et casserait de nombreux pointeurs vivants (`AGENTS.md`, `README.md`, `conductor.md`, fiches de stage, sensors) au prix d'une pure conformité de nommage.

**Divergence assumée et tracée** : emplacement `homelab/rules/` (et non `homelab/memory/`) ; sous-répertoires `stacks/`, `phases/`, `scopes/` (et non fichiers à plat). La **portée reste dérivable du chemin** (nom de fichier + répertoire), dans l'esprit amont « pas de champ `scope:`, la portée vient du fichier ».

### 3. Précédence et contrôle de conflit — précédence explicite ⊇ strict-additif, conflit réglé à l'admission

Le système Homelab **énonce une précédence de couches** (`global > stack > phase > scope`) **ET** applique un **contrôle de conflit à l'admission** : une règle basse **ne peut pas contredire** une règle haute sans **arbitrage humain** (jamais tranché seul par un agent). Les deux modèles — le strict-additif amont et la précédence explicite maison — convergent sur l'essentiel : **le conflit se règle à l'écriture, jamais silencieusement au runtime**.

Notre précédence explicite est un **sur-ensemble conservateur** du strict-additif : elle donne une clé de lecture déterministe *et* refuse la contradiction à l'admission. Divergence assumée : nous n'implémentons pas la concaténation strict-additive runtime du moteur amont (pas de moteur), mais nous en **préservons l'invariant de sûreté** par la précédence + le contrôle d'admission (revise / skip / escalate → chez nous : arbitrage humain). Le contrôle est un **aide-audit**, pas une frontière d'enforcement runtime — conforme au contrat amont.

Le **contrôle de conflit à l'admission** (documenté au README `homelab/rules/`, section « Boucle d'apprentissage » et « Clauses de sécurité ») combine :

1. **précédence des couches** (`global > stack > phase > scope`) ;
2. **invariants non contournables** (§4 ci-dessous) — rejet d'office si contradiction ;
3. **contrôle sécurité systématique** de l'**Architecte de sécurité Homelab** pour toute règle `global` et toute règle visant un scope à garde-fous / une phase de vérification / un contrôle de sécurité (clauses SEC-2 / SEC-4).

### 4. Garde-fous absolus — formalisés comme règles non surchargeables

Aucune règle apprise, à aucune couche, ne peut affaiblir les **garde-fous absolus** du Homelab. Ils sont formalisés à deux endroits complémentaires :

- **En données**, couche `global` (précédence maximale, toujours chargée) : `RULE-GL-004` (un seul traitement par stack — verrou `active_step`), `RULE-GL-005` (aucun secret en clair), `RULE-GL-006` (jamais `${SNI}` en Terraform livré), `RULE-GL-007` (Terraform ne déploie JAMAIS), `RULE-GL-010` (règle absolue n8n §1.1 — délégation immédiate, pas même l'analyse), `RULE-GL-011` (sélection auto d'authentification `oidc → forwardauth → local`).
- **En prose**, README `homelab/rules/`, section « Invariants non contournables » : validation humaine granulaire, ADR sur chaque décision structurante, piste d'audit sur l'issue, règle absolue n8n, sélection auto d'authentification, garde-fous absolus (Terraform ne déploie jamais, aucun secret, jamais `${SNI}`, un seul traitement par stack), et garde-fous sécurité des scopes (plancher de vérification, Depth non abaissable sur `security-patch` / `new-stack`).

**Un candidat qui contredit — ou qui restreint, conditionne, ou ajoute une exception à (clause SEC-1, érosion sémantique) — l'un de ces garde-fous est rejeté d'office**, même sans contradiction littérale. Les clauses **SEC-1 à SEC-5** restent intégralement en vigueur et ferment les vecteurs de dérive de gouvernance. Le périmètre de sécurité est la **sécurité de base d'un homelab** (secrets, exposition, permissions, durcissement Docker/Swarm, Traefik) — aucune notion de conformité réglementaire (Loi 25, PCI DSS, RGPD, LPRPDE), jamais introduite.

### 5. Boucle d'apprentissage — cohérente, et plus conservatrice que l'amont

Après la correction du §1, la boucle d'apprentissage existante ([ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md)) **reste cohérente** avec le contrat amont :

- **Portée par défaut `stack`** (la plus étroite dans le contexte Homelab), aligné sur l'amont (défaut = couche la plus étroite). Promotion `stack → global` = décision structurante + contrôle sécurité systématique (SEC-4) — plus strict que le « un clic » amont, justifié par la fusion `org`+`team` dans `global`.
- **Application différée** : identique à l'amont — une règle apprise s'applique au **prochain** workflow, jamais en cours de route (SEC-3).
- **`SENSOR_PROPOSED`** : levier conceptuel identique via `homelab/sensors/` (pull-authoring par id) ; l'articulation fine « apprentissage → liaison de sensor » relève du **Stage 5 (ALI-213)** et n'est pas figée ici.

Aucun invariant n'est affaibli ; les clauses SEC-1 à SEC-5 restent inchangées.

### 6. Templates — convention de rubriques topicales, IDs et précédence préservés

Les gabarits `stacks/_template.md` et `scopes/_template.md` adoptent déjà la **convention de rubriques topicales** amont (`## Conventions Docker/Swarm`, `## Sécurité / Hardening`, `## Conventions Traefik`, `## Conventions Terraform`, `## Manière de travailler`), une règle = une puce sous la rubrique idoine, **tout en préservant** les identifiants stables `RULE-<COUCHE>-NNN`, la mention de précédence et l'origine + date (traçabilité, invariant SEC-5). Vérifié conforme, **inchangé** par cet ADR. **Pas de template `stage`** : la couche `stage` étant différée (§1), aucun `stages/_template.md` n'est créé — cohérent avec l'amont.

## Conséquences

### Positives

- **POS-001** : Chaîne de couches Homelab **vérifiée conforme** au contrat amont et **tracée** ; alignement maximal (pas de couche `stage` tant que l'amont ne l'ouvre pas ; `org`/`team` fusionnés dans `global` ; 4 fichiers de phase comme l'amont et comme le core).
- **POS-002** : Cohérence **5 phases** rétablie entre l'[ADR-0017](0017-passage-5-phases-et-mode-autonomie-homelab.md) et la couche `phase` des règles (ajout `phases/ideation.md`) ; parité avec l'[ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md) (core).
- **POS-003** : Emplacement `homelab/rules/` **confirmé** et justifié (cohérence maison, agnostique de méthodologie, zéro pointeur cassé) ; divergence assumée et tracée.
- **POS-004** : L'invariant de sûreté amont (conflit réglé à l'écriture, jamais au runtime) est **préservé et renforcé** par la précédence explicite + le contrôle de conflit à l'admission.
- **POS-005** : Les garde-fous absolus sont **formalisés comme non surchargeables** en données (`RULE-GL-*`) et en prose (invariants + SEC-1..5), avec rejet d'office de tout candidat qui les contredit ou les érode.

### Négatives

- **NEG-001** : Divergence de **nommage** persistante avec l'amont (`homelab/rules/` vs `core/memory/`, `global` vs `org`/`team`) ; atténuée par la documentation explicite et par la dérivabilité de la portée depuis le chemin.
- **NEG-002** : L'absence de couche `stage` peut nécessiter, si un besoin réel émerge, un ADR ultérieur d'ouverture (réévaluation liée à l'amont).
- **NEG-003** : La couche `phase` passe à 4 fichiers ; `ideation.md` est vide de règles apprises pour l'instant (attendu — la boucle d'apprentissage l'alimentera).

## Alternatives étudiées

### ALT-001 — Ajouter une couche `stage` maison dès maintenant

Créer `homelab/rules/stages/<slug>.md` + template `stage`.

**Raison du rejet** : l'amont **réserve** la couche `stage` et **interdit d'en écrire une** aujourd'hui ; l'ajouter irait *au-delà* du contrat, pour une granularité déjà couverte par la couche `scope` et par les fiches de stage. Différé, réévaluable si l'amont l'ouvre (miroir ADR-0011 ALT-001).

### ALT-002 — Modéliser `org` et `team` en couches distinctes

Créer `homelab/rules/org.md` + `homelab/rules/team.md` en plus de `global.md`.

**Raison du rejet** : le périmètre Homelab n'a pas de frontière org/équipe distincte à modéliser ; deux couches supplémentaires seraient vides et introduiraient une précédence sans portée réelle. `global` fusionne les deux (miroir ADR-0011 ALT-002).

### ALT-003 — Renommer `homelab/rules/` en `homelab/memory/`

Aligner littéralement l'emplacement sur l'amont.

**Raison du rejet** : aucun bénéfice d'exécution (pas de tooling amont importé), casse de nombreux pointeurs vivants, et `memory` recouvre chez l'amont un périmètre plus large non répliqué. `homelab/rules/` est plus explicite et cohérent avec les autres surfaces Homelab (miroir ADR-0011 ALT-003, ADR-0015 §2).

### ALT-004 — Adopter le strict-additif pur (supprimer la précédence explicite)

Remplacer la précédence `global > stack > phase > scope` par une simple concaténation strict-additive.

**Raison du rejet** : sans moteur qui compile la vue additive au démarrage, une concaténation « à plat » perdrait la clé de lecture déterministe et le refus de contradiction à l'admission — un affaiblissement de l'invariant de sûreté. La précédence explicite + le contrôle d'admission **préservent** l'invariant amont et le renforcent ; c'est un sur-ensemble conservateur, pas une contradiction (miroir ADR-0011 ALT-004).

## Notes d'implémentation

- **IMP-001** : `homelab/rules/README.md` mis à jour — bullet « Phases » et tableau des couches passés à **4 fichiers** (`ideation`, `cadrage`, `production`, `validation`) ; note d'alignement AI-DLC référençant le présent ADR et le miroir core [ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md).
- **IMP-002** : Fichier `homelab/rules/phases/ideation.md` **créé** (couche `phase`, chargement à la demande, format `RULE-PH-NNN`, aucune règle apprise), pour cohérence avec l'[ADR-0017](0017-passage-5-phases-et-mode-autonomie-homelab.md) et parité avec l'[ADR-0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md) IMP-002. **Aucun fichier `initialisation`** (bootstrap-only, aligné amont).
- **IMP-003** : Templates `stacks/_template.md` et `scopes/_template.md` **vérifiés conformes** (rubriques topicales, IDs `RULE-*`, précédence, traçabilité) — **inchangés**. **Pas** de `stages/_template.md` (couche `stage` différée).
- **IMP-004** : Pointeurs — `README.md`, `AGENTS.md` : plage `decisions/` mise à jour pour inclure le présent ADR. **Numérotation** : ADR-0022 (l'ADR-0021 est réservé par la PR ouverte #90 du Stage 3 / ALI-211, non encore fusionnée). La **collision de numérotation ADR-0020 pré-existante** sur `main` (deux ADR 0020) et les **6 marqueurs de conflit Git résiduels** dans `decisions/0011-*.md` sont **hors périmètre** de cet ADR — signalés et déférés à la vérification globale **ALI-214**.
- **IMP-005** : Aucune règle écrite dans `homelab/rules/` par cet ADR (structure uniquement) ; la boucle d'apprentissage (capture → confirmation → contrôle de conflit) et les clauses SEC-1..5 restent inchangées. L'articulation `SENSOR_PROPOSED` → liaison de sensor est déférée au **Stage 5 (ALI-213)**.
- **IMP-006** : Aucune modification de la posture de sécurité ni d'un garde-fou de gouvernance. Les garde-fous absolus sont seulement **formalisés / explicités** comme non surchargeables (déjà en vigueur en données `RULE-GL-*` et en prose README).

## Références

- **REF-001** : Issue ALI-212 (Stage 4 — Rules Homelab : chaîne de couches, précédence, garde-fous non surchargeables) ; issue parente ALI-208.
- **REF-002** : [ADR-0015 - Boucle d'apprentissage et règles persistantes Homelab](0015-learning-loop-et-regles-persistantes-homelab.md)
- **REF-003** : [ADR-0011 - Alignement de la mémoire de règles (core) sur AI-DLC](0011-alignement-memoire-de-regles-sur-ai-dlc.md)
- **REF-004** : [ADR-0004 - Boucle d'apprentissage et règles persistantes multi-couches (core)](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-005** : [ADR-0014 - Scopes Homelab et axes Depth / vérification](0014-scopes-homelab-et-axes-depth-verification.md)
- **REF-006** : [ADR-0017 - Passage à 5 phases et mode d'autonomie Homelab](0017-passage-5-phases-et-mode-autonomie-homelab.md)
- **REF-007** : [ADR-0016 - Verification gates et Sensors Homelab](0016-verification-gates-et-sensors-homelab.md)
- **REF-008** : [AI-DLC — Harness Engineer Guide, « Rules and the Learning Loop »](https://awslabs.github.io/aidlc-workflows/harness-engineering/05-rules-and-the-loop/)
- **REF-009** : [AI-DLC workflows (awslabs) — core/memory](https://github.com/awslabs/aidlc-workflows/tree/main/core/memory)
