# Création du skill `terraform-qa` (vérification adversariale d'une configuration Terraform)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-24
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine granulaire explicite obtenue (multica.gaston, 2026-09-24, HOM-216 : « Merge effectué. Adr-0028 acceptée par Sylvain »). Aucune posture de sécurité n'est modifiée : le skill `terraform-qa` est un **asset de skill** (outil de travail de vérification, advisory par nature), sans couplage `core → plugin` ni sensor modifié. La PR portant le skill et cet ADR ([homelab-portfolio#167](https://github.com/Gsyltc/homelab-portfolio/pull/167)) est mergée sur `main`.

## Contexte

À la suite de l'incident **HOM-214** et de la décision d'**élargir le rôle QA au Terraform** (réorganisation du workflow tracée dans [ADR-0027](0027-reorganisation-workflow-qa-terraform.md)), l'agent QA — renommé **Analyste QA** — voit son périmètre étendu à la vérification des livrables Terraform, en miroir de ce qui existe déjà côté Docker Compose.

Côté génération, deux skills couvraient déjà la production de livrables :

- `docker-composer` — génération d'un `docker-compose.yml` de stack ;
- `configuration-applications` — production du fichier de configuration Terraform d'une stack, dont [`references/template-stack.md`](../plugins/homelab-assistant/skills/configuration-applications/references/template-stack.md) est le format de sortie officiel.

Mais **aucun skill dédié** ne décrivait comment **vérifier** un fichier de configuration Terraform (`.tf` / `.tfvars`) de façon adversariale et autonome. L'Analyste QA disposait de la matière côté compose (validation de livrables Docker) sans équivalent côté Terraform, alors même que ces fichiers alimentent directement les playbooks Terraform (`cloudflare`, `swarm`, `updatime_kuma`, configuration Authentik) et concentrent des points de défaillance sensibles (domaines/URLs en clair, secrets en clair, incohérences de variables).

## Décision

**Créer le skill `terraform-qa`** à l'emplacement
[`plugins/homelab-assistant/skills/terraform-qa/SKILL.md`](../plugins/homelab-assistant/skills/terraform-qa/SKILL.md), dédié à la **vérification adversariale** d'un fichier de configuration Terraform.

Caractéristiques de la décision :

- **Skill agnostique du workflow.** Le skill décrit **uniquement** comment vérifier un fichier `.tf` / `.tfvars`. Il ne référence **aucune** phase, aucun agent (Analyste QA, André…), aucun scope, aucun ordre d'exécution, ni aucun format de rapport propre au contrat (ALI-204, SG-3, `report-format.schema.json`). Le rattachement du skill à l'agent `Analyste QA` et son intégration au workflow sont traités **côté workflow**, dans [ADR-0027](0027-reorganisation-workflow-qa-terraform.md).
- **Rôle adversarial en lecture seule.** Le skill contrôle et classifie ; il ne modifie jamais le fichier et n'exécute jamais Terraform. Sur défaut → RENVOI à l'auteur ; sinon → OK.
- **Six points de contrôle** : (1) syntaxe & structure HCL, (2) conformité au template de configuration de stack, (3) cohérence des variables (dont `cloudflare_dns_nb` = nombre d'hôtes publics distincts), (4) absence de `${SNI}` (domaines/URLs en clair) — critique, (5) absence de secret en clair — critique, (6) absence d'exécution Terraform.
- **Sortie** : rapport structuré autosuffisant (`verdict` OK / RENVOI / BLOQUE ; par point `constat` / `cause` / `correction` / `domaine_correction` ; classification `critical` / `warning` / `info` ; RENVOI dès un point `critical` ou `warning`).
- **Description du frontmatter < 250 caractères** (233 car.), conforme à la contrainte de format des skills.
- **Externalisation ciblée** : la règle de déduction de `cloudflare_dns_nb` est placée dans [`references/cloudflare-dns-nb.md`](../plugins/homelab-assistant/skills/terraform-qa/references/cloudflare-dns-nb.md) ; le format à vérifier reste porté par le template existant [`configuration-applications/references/template-stack.md`](../plugins/homelab-assistant/skills/configuration-applications/references/template-stack.md), cité comme source de vérité sans coupler le skill au workflow.

## Conséquences

### Positives

- **POS-001** : l'Analyste QA dispose d'un skill de vérification Terraform dédié, en miroir du volet Docker Compose — couverture QA symétrique sur les deux types de livrables de stack.
- **POS-002** : skill **réutilisable** hors de tout workflow (agnostique) : il peut servir toute relecture d'un `.tf` / `.tfvars`, indépendamment des phases, agents ou scopes.
- **POS-003** : les défauts les plus sensibles (`${SNI}` en clair, secret en clair) sont explicitement classés `critical`, réduisant le risque de fuite de domaine/URL ou de secret via un fichier de configuration.
- **POS-004** : aucun couplage `core → plugin`, aucun sensor modifié, caractère advisory préservé.

### Négatives

- **NEG-001** : cohérence à maintenir entre le skill `terraform-qa` (points de contrôle 2 et 3) et le template `configuration-applications/references/template-stack.md` s'il évolue ; atténuée par la citation du template comme source de vérité (pas de duplication du format).
- **NEG-002** : l'intégration au workflow (rattachement à l'Analyste QA, ordonnancement, format de rapport contractuel) n'est **pas** portée par ce skill ; elle dépend d'[ADR-0027](0027-reorganisation-workflow-qa-terraform.md) et doit rester cohérente avec elle.

## Alternatives étudiées

### ALT-001 — Étendre le skill `configuration-applications` avec un mode « vérification »

Ajouter la vérification adversariale au skill de génération existant plutôt qu'un skill dédié.

**Raison du rejet** : mêlerait production et contrôle adversarial dans un même asset, brouillant la séparation des rôles (auteur vs vérificateur). Un skill de vérification distinct, agnostique du workflow, est réutilisable et clarifie le rôle adversarial en lecture seule.

### ALT-002 — Décrire la vérification Terraform directement dans le workflow / la définition de l'Analyste QA

Porter les points de contrôle dans les fichiers de workflow (`homelab/common/`) ou dans la définition de l'agent.

**Raison du rejet** : coupler la logique de vérification au workflow la rendrait non réutilisable et dupliquerait la connaissance du format. La contrainte forte de HOM-216 est précisément un skill **agnostique du workflow** ; l'intégration reste tracée séparément dans [ADR-0027](0027-reorganisation-workflow-qa-terraform.md).

## Notes d'implémentation

- **IMP-001** : [`plugins/homelab-assistant/skills/terraform-qa/SKILL.md`](../plugins/homelab-assistant/skills/terraform-qa/SKILL.md) — frontmatter (`name: terraform-qa`, `description` 233 car.), rôle adversarial en lecture seule, objectif, « ce que le skill ne fait pas », six points de contrôle, format de sortie et règle de verdict, table de référence. Aucune mention de phase / agent / scope / format de rapport contractuel.
- **IMP-002** : [`plugins/homelab-assistant/skills/terraform-qa/references/cloudflare-dns-nb.md`](../plugins/homelab-assistant/skills/terraform-qa/references/cloudflare-dns-nb.md) — règle de déduction de `cloudflare_dns_nb` (nombre d'hôtes publics distincts) et cas limites, externalisée pour le point de contrôle 3.
- **IMP-003** : le format vérifié n'est pas dupliqué : le skill cite [`configuration-applications/references/template-stack.md`](../plugins/homelab-assistant/skills/configuration-applications/references/template-stack.md) comme source de vérité.
- **IMP-004** : validation humaine granulaire obtenue (multica.gaston, 2026-09-24, HOM-216) ; passage *Proposed* → *Accepted* et `accepté le` renseigné. PR [homelab-portfolio#167](https://github.com/Gsyltc/homelab-portfolio/pull/167) mergée sur `main` (pas de merge autonome).

## Références

- **REF-001** : [ADR-0027 — Réorganisation du workflow : élargissement du rôle QA au Terraform (Analyste QA)](0027-reorganisation-workflow-qa-terraform.md) — rattachement du skill `terraform-qa` à l'agent et intégration au workflow.
- **REF-002** : [`plugins/homelab-assistant/skills/terraform-qa/SKILL.md`](../plugins/homelab-assistant/skills/terraform-qa/SKILL.md) — skill créé par cette décision.
- **REF-003** : [`plugins/homelab-assistant/skills/configuration-applications/references/template-stack.md`](../plugins/homelab-assistant/skills/configuration-applications/references/template-stack.md) — template de configuration de stack (format de sortie officiel vérifié par le skill).
- **REF-004** : [`plugins/homelab-assistant/skills/docker-composer/SKILL.md`](../plugins/homelab-assistant/skills/docker-composer/SKILL.md) — skill de génération côté Docker Compose, miroir de génération du volet vérifié ici.
