---
name: homelab-vault-access
description: "Accès Vault du Homelab (AppRole) pour lire secrets et variables des stacks (montages services/ et env_variables/). Lecture seule sauf écriture encadrée de la seule clé VERSION (env_variables, parcours service-version-update)."
---

# homelab-vault-access

Accès programmatique au HashiCorp Vault du Homelab pour lire les secrets et les
variables d'environnement des stacks Docker. Il n'existe **pas** de fichier
`.env` : toute valeur provient exclusivement de Vault.

## Emplacements dans Vault (layout réel du Homelab)

Chaque catégorie est un **montage KV dédié** (KV version 2), PAS un dossier sous
`secret/`. Pour une stack `<stack>` :

| Contenu | Montage | Chemin API complet |
|---|---|---|
| Secrets | `services/` | `${VAULT_ADDR}/v1/services/data/<stack>` |
| Variables d'environnement | `env_variables/` | `${VAULT_ADDR}/v1/env_variables/data/<stack>` |

Le segment `data/` fait partie de la convention KV v2 : il apparaît dans l'URL
API mais pas dans le nom logique du chemin.

Fallback : si un montage dédié renvoie 404 alors que la policy autorise la
lecture, tenter le même chemin sous le montage générique
(`/v1/secret/data/services/<stack>`, `/v1/secret/data/env_variables/<stack>`).

## Prérequis obligatoires

Les identifiants AppRole sont fournis via les variables d'environnement de
l'agent (configurées par le propriétaire du workspace avec
`multica agent env set`) :

- `VAULT_APPROLE_ROLE_ID` (ou `VAULT_ROLE_ID`) — le `role_id`
- `VAULT_APPROLE_SECRET_ID` (ou `VAULT_SECRET_ID`) — le `secret_id`
- `VAULT_ADDR` optionnel (défaut : `https://vault.jeedom-gaston.ovh`)

Si ces variables sont absentes : **STOP**. Signaler explicitement que les
identifiants AppRole ne sont pas configurés et demander au propriétaire du
workspace de les définir. Ne jamais inventer, déduire ou chercher ailleurs une
valeur d'identifiant.

## Étape 1 — Authentification AppRole (API officielle)

```bash
VAULT_ADDR="${VAULT_ADDR:-https://vault.jeedom-gaston.ovh}"
ROLE_ID="${VAULT_APPROLE_ROLE_ID:-${VAULT_ROLE_ID:?ROLE_ID manquant}}"
SECRET_ID="${VAULT_APPROLE_SECRET_ID:-${VAULT_SECRET_ID:?SECRET_ID manquant}}"

TOKEN=$(curl -sS --fail-with-body -X POST \
  -H "Content-Type: application/json" \
  -d "{\"role_id\":\"${ROLE_ID}\",\"secret_id\":\"${SECRET_ID}\"}" \
  "${VAULT_ADDR}/v1/auth/approle/login" | jq -r '.auth.client_token')
```

Vérifier ensuite que le token est non vide :

```bash
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "Échec de connexion AppRole (voir réponse API sans afficher les identifiants)" >&2
  exit 1
fi
```

Le token (`auth.client_token`) reste en mémoire shell uniquement : jamais
affiché, jamais écrit dans un fichier, jamais passé en argument de commande
visible par `ps`.

En cas d'échec (`400 invalid request`, `permission denied`) : signaler
l'échec d'authentification sans jamais répéter `role_id` ni `secret_id`.
Un `secret_id` AppRole peut avoir une durée de vie limitée ou un nombre
d'utilisations restreint — si l'échec persiste, demander au propriétaire du
workspace de générer un nouveau `secret_id`.

## Étape 2 — Lire les données d'une stack

Variables d'environnement de la stack `multica` (cas réel vérifié) :

```bash
curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/env_variables/data/multica"
```

Secrets d'une stack :

```bash
curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/services/data/<stack>"
```

- Réponse KV v2 : `.data.data` contient les clés/valeurs ;
  `.data.metadata.version` la version.
- **403 `permission denied`** : la policy du rôle AppRole n'accorde pas ce
  chemin — le signaler au propriétaire du workspace (il faut ajouter `read`
  sur `env_variables/data/*` et `services/data/*` du montage concerné). Un 403
  ne dit rien de l'existence du chemin.
- **404** : chemin inexistant pour ce token — tenter le fallback sous
  `secret/` puis signaler si toujours absent, sans deviner.

Lister uniquement les NOMS de clés (sortie sûre, sans valeurs) :

```bash
curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/env_variables/data/multica" | jq -r '.data.data | keys[]'
```

Extraire UNE valeur pour comparaison locale (la capturer, ne jamais l'afficher) :

```bash
VALUE=$(curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/env_variables/data/multica" | jq -r '.data.data["NOM_CLE"]')
```

Comparer sans révéler (exemple : cohérence avec un fichier local) :

```bash
LOCAL_VALUE=$(grep '^NOM_CLE=' fichier.env | cut -d= -f2-)
[ "$VALUE" = "$LOCAL_VALUE" ] && echo "NOM_CLE: OK" || echo "NOM_CLE: DIFFERENCE"
```

### Détection alternative de montages (si le layout évolue)

Si les chemins ci-dessus échouent et que la policy le permet, lister les
montages KV et leur version :

```bash
curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/sys/mounts" | jq -r '.data | to_entries[]
      | select(.value.type == "kv")
      | "\(.key)\t\(.value.options.version // "?")"'
```

(`sys/mounts` peut lui-même être refusé par une policy restrictive → 403 :
passer directement aux chemins documentés ci-dessus.)

## Étape 3 — Écriture encadrée de la clé `VERSION` (SEUL cas d'écriture autorisé)

> **Portée stricte.** Cette skill est en **lecture seule** pour tous les parcours du workflow,
> **sauf** le parcours [`service-version-update`](../../../../homelab/scopes/service-version-update.md),
> et uniquement pour écrire la **seule** clé `VERSION` du montage `env_variables/data/<service>`.
> **Jamais** un secret du montage `services/`. **Jamais** une autre clé que `VERSION`. Toute autre
> écriture est **interdite**. L'écriture est **gardée par le gate léger unique (A1)** du stage
> [`version-update-application`](../../../../homelab/common/stages/validation/version-update-application.md) :
> aucune écriture sans l'acceptation humaine A1.

L'API KV v2 **écrase l'ensemble du secret** à chaque POST sur `.../data/<service>`. Pour ne modifier
que `VERSION` **sans perdre les autres clés**, utiliser un pattern **read-modify-write** : relire
l'objet `.data.data` complet, n'y remplacer que `VERSION`, puis réécrire l'objet entier.

```bash
# Pré-requis : TOKEN obtenu à l'Étape 1 ; $SERVICE et $NEW_VERSION fournis par le workflow.
# La NOUVELLE version est une donnée de version (non secrète) ; elle n'est pas un secret Vault,
# mais on ne logge jamais le contenu complet du secret relu.

# 1. Relire l'objet complet des variables d'environnement du service (toutes les clés).
CURRENT=$(curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/env_variables/data/${SERVICE}" | jq -c '.data.data')

# 2. Construire le nouvel objet en ne remplaçant QUE la clé VERSION (toutes les autres préservées).
NEW_DATA=$(printf '%s' "$CURRENT" | jq -c --arg v "$NEW_VERSION" '.VERSION = $v')

# 3. Réécrire l'objet entier (KV v2 : enveloppe {"data": {...}}).
#    Le corps transite par stdin (jamais en argument visible par `ps`).
printf '{"data": %s}' "$NEW_DATA" | curl -sS --fail-with-body -X POST \
  -H "X-Vault-Token: $TOKEN" -H "Content-Type: application/json" \
  --data @- "${VAULT_ADDR}/v1/env_variables/data/${SERVICE}" >/dev/null

# 4. Vérifier que VERSION vaut bien la nouvelle valeur, SANS afficher les autres clés.
WROTE=$(curl -sS --fail-with-body -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/env_variables/data/${SERVICE}" | jq -r '.data.data.VERSION')
[ "$WROTE" = "$NEW_VERSION" ] && echo "VERSION: écrite" || echo "VERSION: échec"

unset CURRENT NEW_DATA WROTE
```

Garde-fous **non débordables** pour cette écriture :

- **Une seule clé** : `VERSION`. Ne jamais ajouter, modifier ni supprimer une autre clé.
- **Un seul montage** : `env_variables/`. **Jamais** `services/` (secrets).
- **Préservation** : le read-modify-write relit puis réécrit toutes les autres clés à l'identique ;
  ne jamais réécrire un objet partiel qui écraserait les clés existantes.
- **Pas de divulgation** : ne jamais afficher ni logger l'objet `.data.data` relu (il contient
  d'autres variables) ; ne tracer sur l'issue que **le nom de clé `VERSION` + le statut** (écrite /
  échec) — jamais la valeur.
- **403 `permission denied` en écriture** : la policy AppRole n'accorde pas `update`/`create` sur
  `env_variables/data/<service>` — le signaler au propriétaire du workspace (il faut ajouter la
  capability d'écriture sur ce chemin **précis**). Ne jamais contourner.
- **Révocation** : révoquer le token en fin d'opération (voir § Règles de sécurité, point 5).

## Règles de sécurité ABSOLUES

1. **AUCUN secret ne doit être divulgué.** Jamais de valeur de secret,
   de token, de `role_id` ou de `secret_id` dans :
   - un commentaire ou un livrable d'issue Multica ;
   - une pièce jointe ;
   - une notification (ntfy ou autre) ;
   - une sortie de commande destinée à être partagée ;
   - un fichier livrable (rapport, archive, export).
2. Dans les comptes-rendus, ne citer que les **noms de clés** et leur statut
   (présente / absente / conforme / différente) — jamais les valeurs.
3. Ne pas écrire le token ni les valeurs récupérées dans un fichier disque.
   Utiliser des variables shell et `$TMPDIR` uniquement si indispensable,
   puis supprimer immédiatement (`rm -f`).
4. Ne pas logger les commandes contenant des valeurs sensibles ; préférer les
   en-têtes et variables plutôt que des arguments en ligne.
5. En fin de tâche, révoquer le token :

```bash
curl -sS -X POST -H "X-Vault-Token: $TOKEN" \
  "${VAULT_ADDR}/v1/auth/token/revoke-self"
unset TOKEN VALUE SECRET_ID ROLE_ID
```

6. Si une donnée demandée n'existe pas dans Vault (404), le signaler tel quel
   — ne pas la deviner ni la remplacer par une valeur arbitraire.
7. **Écriture = exception unique.** La seule écriture autorisée est la clé
   `VERSION` du montage `env_variables/data/<service>`, dans le cadre du parcours
   `service-version-update` et sous le gate léger unique (A1). **Jamais** une
   écriture sur le montage `services/`, jamais sur une autre clé que `VERSION`,
   jamais sans l'acceptation humaine A1. Toute autre demande d'écriture est
   refusée et signalée.
