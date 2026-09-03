---
name: ntfy-notifications
description: "Envoi de notifications push via ntfy. Utiliser pour notifier l'humain de tout évènement devant être partagé."
user-invocable: false
allowed-tools: Bash(curl), Bash(multica *)
---

# Notifications ntfy

Tu peux envoyer une notification push à l'humain via le serveur ntfy du workspace.

## Paramètres fixes

- **Serveur** : l'adresse du serveur est stocké dans la variable d'environnement `NTFY_URL` (url duy serveur)
- **Topic** : le nom du topic est stocké dans la variable d'environnement `NTFY_CHANNEL` (topic de la notification)
- **Authentification** : HTTP Basic avec l'utilisateur `multica`. Le mot de passe est stocké dans les variables d'environnement de l'agent : `NTFY_USER` (utilisateur) et `NTFY_PASSWORD` (mot de passe). **Ne jamais écrire le mot de passe en clair** dans un commentaire, un rapport ou une commande affichée.

### Vérifier que les identifiants sont disponibles

Avant d'envoyer, vérifier que les variables sont présentes :

```bash
[ -n "$NTFY_USER" ] && [ -n "$NTFY_PASSWORD" ] && echo "identifiants OK" || echo "identifiants manquants"
```
```bash
[ -n "$NTFY_URL" ] && echo "URL OK" || echo "URL manquante"
```
```bash
[ -n "$NTFY_CHANNEL" ] && echo "Topic OK" || echo "Topic manquant, utilisation du topic par defaut"
```

Si elles manquent, le signaler dans le rapport et à l'humain : l'environnement secret de l'agent n'est pas configuré (voir « Configuration des identifiants » ci-dessous).

## Envoyer une notification

Commande de base (avec authentification) :

```bash
curl -u "$NTFY_USER:$NTFY_PASSWORD" -d "Votre message" $NTFY_URL/$NTFY_CHANNEL
```

Avec un titre et un niveau de priorité :

```bash
curl -u "$NTFY_USER:$NTFY_PASSWORD" \
     -H "Title: Rapport journalier prêt" \
     -H "Priority: default" \
     -H "Tags: tada" \
     -d "Le rapport journalier est disponible sur l'issue ALI-XX." \
     $NTFY_URL/$NTFY_CHANNEL
```

### Options utiles

| En-tête | Valeurs | Usage |
|---|---|---|
| `Title` | Texte libre | Titre de la notification |
| `Priority` | `min` / `low` / `default` / `high` / `urgent` | Niveau d'importance |
| `Tags` | `tada`, `chart_with_upwards_trend`, `warning`, `chart_with_downwards_trend`, `moneybag`, … | Emoji d'illustration |
| `Click` | URL | Ouvre l'issue/rapport au clic |
| `Markdown` | `yes` | Rend le message en Markdown |

### Exemple de notification de rapport (cas type)

Quand Hector a terminé un rapport et que la tâche passe **en revue** :

```bash
curl -u "$NTFY_USER:$NTFY_PASSWORD" \
     -H "Title: Rapport prêt" \
     -H "Priority: high" \
     -H "Tags: tada,moneybag" \
     -H "Click: https://multica.app/issues/<issue-id>" \
     -d "Le rapport (journalier/hebdomadaire) est prêt : résumé dispo sur l'issue <identifier>." \
     $NTFY_URL/$NTFY_CHANNEL
```

## Configuration des identifiants

L'utilisateur et le mot de passe ntfy sont définis dans l'environnement secret de l'agent par le **propriétaire du workspace** (les agents ne peuvent pas modifier l'environnement secret). La configuration se fait avec la commande suivante (le mot de passe est lu depuis stdin, jamais sur la ligne de commande) :

```bash
multica agent env set <agent-id> --custom-env-stdin
```

avec sur stdin :
```json
{"NTFY_USER": "multica", "NTFY_PASSWORD": "<mot-de-passe>"}
```

## Règles

- Toujours utiliser le serveur "$NTFY_URL" et le topic "$NTFY_CHANNEL" sauf demande explicite contraire.
- Authentification obligatoire via `-u "$NTFY_USER:$NTFY_PASSWORD"` ; si les variables sont absentes, signaler que l'environnement secret n'est pas configuré.
- Le message doit être court, clair et utile à un humain intermédiaire.
- Après l'envoi, vérifier que la commande curl a réussi (code HTTP 2xx).
- Ne jamais envoyer de données sensibles (mot de passe, clé API) dans le message.
- Ne jamais afficher ni logger le mot de passe en clair.
