# Déduction de `cloudflare_dns_nb`

Fichier de référence de la skill `terraform-qa`, pour le contrôle de cohérence de la variable `cloudflare_dns_nb` (point de contrôle 3).

## Règle

`cloudflare_dns_nb` = **nombre de noms d'hôte publics distincts** exposés par la stack. Chaque nom d'hôte public distinct correspond à **un CNAME** à créer dans Cloudflare.

Lors de la vérification, la valeur écrite dans le fichier doit être **égale** au nombre d'hôtes publics distincts que la configuration expose. Un écart est un défaut de cohérence à signaler (RENVOI).

## Exemples

- Une seule interface web (`portainer.exemple.tld`) → `cloudflare_dns_nb = 1`.
- Application et API sur des hôtes distincts (`app.exemple.tld` + `api.exemple.tld`) → `cloudflare_dns_nb = 2`.

## Cas limites

- **Plusieurs entrées sur le même hôte** (ex. un chemin `/api` supplémentaire sur le même domaine) : compter les **hôtes**, pas les entrées → toujours 1 CNAME pour cet hôte.
- **Service purement interne** (aucune exposition publique) : non compté.
- **Hôte incertain** (motif générique / wildcard rendant le nombre d'hôtes non déterminable statiquement) : ne pas trancher ; signaler l'ambiguïté dans le rapport comme point à lever par l'auteur.
