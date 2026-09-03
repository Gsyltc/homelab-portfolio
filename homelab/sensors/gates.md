# Verification gates Homelab — contrôle de traçabilité aux frontières de phases

Manifeste déclaratif des **verification gates** du workflow Homelab, référencés par le triptyque [`homelab/common/`](../common/conductor.md) (source unique — voir [`conductor.md`](../common/conductor.md), « Verification gates aux frontières de phases ») et exécutés aux **frontières de phases** par le **Tech Lead Homelab**. **Advisory** : produit un « Rapport de vérification » sur l'issue, **ne bloque jamais** la validation humaine granulaire. Vue narrative historique (stub) : [`docs/homelab-workflow.md`](../../docs/homelab-workflow.md).

Pendant Homelab de [`../../core/sensors/gates.md`](../../core/sensors/gates.md) : même forme déclarative, **frontières et artefacts spécifiques au Homelab** (documentation officielle, paramètres requis §2.4, livrables compose + `.tfvars`, QA Docker, prérequis de déploiement §4.0).

À chaque **frontière de phase**, en amont de la validation humaine, trois contrôles déterministes :

1. **`artefacts-presents`** — les artefacts requis en sortie de phase existent.
2. **`liaison-tracabilite`** — chaque paramètre / décision retenu est relié à la demande, aux paramètres collectés (§2.4) ou à un ADR ; chaque décision structurante est tracée en ADR.
3. **`absence-orphelin`** — aucun livrable (compose, `.tfvars`) ni décision n'est déconnecté (sans paramètre amont ni référence).

## Frontières et artefacts requis

> Adossé aux **5 phases** du workflow Homelab (Phase 0 Initialisation / Phase 1 Idéation / Phase 2 Cadrage et Paramètres / Phase 3 Production et Contrôle / Phase 4 Validation et Déploiement — [ADR-0017](../../decisions/0017-passage-5-phases-et-mode-autonomie-homelab.md), triptyque [`homelab/common/`](../common/conductor.md) au Stage 7). Le prérequis de déploiement **§3.0 devient §4.0** ; le rappel advisory anticipé est en §0.3.

```yaml
type: verification-gates
nature: advisory
origine: ALI-204
boundaries:
  - id: entree-phase0
    frontiere: "Demande → Phase 0 (Initialisation)"
    artefacts_requis:
      - demande_brute_consignee            # entrée brute sur l'issue (§0.4)
      - label_homelab_pose                 # label Homelab (+ Docker Swarm si compose)
      - detection_stack                    # stack existante vs nouvelle consignée (§0.1)
      - verrou_concurrence_lu              # active_step lu (§0.2)
    checks: [artefacts-presents]

  - id: phase0-phase1
    frontiere: "Phase 0 → Phase 1 (Initialisation → Idéation)"
    artefacts_requis:
      - intention_capturee                 # intention consignée (§1.1)
      - scope_propose                      # scope auto-détecté (§1.2, homelab/scopes/)
    checks: [artefacts-presents]

  - id: phase1-phase2
    frontiere: "Phase 1 → Phase 2 (Idéation → Cadrage)"
    artefacts_requis:
      - scope_confirme                     # scope confirmé au gate léger (§1.3)
      - intention_perimetre_approuves      # gate humain léger (§1.3)
      - arbitrage_swarm_proxmox_amorce     # conditionnel : arbitrage amorcé (§1.2)
    checks: [artefacts-presents]

  - id: phase2-phase3
    frontiere: "Phase 2 → Phase 3 (Cadrage → Production)"
    artefacts_requis:
      - lien_documentation_officielle      # règle préalable de documentation officielle (§2.2)
      - parametres_requis_complets         # tous les paramètres §2.4 renseignés (${stack_name}, ${traefik_network}, …)
      - arbitrage_swarm_proxmox            # conditionnel : si les deux existent (§2.3)
      - auth_type_fige_ou_reporte          # §2.4 : choisi automatiquement ou arbitré par l'humain
    checks: [artefacts-presents, liaison-tracabilite]
    # note : le lien de documentation officielle est un artefact requis PROPRE au Homelab

  - id: phase3-phase4
    frontiere: "Phase 3 → Phase 4 (Production → Validation)"
    artefacts_requis:
      - livrable_compose_present           # docker-compose téléchargeable (§3.1)
      - livrable_tfvars_present            # config Terraform .tfvars (§3.3) — conditionnel selon scope
      - qa_docker_passe                    # vérification QA Docker rendue et contrôlée (§3.2)
      - controle_qualite_central_go        # aiguillage GO du Tech Lead (§3.6)
    checks: [artefacts-presents, liaison-tracabilite, absence-orphelin]
    sensors: [yaml-validity, swarm-deploy-section, plaintext-secret, terraform-no-sni, traefik-coherence]
    prerequis_40:                          # prérequis de déploiement anticipés (§4.0)
      - repertoire_travail_defini          # variable [répertoire de travail] définie et non vide
      - flux_kestra_accessible             # flux Kestra configure_service accessible
    # en cas de prérequis §4.0 manquant : signaler, ne pas promettre le déploiement automatique

  - id: phase4-cloture
    frontiere: "Phase 4 → Clôture (Validation → Done)"
    artefacts_requis:
      - validation_humaine_explicite       # §4.2 — chaque élément validé séparément
      - depot_fichiers_confirme            # §4.3 — chemins confirmés + fichiers vérifiés
      - deploiement_kestra_si_demande      # §4.4 — conditionnel, sur « oui » explicite
    checks: [artefacts-presents]
    sensors: [vault-secret-exists]         # actif (ALI-204), existence seule, jamais la valeur
```

## Articulation avec les prérequis §4.0

Le contrôle `phase3-phase4` **anticipe** les prérequis de déploiement du §4.0 (`[répertoire de travail]` défini, flux Kestra `configure_service` accessible) : il les vérifie **avant** d'entrer en Phase 4, pour éviter qu'un prérequis manquant ne fasse échouer silencieusement le dépôt (§4.3) ou ne bloque le §4.4 sans explication. C'est le pendant automatisé et anticipé du garde-fou §4.0, qui reste par ailleurs le contrôle bloquant de référence exécuté par le Tech Lead en entrée de Phase 4.

## En cas d'écart (advisory)

- Le Tech Lead Homelab **ne bloque pas** : il **signale l'écart** dans le « Rapport de vérification » sur l'issue et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.
- Le gate automatique ne remplace, n'abaisse ni ne court-circuite jamais la validation humaine granulaire, le QA Docker systématique ni les garde-fous absolus (invariants non négociables — SG-3).
- Un écart advisory récurrent peut alimenter un **candidat-règle** de la boucle d'apprentissage ([`homelab/rules/`](../rules/README.md)), sans court-circuiter la validation (`SENSOR_PROPOSED`).

## Rapport de gate (piste d'audit)

Posté en commentaire sur l'issue, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (non exécuté / en erreur / hors périmètre — **jamais lu comme conforme**, SG-2). Le rapport porte sa **source** (manifeste + commit) pour être non répudiable (SG-5).

```
Rapport de vérification — <frontière>   (source : homelab/sensors/gates.md @ <commit>)
- artefacts-presents : ✅ | ⚠️ <artefact manquant> | ⛔ <indisponible>
- liaison-tracabilite : ✅ | ⚠️ <paramètre / décision sans amont ni ADR> | ⛔ <indisponible>
- absence-orphelin : ✅ | ⚠️ <livrable / décision orphelin> | ⛔ <indisponible>
- prérequis §4.0 (frontière Phase 3 → Phase 4) : ✅ | ⚠️ <[répertoire de travail] / Kestra> | ⛔ <indisponible>
```
