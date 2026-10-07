/**
 * n8n backend external hook — bypass de l'authentification native via header
 * de confiance (Trusted Header SSO : Authelia / Authentik / oauth2-proxy...).
 *
 * Compatible n8n >= 2.30.X (Express 5 / paquet `router` v2.x).
 *
 * Pourquoi l'ancien hook casse à partir de 2.30.X
 * ------------------------------------------------
 * L'ancien hook reposait sur deux hypothèses fragiles qui ne tiennent plus
 * avec le routeur embarqué par Express 5 (paquet `router` 2.x) :
 *
 *   1. `app.router` : selon le build, le routeur applicatif est exposé sur
 *      `app.router` OU `app._router`. On résout les deux.
 *
 *   2. `stack.findIndex((l) => l.name === 'cookieParser')` : dans `router` 2.x
 *      les couches internes sont souvent construites à partir de fonctions
 *      fléchées / anonymes dont le `.name` n'est plus `"cookieParser"`.
 *      `findIndex` renvoie alors `-1`, et `splice(-1 + 1, 0, ...)` insère la
 *      couche d'auth en position 0 — AVANT le cookie-parser. `req.cookies` est
 *      alors `undefined` et le bypass ne fonctionne jamais correctement.
 *      On détecte le cookie-parser par plusieurs heuristiques et on retombe
 *      sur une insertion sûre si aucune n'aboutit.
 *
 * Le constructeur `new Layer(path, options, fn)` reste valide : `fn` est stocké
 * sur `this.handle` et invoqué par `Layer.prototype.handleRequest`. Un handler
 * `async (req, res, next) => {}` (arité 3) est traité comme un handler de
 * requête standard — inchangé.
 */

const { dirname, resolve } = require('path')

// Le paquet `router` est une dépendance d'Express 5 ; `express/lib/router/layer`
// n'existe plus. On tente d'abord `router/lib/layer`, puis des chemins de repli.
function loadLayer() {
  const candidates = [
    'router/lib/layer',
    'express/lib/router/layer', // anciens n8n (< 2.x) — repli
  ]
  for (const mod of candidates) {
    try {
      return require(mod)
    } catch (_) {
      /* on essaie le suivant */
    }
  }
  throw new Error(
    "n8n forward-auth hook: impossible de charger la classe Layer " +
      "(ni 'router/lib/layer' ni 'express/lib/router/layer')."
  )
}

const Layer = loadLayer()
const { issueCookie } = require(resolve(dirname(require.resolve('n8n')), 'auth/jwt'))

const ignoreAuthRegexp = /^\/(assets|healthz|webhook|rest\/oauth2-credential)/

/**
 * Localise la position d'insertion : juste après le cookie-parser.
 * Renvoie l'index où insérer, ou `0` en dernier recours (le hook restera
 * fonctionnel pour les requêtes où le cookie n'est pas requis, et n'empêchera
 * pas n8n de démarrer).
 */
function findInsertIndex(stack) {
  // 1) Nom exact (anciens routeurs).
  let i = stack.findIndex((l) => l && l.name === 'cookieParser')
  if (i !== -1) return i + 1

  // 2) Nom approché (handler nommé différemment mais reconnaissable).
  i = stack.findIndex(
    (l) => l && typeof l.name === 'string' && /cookie/i.test(l.name)
  )
  if (i !== -1) return i + 1

  // 3) Introspection du handler : certaines versions exposent le parser via
  //    `l.handle` dont le nom/toString contient "cookie".
  i = stack.findIndex((l) => {
    const fn = l && l.handle
    if (typeof fn !== 'function') return false
    if (/cookie/i.test(fn.name || '')) return true
    try {
      return /cookie/i.test(Function.prototype.toString.call(fn))
    } catch (_) {
      return false
    }
  })
  if (i !== -1) return i + 1

  // 4) Dernier recours : insérer en tête. Mieux vaut un bypass partiel qu'un
  //    crash au démarrage. Les requêtes déjà porteuses du cookie passent de
  //    toute façon par la vérification JWT native de n8n.
  console.warn(
    'n8n forward-auth hook: cookie-parser introuvable dans la stack du ' +
      'routeur ; insertion en tête (index 0). Vérifiez la version du paquet ' +
      '`router` si le bypass ne fonctionne pas.'
  )
  return 0
}

/**
 * Recherche de l'utilisateur, robuste aux variations d'API du repository
 * (TypeORM) entre versions de n8n.
 */
async function findUserByEmail(dbCollections, email) {
  const UserRepo = dbCollections.User
  // API récente : findOneBy({ email })
  if (typeof UserRepo.findOneBy === 'function') {
    return UserRepo.findOneBy({ email })
  }
  // API plus ancienne : findOne({ where: { email }, relations: ['role'] })
  if (typeof UserRepo.findOne === 'function') {
    return UserRepo.findOne({ where: { email }, relations: ['role'] })
  }
  throw new Error('n8n forward-auth hook: API User repository inattendue.')
}

module.exports = {
  n8n: {
    ready: [
      async function ({ app }, config) {
        const router = app.router || app._router
        if (!router || !Array.isArray(router.stack)) {
          console.error(
            'n8n forward-auth hook: routeur applicatif introuvable ' +
              '(ni app.router ni app._router). Hook non installé.'
          )
          return
        }

        const { stack } = router
        const index = findInsertIndex(stack)

        stack.splice(
          index,
          0,
          new Layer(
            '/',
            { strict: false, end: false },
            async (req, res, next) => {
              // Ignorer les URLs publiques / internes.
              if (ignoreAuthRegexp.test(req.url)) return next()

              // Ignorer tant que l'owner de l'instance n'est pas configuré.
              if (!config.get('userManagement.isInstanceOwnerSetUp', false)) {
                return next()
              }

              // Ignorer si un cookie d'auth existe déjà.
              if (req.cookies?.['n8n-auth']) return next()

              // Ignorer si le header de forward-auth n'est pas configuré.
              if (!process.env.N8N_FORWARD_AUTH_HEADER) return next()

              // Lire l'email depuis le header de confiance (injecté par le
              // reverse proxy / SSO). En minuscules : les headers Node sont
              // normalisés en minuscules.
              const headerName = process.env.N8N_FORWARD_AUTH_HEADER.toLowerCase()
              const email = req.headers[headerName]
              if (!email) return next()

              try {
                const user = await findUserByEmail(this.dbCollections, email)
                if (!user) {
                  res.statusCode = 401
                  res.end(
                    `User ${email} not found, please have an admin invite the user first.`
                  )
                  return
                }

                // Certaines versions attendent un objet `role` présent.
                if (!user.role) {
                  user.role = {}
                }

                // Émettre le cookie JWT n8n si tout est OK.
                issueCookie(res, user)
                return next()
              } catch (err) {
                // Ne jamais faire tomber la requête silencieusement : loguer et
                // laisser n8n gérer l'auth nativement.
                console.error('n8n forward-auth hook: erreur de traitement :', err)
                return next()
              }
            }
          )
        )
      },
    ],
  },
}
