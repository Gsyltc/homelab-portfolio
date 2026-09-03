# Federated Identity

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/federated-identity). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déléguer l'authentification à un fournisseur d'identité externe (IDP) pour centraliser la gestion des identités et des accès, et décharger l'application de l'authentification.

## Quand l'envisager

- Pour s'appuyer sur un annuaire d'entreprise existant (Entra ID/Azure AD, AD) ou un IDP tiers.
- Pour offrir le SSO (authentification unique) à travers plusieurs applications.
- Pour décharger la gestion des utilisateurs, MFA et la détection des menaces.

## Quand ne PAS l'envisager

- Pour des applications isolées sans besoin d'identité d'entreprise ou d'externalisation.
- Lorsque l'externalisation est interdite par la réglementation ou le contexte (données sensibles).
- Si la dépendance à un IDP externe est inacceptable (disponibilité).

## Prérequis

### Logiciel

- Protocoles d'identité (OIDC, OAuth 2.0, SAML) ; bibliothèques client et configuration du fournisseur d'identité.

### Infrastructure

- Fournisseur d'identité (ex. Microsoft Entra ID, AWS IAM Identity Center, Okta) et fédération avec l'annuaire.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Centralisation de l'authentification, MFA et gouvernance des identités. | Dépendance à un fournisseur externe (disponibilité, coût). |
| Réduction du développement lié à la gestion des utilisateurs. | Complexité de fédération et de protocoles. |
| SSO et expérience utilisateur améliorés. | Gouvernance et juridiction des données d'identité à clarifier. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Gestion centralisée des pannes d'authentification et mécanismes de reprise. |
| Sécurité | Externalisation de l'authentification, MFA, détection des menaces, moindre privilège. |
| Efficacité des performances | Déchargement de la gestion des utilisateurs et de l'authentification. |

## Source

[Patron Federated Identity – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/federated-identity)
