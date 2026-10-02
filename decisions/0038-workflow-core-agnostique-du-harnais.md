# Rendre le workflow `core` agnostique du harnais via une couche d'adaptation

---
auteurs: Sylvain G.
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

Le workflow `core` (architecture de solution & intégration) a été conçu et éprouvé **sous Multica** : la coordination multi-agents (A2A), le suivi d'état du run et la piste d'audit s'appuient sur des primitives propres à ce harnais. L'humain demandeur (multica.gaston, ORIG-71) souhaite **réutiliser le même workflow depuis d'autres harnais** (Codex, Hermes, OpenCode, etc.) **tout en conservant intactes les capacités Multica** lorsque l'exécution a bien lieu sous Multica.

Le diagnostic du dépôt (ORIG-71) établit deux faits :

1. **Le couplage à Multica est concentré, pas diffus.** Il tient à **4 primitives** d'orchestration, localisées dans `core/common/` (conductor + protocoles) et quelques fiches d'agent :
   - **Délégation A2A** — `[@Label](mention://agent/<uuid>)` + résolution d'UUID via `multica agent list --output json` (`conductor.md`, `protocols/governance-security.md`, `protocols/stage-protocol.md`, `agents/README.md`) ;
   - **Statut d'issue** comme machine à états du run — `multica issue status <id> in_review|blocked|…` ;
   - **Piste d'audit** portée par les **commentaires d'issue** (`conductor.md` : « la piste d'audit vit sur l'issue Multica, jamais dans un fichier `audit.md` ») ;
   - **Métadonnées de projet** — labels (`OpenSpec`), description de projet (`Git: Oui`, `Méthodologie:`, `CDAE-AI:`), pièces jointes (`multica attachment upload`).

2. **Le workflow est déjà partiellement agnostique.** Les acteurs sont désignés par leur **fonction**, jamais par un UUID figé (`governance-security.md`, `stage-definition.md`) ; la forme déclarative `conductor / stages / protocols` sépare déjà le **parseur** (front-matter) de l'**agent exécutant** (corps) et pose « aucun tooling exécutable n'est requis » (`stage-definition.md`) ; plusieurs étapes sont **déjà gardées** par « contexte Multica uniquement » / « hors contexte Multica, cette étape est sautée » (tag `OpenSpec` dans `stage-protocol.md`, `deliverables-breakdown.md`, `openspec-agent.md`).

Autrement dit : la **méthode** (5 phases, scopes, gates/sensors advisory, validation humaine granulaire, décisions structurantes, sécurité OWASP/STRIDE) est **déjà portable** ; seule la **mécanique de coordination** est liée à Multica. Le découplage ne demande donc pas une réécriture, mais de **finir** un travail entamé et d'en poser le principe explicitement.

## Décision

**Introduire une couche d'adaptation du harnais (« harness adapter ») qui sépare la *méthode* (invariante) de la *mécanique de réalisation* (variable selon le harnais).** Le corps normatif du workflow `core` parle en **capacités abstraites** ; chaque harnais fournit sa **traduction**. **Multica est la première implémentation de référence** (complète) ; les autres harnais retombent sur une implémentation **dégradée à base de fichiers**.

### Les 4 capacités abstraites

| Capacité abstraite | Contrat | Implémentation Multica (référence) | Implémentation dégradée (Codex / Hermes / OpenCode / …) |
| --- | --- | --- | --- |
| `DELEGATE(fonction, mission)` | Confier une mission cadrée (objectif, périmètre, critères d'acceptation) à l'agent portant une **fonction**. | Mention `[@Label](mention://agent/<uuid>)` ; UUID résolu via `multica agent list --output json` ; retour A2A par mention active. | Sous-agent / appel d'outil du harnais **ou** exécution séquentielle par le même runtime jouant les fonctions tour à tour (voir « boucle A2A hors Multica »). |
| `SET_RUN_STATE(état)` | Rendre visible l'état du run : `in_progress` / `in_review` / `blocked` / `done`. | `multica issue status <id> <état>`. | Fichier d'état local (`.workflow-state`) **ou** sortie structurée **ou** no-op explicitement tracé. |
| `AUDIT(entrée)` | Journaliser chaque étape (analyse, décision, délégation, résultat, sollicitation sécurité, validation) sans jamais écraser l'historique ; capturer l'entrée brute des arbitrages humains. | Commentaire d'issue (`multica issue comment add`). | Fichier `audit.md` **append-only** dans le répertoire du projet — le fallback que `core` **interdit sous Multica** redevient le **défaut hors Multica**. |
| `TAG` / `PROJECT_META` | Porter des métadonnées de routage/méthodologie (`OpenSpec`, `Git: Oui`, `Méthodologie:`, `CDAE-AI:`) et mettre à disposition les livrables. | Labels d'issue + description de projet + `multica attachment upload`. | Front-matter de fichier / `project.md` à la racine du projet / dépôt de fichiers dans le répertoire projet. |

### Règle de dégradation (non négociable)

Une capacité absente ne **bloque jamais** la méthode : elle retombe sur un équivalent fichier ou devient un no-op **tracé**. **La dégradation porte sur le *support*, jamais sur l'*obligation*.** Les invariants non contournables (`protocols/governance-security.md`) restent intacts quel que soit le harnais :

1. Validation humaine granulaire (chaque choix validé/rejeté séparément) ;
2. Décision structurante tracée dans le registre de décisions ;
3. Piste d'audit (le *support* change : issue → `audit.md`) ;
4. Contrôle sécurité minimal OWASP / STRIDE, systématique ;
5. Aucune action à impact sans validation humaine explicite ; rollback validé avant action destructive ;
6. Mention humaine obligatoire sur blocage → hors Multica, devient un **`halt-and-ask`** qui rend explicitement la main à l'humain du harnais (l'obligation de ne pas avancer demeure).

Même logique que le plancher sécurité SG-3 : aucun gate/sensor ne court-circuite le contrôle sécurité ; ici, **aucun harnais ne supprime un invariant**.

### Détection du harnais

Au **bootstrap du coordinateur** (une seule fois par run), le workflow détecte le harnais d'exécution et sélectionne l'implémentation des capacités :

- **Multica détecté** (CLI `multica` disponible / variables de run Multica présentes) → implémentation **complète**.
- **Sinon** → implémentation **dégradée à base de fichiers**.

Les **fiches de stage ne changent pas** : elles ne parlent déjà qu'en **fonctions** et, après cet ADR, qu'en **capacités abstraites**.

## Conséquences

### Positives

- **POS-001** : Le workflow `core` devient réutilisable par n'importe quel harnais sans fork ; Multica garde 100 % de ses capacités (parité préservée).
- **POS-002** : Le mapping harnais↔capacités est **centralisé** en un seul protocole (source unique), au lieu d'être dispersé en conditions `multica …` dans le corps normatif.
- **POS-003** : Les invariants de gouvernance et de sécurité sont **explicitement indépendants du harnais**, ce qui durcit la posture plutôt que de l'affaiblir.
- **POS-004** : Transition douce — on **généralise** un pattern déjà présent (« contexte Multica uniquement ») au lieu d'introduire un mécanisme neuf.

### Négatives

- **NEG-001** : Maintien d'un tableau de correspondance par harnais à tenir à jour à mesure que de nouveaux harnais sont ajoutés.
- **NEG-002** : La boucle A2A hors Multica est nécessairement une **simulation** (sous-agent ou exécution séquentielle) ; la richesse « multi-agents concurrents » reste propre à Multica.
- **NEG-003** : Coexistence temporaire, pendant la migration du vocabulaire du triptyque, de tournures « Multica » et de capacités abstraites.

## Alternatives étudiées

### ALT-001 — Fork par harnais

Dupliquer `core` en une variante par harnais.

**Raison du rejet** : divergence inévitable, double maintenance, perte de la source unique ; contraire à l'esprit déclaratif du dépôt.

### ALT-002 — Conditions `if Multica` dispersées dans le corps normatif

Garder la logique Multica inline et multiplier les gardes `sous Multica / hors Multica` partout.

**Raison du rejet** : le couplage resterait diffus et illisible ; pas de source unique du mapping ; érosion possible des invariants au fil des gardes ad hoc.

### ALT-003 — Statu quo (Multica-only)

Ne rien changer.

**Raison du rejet** : ne répond pas au besoin de réutilisation par d'autres harnais (ORIG-71).

## Notes d'implémentation — scénario complet à jouer sur acceptation

> Cette section rend l'ADR **jouable** : à l'acceptation (passage en `Accepted`) et sur décision explicite de l'humain, le scénario ci-dessous s'exécute dans l'ordre. **Chaque étape à impact reste soumise à la validation humaine granulaire et à la règle workspace « aucun commit/push/PR sans accord explicite ».** Les travaux se font dans une **branche git dédiée** à l'issue.

- **IMP-001 — Protocole `core/common/protocols/harness-adapter.md`** (nouveau, transverse) : définit les 4 capacités abstraites, le contrat de chaque opération, le tableau de correspondance par harnais (colonne Multica remplie = référence ; colonne dégradée = fallback fichier), la règle de dégradation et la procédure de détection du harnais. Devient la **source unique** du mapping. Référencé depuis `conductor.md` et `governance-security.md`.

- **IMP-002 — Dé-couplage du vocabulaire du triptyque** (`conductor.md`, `protocols/governance-security.md`, `protocols/stage-protocol.md`) : remplacer les tournures impératives couplées (« poste un commentaire d'issue », « passe l'issue en `in_review` », « mention `mention://agent/<uuid>` ») par les **capacités abstraites** `AUDIT(...)`, `SET_RUN_STATE(in_review)`, `DELEGATE(fonction, mission)`, chacune renvoyant à `harness-adapter.md`. Déplacer les commandes CLI `multica …` concrètes **hors du corps normatif**, dans la seule colonne Multica du tableau d'adaptation.

- **IMP-003 — Généralisation des gardes de contexte** : partout où un `multica issue label …` / `multica attachment …` / `multica project update …` apparaît (`deliverables-breakdown.md`, `openspec-agent.md`, `git-detection.md`, `archiving-agent.md`), le motif « sous Multica → … ; hors Multica → <fallback fichier> » devient la **forme par défaut**, non l'exception. Les fiches de stage ne sont pas modifiées sur le fond (fonctions + capacités uniquement).

- **IMP-004 — Détection du harnais au bootstrap** : ajouter au chargement de contexte du coordinateur (`conductor.md`, « OBLIGATOIRE : chargement du contexte au démarrage ») une étape de détection du harnais qui lie les capacités à leur implémentation pour toute la durée du run, et la tracer via `AUDIT`.

- **IMP-005 — Arbitrage « boucle A2A hors Multica »** : décider, à l'implémentation, du degré de simulation du multi-agent hors Multica (sous-agent du harnais vs exécution séquentielle par le même runtime). Tracer le choix dans un ADR de suivi si structurant.

- **IMP-006 — Non-régression Multica** : vérifier qu'après la bascule, un run **sous Multica** produit exactement les mêmes effets qu'avant (mentions, statuts, commentaires d'audit, labels) — la colonne Multica du tableau est la référence, aucune capacité perdue.

- **IMP-007 — Compatibilité ascendante** : aligner la stratégie sur ADR-0002 (aucune référence existante cassée, mapping Multica = référence complète). Introduction **opt-in / advisory** si besoin pendant la transition.

**Critères de suivi** : (a) `harness-adapter.md` est la source unique du mapping ; (b) aucune commande `multica …` ne subsiste dans le corps normatif du triptyque hors de la colonne Multica ; (c) les 6 invariants sont vérifiés indépendants du harnais ; (d) un run Multica est non-régressé (IMP-006).

## Références

- **REF-001** : ORIG-71 — « Rendre le workflow Agnostique » (issue d'origine, diagnostic et plan de cadrage).
- **REF-002** : [ADR-0002 — Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md) (stratégie de compatibilité ascendante réutilisée ici).
- **REF-003** : `core/common/conductor.md`, `core/common/protocols/governance-security.md`, `core/common/protocols/stage-protocol.md`, `core/common/protocols/stage-definition.md` (surfaces de couplage et forme déclarative existante).
- **REF-004** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows) (modèle Harness Engineer Guide, aligné dans le dépôt).
