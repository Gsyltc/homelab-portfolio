# Retrait temporaire de SAML et LDAP de la sélection d'authentification Homelab

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — décision humaine explicite (multica.gaston, issue HOM-147, commentaire du 2026-09-03 : « A2 : retire saml et ldap. Ajoute une ADR qu'il faudra les ajouter ultérieurement et trace les actions qui seront nécessaires »). Cet ADR **trace** un retrait et les actions de ré-intégration ; il n'introduit aucune nouvelle surface d'exécution et ne touche à aucun secret.

## Contexte

L'analyse du workflow Homelab menée sur l'issue **HOM-147** (confrontation workflow `homelab/common/` ↔ skills du plugin `homelab-assistant`) a mis en évidence une **incohérence de périmètre** sur les types d'authentification (action A2) :

- Le **workflow** imposait un ordre de sélection automatique à **cinq valeurs** :
  `oidc → saml → ldap → forwardauth → local` (dans `conductor.md`, `stages/ideation/auth-preselection.md`, `stages/cadrage/required-parameters-collection.md`, `protocols/governance-security.md`, `rules/global.md` — RULE-GL-011, `rules/README.md`, `scopes/README.md`).
- Les **skills** ne couvraient pas ces cinq valeurs :
  - `configuration-applications/references/network.md` (skill `docker-composer`) mappait seulement `none / local / oidc / forwardauth` vers des middlewares `@file` — **ni `saml` ni `ldap`** ;
  - `configuration-applications/references/authentification.md` documentait `SAML` avec la mention explicite « — (aucun à ce jour) » côté middleware Homelab ;
  - **`ldap` n'était traité nulle part** côté skill (aucun middleware, aucun bloc de template).

Autrement dit, `saml` et `ldap` figuraient dans la règle de priorité **sans implémentation réelle** (pas de middleware Traefik `@file`, pas de playbook Authentik consommant un bloc dédié fiable). Un agent appliquant la règle pouvait « choisir » `saml`/`ldap` sans qu'aucune brique aval ne sache les matérialiser.

## Décision

**Retirer `saml` et `ldap`** de la sélection d'authentification du Homelab, sur toute la chaîne workflow + skill, jusqu'à leur ré-implémentation complète et tracée.

### Portée effective du retrait (état après cette décision)

- **Ordre de sélection** ramené à : `oidc → forwardauth → local`.
- **Valeurs `${auth_type}` autorisées** : `none`, `local`, `forwardauth`, `oidc`.
- Une stack requérant SAML ou LDAP est **remontée à l'humain** (aucun choix implicite).

### Fichiers modifiés par le retrait

**Workflow (`homelab/`)**

| Fichier | Modification |
|---|---|
| `common/conductor.md` | Ordre d'auth (règle préalable + garde-fous) ramené à `oidc → forwardauth → local` ; suppression de la référence à la skill fantôme `homelab-stack-workflow` (action A1). |
| `common/stages/ideation/auth-preselection.md` | Ordre d'auto-sélection mis à jour. |
| `common/stages/cadrage/required-parameters-collection.md` | Valeurs `${auth_type}` (`none/local/forwardauth/oidc`) ; liste numérotée d'auto-sélection à 3 entrées ; note « SAML/LDAP non supportés ». |
| `common/protocols/governance-security.md` | Invariant §2 auth mis à jour. |
| `rules/global.md` | RULE-GL-011 mise à jour. |
| `rules/README.md`, `scopes/README.md` | Rappels de l'ordre d'auth mis à jour. |

**Skill `configuration-applications` (plugin `homelab-assistant`)**

| Fichier | Modification |
|---|---|
| `SKILL.md` | `description` (Authentik OAuth/ForwardAuth) ; « quatre cas » → « trois cas » (aucune / ForwardAuth / OAuth) ; règle transverse « deux modes Authentik » + note SAML/LDAP non supportés. |
| `references/authentification.md` | Ligne SAML de la table de décision transformée en marqueur « retiré » ; retrait de SAML de la table de correspondance template ; note de ré-intégration. |
| `references/template-stack.md` | Bloc HCL `saml`/`saml_description`/`acs_url` retiré du template ; section doc « mode SAML » transformée en marqueur « retiré » ; note `publisher` limitée à OAuth. |

## Actions nécessaires pour la ré-intégration ultérieure

Ces actions sont **requises avant** de ré-autoriser `saml` et/ou `ldap` dans l'ordre de sélection. À traiter dans une issue dédiée le moment venu.

### SAML

1. **Middleware Traefik** : définir et documenter un middleware `@file` officiel du Homelab pour SAML (colonne « Middleware(s) du Homelab » de `authentification.md`, aujourd'hui « — »), et l'ajouter à la table `${auth_type} → ${auth_label}` de `configuration-applications/references/network.md` (skill `docker-composer`).
2. **Template Terraform** : restaurer le bloc `saml`, `saml_description`, `acs_url` dans `template-stack.md` (HCL + doc des variables) ; confirmer que le playbook Authentik consomme bien ces variables (boucle `meta_publisher` SAML).
3. **Détection** : restaurer la ligne SAML de la table de décision de `authentification.md` (indices : `SAML_METADATA_URL`, `SAML_ENTITY_ID`, chemin ACS, URLs Authentik `/application/saml/<slug>/…`) et les cas limites (`forwardAuth` + variables SAML → humain).
4. **Workflow** : réinsérer `saml` dans l'ordre `oidc → saml → forwardauth → local` (ou position validée) dans les 7 emplacements listés ci-dessus + valeur `${auth_type}`.

### LDAP

1. **Décision d'architecture d'auth** : statuer sur la manière dont LDAP s'intègre au Homelab (proxy Authentik LDAP outpost vs middleware dédié) — LDAP n'a **jamais** eu de brique aval, contrairement à SAML.
2. **Middleware / mécanisme** : définir le mécanisme concret (middleware `@file` ou intégration applicative) et le documenter dans `network.md` + `authentification.md`.
3. **Template Terraform** : si des variables sont nécessaires, les ajouter au template et au playbook.
4. **Workflow** : réinsérer `ldap` à la position validée dans l'ordre de sélection + valeur `${auth_type}`.

### Commun

- Mettre à jour cet ADR (`superseded_by`) et RULE-GL-011 ; valider la ré-intégration au **gate humain granulaire** ; repasser au contrôle sécurité (Architecte de sécurité Homelab) toute règle touchant l'authentification (SEC-2/SEC-4).

## Conséquences

- **Positif** : la règle de sélection ne propose plus que des types réellement implémentés (plus de choix « fantôme » ingérable en aval) ; cohérence workflow ↔ skill rétablie sur l'authentification.
- **Négatif / limite** : une stack nécessitant SAML/LDAP ne peut pas être configurée automatiquement ; elle est remontée à l'humain jusqu'à ré-intégration. Aucune stack existante n'utilisait SAML côté Homelab (mention « aucun à ce jour » dans la skill) — impact rétroactif nul attendu.
- **Invariant préservé** : « en cas de doute → demander à l'humain » ; aucun choix d'auth implicite.
