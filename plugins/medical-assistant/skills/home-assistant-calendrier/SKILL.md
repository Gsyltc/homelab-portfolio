---
name: home-assistant-calendrier
description: "Écrit et relit les repas du calendrier Home Assistant (défaut calendar.repas) via le serveur MCP de HA : crée le repas 19h-20h (description = ingrédients en puces, Lieu = lien de la recette) et un créneau le lendemain 12h-13h sans description ni Lieu ; relit les repas déjà présents sur la semaine lundi-dimanche (nom, jour, lien du Lieu) pour le tableau de clôture. Adresse et jeton lus depuis l'environnement (secrets, jamais en clair). Se déclenche sur : calendrier, Home Assistant, repas au calendrier, repas déjà présents, lire le calendrier, planifier un repas dans l'agenda, ajouter un évènement, create_event, get_events, mcp home assistant."
metadata:
  user-invocable: "false"
allowed-tools: Bash(curl) Bash(jq)
---

# home-assistant-calendrier — évènements de repas au calendrier `repas`

Cette skill décrit **comment** ajouter des évènements de repas dans un
calendrier Home Assistant (HA) — par défaut le calendrier **`repas`** — et
comment **relire** les repas déjà présents sur la semaine (lundi → dimanche)
pour alimenter le tableau final de l'agent. La connexion privilégiée se fait
par le **serveur MCP de HA** (déclaré dans le `mcp.json` du plugin) ; un
**repli REST** est documenté pour l'usage en ligne de commande.

## Règle de création — DEUX évènements par repas

Pour **chaque repas planifié et validé**, créer **deux évènements** dans le
calendrier cible (`calendar.repas` par défaut) :

1. **Évènement « repas »** — le jour du repas, **de 19h00 à 20h00**.
   - `summary` = nom du plat.
   - `description` = **liste des ingrédients en puces** (une puce `-` par
     ingrédient). Format de chaque ligne :

     ```
     <quantité><unité si disponible> <ingrédient au pluriel>
     ```

     - La quantité est collée à l'unité quand une unité existe (`200g`, `2càs`,
       `50cl`), puis une espace, puis l'ingrédient au **pluriel**.
     - Sans unité, écrire la quantité seule suivie de l'ingrédient (`4 carottes`,
       `2 oignons`).
     - Les ingrédients principaux (pour 4 personnes) ; **exclure les condiments**
       (sel, poivre, épices, huile, vinaigre, eau…), cohérent avec la skill
       `recherche-repas`.
   - `location` (champ **« Lieu »** de HA) = **emplacement de la recette** tel
     qu'il figure dans la suggestion / `repas-retenus.md` : URL directe si elle
     existe, sinon la référence exacte du référentiel (livre + page ou chemin).
     **Ne jamais fabriquer de lien ni inventer d'URL.**

2. **Évènement du lendemain** — **le jour suivant, de 12h00 à 13h00**,
   **sans description ni `location`**.
   - `summary` = nom du plat (même intitulé que l'évènement « repas »).
   - **Aucune** `description` (ne pas envoyer le champ).
   - **Aucun** `location` (ne pas envoyer le champ).

> Les deux évènements sont des évènements **horaires** (`start_date_time` /
> `end_date_time`), jamais « journée entière ». La date du second évènement est
> `date_du_repas + 1 jour`.

### Exemple de description (évènement « repas »)

Pour un « Dahl de lentilles corail » (4 personnes) :

```
- 250g lentilles corail
- 400ml laits de coco
- 2 oignons
- 2 gousses d'ails
- 1boîtes de tomates concassées
- 200g riz basmati
```

### Exemple de champ `Lieu` (`location`)

- URL : `https://<hôte>/recettes/<slug>` (telle que relevée dans le référentiel)
- Livre : `Companion XL — Recipebook FR, p. 42`
- Fichier : `recettes/dahl-de-lentilles-corail.md`

La valeur est **recopiée telle quelle** depuis la suggestion de recette ou
`repas-retenus.md`. Si aucun emplacement n'est connu, le signaler à l'humain
plutôt que d'en inventer un.

## Lecture des repas déjà présents (semaine lundi → dimanche)

**Avant toute création**, relire le calendrier cible sur la semaine considérée
(du lundi 00h00 au dimanche 23h59 — la semaine de l'étape 8 de l'agent, qui
commence au prochain lundi) :

- avec le serveur MCP : `calendar.get_events` sur `calendar.repas`, avec la
  fenêtre `YYYY-MM-DDT00:00:00` → `YYYY-MM-DDT23:59:59` ;
- en repli REST : `GET {HOMEASSISTANT_URL}/api/calendars/<entité>?start=...&end=...`
  avec l'en-tête `Authorization: Bearer "${HA_TOKEN}"`.

Ne retenir que les évènements **horaires 19h–20h** (repas du soir). Pour chacun,
extraire :

| Information | Champ HA | Usage dans la réponse finale |
|---|---|---|
| Nom du repas | `summary` | colonne « Nom de la recette » |
| Jour réel du repas | date de début | colonne « Jour de la semaine » (repas décalés inclus) |
| Lien de la recette | `location` (« Lieu ») | colonne « Lien de la recette » |

Cette lecture est **strictement en lecture seule** : aucun évènement existant
n'est modifié ni supprimé, même si un repas a été décalé. Un repas déjà présent
est ajouté au tableau final avec `Déjà acheté` dans la colonne Ingrédients, sans
être journalisé à nouveau. Si `location` est vide sur un repas existant, le
signaler à l'humain : **ne jamais inventer de lien**.

## Secret — adresse et jeton (jamais en clair)

L'adresse de l'instance HA et le jeton d'accès **NE DOIVENT JAMAIS** apparaître
en clair dans cette skill, le `mcp.json`, un commentaire d'issue, un rapport,
une pièce jointe, une notification ou une commande affichée. Ils sont fournis
par le **propriétaire du workspace** via l'environnement secret de l'agent :

| Variable | Contenu | Exemple (NE PAS écrire la vraie valeur) |
|---|---|---|
| `HOMEASSISTANT_URL` | URL de base de l'instance HA, **sans** `/` final | `https://<hote-ha>` |
| `HOMEASSISTANT_TOKEN` | Long-Lived Access Token HA | `eyJ...` |
| `HOMEASSISTANT_CALENDAR_ENTITY` | *(optionnel)* entité calendrier cible | `calendar.repas` |

Vérifier la présence avant tout appel :

```bash
[ -n "$HOMEASSISTANT_URL" ]   && echo "URL OK"   || echo "HOMEASSISTANT_URL manquante"
[ -n "$HOMEASSISTANT_TOKEN" ] && echo "Token OK" || echo "HOMEASSISTANT_TOKEN manquant"
```

Si une variable manque : **STOP**, le signaler à l'humain et demander au
propriétaire du workspace de la définir. Ne jamais inventer ni deviner une valeur.

Entité calendrier par défaut : **`calendar.repas`** (surchargeable) :

```bash
CAL_ENTITY="${HOMEASSISTANT_CALENDAR_ENTITY:-calendar.repas}"
```

## Connexion privilégiée — serveur MCP de Home Assistant (via `mcp.json`)

La connexion à HA se fait par le **serveur MCP** `home-assistant`

### Champs passés à l'outil `calendar.create_event`

| Champ | Évènement « repas » (19h–20h) | Évènement lendemain (12h–13h) |
|---|---|---|
| `entity_id` | `calendar.repas` | `calendar.repas` |
| `summary` | nom du plat | nom du plat |
| `start_date_time` | `JJ 19:00:00` | `JJ+1 12:00:00` |
| `end_date_time` | `JJ 20:00:00` | `JJ+1 13:00:00` |
| `description` | liste d'ingrédients en puces | *(absent)* |
| `location` | emplacement de la recette (« Lieu ») | *(absent)* |

Format des `*_date_time` : `YYYY-MM-DD HH:MM:SS`. La fin est **exclusive**.

### Codes de retour

- **200 / 201** : évènement créé.
- **400** : corps invalide (format de date incorrect) — corriger.
- **401** : jeton absent/invalide (`www-authenticate: Bearer`) — demander la
  régénération d'un Long-Lived Access Token au propriétaire du workspace.
- **404** : entité calendrier inexistante — vérifier le nom réel, ne pas deviner.
- **405** : méthode incorrecte — l'appel doit être un `POST`.

## Règles de sécurité ABSOLUES

1. **AUCUN secret divulgué.** Ne jamais écrire `HOMEASSISTANT_URL` (adresse),
   `HOMEASSISTANT_TOKEN` ni aucune valeur de jeton dans un commentaire/livrable
   d'issue, une pièce jointe, un rapport, une notification, une sortie partagée,
   ni le `mcp.json` committé (qui ne contient que des `${...}`).
2. Passer le jeton via l'en-tête `Authorization: Bearer "${HA_TOKEN}"` (variable
   shell), jamais en argument visible par `ps` ni dans un log.
3. Ne pas écrire le jeton ni l'adresse dans un fichier disque. En fin de tâche :
   `unset HA_TOKEN HA_URL`.
4. Dans les comptes-rendus, ne citer que **le fait** (« repas “X” ajouté au
   calendrier le JJ/MM, + créneau du lendemain ») — jamais l'URL ni le jeton.
5. Environnement secret absent → **STOP** et signaler, sans deviner.

## Garde-fou métier

- N'ajouter les deux évènements **qu'après validation explicite de l'humain**
  (le chef propose, l'humain valide).
- Ingrédients de la description cohérents avec la skill `recherche-repas`
  (ingrédients principaux pour 4 personnes, condiments exclus).
- `location` renseigné sur l'évènement repas uniquement, recopié du référentiel ;
  aucun `location` sur le créneau du lendemain.
- Le sensor de clôture `repas-calendrier-agenda` (plugin `medical-assistant`,
  `plugins/medical-assistant/scripts/sensors/`) relit ces deux évènements :
  créneau du lendemain **12h–13h** sans description, description en puces
  obligatoire, `location` non vide sur le repas et absent du lendemain. Un
  écart est corrigé avant de clôturer, jamais contourné.
- Ne jamais fusionner, pousser ni ouvrir de PR sur `homelab-portfolio` sans
  validation explicite de l'humain.
