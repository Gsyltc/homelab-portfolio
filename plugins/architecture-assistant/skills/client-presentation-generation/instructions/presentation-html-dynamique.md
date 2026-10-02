# Instructions — produire une présentation client HTML dynamique

Fichier d'**instructions** (pas un gabarit figé) : il guide la production, de bout en bout, d'une présentation client au format **HTML dynamique autoportant**. Il remplace l'ancien fichier HTML modèle. Toutes les règles ci-dessous sont issues d'un test de référence validé par l'humain : les suivre évite de réapprendre des corrections déjà payées.

> **À quoi sert ce fichier** : tu construis le HTML **toi-même**, section par section, en appliquant ces instructions. Les blocs de code ci-dessous sont des **références prêtes à copier** (CSS, moteur de slides, moteur de diagramme « System overview ») — adapte-les, ne les traite pas comme un livrable immuable.

## Contrainte dure — autoportance

Un **fichier HTML unique**, ouvrable sans réseau. **Aucune** ressource externe : pas de `<link>`, `<script src>`, `@import`, CDN, `url(http…)`. Tout en inline : CSS, JS, logo (data URI base64), SVG de diagramme. **Vérifier `0`** occurrence de `http(s)://` hors du namespace SVG (`http://www.w3.org/2000/svg`) avant livraison.

## 0. Page de garde + sommaire (par défaut, tous types)

Toute présentation s'ouvre par **deux slides fixes**, avant les chapitres de contenu : une **page de garde**, puis un **sommaire**. Elles sont requises quel que soit le type (en Technique/Fonctionnelle comme ailleurs, ici en HTML dynamique).

**Slide 1 — page de garde** (`class="slide active"`, `data-chapter="Page de garde"`) : mise en forme graphique moderne reprenant la charte réelle de `theme/` (dégradé `--al-primary → --al-secondary`, accent `--al-accent`, logo inliné en data URI). **Champs normalisés** : **titre**, **sous-titre**, **public visé**, **auteur**, **année**, **date / version**, **baseline / tagline** (ligne d'accroche organisation/programme), **mention de confidentialité**. Ne rien inventer : titre/public/auteur issus du cadrage ; jamais d'approximation de charte.

```html
<section class="slide active cover" data-chapter="Page de garde" data-sub="Page de garde">
  <img class="cover-logo" src="data:image/png;base64,…" alt="Logo client">
  <h1>Titre de la présentation</h1>
  <p class="cover-sub">Sous-titre — public visé</p>
  <p class="cover-author">Auteur · AAAA</p>
  <p class="cover-tagline">Baseline / tagline — accroche organisation ou programme</p>
  <p class="cover-meta">Version 1.0 · AAAA-MM-JJ · Confidentiel</p>
</section>
```
```css
.cover{display:flex;flex-direction:column;justify-content:center;gap:.8rem;
  background:linear-gradient(135deg,var(--al-primary),var(--al-secondary));color:#fff}
.cover-logo{width:180px;max-width:40%}
.cover h1{font-size:clamp(1.8rem,4vw,3rem);border:0}
.cover-sub{font-size:clamp(1.1rem,2vw,1.4rem);opacity:.95}
.cover-author{font-size:clamp(1rem,1.6vw,1.15rem);opacity:.9}
.cover-tagline{font-size:clamp(.95rem,1.5vw,1.1rem);opacity:.85;font-style:italic}
.cover-meta{color:#dbe6f4;border-top:3px solid var(--al-accent);padding-top:.6rem;display:inline-block}
```

**Slide 2 — sommaire** (`data-chapter="Sommaire"`) : table des matières des **chapitres de niveau 1 réellement présents** (thèmes `data-chapter`, hors « Page de garde » / « Sommaire »). Générée **automatiquement** depuis les slides pour rester cohérente avec le menu latéral ; ne lister que les chapitres existants (un chapitre exclu faute de documentation n'y figure pas).

```html
<section class="slide" data-chapter="Sommaire" data-sub="Sommaire">
  <h2><span class="bar"></span>Sommaire</h2>
  <ol class="toc" id="toc"></ol>
</section>
```
```js
// Sommaire auto : thèmes niveau 1, hors page de garde & sommaire, dans l'ordre d'apparition.
const skip=new Set(['Page de garde','Sommaire']);
const seen=[]; document.querySelectorAll('.slide').forEach(s=>{const c=s.dataset.chapter;
  if(c&&!skip.has(c)&&!seen.includes(c))seen.push(c);});
const toc=document.getElementById('toc');
if(toc)seen.forEach(c=>{const li=document.createElement('li');li.textContent=c;toc.appendChild(li);});
```

> **PowerPoint** : reproduire les deux mêmes ouvertures — une diapositive de garde (charte ; titre, sous-titre, public visé, **auteur**, **année**, version, date, **baseline / tagline**, confidentialité) puis une diapositive de sommaire (chapitres de niveau 1). En Marp, deux premières slides Markdown ; en Pandoc `--reference-doc`, utiliser le masque « page de titre » du gabarit client.

## 1. Créer les sections requises par le type de présentation

Les **sections dépendent du type** demandé — ne pas imposer un jeu de chapitres fixe. Reprendre le plan du gabarit de contenu correspondant :

| Type | Gabarit de contenu | Chapitres (résumé) |
|---|---|---|
| **Executive** | `../executive.md` | Résumé exécutif · Contexte & enjeux · Objectifs & KPIs · Vue d'ensemble solution · Risques · Coûts & jalons · Prochaines étapes |
| **Entreprise / Affaires (TOGAF)** | `../entreprise-affaires.md` | Chapitres orientés affaires/TOGAF (dont dépendances de feuille de route) |
| **Technique / Fonctionnelle** | `../technique-fonctionnelle.md` | Chapitres techniques/fonctionnels, nomenclature client — **HTML dynamique uniquement** |
| **Sécurité / Conformité** | `../securite-conformite.md` | Chapitres sécurité/conformité (sans détails exploitables) |

Procédure :
1. Choisir le type ; ouvrir `../<type>.md` pour la liste des chapitres.
2. Ne **créer une section que lorsqu'elle est requise** par le sujet demandé et disponible dans la documentation (via `presentation-targeting`). Ne pas produire de section vide ; ne pas fusionner les types.
3. Structurer chaque slide ainsi (le menu latéral se génère **automatiquement** à partir de `data-chapter`/`data-sub`). **Alterner un paragraphe rédigé et une liste à puces** (et, selon le propos, cartes / tableau / encadré) : viser un rendu structuré, ni bloc de prose compact ni simple liste de puces.

```html
<section class="slide" data-chapter="Thème (niveau 1 du menu)" data-sub="Sous-chapitre (niveau 2)">
  <div class="eyebrow">SURTITRE</div>
  <h2><span class="bar"></span>Titre de la slide</h2>
  <p class="lead">Paragraphe de contexte rédigé + « pourquoi ça compte ».</p>
  <ul><li>Puce explicative…</li><li>Puce explicative…</li></ul>
  <!-- cartes / tableau / encadré / diagramme selon le chapitre -->
</section>
```

> **Aucune note de génération / méta-production dans le rendu** (règle d'or). Ne **jamais** écrire sur une diapositive : tag de source par slide (« Source : documentation/… »), « aucun contenu inventé », « produit uniquement à partir des documents validés », descripteurs de rendu présentés comme note (« interactif et animé », « syntaxe validée », « fidélité stricte… »), ligne de version-process (« v2 — révisée … »). La traçabilité des sources et la discipline « ne rien inventer » restent des **règles de production** appliquées en travaillant, pas du texte de diapositive. **Seule exception** : le `<span class="demo-tag">` est réservé à l'**étiquette d'une donnée fictive** (« valeurs fictives — démonstration »), jamais à une attribution de source.
La première slide porte `class="slide active"` — c'est la **page de garde** (voir §0), suivie du **sommaire**, puis des chapitres de contenu.

## 2. Créer les diagrammes associés au type de présentation

La skill `archify` produit **5 types** de diagramme (tous SVG autoportants, animés). Choisir le type adapté au propos :

| Type archify | Convient pour |
|---|---|
| **Architecture** | composants, services, stockage, frontières |
| **Workflow** | CI/CD, approbations, appels d'outils, runbooks |
| **Sequence** | appels d'API, cache, auth, traces async |
| **Data Flow** | pipelines, lignage, PII, consommateurs |
| **Lifecycle** | états, retries, attentes, issues terminales |

Deux voies d'intégration (toujours en SVG **inline**, zéro dépendance) :

- **Voie A — SVG `archify`** : générer le diagramme avec `archify` dans le type choisi, l'exporter en **SVG**, puis **coller le `<svg>…</svg>`** dans un conteneur :
  ```html
  <div class="aw"><div class="diagram-embed"><!-- coller ici le <svg> archify --></div></div>
  ```
  CSS du conteneur :
  ```css
  .diagram-embed{width:100%;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:auto}
  .diagram-embed svg{width:100%;height:auto;display:block}
  ```
- **Voie B — moteur natif « System overview »** : pour un schéma **nœuds/arêtes** (typiquement Architecture) rendu animé + interactif **sans dépendre d'archify**. Modèle `nodes`/`edges` + moteur fournis en §7. Interactivité : filtres de canaux, survol/clic → légende ; animation : flux lumineux CSS.

Associer le **nombre et le type** de diagrammes au type de présentation : Executive = 1 vue d'ensemble haut niveau (+ éventuellement 1 parcours) ; Technique/Fonctionnelle = diagrammes plus détaillés et nombreux ; Sécurité = flux/états de contrôle, sans détail exploitable.

## 3. S'assurer que les diagrammes sont bien conçus (pas de chevauchement, etc.)

Pour les SVG `archify`, le layout est géré par l'outil (valider la syntaxe avant export). Pour le **moteur natif**, respecter ces règles de géométrie — chacune corrige un défaut constaté et refusé lors du test de référence ; **ne pas régresser** :

- **R1 — bord à bord** : chaque connecteur part du **bord** d'un nœud et arrive sur le **bord** d'un autre (fonction `anchor`). Aucune flèche flottante. *(défaut v2, corrigé v3)*
- **R2 — aucun passage sous un nœud** : router dans les **couloirs vides** entre blocs via des waypoints `via`. *(défaut v3, corrigé v4)*
- **R3 — grille aérée** : écarts **~140 px** entre rangées, **~130–160 px** entre colonnes, pour laisser un couloir libre à chaque arête. *(défaut v3, corrigé v4)*
- **R4 — étiquette hors pointe** : poser l'étiquette sur le **premier segment**, loin de la pointe de flèche (dernier segment), pour que la pointe reste visible. *(défaut v3, corrigé v4)*
- **R5 — aucun recouvrement colinéaire** : si plusieurs arêtes partent d'un même nœud, utiliser des **ancres fractionnaires** (`ff`/`tf`) et des couloirs distincts ; deux arêtes ne partagent jamais un segment. *(défaut v5, corrigé v6)*

**Vérification attendue** (idéalement au rendu réel) : (a) chaque arête part/arrive sur un bord, (b) aucun segment ne traverse un nœud tiers, (c) **aucun recouvrement colinéaire** entre arêtes distinctes, (d) tout tient dans le `viewBox`, (e) aucune pointe de flèche masquée par une étiquette. En l'absence de navigateur, contrôler la géométrie programmatiquement et le signaler.

## 4. Reproduire la charte graphique (client)

- **Lire la charte réelle dans `theme/`** du projet (`0000-default-styles.dsl`, `alithya.json`). **Ne jamais inventer ni approximer** une couleur : une approximation a coûté deux itérations lors du test de référence. Si la charte n'est pas accessible, **la demander**.
- Définir les tokens dans `:root` (exemple avec la charte **Alithya** réelle) :
  ```css
  :root{
    --al-primary:#002957;        /* primaire (bleu foncé) */
    --al-primary-dark:#001c3d;   /* dérivé foncé (ombres/hover) */
    --al-secondary:#1F96E3;      /* secondaire (bleu clair) */
    --al-accent:#C9ED21;         /* accent (vert) */
    --al-accent-dark:#8fac00;    /* vert foncé lisible sur blanc */
    --al-neutral:#303030;        /* neutre foncé */
    --paper:#fff; --grey:#6b6b68; --grey-light:#f3f6fa; --line:#dde5ee;
    --ink:#303030; --muted:#55606e; --shadow:0 10px 34px rgba(0,41,87,.14);
    /* Canaux de diagramme — 4 teintes DISTINCTES dérivées de la charte */
    --c-decl:#002957; --c-exec:#1F96E3; --c-infer:#6b8fb5; --c-gouv:#8fac00;
  }
  ```
- **Logo** : inliner le PNG/SVG client en `data:image/png;base64,…` (source : clé `logo` de `theme/alithya.json`). Jamais d'URL externe.
- **Police** : appliquer celle de la charte (ex. Poppins). Si aucun fichier de police autoportant n'est disponible, documenter un **fallback système** (`'Poppins', system-ui, …`) — **jamais** de CDN. Un `.woff2` peut être inliné via `@font-face { src:url(data:font/woff2;base64,…) }`.
- Appliquer les tokens **partout** : menu latéral, titres, accents, cartes KPI, tableaux, timeline, et **canaux des diagrammes**. Vérifier qu'aucun code d'une ancienne approximation ne subsiste.

## 5. Densité du contenu

- Viser une densité **adaptée au type**, suffisante. Cible : **diapositive de contenu rédigée ~180–320 mots utiles** ; Technique/Fonctionnelle plutôt vers le haut de la fourchette. **Diapositive à diagramme** : un **paragraphe de contexte au-dessus du schéma** (propos + « pourquoi ça compte »), pas une simple légende.
- Chaque slide apporte **contexte + puces explicatives + « pourquoi ça compte »**, en **alternant paragraphe rédigé et liste à puces** (règle de clarté rédactionnelle), pas seulement des libellés.
- **Puiser dans la documentation réelle** (`documentation/…`). La **traçabilité des sources est une discipline de production** (tenue par l'agent / le périmètre), **pas un texte de diapositive** : ne pas afficher de tag « Source : … » sur les slides (voir §1). Ne pas inventer le contenu qualitatif : si la matière manque, **le signaler** plutôt que combler.
- **Frontière fictif/réel** : hors du principe « ne rien inventer », une démonstration/un test peut autoriser (sur **accord humain explicite**) des KPI/CAPEX-OPEX/feuille de route inventés — chacun **clairement étiqueté « démonstration »** (`demo-tag`), la **méthode** restant réelle. Ne jamais brouiller la frontière.

## 6. Longueur / largeur de prose

- La prose doit occuper une **largeur dynamique ≥ 70 %** de la zone de contenu, à toutes les résolutions usuelles.
- **Ne jamais poser de `max-width:…ch`** sur un bloc de prose : c'est exactement ce plafond qui ramenait le texte sous 70 % sur grand écran (défaut v6, corrigé v7). La zone `.slide` applique déjà `padding:3.5vh 5vw` (prose ~90 % de la largeur utile).
  ```css
  p.lead{font-size:clamp(1rem,1.55vw,1.2rem);color:var(--muted);max-width:none;width:100%;line-height:1.6}
  ```
- Les grilles de cartes et tableaux structurés ne sont pas concernés par ce seuil ; aucun bloc de prose ne doit retomber sous 70 %.

## 7. Autres éléments pertinents

- **Navigation** : **menu latéral gauche hiérarchique** (thème niveau 1, sous-chapitres niveau 2), état actif synchronisé, repli/déploiement, barre de progression, **raccourcis clavier** (← → Espace, Début/Fin). Le menu est **généré automatiquement** depuis les slides.
- **Accessibilité** : respecter `prefers-reduced-motion` (couper les animations) :
  ```css
  @media (prefers-reduced-motion: reduce){.edge-flow{animation:none;stroke-dasharray:none}}
  ```
- **Responsive** : repli en une colonne sous ~900 px (sidebar en bandeau haut).
- **Sécurité / confidentialité** : aucun secret ni identifiant dans le livrable ; sur une présentation Sécurité/Conformité, pas de détail exploitable.
- **Langue** : celle du destinataire (français par défaut).
- **Étiquetage** : toute donnée fictive porte un `<span class="demo-tag">`.

### Référence — moteur de slides + menu (JS inline à copier/adapter)

```js
const slides=[...document.querySelectorAll('.slide')];
const menu=document.getElementById('menu'); const counter=document.getElementById('counter');
const progress=document.getElementById('progress'); const prev=document.getElementById('prev'), next=document.getElementById('next');
let i=0; const chapters=[];
slides.forEach((s,idx)=>{const ch=s.dataset.chapter,sub=s.dataset.sub;let c=chapters.find(x=>x.name===ch);if(!c){c={name:ch,items:[]};chapters.push(c);}c.items.push({sub,idx});});
chapters.forEach((c,ci)=>{const wrap=document.createElement('div');wrap.className='chapter';wrap.dataset.ci=ci;
  const btn=document.createElement('button');btn.innerHTML='<span class="num">'+(ci+1).toString().padStart(2,'0')+'</span><span>'+c.name+'</span><span class="caret">▶</span>';
  btn.onclick=()=>wrap.classList.toggle('open');const subs=document.createElement('div');subs.className='subs';
  c.items.forEach(it=>{const a=document.createElement('a');a.href='#';a.textContent=it.sub;a.dataset.idx=it.idx;a.onclick=e=>{e.preventDefault();go(it.idx);};subs.appendChild(a);});
  wrap.appendChild(btn);wrap.appendChild(subs);menu.appendChild(wrap);});
const subLinks=[...menu.querySelectorAll('.subs a')]; const chapEls=[...menu.querySelectorAll('.chapter')];
function go(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,k)=>s.classList.toggle('active',k===i));
  counter.textContent=(i+1)+' / '+slides.length;prev.disabled=i===0;next.disabled=i===slides.length-1;progress.style.width=((i+1)/slides.length*100)+'%';
  subLinks.forEach(a=>a.classList.toggle('active',+a.dataset.idx===i));const activeCh=slides[i].dataset.chapter;
  chapEls.forEach(el=>{const ci=+el.dataset.ci;const on=chapters[ci].name===activeCh;el.classList.toggle('active',on);if(on)el.classList.add('open');});
  document.getElementById('slides').scrollTop=0;}
prev.onclick=()=>go(i-1);next.onclick=()=>go(i+1);
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')go(i+1);if(e.key==='ArrowLeft'||e.key==='PageUp')go(i-1);if(e.key==='Home')go(0);if(e.key==='End')go(slides.length-1);});
go(0);
```

### Référence — moteur de diagramme « System overview » (nœuds/arêtes, R1–R5)

Fonctions clés : `anchor(n,side,f)` renvoie un point sur le **bord** d'un nœud selon le côté (`l/r/t/b`) et une fraction `f∈(0,1)` (ancres distinctes = pas de recouvrement, R5) ; `routePoints(a,b,e)` construit la polyligne orthogonale, en passant par les waypoints `e.via` (couloirs vides, R2) ; l'étiquette est posée sur le **premier segment** (R4).

```js
const SVGNS='http://www.w3.org/2000/svg';
const CH={decl:{label:'Déclenchement',color:'#002957'},exec:{label:'Exécution',color:'#1F96E3'},
          infer:{label:'Inférence',color:'#6b8fb5'},gouv:{label:'Gouvernance',color:'#8fac00'}};
function el(t,a){const e=document.createElementNS(SVGNS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
function anchor(n,side,f){const t=(f==null?0.5:f);switch(side){
  case 'l':return{x:n.x,y:n.y+n.h*t};case 'r':return{x:n.x+n.w,y:n.y+n.h*t};
  case 't':return{x:n.x+n.w*t,y:n.y};case 'b':return{x:n.x+n.w*t,y:n.y+n.h};}}
function routePoints(a,b,e){const pts=[a];
  if(e.via){e.via.forEach(p=>pts.push(p));}
  else if(e.fs==='r'||e.fs==='l')pts.push({x:(a.x+b.x)/2,y:a.y},{x:(a.x+b.x)/2,y:b.y});
  else pts.push({x:a.x,y:(a.y+b.y)/2},{x:b.x,y:(a.y+b.y)/2});
  pts.push(b);return pts;}
// Dessiner, par arête : <path class="edge-path"> (trait) + <path class="edge-flow"> (flux animé,
// stroke-dasharray + animation dash) + étiquette (rect+cercle+texte) sur le premier segment.
// Par nœud : <rect class="box"> + accent coloré du canal + icône + titre + sous-titre ;
// survol/clic → mise à jour d'une légende. Barre de canaux : « Tous » + un onglet/canal (dim les autres).
```
CSS d'animation du flux :
```css
.edge-flow{fill:none;stroke-width:2.4;stroke-linecap:round;stroke-dasharray:2 12;animation:dash 1.4s linear infinite}
@keyframes dash{to{stroke-dashoffset:-56}}
```
Modèle d'une arête :
```js
{from:'n4',to:'n6',fs:'b',ff:0.72,ts:'t',tf:0.5,c:'exec',label:'artefacts',via:[{x:521,y:460},{x:840,y:460}],lo:{x:0,y:-14}}
// fs/ts = côté départ/arrivée ; ff/tf = fraction sur ce côté ; c = canal ; via = couloirs ; lo = décalage d'étiquette.
```

## Checklist de livraison

- [ ] **Autoportance** : `0` `http(s)://` hors namespace SVG ; aucun `<link>`/`<script src>`/`@import`/CDN.
- [ ] **Page de garde + sommaire** : présentation ouverte par une page de garde (charte `theme/` ; titre, sous-titre, public visé, **auteur**, **année**, version/date, **baseline/tagline**, confidentialité) puis un sommaire (chapitres de niveau 1 réellement présents) — HTML dynamique **et** PPTX (sauf Technique/Fonctionnelle = HTML uniquement).
- [ ] **Sections** : conformes au type de présentation ; aucune section vide ; menu latéral correct.
- [ ] **Diagrammes** : type archify adapté ; géométrie R1–R5 (natif) ; aucun chevauchement/recouvrement ; pointes visibles.
- [ ] **Charte** : tokens réels de `theme/`, logo inliné, aucune approximation résiduelle.
- [ ] **Densité** : ~180–320 mots/slide de contenu ; diapo à diagramme = paragraphe de contexte au-dessus du schéma ; matière manquante **signalée**, jamais comblée.
- [ ] **Clarté rédactionnelle** : alternance paragraphes rédigés / listes à puces ; ni bloc de prose compact ni simple liste de puces.
- [ ] **Aucune note de génération** : aucun tag « Source : … », « rien d'inventé », process-sourcing, descripteur de rendu ni ligne de version-process dans le rendu ; `demo-tag` réservé aux seules données fictives.
- [ ] **Prose** : largeur dynamique ≥ 70 % ; aucun `max-width:…ch`.
- [ ] **Accessibilité** : `prefers-reduced-motion` respecté ; responsive.
- [ ] **Sécurité** : aucun secret ni identifiant.

## Pourquoi ces règles (défauts à éviter)

Chaque règle corrige un défaut déjà constaté et refusé en validation ; les garder évite de le réintroduire.

| Défaut constaté | Règle encodée |
|---|---|
| Navigation à plat ; pas de diagramme ni de charte ; chiffres non structurés | Menu latéral hiérarchique ; diagramme ; tokens de charte ; tableaux ; timeline |
| Flèches « dans le vide » ; diagrammes statiques | Connecteurs bord-à-bord (R1) ; filtres de canaux + flux animé |
| Flèches cachées sous des blocs ; espacements trop serrés | Couloirs `via` (R2) ; grille aérée (R3) ; étiquette hors pointe (R4) |
| Charte approximée au lieu de la charte réelle | Lire `theme/`, ne jamais approximer |
| Contenu trop court ; connecteurs superposés | Densité ~180–320 mots/slide ; ancres fractionnaires (R5) |
| Textes de prose trop étroits | Prose ≥ 70 %, aucun `max-width:…ch` |
| Bloc de prose compact ou simple liste de puces | Alternance paragraphes rédigés / listes à puces (clarté rédactionnelle) |
| Notes de production affichées sur les slides (« Source : … », « rien d'inventé », « v2 — révisée », descripteurs de rendu) | Aucune note de génération dans le rendu ; traçabilité = discipline de production, pas texte de slide ; `demo-tag` réservé au fictif |

## Arrimage

- `presentation-targeting` — repérer l'information dans les documents d'architecture.
- `archify` — produire les diagrammes de tout type (Architecture, Workflow, Sequence, Data Flow, Lifecycle) en SVG autoportant.
- `project-defaults` — structure du projet et emplacement d'archivage.
- Gabarits de contenu par type : `../executive.md`, `../entreprise-affaires.md`, `../technique-fonctionnelle.md`, `../securite-conformite.md` (quels **chapitres** retenir).
