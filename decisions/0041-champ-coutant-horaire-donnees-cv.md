# Champ `coutant` (coûtant horaire — coût interne) dans les données CV du workflow Matching

---
auteurs: Gestionnaire CV (agent)
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — décision de **schéma des données CV** prise par le **Gestionnaire CV**
> (propriétaire du schéma, source unique `plugins/rh-assistant/skills/cv-analyse/SKILL.md`), sur
> mission A2A du **Coordinateur Matching** (EXPE-129) à la demande de l'humain. Le champ est
> **appliqué** aux deux analyses visées par la mission (enregistrement
> demandé), mais l'**évolution de schéma** reste soumise à **validation humaine granulaire** au gate.
> Évolution **documentaire + données** : ajout d'un champ, **sans** modification des poids de scoring,
> de la logique d'éligibilité, ni d'aucune posture de sécurité. Invariants de gouvernance préservés
> (validation humaine, piste d'audit, « ne rien inventer », non-transmission des CV, aucun secret).

## Contexte

Le **Gestionnaire CV** (workflow `matching-cv-ao`) maintient le référentiel des collaborateurs sous
`${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv` via la compétence `cv-analyse`, dont le schéma YAML
des données CV est la **source unique**.

L'humain a demandé, **hors run de matching** (maintenance du
référentiel), d'enregistrer le **coûtant horaire** (coût interne, $CAD/heure) de deux collaborateurs
internes (valeurs réelles omises de l'ADR — donnée interne confidentielle) :

- Collaborateur A (`collab-a`), `alithya` — coûtant horaire interne (valeur omise) ;
- Collaborateur B (`collab-b`), `alithya` — coûtant horaire interne (valeur omise).

Le schéma existant ne portait **aucun champ dédié au coûtant**. Le seul champ monétaire voisin,
`remuneration`, modélise la **rémunération du collaborateur** (`taux_horaire_cad` pour un pigiste,
`salaire_annuel_cad` pour un `alithya` / `offre_conditionnelle`) — concept **différent** du coûtant :

- la **rémunération** est ce que le collaborateur **perçoit** (salaire / taux de pige) ;
- le **coûtant** est le **coût interne horaire** du collaborateur pour la firme.

Les deux collaborateurs sont `alithya` : écrire le coûtant dans `remuneration.taux_horaire_cad`
(réservé aux pigistes) l'aurait **corrompu** et confondu avec un taux de pige inexistant.

## Décision

Ajout, au **niveau du collaborateur** dans le schéma des données CV, d'un **objet `coutant` distinct**
de `remuneration` et **indépendant du `type_collaborateur`** :

```yaml
coutant:
  type: coutant_horaire          # seul type à ce jour (coût interne horaire)
  coutant_horaire_cad: 0         # $CAD/heure — null si non connu (ne rien inventer)
  source: cv | humain | null     # provenance de la donnée
  date_saisie: "<AAAA-MM-JJ>"    # date de saisie / mise à jour (quotée)
  commentaire: <provenance / précision, ou omis>
```

Règles :

- **Distinct de `remuneration`** : le coûtant n'est **jamais** écrit dans `remuneration.taux_horaire_cad`
  ni `remuneration.salaire_annuel_cad`. Un `alithya` peut porter **à la fois** un salaire annuel
  (`remuneration`) et un coûtant horaire (`coutant`).
- **Indépendant du `type_collaborateur`** : applicable à tout type (le coûtant est un coût interne,
  pas un mode de rémunération).
- **Montant décimal** : vrai nombre non quoté, **point décimal** (une saisie FR « 12,34 » est
  normalisée en `12.34`). Voir la règle de validité YAML correspondante dans `cv-analyse`.
- **Ne rien inventer** : coûtant non connu ⇒ objet omis ou `coutant_horaire_cad: null` + mention
  humaine. **Aucun secret** : donnée métier factuelle, jamais fabriquée.

## Portée et application

- **Source unique mise à jour** : `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (bloc de schéma
  YAML, règles de validité, bullet `coutant`, mots-clés).
- **Données appliquées** (mission EXPE-129) — valeurs réelles omises de l'ADR (donnée interne confidentielle) :
  - `collaborateurs/collab-a/cv/<AAAA-MM-JJ>-collab-a.yaml` → `coutant.coutant_horaire_cad: <valeur omise>` ;
  - `collaborateurs/collab-b/cv/<AAAA-MM-JJ>-collab-b.yaml` → `coutant.coutant_horaire_cad: <valeur omise>`
    (couple antérieur archivé, re-daté à la date de la modification).
- **Hors périmètre** : aucun impact sur le **scoring** (poids inchangés), la **sélection d'éligibilité**
  (axes inchangés) ni les **sensors**. Le coûtant est une donnée métier informative ; il n'entre dans
  aucun critère d'éligibilité ni de matching tant qu'une décision ultérieure ne l'y introduit pas.

## Conséquences

- Le référentiel peut désormais porter le coût interne horaire d'un collaborateur sans ambiguïté avec
  sa rémunération.
- Les analyses déjà extraites **sans** coûtant restent valides (champ optionnel, absence = non connu).
- Une éventuelle utilisation du coûtant dans le scoring (ex. arbitrage coût/pertinence) relèverait
  d'une **décision distincte**, à trancher par l'humain.
