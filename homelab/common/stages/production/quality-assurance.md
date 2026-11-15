---
slug: quality-assurance
phase: production
execution: CONDITIONAL
condition: "Vérification systématique de chaque livrable produit — compose ET Terraform (jamais sautée) ; ignoré sous branches autonomes. Sous infra-terraform : vérification du seul livrable Terraform (pas de compose)."
lead_agent: Analyste QA
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: Analyste QA
review_class: adversarial
review_artifact: rapport-qa.md
human_gate: granular
produces: [rapport_qa, coherence_traefik_verifiee, verdict_terraform]
consumes: [{artifact: livrable_tfvars, required: false}, {artifact: livrable_compose, required: false}]
requires_stage: [terraform-configuration, docker-compose-creation]
sensors: [swarm-deploy-section, plaintext-secret, traefik-coherence, terraform-no-sni]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Livrables produits : docker-compose et / ou configuration Terraform (.tfvars)"
outputs: "Rapport QA YAML par livrable (compose : syntaxe, Swarm, hardening, Traefik ; Terraform : structure HCL, template, variables, absence de ${SNI}/secret) — verdict OK / RENVOI / BLOQUE + classification (critical / warning / info) ; sur défaut, RENVOI rendu au Tech Lead, qui synthétise avec la revue sécurité avant tout renvoi au spécialiste créateur"
---

# Vérification qualité des livrables (Analyste QA)

## Objectif

Vérifier et durcir (par le contrôle) chaque livrable de la stack avant toute suite — **docker-compose ET configuration Terraform** — vérification obligatoire. **L'Analyste QA ne modifie jamais le livrable** : sur défaut, il émet un RENVOI dans son rapport YAML, adressé au Tech Lead (Step 5).

> **Périmètre par scope.** Sur `new-stack` / `stack-update` / `security-patch` : l'Analyste QA vérifie le Terraform **et** le compose, et — ces deux livrables étant produits **en parallèle** — porte explicitement la **réconciliation de leur cohérence croisée** (domaine / FQDN, auth, réseau Traefik) ; tout désaccord est rapporté au Tech Lead (synthèse unique, cf. Step 5). Sous `infra-terraform` : il vérifie **uniquement le Terraform** (aucun compose n'est produit). Sous `config-change` : au juste nécessaire selon les livrables présents.

## Steps

### Step 1 — Déléguer à l'Analyste QA

Le Tech Lead délègue à l'**Analyste QA** (mission + mention valide). Ordre imposé : **tout livrable (compose ou Terraform) passe par l'Analyste QA avant l'aiguillage du Tech Lead** ([`central-quality-control.md`](central-quality-control.md)). Compose et `.tfvars` étant produits en parallèle, l'Analyste QA les reçoit tous deux quand **tous** les livrables sont livrés (`in_review`). Le Tech Lead lance **dans le même tour** la revue sécurité ([`security-delegation`](security-delegation.md)) sur la même version : les deux revues sont parallèles et indépendantes.

**Une passe QA par version.** La QA contrôle une **version** du lot (compose et `.tfvars` ensemble), une seule fois. Elle produit **un rapport par livrable pour cette version**, avec tous les points d'un coup (numérotation `P1…` stable, aucun second rapport sur la même version, aucun renumérotage). Le Tech Lead ne relance la QA que sur une **nouvelle version**, c'est-à-dire quand **tous** les livrables renvoyés ont été corrigés. Une livraison partielle (un seul des deux livrables corrigés) ne déclenche aucun re-contrôle.

### Step 2 — Vérifier le Terraform (volet `.tfvars`, skill `terraform-qa`)

Sur les scopes produisant du Terraform, analyser le livrable `.tfvars` (skill `terraform-qa`) :

- Structure HCL.
- Conformité au template de configuration de stack.
- Cohérence des variables (dont `cloudflare_dns_nb`).
- **Absence de `${SNI}`** (domaines / URLs en clair) : critique.
- **Absence de secret en clair** : critique.
- Absence de toute exécution Terraform.

Classement et rapport :

1. Classer les problèmes (critical / warning / info).
2. Rédiger chaque point de façon **autosuffisante** (`constat` / `cause` / `correction` / `domaine_correction`) dans le rapport YAML (`report-format.schema.yaml`).
3. Au moins un défaut `critical` / `warning` : `verdict = RENVOI`, rapporté au **Tech Lead** (qui renvoie au Spécialiste Terraform après synthèse).
4. Sinon : `verdict = OK`.

### Step 3 — Analyser et classer le compose (revue adversariale — plancher SG-3)

Sur les scopes produisant un compose, analyser :

- Syntaxe.
- Compatibilité Swarm.
- Réseaux, volumes, secrets.
- Hardening (skill `docker-composer`).

Classement et rapport :

1. Classer les problèmes (critical / warning / info).
2. Rédiger chaque point de façon **autosuffisante** dans le rapport YAML.
3. Au moins un défaut : `verdict = RENVOI`, rapport rendu au **Tech Lead** (qui renvoie au Spécialiste Docker après synthèse).
4. Sans défaut : `verdict = OK`.

Règles propres au volet Docker :

- La skill `dockerfile-validator` s'applique **uniquement aux stacks *build-from-source*** (`Dockerfile` construit localement, `build:` dans le compose) : elle valide alors le `Dockerfile`.
- Stack tirant des **images publiées** : `dockerfile-validator` ne s'applique pas.
- L'Analyste QA porte le **contrôle sécurité technique** (revue adversariale) sur les deux livrables.
- Sur `security-patch` / `new-stack` : vérification `renforcé`, non abaissable.

### Step 4 — Cohérence Traefik

Vérifier via **`traefik-manager-read`** que services, middlewares et entrypoints sont cohérents (aucune `configErrors`). Présenter la conformité et, le cas échéant, le verdict `RENVOI` avec les `id` des points à corriger.

### Step 5 — Rapport au Tech Lead (aucune correction directe)

**La QA rend son rapport au Tech Lead et à lui seul.**

- Elle ne mentionne **jamais** le spécialiste créateur et ne déclenche aucune correction.
- La revue sécurité ([`security-delegation`](security-delegation.md)) tourne **en parallèle sur la même version**.
- Le Tech Lead **attend obligatoirement les deux rapports** avant toute suite.

Suite, dans l'ordre :

1. Le Tech Lead fait **une synthèse unique** : écarts dédoublonnés, classés, points à décision humaine isolés.
2. Si une décision est requise, il la présente à l'humain en un message ([`output-format`](../../protocols/output-format.md)).
3. Il délègue **un seul lot de correctifs par livrable**.
4. La QA et la revue sécurité font **une revue partielle**, en parallèle et **une seule fois**, de la version corrigée : uniquement les éléments corrigés et leurs effets directs (liste `points_corriges` fournie par le Tech Lead).

**L'Analyste QA ne s'adresse jamais à l'humain** : sur un rapport bloquant, le Tech Lead présente le point à l'humain.

**Statut des sous-issues.** Le Tech Lead passe la sous-issue du livrable à `done` quand QA **et** sécurité ont rendu `OK` ; un `RENVOI` la laisse en `in_review`. Cycle complet : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage).

Lorsque le(s) livrable(s) sont `OK`, l'Analyste QA **rend compte au Tech Lead** (l'Analyste QA construit lui-même son lien de retour — cf. Step 1) : la phase QA est passée, le travail finalisé est prêt pour le contrôle qualité central. L'Analyste QA **ne présente aucun livrable modifié** : il ne produit qu'un rapport.

## Sensors

Outputs: rapport(s) QA (compose et / ou Terraform) + cohérence Traefik + verdict Terraform. Gate humain granulaire **selon le mode d'exécution** ([`autonomy-mode`](autonomy-mode.md)) : gated → validation à ce stage ; autonome → regroupée au point de synchronisation.
Imports: `swarm-deploy-section` (gate) et `traefik-coherence` (gate), **lancés par la QA** (propriétaire). `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**) et `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**) sont **repris** du retour de l'auteur (`origine: repris`) si le `sha256` du livrable est identique, relancés sinon. Règle : [`governance-security.md`](../../protocols/governance-security.md) § « Un contrôle, un propriétaire ».
Review artifact: `rapport-qa.md` porte la section `## Review` (revue adversariale de l'Analyste QA, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de non-conformité récurrents compose ou Terraform, patterns de hardening, corrections QA répétées) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](../validation/closure.md)); toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2/SEC-4).
