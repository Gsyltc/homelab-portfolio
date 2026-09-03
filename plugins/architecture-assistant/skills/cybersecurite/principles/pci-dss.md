# PCI DSS — Sécurité des données de paiement par carte

## Vue d'ensemble

PCI DSS (Payment Card Industry Data Security Standard) est une norme de sécurité mondiale pour les organisations qui traitent, stockent ou transmettent des informations de cartes de crédit ou de débit. Elle est gérée par le PCI Security Standards Council (PCI SSC).

## Les 6 objectifs et 12 exigences

### Objectif 1 : Construire et maintenir un réseau et des systèmes sécurisés
1. Installer et maintenir un pare-feu de contrôle de sécurité pour protéger les données des titulaires de carte.
2. Ne pas utiliser les paramètres de sécurité par défaut des fournisseurs de systèmes.

### Objectif 2 : Protéger les données des titulaires de carte
3. Protéger les données stockées des titulaires de carte.
4. Chiffrer la transmission des données des titulaires de carte sur les réseaux publics ouverts.

### Objectif 3 : Maintenir un programme de gestion des vulnérabilités
5. Utiliser et mettre à jour régulièrement un logiciel anti-virus ou des programmes anti-malwares.
6. Développer et maintenir des systèmes et applications sécurisés.

### Objectif 4 : Mettre en œuvre des mesures de contrôle d'accès strictes
7. Restreindre l'accès aux données des titulaires de carte selon le besoin d'en connaître.
8. Attribuer un identifiant unique à chaque personne ayant accès aux systèmes informatiques.
9. Restreindre l'accès physique aux données des titulaires de carte.

### Objectif 5 : Surveiller et tester régulièrement les réseaux
10. Traquer et surveiller l'accès aux ressources réseau et aux données des titulaires de carte.
11. Tester régulièrement les systèmes et processus de sécurité.

### Objectif 6 : Maintenir une politique de sécurité de l'information
12. Maintenir une politique qui traite la sécurité de l'information pour le personnel.

## Niveaux de conformité

| Niveau | Nombre de transactions | Exigences |
|---|---|---|
| Niveau 1 | Plus de 6 millions de transactions/an | Audit QSA annuel + scans ASV trimestriels |
| Niveau 2 | 1 à 6 millions de transactions/an | Auto-évaluation annuelle + scans ASV trimestriels |
| Niveau 3 | 20 000 à 1 million de transactions e-commerce/an | Auto-évaluation annuelle + scans ASV trimestriels |
| Niveau 4 | Moins de 20 000 transactions e-commerce/an ou moins de 1 million de transactions/an | Auto-évaluation recommandée + scans ASV trimestriels |

## Données couvertes

- Numéro de carte (PAN)
- Date d'expiration
- Code de service (CVV/CVC)
- Nom du titulaire
- Données de piste magnétique

## Application dans l'analyse

1. Vérifier si le projet traite des données de paiement par carte.
2. Si oui, identifier le niveau de conformité applicable.
3. Évaluer chaque exigence PCI DSS contre l'architecture proposée.
4. Documenter les écarts et proposer un plan de conformité.
5. Prioriser les actions critiques (encryption, accès physique, réseau).
