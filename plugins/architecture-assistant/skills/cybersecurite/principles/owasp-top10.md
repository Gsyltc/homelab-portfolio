# OWASP Top 10 — Risques de sécurité des applications web

## Vue d'ensemble

L'OWASP (Open Web Application Security Project) Top 10 est une liste standardisée des risques de sécurité les plus critiques pour les applications web. Elle est mise à jour régulièrement et sert de référence mondiale pour la sécurité des applications.

## Les 10 risques (édition 2021)

### A01 — Broken Access Control (Contournement des contrôles d'accès)
- **Description** : Les restrictions sur ce que les utilisateurs authentifiés sont autorisés à faire ne sont pas correctement appliquées.
- **Impacts** : Divulgation non autorisée de données, modification ou destruction de données, effectuer une opération en dehors des limites de l'utilisateur.
- **Contre-mesures** : Appliquer le principe du moindre privilège, restreindre l'accès côté serveur, valider les contrôles d'accès à chaque requête.

### A02 — Cryptographic Failures (Échecs de cryptographie)
- **Description** : Échec lié à la protection des données sensibles par le chiffrement ou des algorithmes obsolètes.
- **Impacts** : Vol de données sensibles (données personnelles, cartes de crédit, identifiants).
- **Contre-mesures** : Classifier les données, appliquer les contrôles appropriés, ne stocker que les données nécessaires, chiffrer les données au repos et en transit.

### A03 — Injection
- **Description** : L'application est vulnérable aux attaques par injection (SQL, NoSQL, OS, LDAP).
- **Impacts** : Exécution de code non autorisé, vol de données, destruction de données.
- **Contre-mesures** : Utiliser des requêtes paramétrées, valider et assainir les entrées, appliquer le principe de défense en profondeur.

### A04 — Insecure Design (Conception non sécurisée)
- **Description** : Faiblesses architecturales et de conception qui ne peuvent pas être corrigées par une implémentation parfaite.
- **Impacts** : Vulnérabilités systémiques, manque de modélisation des menaces.
- **Contre-mesures** : Intégrer la sécurité dès la conception, utiliser des patterns de conception sécurisés, effectuer des revues de conception.

### A05 — Security Misconfiguration (Mauvaise configuration de sécurité)
- **Description** : Mauvaise configuration de l'application, du framework, du serveur ou de l'infrastructure.
- **Impacts** : Accès non autorisé, détails d'erreur exposés, fonctionnalités non nécessaires actives.
- **Contre-mesures** : Processus de configuration automatisé, durcissement de l'environnement, revue régulière des configurations.

### A06 — Vulnerable and Outdated Components (Composants vulnérables et obsolètes)
- **Description** : Utilisation de composants (bibliothèques, frameworks) avec des vulnérabilités connues.
- **Impacts** : Exploitation de vulnérabilités connues, compromission de l'application.
- **Contre-mesures** : Inventaire des composants, surveillance des CVE, mise à jour régulière, composition logicielle.

### A07 — Identification and Authentication Failures (Échecs d'identification et d'authentification)
- **Description** : Confirmation de l'identité des utilisateurs, gestion des sessions et protection des comptes.
- **Impacts** : Compromission des comptes utilisateurs, usurpation d'identité.
- **Contre-mesures** : Authentification multi-facteurs, gestion sécurisée des sessions, politiques de mots de passe robustes.

### A08 — Software and Data Integrity Failures (Échecs d'intégrité logicielle et de données)
- **Description** : Attaques visant l'intégrité des logiciels et des données (pipelines CI/CD, mises à jour non vérifiées).
- **Impacts** : Injection de code malveillant, données corrompues.
- **Contre-mesures** : Vérifier l'intégrité des composants, sécuriser les pipelines CI/CD, utiliser des signatures numériques.

### A09 — Security Logging and Monitoring Failures (Échecs de journalisation et de surveillance de sécurité)
- **Description** : Insuffisance des mécanismes de journalisation, de détection et d'alerte.
- **Impacts** : Détection retardée d'incidents, incapacité à répondre aux attaques.
- **Contre-mesures** : Journaliser les événements de sécurité, surveiller les journaux, mettre en place des alertes.

### A10 — Server-Side Request Forgery (Falsification de requêtes côté serveur)
- **Description** : L'application récupère une ressource distante sans valider l'URL fournie par l'utilisateur.
- **Impacts** : Accès non autorisé aux services internes, lecture de fichiers, exécution de code à distance.
- **Contre-mesures** : Valider et assainir les URLs, restriindre les sorties réseau, utiliser des listes blanches.

## Application dans l'analyse

1. Évaluer chaque risque contre l'application/architecture en cours d'analyse.
2. Documenter les vulnérabilités identifiées avec leur niveau de sévérité (critique, élevé, moyen, faible).
3. Proposer des contre-mesures spécifiques pour chaque vulnérabilité identifiée.
4. Prioriser les remédiations selon l'impact et la faisabilité.
