---
name: cybersecurite
description: "Analyse cybersécurité — Principes fondamentaux : OWASP Top 10, PCI DSS, GDPR, Loi 25, LPRPDE, NIST, COBIT, STRIDE. Fournit les capacités d'analyse pour évaluer la sécurité des architectures, identifier les menaces et proposer des contre-mesures conformes."
---

# Skill: cybersécurité

# Analyse Cybersécurité — Principes fondamentaux

Skill d'analyse cybersécurité pour l'Architecte cybersécurité et le coordinateur Architecture Solution & Intégration. Fournit les capacités d'analyse nécessaires pour évaluer la sécurité des architectures, identifier les menaces et proposer des contre-mesures conformes aux normes et réglementations en vigueur.

## Utilisation

- **Architecte cybersécurité** : utiliser cette skill pour chaque analyse de sécurité d'un projet. Appliquer **uniquement** les principes pertinents selon le contexte (technologies, données traitées, secteur d'activité) et les demandes explicites.
- **Architecture Solution & Intégration (coordinateur)** : utiliser cette skill lors de la coordination pour solliciter l'Architecte cybersécurité sur les aspects sécurité.

## Règles d'activation conditionnelle des principes (IMPORTANT)

**Ne jamais charger l'ensemble des principes d'un coup.** Respecter strictement les catégories ci-dessous pour limiter la taille de la fenêtre de contexte.

### Par défaut — Toujours actifs

| Principe | Fichier | Raison |
|---|---|---|
| **OWASP Top 10** | `principles/owasp-top10.md` | Risques de sécurité des applications web — applicable à tout projet logiciel |
| **STRIDE** | `principles/stride.md` | Modèle d'identification des menaces — fondamental pour toute analyse |

### Conditionnels — Actifs uniquement si documente les risques

| Principe | Fichier | Condition |
|---|---|---|
| **COBIT** | `principles/cobit.md` | Activé si l'analyse doit **documenter les risques** de gouvernance et de gestion IT |
| **NIST** | `principles/nist.md` | Activé si l'analyse doit **documenter les risques** avec le cadre NIST CSF 2.0 ou SP 800-53 |

### Sur demande — Actifs uniquement si explicitement demandés

| Principe | Fichier | Condition |
|---|---|---|
| **PCI DSS** | `principles/pci-dss.md` | Activé uniquement si **explicitement demandé** par l'humain ou le coordinateur |
| **GDPR** | `principles/gdpr.md` | Activé uniquement si **explicitement demandé** par l'humain ou le coordinateur |
| **Loi 25 du Québec** | `principles/loi25-quebec.md` | Activé uniquement si **explicitement demandé** par l'humain ou le coordinateur |
| **LPRPDE** | `principles/lcpp.md` | Activé uniquement si **explicitement demandé** par l'humain ou le coordinateur |

> **Règle stricte** : pour les normes « sur demande » (PCI DSS, GDPR, Loi 25, LPRPDE), l'Architecte cybersécurité ne doit **jamais décider seul** de les appliquer. La norme doit être **explicitement mentionnée** dans la demande par l'humain ou le coordinateur.

## Principes fondamentaux

Cette skill référence 8 principes fondamentaux en cybersécurité. Chaque principe est documenté dans un fichier dédié :

| Principe | Fichier | Description |
|---|---|---|
| OWASP Top 10 | `principles/owasp-top10.md` | Risques de sécurité des applications web |
| PCI DSS | `principles/pci-dss.md` | Sécurité des données de paiement par carte |
| GDPR | `principles/gdpr.md` | Règlement général sur la protection des données (UE) |
| Loi 25 du Québec | `principles/loi25-quebec.md` | Loi modernisant les dispositions de la LPRPDE au Québec |
| Loi canadienne sur la protection des renseignements personnels | `principles/lcpp.md` | Loi canadienne sur la protection des renseignements personnels et les documents électroniques (LPRPDE) |
| NIST | `principles/nist.md` | Cadre de cybersécurité du NIST |
| COBIT | `principles/cobit.md` | Cadre de gouvernance et de gestion de l'IT |
| STRIDE | `principles/stride.md` | Modèle d'identification des menaces par catégorisation |

## Workflow d'analyse

1. **Identifier les principes à activer** selon la demande et les règles ci-dessus.
2. **Évaluer le contexte** : identifier les technologies utilisées, les données traitées, le secteur d'activité, les exigences réglementaires applicables.
3. **Appliquer les principes activés** : lire uniquement les fichiers correspondant aux principes activés et suivre la méthodologie d'analyse décrite.
4. **Croiser les résultats** : identifier les chevauchements et prioriser les recommandations.
5. **Documenter** : produire un rapport d'analyse clair avec les risques identifiés, les recommandations et les priorités.
6. **Créer une issue par aspect** : pour chaque aspect à analyser, créer une issue dédiée avec un titre descriptif.
7. **Notifier** : informer celui qui a sollicité l'analyse (coordinateur ou humain) du résultat en fin de traitement.

## Workflow — Une issue par aspect

Pour chaque aspect à analyser, créer une issue dédiée :
- Titre descriptif (ex. « Analyse cybersécurité — Stratégie d'authentification »)
- Réaliser l'analyse dans cette issue
- Publier les résultats en commentaire
- Référencer l'issue parente si applicable

## Notification obligatoire en fin de traitement

En fin de traitement, **toujours** notifier la personne ou l'agent qui a sollicité l'analyse pour que le traitement puisse se poursuivre :
- Si c'est le **coordinateur (Architecture Solution & Intégration)** : poster un commentaire sur l'issue et le mentionner avec le résultat.
- Si c'est un **humain** : poster un commentaire sur l'issue pour lui transmettre le résultat directement.
- Ne jamais terminer une analyse sans avoir communiqué les résultats à l'auteur de la demande.
- La notification doit contenir un résumé clair des conclusions et des recommandations.

## Contraintes

- Toujours citer les normes et références pertinentes dans les analyses.
- Proposer des solutions concrètes et priorisées.
- Adapter le niveau de détail au contexte (audit technique, conseil stratégique, réponse à incident).
- Ne jamais omettre une exigence réglementaire applicable.
- Respecter le triangle CIA : Confidentialité, Intégrité, Disponibilité.
- **Ne jamais charger plus de principes que nécessaire** — respecter les règles d'activation conditionnelle.

Base directory for this skill: the workspace skills directory (managed by `multica skill`).
Relative paths in this skill (e.g. `principles/`) are relative to this base directory.
