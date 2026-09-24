# Réorganisation du workflow : Terraform avant compose + élargissement du rôle QA au Terraform (Analyste QA)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-24
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine granulaire explicite obtenue (multica.gaston, 2026-09-24, acceptation de la PR). Cette réorganisation est **documentaire** (contrat `homelab/common/` + définitions d'agents + sensors) : elle ne modifie **aucune** posture de sécurité de fond — les invariants (Terraform ne déploie jamais, aucun secret en clair, jamais `${SNI}` dans un livrable Terraform, validation humaine granulaire, un seul traitement par stack), les clauses SG-1 à SG-6 et l'exception bloquante ALI-204 sont **préservés à l'identique**.

## Contexte

Sur **HOM-214** (stack FreeLLMAPI), le livrable Terraform — pourtant **obligatoire et inconditionnel** sur scope `new-stack` (invariant SEC-1, voir [`homelab/common/stages/production/terraform-configuration.md`](../homelab/common/stages/production/terraform-configuration.md) et [`homelab/scopes/new-stack.md`](../homelab/scopes/new-stack.md)) — a été déclaré « non requis » par le coordinateur et **sauté**. Le jugement de sécurité (Architecte de sécurité Homelab) a donc porté sur le **seul docker-compose**, laissant la configuration Terraform hors du champ de contrôle. Cet incident a mis en évidence deux faiblesses de l'ordonnancement de la **Phase 3 (Production et Contrôle)** :

1. **Ordre de production inadapté.** L'ordre historique était `docker-compose-creation → docker-compose-qa → terraform-configuration`. Le Terraform arrivait **en dernier**, après le QA du compose, ce qui :
   - rendait le livrable `.tfvars` facile à « oublier » ou à déclasser en fin de parcours (le cas HOM-214) ;
   - forçait le skill `configuration-applications` à **déduire** certaines valeurs (auth, `cloudflare_dns_nb`, domaine) depuis le docker-compose déjà produit, alors que ces paramètres sont **déjà collectés en Cadrage (§2.4)**.
2. **Périmètre QA trop étroit.** L'agent QA (`QA Docker`) ne vérifiait que le docker-compose. Le fichier de configuration Terraform — qui alimente directement les playbooks (`cloudflare`, `swarm`, `updatime_kuma`, configuration Authentik) et concentre des points de défaillance sensibles (domaines/URLs en clair, secrets, incohérences de variables) — n'avait **aucun contrôle adversarial équivalent**.

L'humain (multica.gaston) a décidé une refonte de la Phase 3 pour corriger ces deux points, avec ADR à l'appui.

## Décision

**Réorganiser la Phase 3 et élargir le rôle QA**, en quatre volets :

1. **Terraform AVANT le docker-compose.** L'ordre de production de la Phase 3 devient :
   `autonomy-mode → terraform-configuration → docker-compose-creation → quality-assurance → central-quality-control`.
   - [`terraform-configuration.md`](../homelab/common/stages/production/terraform-configuration.md) : `requires_stage` rattaché à `autonomy-mode` (au lieu d'être placé après le QA) ; `consumes` = `parametres_requis_complets` (required) + `walking_skeleton_valide` (required) ; le passage QA est décrit en aval (Step 3).
   - [`docker-compose-creation.md`](../homelab/common/stages/production/docker-compose-creation.md) : `requires_stage` = `terraform-configuration` ; `consumes` ajoute `livrable_tfvars` (required sur `new-stack` / `infra-terraform`, déjà produit en amont).

2. **L'agent QA valide désormais aussi le Terraform.** La fiche de stage `docker-compose-qa.md` est **renommée** [`quality-assurance.md`](../homelab/common/stages/production/quality-assurance.md) et couvre **compose ET Terraform** : `consumes` = `livrable_tfvars` + `livrable_compose` ; `produces` ajoute `verdict_terraform` ; `scopes` ajoute `infra-terraform` ; imports du sensor `terraform-no-sni` ; volet Terraform porté par le skill `terraform-qa` ([ADR-0028](0028-creation-skill-terraform-qa.md)).

3. **Renommage `QA Docker` → `Analyste QA`.** Le rôle et l'agent sont renommés (Docker **et** Terraform). Fiche d'agent `qa-docker-agent.md` renommée [`analyste-qa-agent.md`](../homelab/agents/analyste-qa-agent.md) avec le skill `terraform-qa` rattaché ; jeton de rôle `qa-docker` → `analyste-qa` dans [`report-format.schema.json`](../homelab/common/protocols/report-format.schema.json) (enums `agent` et `domaine_correction`, « aligné sur les rôles du workflow ») ; artefact `rapport_qa_docker` → `rapport_qa`, `qa_docker_passe` → `qa_passe`.

4. **Sur scope `infra-terraform` : QA du seul Terraform.** Aucun compose n'étant produit sous ce scope, l'Analyste QA y vérifie **uniquement** le livrable Terraform ; la mention « ignoré sous infra-terraform » du volet QA est levée.

**Point de conception acté.** Terraform passant avant le compose, les valeurs des variables Terraform proviennent des **paramètres collectés en Cadrage (§2.4)**, et non plus d'une déduction depuis le docker-compose. Le skill `configuration-applications` (qui déduit auth / `cloudflare_dns_nb` / domaine depuis le compose) devra être **revu en conséquence** ou ses entrées réorientées vers les paramètres §2.4 (voir Conséquences, NEG-002).

**Périmètre du changement (contrat vivant uniquement).** conductor (table des phases + diagrammes mermaid : Terraform avant Docker, QA sur les deux livrables), `gates.md` (ordre interne de la frontière `phase3-phase4` — `.tfvars` produit et vérifié en premier ; exception bloquante ALI-204 sur `livrable_tfvars_present` **inchangée**), `reviewer.md` et `central-quality-control.md` (« tout compose passe par le QA » → « tout livrable, compose **et** Terraform, passe par l'Analyste QA »), `scopes-and-axes.md` (matrice réordonnée, `quality-assurance` actif sous `infra-terraform`), sensors, scopes, règles, `README` / `CHANGELOG` du plugin `homelab-assistant`. Les **enregistrements ADR historiques** (0013…0026) ne sont **pas réécrits** : leur prose est immuable ; le renommage ne vaut que pour le contrat vivant.

## Conséquences

### Positives

- **POS-001** : le livrable `.tfvars` est produit et vérifié **tôt** dans la Phase 3, ce qui rend impossible de le « déclasser » en fin de parcours comme sur HOM-214 — renforcé par l'exception bloquante ALI-204 (inchangée) à la frontière `phase3-phase4`.
- **POS-002** : couverture QA **symétrique** sur les deux livrables de stack (compose et Terraform), le contrôle adversarial du Terraform s'appuyant sur le skill dédié `terraform-qa` ([ADR-0028](0028-creation-skill-terraform-qa.md)).
- **POS-003** : les valeurs Terraform proviennent des paramètres §2.4 (source unique de cadrage), supprimant la déduction fragile depuis le compose et l'écart de cohérence qu'elle pouvait introduire.
- **POS-004** : renommage `Analyste QA` cohérent avec le périmètre élargi (Docker + Terraform), sans ambiguïté résiduelle dans le contrat vivant.
- **POS-005** : aucun invariant ni clause de sécurité modifié — refonte documentaire à posture de sécurité constante.

### Négatives

- **NEG-001** : jeton de rôle `qa-docker` → `analyste-qa` dans `report-format.schema.json` : les comptes-rendus A2A émis avant ce changement portaient `qa-docker`. Impact limité — ces rapports sont **éphémères** (pièces jointes d'issue, non persistées comme contrat de long terme) et le schéma impose l'alignement des jetons sur les rôles du workflow ; les runs postérieurs émettent `analyste-qa`.
- **NEG-002** : le skill `configuration-applications` déduit encore auth / `cloudflare_dns_nb` / domaine depuis le compose. Terraform passant désormais **avant** le compose, cette déduction est caduque : le skill doit être revu (entrées réorientées vers les paramètres §2.4) dans une itération dédiée. Tant que ce n'est pas fait, le Spécialiste Terraform s'appuie sur les paramètres §2.4 conformément à la fiche de stage mise à jour.
- **NEG-003** : le nom de fichier de stage change (`docker-compose-qa.md` → `quality-assurance.md`) et la fiche d'agent aussi (`qa-docker-agent.md` → `analyste-qa-agent.md`) : toute référence externe au dépôt (hors contrat vivant) devra suivre. Atténué : toutes les références **internes** au contrat vivant ont été mises à jour, et les ADR historiques conservent leurs anciens noms (prose immuable).

## Alternatives étudiées

### ALT-001 — Gate `pré-sécurité` intra-phase (envisagée puis abandonnée)

Introduire, à l'intérieur de la Phase 3, une **gate de pré-sécurité** dédiée qui aurait bloqué l'avancée tant que le livrable Terraform n'était pas produit et contrôlé, **sans** réordonner les stages ni élargir le rôle QA.

**Raison du rejet** : la gate n'aurait traité que le **symptôme** (Terraform oublié) sans corriger la **cause** (Terraform produit en dernier, déduction depuis le compose, absence de contrôle QA du Terraform). Elle aurait ajouté un mécanisme de blocage supplémentaire là où l'exception ALI-204 existante suffit déjà à rendre le `.tfvars` bloquant sur `new-stack` / `infra-terraform`. Réordonner la production (Terraform d'abord) et élargir le QA règle la cause à la racine, sans multiplier les gates.

### ALT-002 — Stage QA Terraform dédié, distinct du QA compose

Créer un stage QA Terraform **séparé** du QA compose plutôt que d'élargir un unique stage QA.

**Raison du rejet** : deux stages QA distincts auraient dupliqué la mécanique de revue adversariale (mêmes verdicts, même format de rapport, même agent) et fragmenté le rôle. Un **unique** stage `quality-assurance`, porté par un **unique** rôle `Analyste QA` couvrant les deux volets (skills `docker-composer` / `dockerfile-validator` pour le compose, `terraform-qa` pour le Terraform), est plus lisible et évite la divergence entre deux fiches QA.

## Notes d'implémentation

- **IMP-001** : fiches de stage `production/` réécrites — `terraform-configuration.md` (avant compose), `docker-compose-creation.md` (après Terraform, `consumes` `livrable_tfvars`), `quality-assurance.md` (nouveau nom, compose + Terraform), `autonomy-mode.md` et `central-quality-control.md` (rename + `requires_stage` sur `quality-assurance`).
- **IMP-002** : `conductor.md` (table des phases + diagrammes mermaid réordonnés), `sensors/gates.md` (frontière `phase3-phase4` : `.tfvars` en premier, `qa_docker_passe` → `qa_passe`, exception ALI-204 inchangée), `protocols/reviewer.md`, `protocols/scopes-and-axes.md` (matrice), `protocols/report-format.schema.json` (jeton de rôle).
- **IMP-003** : agent `analyste-qa-agent.md` (rename + skill `terraform-qa`) ; renommage `QA Docker` → `Analyste QA` propagé au triptyque `homelab/common/`, aux sensors, aux scopes, aux règles et au `README` / `CHANGELOG` du plugin ; **prose historique des ADR 0013…0026 laissée intacte**.
- **IMP-004** : l'**objet agent Multica** `QA Docker` (id `f20d1bca-ec23-422c-8cea-2558fea5eac4`) est renommé `Analyste QA`, ses instructions Multica mises à jour (périmètre Docker + Terraform) et le skill `terraform-qa` rattaché.
- **IMP-005** : validation humaine granulaire à obtenir en revue de PR (passage *Proposed* → *Accepted*, renseigner `accepté le`) ; pas de merge autonome sur `main`.

## Références

- **REF-001** : [ADR-0028 — Création du skill `terraform-qa`](0028-creation-skill-terraform-qa.md) — skill de vérification adversariale du Terraform rattaché à l'Analyste QA par la présente décision.
- **REF-002** : [ADR-0017 — Passage à 5 phases et mode autonomie (Homelab)](0017-passage-5-phases-et-mode-autonomie-homelab.md) — structure des 5 phases dont relève la Phase 3 réorganisée ici.
- **REF-003** : [ADR-0016 — Verification gates et sensors (Homelab)](0016-verification-gates-et-sensors-homelab.md) — exception bloquante ALI-204 sur `livrable_tfvars_present`, préservée.
- **REF-004** : [`homelab/common/stages/production/quality-assurance.md`](../homelab/common/stages/production/quality-assurance.md) — stage QA élargi (compose + Terraform).
- **REF-005** : [`homelab/agents/analyste-qa-agent.md`](../homelab/agents/analyste-qa-agent.md) — définition d'agent renommée.
- **REF-006** : incident **HOM-214** (FreeLLMAPI) — déclencheur de la refonte.
