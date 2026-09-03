# NIST — Cadre de cybersécurité

## Vue d'ensemble

Le National Institute of Standards and Technology (NIST)提供 plusieurs cadres et standards de cybersécurité. Les plus pertinents sont le NIST Cybersecurity Framework (CSF) et le NIST SP 800-53.

## NIST Cybersecurity Framework (CSF 2.0)

### 6 Fonctions

| Fonction | Description |
|---|---|
| **Govern** | Établir la stratégie de cybersécurité, les politiques, les rôles et les responsabilités |
| **Identify** | Comprendre le contexte organisationnel, les risques et les ressources |
| **Protect** | Mettre en œuvre les mesures de sécurité pour protéger les actifs |
| **Detect** | Détecter les événements de sécurité en temps opportun |
| **Respond** | Agir en cas d'incident de sécurité |
| **Recupérer** | Rétablir les capacités et services touchés |

### Categories et Sous-categories

Chaque fonction contient des catégories et sous-catégories détaillant les résultats attendus. Exemple :

**Govern (GV) :**
- GV.OC — Contexte organisationnel
- GV.RM — Gestion des risques
- GV.PO — Politiques
- GV.OV — Supervision
- GV.SC — Chaîne d'approvisionnement

**Identify (ID) :**
- ID.AM — Gestion des actifs
- ID.RA — Évaluation des risques
- ID.IM — Amélioration continue

**Protect (PR) :**
- PR.AA — Gestion des accès et de l'authentification
- PR.AT — Sensibilisation et formation
- PR.DS — Sécurité des données
- PR.PS — Sécurité de la plateforme
- PR.IR — Résilience de l'infrastructure

**Detect (DE) :**
- DE.CM — Surveillance continue
- DE.AE — Analyse adverse

**Respond (RS) :**
- RS.MA — Gestion des incidents
- RS.AN — Analyse des incidents
- RS.CO — Communications
- RS.MI — Atténuation

**Recover (RC) :**
- RC.RP — Plan de récupération
- RC.CO — Communications de récupération

## NIST SP 800-53 — Contrôles de sécurité

Le NIST SP 800-53 catalogue plus de 1000 contrôles de sécurité organisés en familles :

| Famille | Description |
|---|---|
| AC | Contrôle d'accès |
| AT | Sensibilisation et formation |
| Audit et accountability | Audit et responsabilité |
| CA | Évaluation de la sécurité et affirmação |
| CM | Gestion de la configuration |
| CP | Planification de continuité d'activité |
| IA | Identification et authentification |
| IR | Response à incident |
| MA | Maintenance |
| MP | Protection des médias |
| PE | Protection physique et environnementale |
| PL | Planification de la sécurité |
| PM | Programmes de sécurité organisationnels |
| PS | Gestion de la sécurité du personnel |
| PT | Protection des renseignements personnels |
| RA | Évaluation des risques |
| SA | Acquisition du système |
| SC | Sécurité et protection des communications |
| SI | Intégrité du système |
| SR | Chaîne d'approvisionnement |

## Application dans l'analyse

1. Appliquer le CSF 2.0 en commençant par Govern pour définir le contexte.
2. Identifier les catégories pertinentes selon le projet.
3. Pour chaque catégorie, évaluer le niveau de maturité actuel.
4. Proposer des contrôles NIST SP 800-53 spécifiques si nécessaire.
5. Documenter les recommandations avec les références exactes (ex. PR.DS-1).
6. Prioriser selon l'impact et la faisabilité.
