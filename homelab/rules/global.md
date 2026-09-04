# Règles — couche `global`

Règles valables pour **tout le Homelab**, chargées au démarrage de chaque workflow. Couche de plus forte précédence. Toute règle ajoutée ici passe par un **contrôle sécurité systématique** de l'**Architecte de sécurité Homelab** à l'admission (voir « Boucle d'apprentissage » dans le README).

Pendant Homelab de [`../../core/rules/workspace.md`](../../core/rules/workspace.md).

Ces règles reprennent les **invariants non négociables** du workflow Homelab — elles ne peuvent pas être affaiblies par une couche inférieure ni par un override :

## Gouvernance et validation

- **RULE-GL-001** — Validation humaine granulaire avant toute action à impact (dépôt de fichiers dans les répertoires de travail, déclenchement de flux Kestra) — NON négociable.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-002** — Chaque décision structurante est tracée dans un ADR ; aucune décision acceptée sans validation humaine.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-003** — La piste d'audit vit sur l'issue Multica ; on ajoute des commentaires, on n'écrase jamais l'historique.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-004** — Un seul traitement en cours par stack (verrou metadata `active_step`) ; toute tentative de traitement concurrent est bloquée et remontée à l'humain.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03

## Sécurité / Hardening

- **RULE-GL-005** — Aucun secret en clair dans un livrable (docker-compose, Terraform, config). Utiliser systématiquement `_FILE` ou Docker secrets.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-006** — Jamais `${SNI}` dans un fichier Terraform livré — interpolation locale interdite dans les livrables.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-007** — Terraform ne déploie JAMAIS : `terraform init`, `apply`, `destroy` sont interdits. Seul le `.tfvars` est livré.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03

## Conventions Docker/Swarm

- **RULE-GL-008** — Tout docker-compose Swarm doit inclure une section `deploy` avec contraintes de placement et ressources.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03
- **RULE-GL-009** — Les réseaux doivent être déclarés `external: true` pour les réseaux partagés (ex. `traefik-public`).
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03

## Règles métier Homelab

- **RULE-GL-010** — Règle absolue n8n (§1.1) : toute demande n8n déclenche le scope `n8n` et une délégation immédiate à l'Expert N8n — pas même l'analyse par le Tech Lead.
  - _portée_ : global · _origine_ : homelab-workflow.md §1.1 · _ajoutée le_ : 2026-09-03
- **RULE-GL-011** — Sélection automatique du type d'authentification : `oidc → forwardauth → local` (§1.4) ; en cas de doute → humain.
  - _portée_ : global · _origine_ : homelab-workflow.md §1.4 · _ajoutée le_ : 2026-09-03
- **RULE-GL-012** — Règle préalable universelle de documentation officielle : avant toute modification, la documentation officielle du composant est consultée et le lien est consigné sur l'issue.
  - _portée_ : global · _origine_ : homelab-workflow.md · _ajoutée le_ : 2026-09-03

> Les nouvelles règles apprises de portée `global` sont ajoutées ci-dessous, après confirmation humaine **et** contrôle sécurité.
