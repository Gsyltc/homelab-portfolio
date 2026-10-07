# n8n — Bypass d'authentification par header de confiance (Trusted Header SSO)

Hook backend externe n8n (`n8n.ready`) qui émet un cookie JWT n8n lorsqu'un
reverse proxy / SSO (Authelia, Authentik, oauth2-proxy...) injecte un header de
confiance contenant l'email de l'utilisateur. Cela évite la double
authentification (SSO + page de login n8n).

## Contexte — HOM-231

Le `hook.js` historique (snippet communautaire « v1.110.1 onwards ») **ne
fonctionne plus à partir de n8n 2.30.X**. La cause est le passage à Express 5,
qui embarque le paquet `router` en version 2.x.

### Cause racine

1. **Lookup du cookie-parser cassé.** L'ancien hook insère sa couche d'auth
   juste après la couche nommée `cookieParser` :

   ```js
   const index = stack.findIndex((l) => l.name === 'cookieParser')
   stack.splice(index + 1, 0, new Layer(...))
   ```

   Dans `router` 2.x, les couches internes sont construites à partir de
   fonctions fléchées / anonymes dont le `.name` n'est plus `"cookieParser"`.
   `findIndex` renvoie alors `-1` → `splice(-1 + 1, 0, ...)` = `splice(0, 0, ...)`
   insère la couche **avant** le cookie-parser. Résultat : `req.cookies` est
   `undefined`, le test « cookie déjà présent » est faussé et le bypass ne
   s'applique pas de façon fiable.

2. **Accès au routeur.** Selon le build, le routeur applicatif est exposé sur
   `app.router` **ou** `app._router`.

3. **Chargement de la classe `Layer`.** `express/lib/router/layer` n'existe plus
   avec Express 5 ; il faut passer par `router/lib/layer`.

Le constructeur `new Layer(path, options, fn)` reste compatible : `fn` est
stocké sur `this.handle` et invoqué par `Layer.prototype.handleRequest`. Un
handler `async (req, res, next) => {}` (arité 3) est traité comme un handler de
requête standard — ce point n'a pas changé.

### Correctif (`hooks.js`)

- Résolution de `Layer` via `router/lib/layer` (repli `express/lib/router/layer`).
- Résolution du routeur via `app.router || app._router`.
- Détection du cookie-parser multi-heuristiques (nom exact → nom approché →
  introspection du handler), avec repli sûr qui n'empêche jamais n8n de démarrer.
- Recherche utilisateur robuste (`findOneBy` récent / `findOne` + `relations`
  ancien).
- `try/catch` autour du traitement : en cas d'erreur, on loggue et on laisse
  l'authentification native de n8n reprendre la main.

## Déploiement

1. Monter `hooks.js` dans le conteneur n8n (ex. `/home/node/.n8n/hooks.js`).
2. Définir les variables d'environnement :

   ```env
   EXTERNAL_HOOK_FILES=/home/node/.n8n/hooks.js
   N8N_FORWARD_AUTH_HEADER=Remote-Email
   ```

3. L'email n8n de chaque utilisateur doit correspondre à l'email fourni par le
   SSO dans le header de confiance.

## ⚠️ Précaution de sécurité

n8n doit être **exclusivement** accessible via le reverse proxy qui pose le
header de confiance. Si l'accès direct est possible, n'importe qui peut
usurper un utilisateur en envoyant lui-même le header
`N8N_FORWARD_AUTH_HEADER`. Verrouillez l'accès réseau en conséquence.

## Références

- External hooks n8n : https://docs.n8n.io/hosting/configuration/external-hooks/
- Paquet `router` (Express 5) : https://github.com/pillarjs/router
- Guide communautaire d'origine (Authelia) :
  https://kb.jarylchng.com/i/n8n-and-authelia-bypass-n8n-native-login-page-usin-sNRmS-7j5u1/
