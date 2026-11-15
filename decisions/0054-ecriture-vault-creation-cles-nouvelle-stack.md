---
auteurs: Sylvain Goubaud
parties_prenantes: Architecte de sécurité Homelab
accepte_par: Sylvain Goubaud
accepte_le: "2026-11-15"
supersedes: ""
superseded_by: ""
---

# Écriture Vault limitée à la création de clés d'une nouvelle stack (amende ADR-0044)

## Status

Accepted

> Statut **Accepted** : l'humain (`accepte_par`, 2026-11-15) a retenu l'**option A** (AppRole d'écriture dédié) sur HOM-320. Revue de l'Architecte de sécurité Homelab : RENVOI corrigé, re-contrôle partiel demandé avant commit.

## Date de création

2026-11-15

## Contexte

[ADR-0044](0044-parcours-service-version-update-gate-leger-unique-ecriture-vault-version.md) a ouvert une **exception d'écriture étroite** : la skill `homelab-vault-access` n'écrit que les clés de version (`VERSION` / `VERSION_<NOM_DU_SERVICE>`) du montage `env_variables/`, jamais `services/`, sur gate léger unique.

À la validation finale d'une nouvelle stack, l'humain peut vouloir que les clés Vault de la stack soient créées par le workflow, **indépendamment du déploiement Kestra** (retour du point 9 de HOM-320). Cela suppose d'écrire des clés de la stack dans `services/` (secrets) et `env_variables/` (variables), ce que l'ADR-0044 interdit. La revue de l'Architecte de sécurité Homelab (RENVOI, aucun critique, 3 majeurs) a demandé que cet élargissement soit **tracé**, borné techniquement et séparé des droits de lecture.

## Décision

1. **Seconde exception d'écriture**, après celle de l'ADR-0044 : **création seule** de clés absentes d'une nouvelle stack, sur `services/data/<stack>` et `env_variables/data/<stack>`, de la stack traitée uniquement.
2. **Déclenchement** : « oui » explicite à la décision « écriture des clés Vault » du gate final (défaut « non », absence de réponse = non), pour la liste `vault` montrée à l'humain. Une liste modifiée après le « oui » annule l'accord.
3. **Contenu écrit** : secrets `generable` (aléatoires, `openssl rand`), variables `variable` à valeur validée. Les clés `humain` (défaut) ne sont jamais écrites. La catégorie est fixée au Cadrage dans `parametres.json` et contrôlée par le sensor `required-parameters`.
4. **Garde-fous techniques** : check-and-set KV v2 (aucun écrasement, aucune écriture concurrente forcée), injection des valeurs par l'environnement du processus (`env.K`, `env.V`), jamais par argument de commande, `trap` qui efface les variables et révoque le token, noms de stack et de clés validés par expression régulière.
5. **Policy attendue** : `read` + `create` + `update` nominatifs sur les deux chemins de la stack, aucun joker, ni `delete`, `destroy` ni `list`. `read` est indispensable au check-and-set et au read-modify-write ; le rôle d'écriture, porté par le seul Tech Lead, peut donc lire les clés de la stack traitée (conséquence assumée).
6. **Agent écrivant** : le Tech Lead Homelab, lui seul.
7. **Identité d'écriture (option A retenue)** : **AppRole d'écriture dédié**, distinct de l'AppRole de lecture partagé par les spécialistes Docker, QA et Terraform. Ses identifiants sont portés **uniquement** par l'environnement de l'agent Tech Lead (`VAULT_WRITE_APPROLE_ROLE_ID`, `VAULT_WRITE_APPROLE_SECRET_ID`) ; les autres agents ne les ont pas. Sa policy ne contient que les droits des points 5 ci-dessus. Création du rôle et de la policy : action du propriétaire du workspace, hors dépôt. **Limites recommandées pour le rôle** : `token_ttl` court (5 min) et `token_max_ttl` identique, `token_num_uses` borné, `secret_id_ttl` et `secret_id_num_uses` limités, `token_bound_cidrs` sur l'hôte de l'agent Tech Lead si possible. Vérifier que les variables du rôle d'écriture sont **absentes** de l'environnement des autres agents (`multica agent env` de Bob, Kevin, André).

### Option écartée

- **Option B** : policy élargie sur le rôle de lecture existant. Plus simple, mais tous les agents lecteurs gagneraient le droit de créer des clés.

## Conséquences

### Positives

- **POS-001** : l'humain peut faire créer les clés sans déployer, sans écrire de valeur dans un commentaire.
- **POS-002** : aucune clé existante modifiée ; écriture concurrente détectée par CAS.
- **POS-003** : les secrets non générables ne passent jamais par l'agent.

### Négatives

- **NEG-001** : le principe « lecture seule hors clés de version » de l'ADR-0044 est élargi au montage `services/`.
- **NEG-002** : un secret généré par l'agent a transité par la mémoire du shell de l'agent (effacée par `trap`).
- **NEG-003** : l'option A demande de provisionner un second AppRole et de renseigner ses identifiants dans l'environnement de l'agent Tech Lead (hors périmètre documentaire). Tant que ce n'est pas fait, l'écriture échoue proprement (« identifiants d'écriture absents »), sans repli sur le rôle de lecture.

## Alternatives étudiées

- **ALT-001** : écriture limitée aux variables non secrètes. Rejetée par défaut (retire l'intérêt pour les secrets générables), mais reste valable si l'humain refuse NEG-002.
- **ALT-002** : valeurs générées par l'humain. Rejetée : transit de la valeur hors Vault.

## Notes d'implémentation

- **IMP-001** : `homelab-vault-access` Étape 4, `human-granular-validation` (décision 3), `file-deposit` Step 3 bis, `kestra-deployment`, `required-parameters` (`categorie`, `valeur`), `plugins/homelab-assistant/README.md`, `homelab/scopes/service-version-update.md`.
- **IMP-002** : invariants de gouvernance inchangés (SG-1..6, SEC-1..5).

## Références

- **REF-001** : [ADR-0044](0044-parcours-service-version-update-gate-leger-unique-ecriture-vault-version.md) — exception d'écriture `VERSION`.
- **REF-002** : rapport `review-securite-vault-write.yaml` (HOM-320).
