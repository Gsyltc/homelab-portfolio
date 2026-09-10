# Cadre de gouvernance des données (Data Governance Framework)

## Définition de la source unique de vérité (SSOT)

### Modèle de matrice SSOT

| Entité métier | Système source de référence | Clé primaire | Fréquence de mise à jour | Owner des données | Règle de Golden Record |
|----------|-----------|------|----------|------------|-------------------|
| Client | CRM | customer_id | Temps réel | Service commercial | CRM fait foi, fusionné avec les champs complémentaires de l'ERP |
| Produit | ERP | sku_code | Quotidienne | Service produit | ERP prioritaire, complété par les informations de la plateforme e-commerce |
| Commande | Plateforme e-commerce | order_id | 5 minutes | Service opérations | La plateforme e-commerce fait foi |
| Fournisseur | SRM | vendor_code | Quotidienne | Service achats | SRM fait foi |
| Employé | HRIS | employee_id | Quotidienne | Service ressources humaines | HRIS fait foi |

### Principes de conception de la SSOT
1. **Une entité, une source de référence** — identifier clairement le primary source system de chaque entité
2. **Éviter autant que possible la double écriture** — toutes les écritures doivent passer par le système source de référence
3. **Règles de résolution des conflits** — définir des règles de priorité en cas de conflit de données multi-sources
4. **Golden Record** — générer l'enregistrement optimal par fusion de sources multiples

## Découpage en domaines de données

### Domaines de données courants

| Domaine de données | Entités incluses | Owner typique | Niveau de sécurité |
|--------|----------|-----------|----------|
| Domaine client | Client, contact, adresse | CMO/VP Ventes | Confidentiel |
| Domaine produit | Produit, SKU, catégorie | CPO/VP Produit | Interne |
| Domaine commande | Commande, paiement, remboursement | COO/VP Opérations | Confidentiel |
| Domaine chaîne d'approvisionnement | Fournisseur, achats, stock | CSCO/VP Supply Chain | Interne |
| Domaine financier | Compte, écriture, rapport | CFO | Top secret |
| Domaine RH | Employé, paie, performance | CHRO | Top secret |
| Domaine marketing | Campagne, canal, lead | CMO | Interne |
| Domaine journaux | Journaux de comportement, flux de clics | CTO | Interne |

## Classification et gradation des données

### Standard de classification à quatre niveaux

| Niveau | Nom | Définition | Exemple | Contrôle d'accès | Exigence de chiffrement |
|------|------|------|------|----------|----------|
| L4 | Top secret | Une fuite cause un préjudice grave | Paie, écritures financières, algorithmes cœur | Moindre privilège strict | Chiffrement obligatoire |
| L3 | Confidentiel | Une fuite cause un préjudice important | PII client, détail des commandes, contrats | Autorisation par rôle | Chiffrement recommandé |
| L2 | Interne | Une fuite cause un préjudice mineur | Catalogue produit, organigramme | Visible par les employés | Optionnel |
| L1 | Public | Diffusable à l'externe | Rapport annuel, documentation d'API publique | Sans restriction | Non requis |

### Liste de contrôle du traitement des données PII
- [ ] Identifier et marquer toutes les colonnes contenant des PII (nom, numéro de téléphone, e-mail, numéro d'identité, adresse, etc.)
- [ ] Les colonnes PII sont masquées par défaut à l'affichage (`xxx****@domain.com`, `138****1234`)
- [ ] La transmission des PII doit être chiffrée
- [ ] La durée de conservation des PII ne dépasse pas le besoin métier + les exigences légales
- [ ] Auditer régulièrement les journaux d'accès aux PII

## Rôles et responsabilités

| Rôle | Responsabilité | Personnel typique |
|------|------|----------|
| Owner des données | Responsable final de l'actif de données, approuve les droits d'accès | VP/Director de service métier |
| Intendant des données (Steward) | Gestion quotidienne de la qualité des données, maintenance des métadonnées | Analyste métier senior |
| Architecte de données | Conception des modèles de données, définition des standards | Architecte de données |
| Ingénieur de données | Développement et maintenance des pipelines ETL, exploitation de la plateforme de données | Ingénieur de données |
| Consommateur de données | Utilise les données pour l'analyse et la décision | Analyste, chef de produit |
| Responsable sécurité des données | Audit de conformité, politiques de sécurité | CISO/DPO |

## Standards de données

### Convention de nommage
```
[couche]_[type_entité]_[domaine_métier]_[description]

couche : ods(couche source) / dwd(couche détail) / dws(couche agrégat) / ads(couche application) / dim(couche dimension)
type_entité : fact(table de faits) / dim(table de dimension) / agg(table d'agrégat)
exemple : dwd_fact_ecommerce_orders, dim_customer, dws_agg_daily_sales
```

### Convention de nommage des champs
- Utiliser les minuscules + underscore (snake_case)
- Les champs booléens commencent par `is_` / `has_`
- Les champs temporels se terminent par `_at` (created_at, updated_at)
- Les champs de date se terminent par `_date`
- Les clés étrangères commencent par `fk_`
- Les clés de substitution se terminent par `_sk`

### Standards de types de données
- Type ID : utiliser VARCHAR de longueur adaptée (pas INT, pour éviter le débordement et la confusion de types)
- Type montant : DECIMAL(18,2) ou NUMERIC
- Date : DATE (sans heure)
- Horodatage : TIMESTAMP / DATETIME (avec heure)
- Texte : TEXT / STRING (sans limite de longueur pour éviter la troncature)

## Cycle de vie des données

### Stratégies par étape

| Étape | Données chaudes (0-30 jours) | Données tièdes (30-90 jours) | Données froides (90-365 jours) | Archivage (>1 an) |
|------|----------------|------------------|-------------------|-------------|
| Couche de stockage | SSD haute performance | Stockage standard | Stockage à faible fréquence | Stockage d'archives |
| SLA de requête | À la seconde | À la minute | À la minute | Restauration à la demande |
| Stratégie de partitionnement | DAY | MONTH | YEAR | YEAR |
| Fréquence d'accès | Élevée | Moyenne | Faible | À la demande |
| Stratégie de sauvegarde | Incrémentielle quotidienne | Complète hebdomadaire | Complète mensuelle | Instantané en lecture seule |

### Stratégie de rétention des données
```yaml
retention_policies:
  transaction_data:
    retention: "7 years"  # Exigence de conformité financière
    archive_after: "2 years"
  user_behavior_logs:
    retention: "1 year"
    archive_after: "90 days"
  staging_tables:
    retention: "7 days"
    auto_cleanup: true
  temp_tables:
    retention: "24 hours"
    auto_cleanup: true
```

## Contrôle d'accès aux données

### Modèle RBAC
```yaml
roles:
  data_admin:
    permissions: [SELECT, INSERT, UPDATE, DELETE, DDL]
    scope: all_schemas
  data_engineer:
    permissions: [SELECT, INSERT, UPDATE]
    scope: [dwd, dws, dim, staging]
  data_analyst:
    permissions: [SELECT]
    scope: [dwd, dws, ads, dim]
  data_consumer:
    permissions: [SELECT]
    scope: [ads]  # Couche application uniquement
    masking_rules:
      - column_pattern: "*email*"
        mask: "email_mask"
      - column_pattern: "*phone*"
        mask: "phone_mask"
```

## Liste de contrôle

- [ ] La SSOT des entités métier cœur est-elle définie ?
- [ ] Le découpage en domaines de données et la nomination des Owners sont-ils établis ?
- [ ] La classification et la gradation des données sont-elles terminées ?
- [ ] Les conventions de nommage sont-elles documentées et appliquées ?
- [ ] Une stratégie de cycle de vie des données est-elle définie ?
- [ ] Le contrôle d'accès repose-t-il sur le principe du moindre privilège ?
- [ ] Les données PII sont-elles identifiées et masquées ?
- [ ] Existe-t-il des réunions régulières du comité de gouvernance des données ?
