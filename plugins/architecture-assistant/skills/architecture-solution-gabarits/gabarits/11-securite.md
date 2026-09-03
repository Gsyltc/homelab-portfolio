## Sécurité

> Cette section identifie les risques potentiels de sécurité afin de mettre en place les moyens de sécurité appropriés. Elle décline les contraintes du `08-contraintes.md` (Loi 25, normes `NOR-001`…`NOR-004`) et est harmonisée avec le registre des risques du `04-risques.md` (mêmes échelles de **probabilité/impact**, mêmes statuts).

### Modélisation des menaces (STRIDE)

> Effectuer une **modélisation des menaces (STRIDE : Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege)** en **phase de conception** pour chaque composant / flux identifié dans `06-architecture-solutions.md`.
> Référencer les référentiels **OWASP** (Top 10, API Security) et **OWASP ASVS** (Application Security Verification Standard) pour les exigences de vérification. Les menaces identifiées alimentent le tableau des vulnérabilités et le registre des risques (`04`).

### Sécurité applicative

> Vulnérabilités applicatives issues de la modélisation des menaces (STRIDE) et des scans OWASP/ASVS. Chaque vulnérabilité est liée (sans duplication) au **registre des risques** du `04-risques.md` par son code (`RISQ-xxx`). Échelles de **Vraisemblance** et **Niveau de risques** harmonisées avec le `04`.

| ID | Vulnérabilités | Actifs concernés | Types de dommages | Vraisemblance | Niveau de risques | Contrôle de mitigation | Propriétaire | Échéance | Statut | Lien registre des risques (`04`) |
|----|----------------|------------------|-------------------|---------------|-------------------|------------------------|--------------|----------|--------|----------------------------------|
| VUL-001 | VULNERABILITE 1 | Renseignements personnels | Fuite de données contenant des renseignements personnels (collaborateurs, pigistes) | HAUT | CRITIQUE | | | | | RISQ-xxx |

**Tableau 56. Vulnérabilités applicatives**

#### Vulnérabilité 1 – Plan de traitement

> Le plan de traitement doit identifier les points suivants :
>
> - La planification des mesures à prendre ;
> - La façon de déployer les mesures de sécurité ;
> - La création d'indicateurs afin de surveiller régulièrement la sécurité :
>   - Performances des mesures de sécurité ;
>   - Conformité aux normes ;
> - Formation et sensibilisation du personnel.

### Sécurité Infrastructure

> Vulnérabilités d'infrastructure (segmentation réseau, durcissement, exposition des services). Chaque vulnérabilité est liée au **registre des risques** du `04-risques.md`.

| ID | Vulnérabilités | Actifs concernés | Types de dommages | Vraisemblance | Niveau de risques | Contrôle de mitigation | Propriétaire | Échéance | Statut | Lien registre des risques (`04`) |
|----|----------------|------------------|-------------------|---------------|-------------------|------------------------|--------------|----------|--------|----------------------------------|
| VUL-101 | VULNERABILITE 1 | | | | | | | | | RISQ-xxx |

**Tableau 57. Vulnérabilités Infrastructure**

#### Vulnérabilité 1 – Plan de traitement

> Le plan de traitement doit identifier les points suivants :
>
> - La planification des mesures à prendre ;
> - La façon de déployer les mesures de sécurité ;
> - La création d'indicateurs afin de surveiller régulièrement la sécurité :
>   - Performances des mesures de sécurité ;
>   - Conformité aux normes ;
> - Formation et sensibilisation du personnel.

### Chiffrement

> Décrire la stratégie de chiffrement de la solution :
> - **au repos** (bases de données, stockage objet, sauvegardes) ;
> - **en transit** (TLS, mTLS entre services) ;
> - **en mémoire** (secrets, données sensibles dans les processus) ;
> - **gestion des clés** (KMS / HSM, rotation des clés, séparation des environnements).
> En arrimage avec la Loi 25 et `NOR-001`, et cohérent avec la classification du `10-cycle_vie_donnees.md`.

### Segmentation réseau et durcissement

> Décrire la **segmentation réseau** (zones, DMZ, flux minimaux, micro-segmentation) en lien avec la répartition des zones du `09-deploiement.md`, et les mesures de **durcissement** (durcissement OS et conteneurs, images minimales, suppression des services inutiles, correctifs).

### Sécurité de la chaîne d'approvisionnement (SBOM / SCA)

> Décrire les mesures de sécurisation de la chaîne d'approvisionnement logicielle, en cohérence avec la section DevSecOps du `09-deploiement.md` :
> - **SBOM** (Software Bill of Materials) généré et vérifié pour chaque version ;
> - **SCA** (Software Composition Analysis) / scan des dépendances (CVE, OWASP) ;
> - **scan IaC** et **secret scanning** ;
> - signatures et provenance des artefacts (SLSA).

### Politique « Zero Trust »

> Décrire les choix et solutions de sécurité **Zero Trust** (« ne jamais faire confiance, toujours vérifier ») appliqués **par défaut** à la solution : vérification continue des identités, micro-segmentation, accès conditionnel, moindre privilège.

### Gestion des identités et des accès (GIA)

> Décrire la gestion des identités et des accès de la solution.

| ID | Accès | Groupes concernés | Ressources accessibles | Groupe de sécurité |
|----|-------|-------------------|------------------------|--------------------|
| GIA-001 | Type d'accès | | | |

**Tableau 58. Types d'accès – GIA**

#### Modèle d'authentification

> Décrire le modèle d'authentification retenu : **SSO** (Single Sign-On), **OIDC / OAuth 2.0**, **SAML**, annuaire d'identités (Azure AD / Entra ID, Okta, …), fédération. La décision est tracée dans un ADR.

#### Authentification multi-facteurs (MFA)

> Décrire les exigences d'**MFA** par population (utilisateurs externes, internes, administrateurs, comptes privilégiés).

#### Provisionnement des identités (SCIM)

> Décrire le provisionnement des identités et des accès (**SCIM** — System for Cross-domain Identity Management) : source de vérité RH, cycle de vie des comptes (création, mutation, départ), revue périodique des accès.

#### Gestion des accès privilégiés (PAM)

> Décrire la gestion des **accès privilégiés** (**PAM** — Privileged Access Management) : coffre de mots de passe, accès à la demande, session enregistrée, double validation pour les actions sensibles.

### Politique du moindre privilège

> Une politique de sécurité basée sur le principe du moindre privilège (PoLP, Principle of Least Privilege) est une stratégie de sécurité informatique dans laquelle un utilisateur se voit octroyer le minimum de permissions nécessaires pour accomplir ses tâches.
> Le but, en d'autres termes, sera de n'octroyer à un utilisateur que les informations et ressources strictement nécessaires pour l'accomplissement de son travail.
> S'applique aux utilisateurs comme aux services (identités applicatives, rôles de service) et aux données classées du `10-cycle_vie_donnees.md`.

### Authentification / Autorisation

> Décrire les choix et solutions d'authentification et d'autorisation (modèles RBAC / ABAC, politiques d'accès, gestion des sessions et des jetons).
