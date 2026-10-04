---
slug: security-delegation
phase: production
execution: CONDITIONAL
condition: "Après le contrôle qualité central (travail finalisé), dès qu'un livrable touche une surface de sécurité (compose, Terraform, hardening, exposition, Traefik, secrets) — ignoré sous branches autonomes. Délégation Tech Lead → Architecte de sécurité Homelab."
lead_agent: Tech Lead Homelab
support_agents: [Architecte de sécurité Homelab]
mode: subagent
summary_confirmation: required
reviewer: Architecte de sécurité Homelab
review_class: adversarial
review_artifact: controle-securite.md
human_gate: granular
produces: [controle_securite_posture, branchement_gravite_securite]
consumes: [{artifact: controle_qualite_central_go, required: true}, {artifact: rapport_qa, required: false}, {artifact: livrable_tfvars, required: false}, {artifact: livrable_compose, required: false}]
requires_stage: [central-quality-control]
sensors: [plaintext-secret, terraform-no-sni, traefik-coherence]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Travail finalisé et contrôlé par le Tech Lead (contrôle qualité central GO), livrables compose et / ou Terraform"
outputs: "Jugement de posture sécurité (Architecte de sécurité Homelab) + branchement par gravité : critique/majeur → validation humaine granulaire (escalade « Gate renforcée ») ; non critique → retour Tech Lead par mention valide"
---

# Délégation sécurité (Tech Lead → Architecte de sécurité Homelab)

> Étape de délégation sécurité **dédiée**, placée **après** le contrôle qualité central
> ([`central-quality-control.md`](central-quality-control.md)) : le Tech Lead contrôle d'abord
> le travail finalisé, puis délègue le **jugement de posture** à l'Architecte de sécurité
> Homelab. Elle **ne remplace jamais** le contrôle sécurité technique de l'Analyste QA (porté
> pendant la QA, plancher SG-3) : elle ajoute le jugement de posture et formalise le
> **branchement par gravité**.

## Objectif

Faire porter à l'Architecte de sécurité Homelab le **jugement de posture** sur le travail
finalisé (hardening, secrets, exposition réseau, permissions, cohérence Traefik, absence de
`${SNI}`), **après** le contrôle qualité central, et router la suite selon la **gravité** des
constats.

## Steps

### Step 1 — Déléguer après le contrôle qualité central

Une fois le contrôle qualité central en `GO` (travail finalisé, cf.
[`central-quality-control.md`](central-quality-control.md)), le Tech Lead délègue à
l'**Architecte de sécurité Homelab** (mission + mention valide, UUID résolu via
`multica agent list --output json` — jamais figé) : jugement de posture sécurité sur les
livrables, périmètre « sécurité de base d'un homelab ». (Le contrôle sécurité **précède
toujours** la validation humaine sur toute surface de sécurité — règle normative portée par
[`governance-security.md` § Contrôle sécurité systématique](../../protocols/governance-security.md#contrôle-sécurité-systématique).)

### Step 2 — Jugement de posture et classification

L'Architecte de sécurité Homelab juge la posture et **classe** les constats par gravité
(**critique / majeur** vs **non critique / mineur**), chaque point rédigé de façon
autosuffisante (`constat` / `cause` / `correction` / `domaine_correction`), puis **rend
compte au Tech Lead** par mention valide (lien de retour construit par l'Architecte).

### Step 3 — Branchement par gravité

- **Éléments critiques / majeurs.** L'Architecte mentionne le Tech Lead ; le Tech Lead
  **escalade à l'humain via la [validation humaine granulaire](../validation/human-granular-validation.md)**.
  L'humain tranche **choix par choix** :
  - **Modify** → le Tech Lead **mentionne les spécialistes concernés** (Docker / Terraform) ;
    retour par mention valide, re-contrôle QA, puis re-passage par cette étape.
  - **Redo / refus** → le Tech Lead **télécharge le fichier** pour **validation granulaire**
    élément par élément.
- **Éléments non critiques / mineurs.** **Retour explicite au Tech Lead par mention valide** ;
  le Tech Lead intègre, puis poursuit vers la validation humaine granulaire.

Quel que soit le branchement, les **invariants non contournables** restent pleins (liste
autoritaire : [`governance-security.md` § Invariants non contournables](../../protocols/governance-security.md#invariants-non-contournables)).

## Sensors

Outputs: jugement de posture sécurité + branchement par gravité consigné (piste d'audit sur l'issue).
Imports: `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204), `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**), `traefik-coherence` (gate).
Review artifact: `controle-securite.md` porte la section `## Review` (revue adversariale de l'Architecte de sécurité Homelab, plancher SG-3 — jamais portée / remplacée / conditionnée par un gate / sensor advisory).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de posture récurrents, branchements de gravité) tracés, remontés au **gate humain granulaire** ; toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2 / SEC-4).
