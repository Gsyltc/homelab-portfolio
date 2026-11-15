---
slug: security-delegation
phase: production
execution: CONDITIONAL
condition: "En parallèle de la vérification QA, sur la même version des livrables, dès qu'un livrable touche une surface de sécurité (compose, Terraform, hardening, exposition, Traefik, secrets) — ignoré sous branches autonomes. Délégation Tech Lead → Architecte de sécurité Homelab."
lead_agent: Tech Lead Homelab
support_agents: [Architecte de sécurité Homelab]
mode: subagent
summary_confirmation: required
reviewer: Architecte de sécurité Homelab
review_class: adversarial
review_artifact: controle-securite.md
human_gate: granular
produces: [controle_securite_posture, branchement_gravite_securite]
consumes: [{artifact: livrable_tfvars, required: false}, {artifact: livrable_compose, required: false}]
requires_stage: [terraform-configuration, docker-compose-creation]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Livrables compose et / ou Terraform livrés (même version que celle soumise à la QA)"
outputs: "Jugement de posture sécurité (Architecte de sécurité Homelab) + branchement par gravité : critique/majeur → rapport au Tech Lead, qui seul interroge l'humain après synthèse avec la QA ; non critique → retour Tech Lead par mention valide ; le Tech Lead attend aussi le rapport QA avant toute suite"
---

# Délégation sécurité (Tech Lead → Architecte de sécurité Homelab)

> Étape de délégation sécurité **dédiée**, lancée **en parallèle** de la vérification QA
> ([`quality-assurance.md`](quality-assurance.md)), sur la **même version** des livrables. Elle **ne
> remplace jamais** le contrôle sécurité technique de l'Analyste QA (plancher SG-3) : elle ajoute le
> jugement de posture et formalise le **branchement par gravité**. Le Tech Lead **attend obligatoirement
> les deux rapports** (QA et sécurité) avant de synthétiser les écarts.

## Objectif

Faire porter à l'Architecte de sécurité Homelab le **jugement de posture** sur les livrables
(hardening, secrets, exposition réseau, permissions, cohérence Traefik, absence de
`${SNI}`), **en parallèle** de la QA, et router la suite selon la **gravité** des
constats.

## Steps

### Step 1 — Déléguer en parallèle de la QA

Quand tous les livrables sont livrés (`in_review`), le Tech Lead délègue à l'**Architecte de sécurité Homelab** (mission + mention valide, UUID résolu via `multica agent list --output json` — jamais figé) **dans le même tour** que la QA : jugement de posture sécurité sur les livrables, périmètre « sécurité de base d'un homelab ». Les deux revues portent sur la **même version** ; aucune des deux n'attend l'autre. (Ordre normatif contrôle sécurité → validation humaine : [`governance-security.md` § Contrôle sécurité systématique](../../protocols/governance-security.md#contrôle-sécurité-systématique).)

### Step 2 — Jugement de posture et classification

L'Architecte de sécurité Homelab juge la posture et **classe** les constats par gravité (**critique / majeur** vs **non critique / mineur**), chaque point rédigé de façon autosuffisante (`constat` / `cause` / `correction` / `domaine_correction`), puis **rend compte au Tech Lead** par mention valide (lien de retour construit par l'Architecte).

### Step 3 — Synthèse avec la QA, puis branchement par gravité

**Seul le Tech Lead parle à l'humain.** L'Architecte de sécurité et l'Analyste QA ne sollicitent jamais l'humain, même sur un constat critique, bloquant ou à décision. Ils déposent leur **rapport YAML** et mentionnent le Tech Lead. Sur un rapport bloquant (`verdict = BLOQUE`, constat critique / majeur, `arbitrage_requis: true`), c'est le Tech Lead qui passe l'issue `blocked` et s'adresse à l'humain, après avoir reçu les deux rapports.

**Revue partielle.** Au re-contrôle, la QA et la sécurité ne revoient que les **éléments corrigés** : le Tech Lead leur transmet dans le message A2A la liste des `id` de points corrigés (`points_corriges`) avec le livrable corrigé. Chaque reviewer vérifie ces éléments et leurs **effets directs** (ex. une variable renommée, la cohérence Traefik ou la cohérence compose ↔ tfvars qu'elle touche) ; il ne refait pas la revue complète. Sur un effet de bord nouveau, il l'ajoute comme **nouveau point** dans son rapport. Une version qui apporte des modifications hors liste est signalée par le reviewer au Tech Lead.

Le Tech Lead **attend les deux rapports** (QA et sécurité), obligatoirement, puis produit **une synthèse unique** : écarts dédoublonnés (un même défaut vu par les deux revues compte une fois), classés par gravité, points à décision humaine isolés. Aucun correctif n'est délégué avant cette synthèse.

- **Au moins un constat critique / majeur, ou un point à décision humaine.** Issue `blocked`. Le Tech Lead présente **toute la synthèse en un message** ([`output-format`](../../protocols/output-format.md), proposition par défaut par décision) ; l'humain tranche élément par élément :
  - **Modify** → un seul lot de correctifs par livrable (Docker / Terraform), puis QA **et** sécurité font une **revue partielle** de la nouvelle version, **en parallèle, une fois** (voir « Revue partielle » ci-dessous).
  - **Redo** → retour en Production sur le livrable concerné, même boucle.

  La revue sécurité n'est **close** (`controle_securite_posture`) que lorsqu'il ne reste aucun constat critique / majeur. La [validation humaine granulaire](../validation/human-granular-validation.md) ne reçoit que des livrables dont la revue sécurité est close.
- **Constats non critiques seulement, sans décision humaine.** Le Tech Lead délègue un seul lot de correctifs par livrable, puis revue partielle unique (QA et sécurité en parallèle). Les constats mineurs restants sont listés dans la validation humaine granulaire.

Quel que soit le branchement, les **invariants non contournables** restent pleins (liste
autoritaire : [`governance-security.md` § Invariants non contournables](../../protocols/governance-security.md#invariants-non-contournables)).

## Sensors

Outputs: jugement de posture sécurité + branchement par gravité consigné (piste d'audit sur l'issue).
Aucun sensor déclaré : l'Architecte de sécurité **ne relance rien** et **consomme** les verdicts de l'auteur et de la QA (`sensors_resultats`, même `sha256`) pour porter son jugement de posture. Règle : [`governance-security.md`](../../protocols/governance-security.md) § « Un contrôle, un propriétaire ». Les sensors bloquants (`plaintext-secret`, `terraform-no-sni`) restent bloquants chez leur propriétaire.
Review artifact: `controle-securite.md` porte la section `## Review` (revue adversariale de l'Architecte de sécurité Homelab, plancher SG-3 — jamais portée / remplacée / conditionnée par un gate / sensor advisory).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de posture récurrents, branchements de gravité) tracés, remontés au **gate humain granulaire** ; toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2 / SEC-4).
