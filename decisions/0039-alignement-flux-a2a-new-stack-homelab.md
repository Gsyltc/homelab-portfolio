# Alignement du flux A2A du scope `new-stack` (Homelab) sur le flux désiré

---
auteurs: Sylvain Goubaud  
accepté par : Sylvain Goubaud  
accepté le : 2026-10-04  
supersedes: ""  
superseded_by: ""  

---

## Status

Accepted

## Contexte

Une analyse de conformité a été demandée sur le **scope `new-stack`** du workflow
**Homelab** (coordonné par le Tech Lead Homelab). L'objectif était **uniquement de
vérifier le flux A2A et les gates humaines** décrits par la source unique du workflow
([`homelab/common/conductor.md`](../homelab/common/conductor.md) et les fiches de stage /
protocoles associés) au regard du **flux désiré** exprimé par l'humain, **sans apporter de
modification** au workflow.

Le flux désiré est le suivant :

1. L'humain ouvre une issue pour la création d'une nouvelle stack.
2. Le Tech Lead cadre, détermine le scope et les actions, puis **délègue en parallèle** au
   Spécialiste Docker (docker-compose obligatoire) et au Spécialiste Terraform (`.tfvars`
   obligatoire), et attend le retour des deux agents avec les fichiers en pièces jointes.
3. Le Tech Lead délègue à l'Analyste QA (vérification du compose **et** du Terraform).
   - En cas de problème, l'Analyste QA **mentionne directement le spécialiste concerné**
     (sans passer par le Tech Lead) ; le spécialiste corrige puis **mentionne
     obligatoirement l'Analyste QA** pour continuer.
   - Lorsque les fichiers sont OK, l'Analyste QA **mentionne le Tech Lead** (phase QA passée).
4. Le Tech Lead **délègue ensuite à l'Architecte de sécurité** pour vérifier le respect des
   règles.
   - Éléments de sécurité **critiques ou majeurs** → l'Architecte mentionne le Tech Lead →
     le Tech Lead avertit l'humain par mention **« Gate renforcée »** →
     - si l'humain veut les modifications : le Tech Lead mentionne les spécialistes
       concernés (retour avec mention obligatoire) ;
     - si l'humain ne les veut pas : le Tech Lead télécharge le fichier pour validation
       granulaire de l'humain.
   - Éléments **non critiques / non majeurs** → retour au Tech Lead (mention obligatoire).

La comparaison avec le flux documenté a révélé des divergences structurantes. Le diagramme
d'état détaillé (PlantUML) joint à l'issue représente le flux désiré et annote les écarts.
Cette décision trace ces écarts et les modifications à apporter ; elle **ne modifie pas le
workflow** (statut `Proposed`, en attente de décision humaine).

## Décision

Faire **évoluer le flux A2A documenté du scope `new-stack`** pour l'aligner sur le flux
désiré, en traitant les écarts ci-dessous. Chaque écart est à arbitrer séparément par
l'humain (granularité Keep / Modify / Redo) ; aucune modification de fiche de stage,
protocole ou garde-fou n'est appliquée tant que la décision n'est pas acceptée.

Les écarts (détaillés en « Notes d'implémentation ») portent sur : le parallélisme de la
délégation Docker/Terraform, le routage des `RENVOI` QA (direct vs via Tech Lead), le retour
du spécialiste vers la QA, la formalisation d'une **étape de délégation sécurité
séquentielle**, et surtout l'introduction du mécanisme **« Gate renforcée »** et de son
branchement conditionnel selon la gravité, aujourd'hui **absent** du workflow.

### Arbitrage humain (multica.gaston, 2026-10-04)

L'humain a arbitré chaque écart ; cet arbitrage fonde le passage de l'ADR en `Accepted` :

- **ÉCART-01 — Option A retenue (révision du 2026-10-04)** : la délégation Docker/Terraform
  se fait **en parallèle** (deux livrables disjoints — `.tfvars` et compose — produits
  concurremment, typiquement via **deux sous-issues `--stage 1`** assignées aux spécialistes ;
  la barrière de stage réveille le Tech Lead quand les deux livrables sont prêts, qui lance
  alors la QA). Le verrou de concurrence « un seul traitement par stack » est **requalifié en
  verrou par artefact / livrable** : deux traitements disjoints (compose vs `.tfvars`) sont
  autorisés en parallèle sur la même stack ; toute concurrence de **deux agents sur le même
  artefact** reste interdite (invariant préservé — raffinement sémantique validé par l'humain,
  repasse par le contrôle sécurité au titre de SEC-1). La cohérence `.tfvars` ↔ compose
  (domaine / FQDN, auth) est **réconciliée par l'Analyste QA** en aval, les deux spécialistes
  partant de la même source de vérité (paramètres collectés en Cadrage §2.4). *(Révise la
  première décision « Option B / séquentiel » : voir journal ci-dessous.)*
- **ÉCART-02 & ÉCART-03 — Confirmés** : les échanges de correction se font **directement
  entre l'Analyste QA et les spécialistes** (QA mentionne le spécialiste sur `RENVOI` ; le
  spécialiste corrige et **mentionne la QA** en retour), sans passer par le Tech Lead.
- **ÉCART-04 — Confirmé, avec précision de séquence** : le **Tech Lead contrôle le travail
  finalisé** (contrôle qualité central) **avant** le contrôle de sécurité. La délégation
  sécurité (Tech Lead → Architecte de sécurité) est une **étape séquentielle placée après**
  le contrôle qualité central.
- **ÉCART-05 — « Gate renforcée » ≡ validation humaine granulaire** : on **conserve la
  validation granulaire** ; la « Gate renforcée » et la validation granulaire sont **la même
  chose**. **Aucun nouveau gate distinct n'est créé** : l'escalade sécurité critique/majeure
  est portée par la validation humaine granulaire existante (invariant), avec son branchement
  Keep / Modify / Redo (Modify → mention des spécialistes ; Redo/refus → téléchargement du
  fichier pour validation granulaire).
- **ÉCART-06 — Confirmé** : les éléments de sécurité **non critiques / non majeurs** font
  l'objet d'un **retour explicite au Tech Lead par mention valide** (branchement par gravité
  formalisé).

aucune modification de fiche de stage, protocole ou garde-fou n'est appliquée tant que la
décision n'est pas acceptée — l'arbitrage ci-dessus lève cette réserve.

> **Journal de décision — ÉCART-01.** Première décision (2026-10-04, matin) : **Option B**
> (séquentiel par conception). Révision (2026-10-04, après-midi) : l'humain a finalement opté
> pour le **parallélisme (Option A)** via sous-issues `--stage 1` + barrière de stage, et a
> validé explicitement le passage du verrou de concurrence « par stack » à « **par artefact**
> ». Le présent ADR reflète la décision finale (A) ; les fiches impactées
> ([`new-stack`](../homelab/scopes/new-stack.md),
> [`docker-compose-creation`](../homelab/common/stages/production/docker-compose-creation.md),
> [`terraform-configuration`](../homelab/common/stages/production/terraform-configuration.md),
> [`quality-assurance`](../homelab/common/stages/production/quality-assurance.md),
> [`conductor`](../homelab/common/conductor.md),
> [`governance-security`](../homelab/common/protocols/governance-security.md)) sont alignées
> en conséquence.

## Conséquences

### Positives

- **POS-001** : le flux documenté reflète fidèlement l'intention de l'humain (traçabilité
  et prévisibilité du comportement des agents).
- **POS-002** : l'introduction de la « Gate renforcée » rend explicite et nommée une
  escalade humaine sur sécurité critique/majeure, aujourd'hui seulement implicite.
- **POS-003** : la formalisation du branchement selon la gravité (critique/majeur vs non
  critique) clarifie les responsabilités de l'Architecte de sécurité et du Tech Lead.

### Négatives

- **NEG-001** : le routage direct QA → spécialiste (sans Tech Lead) retire au Tech Lead le
  point de contrôle macro central (`central-quality-control`) et peut affaiblir la piste
  d'audit centralisée et le verrou « un seul traitement par stack ».
- **NEG-002** : la délégation Docker/Terraform en parallèle entre en tension avec la
  dépendance documentée (le `.tfvars` sert de référence de cohérence au compose,
  `requires_stage`) et avec le verrou de concurrence par stack ; un arbitrage technique est
  requis.
- **NEG-003** : toute évolution touchant la sécurité (routage QA, délégation sécurité, gate)
  doit repasser par le contrôle sécurité (clauses SEC-1..5 / SG-1..6) ; un alignement mal
  cadré risque d'être rejeté pour **érosion sémantique** d'un invariant.

## Alternatives étudiées

### ALT-001 - Conserver le flux documenté tel quel (statu quo)

Garder le routage des `RENVOI` via le Tech Lead, la délégation séquentielle
Terraform → Docker et le contrôle sécurité intégré à la phase QA, sans « Gate renforcée ».

**Raison du rejet** : ne répond pas à la demande explicite de l'humain d'aligner le flux
sur son intention ; laisse l'escalade sécurité critique/majeure non nommée et non
formalisée.

### ALT-002 - Aligner uniquement la « Gate renforcée », laisser le reste inchangé

N'introduire que le mécanisme « Gate renforcée » et le branchement par gravité, sans toucher
au parallélisme ni au routage des `RENVOI`.

**Raison du rejet** : couvre l'écart le plus important mais laisse subsister des divergences
de routage A2A (écarts 2, 3, 4) qui restent sources d'incompréhension ; décision partielle à
réserver si l'humain priorise la seule escalade sécurité.

## Notes d'implémentation

- **IMP-001 — ÉCART-01 (délégation parallèle vs séquentielle)** : désiré = délégation
  **parallèle** Docker + Terraform ; documenté = **séquentiel** (Terraform d'abord, le
  `.tfvars` servant de référence de cohérence au compose — `requires_stage:
  [terraform-configuration]` dans
  [`docker-compose-creation.md`](../homelab/common/stages/production/docker-compose-creation.md),
  et verrou « un seul traitement par stack »). Arbitrage requis : lever la dépendance de
  cohérence, ou documenter le flux comme séquentiel-par-conception.
- **IMP-002 — ÉCART-02 (routage des `RENVOI` QA)** : désiré = l'Analyste QA **mentionne
  directement** le spécialiste ; documenté = l'Analyste QA émet `verdict = RENVOI` dans un
  rapport JSON et **rend compte au Tech Lead**, qui aiguille la correction
  ([`quality-assurance.md`](../homelab/common/stages/production/quality-assurance.md),
  [`central-quality-control.md`](../homelab/common/stages/production/central-quality-control.md)).
  Impact sécurité/gouvernance à contrôler (point de contrôle macro, audit, concurrence).
- **IMP-003 — ÉCART-03 (retour spécialiste → QA)** : désiré = le spécialiste **mentionne
  obligatoirement l'Analyste QA** après correction ; documenté = le spécialiste **rend
  compte au Tech Lead**, et le livrable corrigé **repasse par la QA via le Tech Lead**
  ([`report-format.md`](../homelab/common/protocols/report-format.md)).
- **IMP-004 — ÉCART-04 (délégation sécurité séquentielle)** : désiré = le Tech Lead
  **délègue explicitement** à l'Architecte de sécurité comme **étape séquentielle après la
  QA** ; documenté = **aucun stage de délégation sécurité distinct** — le contrôle sécurité
  est porté par l'Analyste QA (technique) et l'Architecte de sécurité (jugement),
  **déclenchés pendant la QA** ([`reviewer.md`](../homelab/common/protocols/reviewer.md),
  [`governance-security.md`](../homelab/common/protocols/governance-security.md)).
- **IMP-005 — ÉCART-05 (« Gate renforcée » — écart majeur, absent)** : désiré = sur sécurité
  critique/majeure, Architecte → mention Tech Lead → mention humaine **« Gate renforcée »** →
  branchement (modifications demandées → mention des spécialistes ; refus → téléchargement du
  fichier pour validation granulaire). Documenté = **aucune notion de « Gate renforcée »**
  ni de branchement conditionnel par gravité ; seuls existent le halt-and-ask sécurité
  ([`autonomy-mode.md`](../homelab/common/stages/production/autonomy-mode.md)) et la
  validation granulaire
  ([`human-granular-validation.md`](../homelab/common/stages/validation/human-granular-validation.md)).
  À créer : un nouveau stage/protocole formalisant l'escalade nommée.
- **IMP-006 — ÉCART-06 (branchement sécurité non critique)** : désiré = retour explicite au
  Tech Lead par mention sur éléments non critiques ; documenté = couvert implicitement
  (contrôle sécurité intégré avant la validation humaine) mais **non formalisé** comme
  branchement par gravité.
- **IMP-007 — Point conforme (non un écart)** : le retour « phase QA passée » (QA → mention
  Tech Lead même sur verdict `OK`) est **déjà exigé** par le workflow documenté
  ([`reviewer.md`](../homelab/common/protocols/reviewer.md), section « Fin de revue »).
- **IMP-008 — Contrainte de gouvernance** : toute implémentation passe par la boucle
  d'apprentissage / PR revue (SEC-1..5, SG-1..6) et le contrôle de l'Architecte de sécurité
  Homelab ; les invariants (validation humaine granulaire, Terraform ne déploie jamais,
  aucun secret en clair, jamais `${SNI}`, un seul traitement par stack, piste d'audit sur
  l'issue) **ne sont pas abaissables**.

## Références

- **REF-001** : [Conductor Homelab — source unique du workflow](../homelab/common/conductor.md)
- **REF-002** : [Scope `new-stack`](../homelab/scopes/new-stack.md)
- **REF-003** : [Stage Vérification qualité (Analyste QA)](../homelab/common/stages/production/quality-assurance.md)
- **REF-004** : [Stage Contrôle qualité central (Tech Lead)](../homelab/common/stages/production/central-quality-control.md)
- **REF-005** : [Protocole gouvernance A2A & sécurité](../homelab/common/protocols/governance-security.md)
- **REF-006** : [Protocole revue (reviewer)](../homelab/common/protocols/reviewer.md)
- **REF-007** : [Agent Architecte de sécurité Homelab](../homelab/agents/security-architect-homelab-agent.md)
