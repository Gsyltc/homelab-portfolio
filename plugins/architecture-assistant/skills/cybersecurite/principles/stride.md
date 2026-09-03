# STRIDE — Modèle d'identification des menaces

## Vue d'ensemble

STRIDE est un modèle d'identification des menaces développé par Microsoft. Il catégorise les menaces en 6 types, chacun associé à une propriété de sécurité compromise. Il est utilisé conjointement avec le modelage des menaces pour identifier les vulnérabilités d'un système.

## Les 6 catégories de menaces

### S — Spoofing (Usurpation d'identité)
- **Propriété compromise** : Authenticité
- **Description** : Se faire passer pour un utilisateur, un système ou une entité légitime.
- **Exemples** :
  - Usurpation d'identité d'un utilisateur via des identifiants volés
  - Falsification d'adresses IP
  - Phishing pour obtenir des identifiants
  - Attaques par passe relais (pass-the-hash)
- **Contre-mesures** :
  - Authentification multi-facteurs (MFA)
  - Certificats et signatures numériques
  - Validation des entrées et des sessions
  - Détection d'usurpation

### T — Tampering (Falsification)
- **Propriété compromise** : Intégrité
- **Description** : Modification non autorisée de données, de messages ou de configurations.
- **Exemples** :
  - Modification de données en transit
  - Altération de logs ou de journaux
  - Falsification de paramètres de configuration
  - Injection de code dans les requêtes
- **Contre-mesures** :
  - Chiffrement et intégrité des données
  - Signatures numériques et HSM
  - Protection des logs et journaux
  - Validation et sanitization des entrées

### R — Repudiation (Désaveu)
- **Propriété compromise** : Traçabilité
- **Description** : Nier avoir effectué une action.
- **Exemples** :
  - Refuser avoir effectué une transaction financière
  - Nier avoir accédé à des données sensibles
  - Altération de preuves d'audit
- **Contre-mesures** :
  - Journalisation complète et non altérable
  - Horodatage certifié
  - Signatures numériques sur les actions
  - Surveillance et alertes

### I — Information Disclosure (Divulgation d'informations)
- **Propriété compromise** : Confidentialité
- **Description** : Accès non autorisé à des informations sensibles.
- **Exemples** :
  - Fuite de données personnelles
  - Exposition d'erreurs détaillées
  - Canaux auxiliaires (timing, énergie)
  - Métadonnées exposées
- **Contre-mesures** :
  - Chiffrement au repos et en transit
  - Masquage des erreurs
  - Protection des métadonnées
  - DLP (Data Loss Prevention)

### D — Denial of Service (Déni de service)
- **Propriété compromise** : Disponibilité
- **Description** : Rendre un service indisponible ou dégradé.
- **Exemples** :
  - Attaques DDoS
  - Saturation de ressources (CPU, mémoire, bande passante)
  - Boucles infinies ou récursion excessive
  - Exclusion de ressources (resource exhaustion)
- **Contre-mesures** :
  - Limitation de débit (rate limiting)
  - Redondance et haute disponibilité
  - Détection et mitigation DDoS
  - Protection contre les attaques par déni de service

### E — Elevation of Privilege (Élévation de privilèges)
- **Propriété compromise** : Autorisation
- **Description** : Obtenir un niveau d'accès supérieur à celui autorisé.
- **Exemples** :
  - Exploitation de failles pour obtenir les droits root/admin
  - Attaques par injection pour exécuter du code
  - Bypass de contrôles d'accès
  - Exploitation de vulnérabilités zero-day
- **Contre-mesures** :
  - Principe du moindre privilège
  - Sandboxing et isolation
  - Mises à jour et correctifs de sécurité
  - Tests de pénétration réguliers

## Matrice de menaces

| Catégorie | Propriété | Questions à se poser |
|---|---|---|
| Spoofing | Authenticité | L'identité peut-elle être falsifiée ? |
| Tampering | Intégrité | Les données peuvent-elles être modifiées ? |
| Repudiation | Traçabilité | L'action peut-elle être niée ? |
| Information Disclosure | Confidentialité | Les données sensibles peuvent-elles être exposées ? |
| Denial of Service | Disponibilité | Le service peut-il être mis hors ligne ? |
| Elevation of Privilege | Autorisation | Un accès non autorisé est-il possible ? |

## Application dans l'analyse

1. Pour chaque composant de l'architecture, évaluer les 6 catégories STRIDE.
2. Pour chaque menace identifiée, évaluer la probabilité et l'impact.
3. Proposer des contre-mesures spécifiques pour chaque menace.
4. Documenter la matrice de menaces dans le rapport d'analyse.
5. Prioriser les remédiations selon le risque (probabilité × impact).
6. Croiser avec les autres normes (OWASP, NIST) pour une couverture complète.
