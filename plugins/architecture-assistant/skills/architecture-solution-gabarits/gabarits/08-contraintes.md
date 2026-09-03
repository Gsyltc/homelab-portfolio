## Contraintes

> Cette section liste l'ensemble des **contraintes** qui s'imposent à la solution : lois et règlementations, référentiels et normes, conformités du domaine d'affaires, contraintes technologiques.
> Chaque contrainte est identifiée par un code (`CT-001`, `CT-002`, …) et déclinée selon les attributs : **Source**, **Responsable**, **Impact architectural**, **Mesure de conformité**, **Degré (imposable / négociable)**.
> Toute contrainte qui **force un choix d'architecture** est tracée dans un **ADR** (skill `create-architectural-decision-record`) et vérifie la **couverture d'un patron** du répertoire `patron-architecture/`.

### Lois et règlementations

> Liste des lois et règlementations applicables, rédigée en collaboration avec le **responsable légal** et le **DPD** (arrimage RACI du `001`). Une contrainte **imposable** doit être satisfaite obligatoirement ; une contrainte **négociable** peut être ajustée avec le client.

| ID | Lois / Réglementation | Description | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------------------|-------------|--------|-------------|----------------------|----------------------|-------|
| CT-001 | Loi 25 | La loi 25 vise à mieux protéger les données personnelles des citoyens et à renforcer leurs droits face aux entreprises qui les collectent et les traitent | Loi 25 (Québec), CAPRP | Responsable légal / DPD | Chiffrement, accès, cycle de vie des données (`10`, `11`) | Déclinée ci-dessous (obligations concrètes) | Imposable |

**Tableau 34. Lois et règlementations**

#### (exemple) Loi 25 (CT-001)

> Cette section, spécifique à la loi ou à la réglementation, décline la **nature** de la loi et ses **obligations concrètes au niveau architecture** (et non une description générale) :

- **Nature** : loi québécoise sur la protection des renseignements personnels (réformée), autorité de régulation : Commission d'accès à l'information (CAI).
- **Consentement** : recueillir et documenter le consentement des personnes lors de la collecte ; l'architecture doit permettre de tracer le consentement (ex. registre de consentement, horodatage, version de la politique).
- **Minimisation des données** : ne collecter que les renseignements nécessaires ; limiter l'accès selon le **moindre privilège** (en lien avec `11-securite.md` et la classification du `10-cycle_vie_donnees.md`).
- **Droits des personnes** : accès, rectification, portabilité et suppression ; prévoir des API/processus d'exercice des droits et des délais de traitement.
- **AIPD** (analyse d'impact relative à la protection des données) : réaliser une AIPD pour les traitements à risque élevé ; les mesures de protection doivent être documentées dans l'architecture.
- **Registre des incidents** : journaliser les incidents de confidentialité ; l'architecture doit fournir les journaux d'audit et d'événements nécessaires à leur signalement.
- **Impact architectural** : chiffrement au repos et en transit, contrôles d'accès, traçabilité, cycle de vie des données (`10`), sécurité (`11`).
- **Responsables** : responsable légal, DPD, architecte de sécurité (arrimage `001`).
- **Lien ADR** : référencer l'ADR de mise en conformité.

### Référentiels et normes

> Référentiels, normes et standards applicables (internes et externes) auxquels la solution doit se conformer ou s'aligner.

| ID | Référentiel / Norme | Domaine | Exigences clés | Applicable à |
|----|---------------------|---------|----------------|--------------|
| NOR-001 | ISO/IEC 27001 | Sécurité de l'information | SMSI, contrôles de sécurité, gestion des risques | Solution, fournisseurs |
| NOR-002 | PIPEDA | Protection des données (fédéral Canada) | Consentement, minimisation, accès aux données | Données personnelles |
| NOR-003 | SOC 2 | Contrôles internes / sécurité | Confiance, confidentialité, disponibilité, intégrité | Hébergement, fournisseurs SaaS |
| NOR-004 | Normes internes (à préciser) | Référentiel d'entreprise | À préciser selon le référentiel de l'organisation | Solution |

**Tableau 35. Référentiels et normes**

### Conformités

> Cette section liste l'ensemble des contraintes de **conformité du domaine d'affaires**. Pour chaque élément, faire un court résumé des contraintes et des impacts liés.

| ID | Contrainte de conformité | Résumé | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|--------------------------|--------|--------|-------------|----------------------|----------------------|-------|
| CT-002 | | | | | | | |

**Tableau 36. Conformités**

### Contraintes technologiques

> Cette section liste l'ensemble des contraintes technologiques (référentiels internes, standards, socle technologique). Chaque contrainte qui oriente un choix fait l'objet d'un ADR.

#### Persistance des données

> Identifier les contraintes liées à la persistance des données. Exemples : type de base de données (NoSQL, relationnel), caching (Redis), etc.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-003 | | | | | | |

**Tableau 37. Contraintes technologiques – Persistance des données**

#### Portabilité

> Identifier les contraintes de portabilité (ex. multi-cloud, sur site / hybride, conteneurisation).

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-004 | | | | | | |

**Tableau 38. Contraintes technologiques – Portabilité**

#### Contraintes serveur

> Identifier les contraintes côté serveur. Exemples : framework, langage (Java, .NET), type de système d'exploitation (Windows, Linux), etc.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-005 | | | | | | |

**Tableau 39. Contraintes technologiques – Serveur**

#### Contraintes clients

> Identifier les contraintes côté client. Exemples : librairies (Angular, React), type d'appareil mobile (Android, Apple), etc.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-006 | | | | | | |

**Tableau 40. Contraintes technologiques – Clients**

#### Intégration / interopérabilité

> Identifier les contraintes d'intégration et d'interopérabilité : protocoles (REST, SOAP, gRPC, MQTT), formats d'échange (JSON, XML, CSV), standards d'API (OpenAPI, AsyncAPI), bus/messagerie.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-007 | | | | | | |

**Tableau 41. Contraintes technologiques – Intégration / interopérabilité**

#### Licences / obsolescence

> Identifier les contraintes de licences et d'obsolescence : type de licence (open source, propriétaire), conformité des licences des dépendances, versions supportées, fin de support, dette technologique.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-008 | | | | | | |

**Tableau 42. Contraintes technologiques – Licences / obsolescence**

#### Performance

> Identifier les contraintes de performance : temps de réponse, débit, latence, volumétrie (en lien avec `12-volumetries.md` et les NFRs du `02-objectifs.md`).

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-009 | | | | | | |

**Tableau 43. Contraintes technologiques – Performance**

#### Accessibilité

> Identifier les contraintes d'accessibilité : normes WCAG, RGAA, conformité des interfaces pour les personnes en situation de handicap.

| ID | Contrainte | Source | Responsable | Impact architectural | Mesure de conformité | Degré |
|----|-----------|--------|-------------|----------------------|----------------------|-------|
| CT-010 | | | | | | |

**Tableau 44. Contraintes technologiques – Accessibilité**
