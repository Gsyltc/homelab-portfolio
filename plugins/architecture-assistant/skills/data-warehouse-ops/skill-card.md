## Description : <br>
La compétence d'exploitation d'entrepôt de données aide les équipes d'ingénierie des données à concevoir, générer et vérifier des actifs de modélisation d'entrepôt, d'ETL/ELT, de qualité des données, de partitionnement, d'optimisation des coûts, de gouvernance, de lignage et de surveillance des SLA. <br>

Cette compétence est prête pour un usage commercial/non commercial. <br>

## Éditeur : <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### Licence/Conditions d'utilisation : <br>
MIT-0 <br>


## Cas d'usage : <br>
Les ingénieurs de données, les analytics engineers et les équipes de plateforme d'entrepôt utilisent cette compétence pour planifier l'architecture de l'entrepôt et générer des actifs opérationnels de modélisation, de pipelines, de vérifications de qualité, de partitionnement, d'optimisation des coûts, de gouvernance, de lignage et de surveillance des SLA. <br>

### Zone géographique de déploiement pour l'usage : <br>
Mondiale <br>

## Risques connus et mesures d'atténuation : <br>
Risque : les fichiers liés à l'entrepôt tels que le SQL, le DDL, les journaux de requêtes, les exports de facturation et les historiques de pipelines peuvent contenir des données opérationnelles ou métier sensibles. <br>
Atténuation : utiliser des échantillons expurgés lorsque c'est possible et éviter de fournir à l'agent des secrets de production ou des lignes sensibles inutiles. <br>
Risque : le SQL, les DAG Airflow et les modèles dbt générés peuvent affecter les tables ou les pipelines de l'entrepôt s'ils sont exécutés sans revue. <br>
Atténuation : réviser les actifs générés dans un environnement hors production avant exécution, en particulier les instructions qui écrasent, fusionnent, tronquent ou suppriment des tables. <br>
Risque : les rapports HTML générés chargent du JavaScript depuis des sources CDN. <br>
Atténuation : n'ouvrir les rapports générés que dans des environnements où le JavaScript chargé depuis un CDN est acceptable selon la politique de sécurité locale. <br>


## Référence(s) : <br>
- [Cadre de gouvernance des données (Data Governance Framework)](references/governance_framework.md) <br>
- [Bibliothèque de modèles SQL (SQL Templates for Data Warehouse)](references/sql_templates.md) <br>
- [Bonnes pratiques de modélisation dimensionnelle (Dimensional Modeling Best Practices)](references/dimensional_modeling.md) <br>
- [Référentiel des règles de qualité des données (Data Quality Rules Reference)](references/data_quality_rules.md) <br>
- [Référence des stratégies de partitionnement (Partition Strategies Reference)](references/partition_strategies.md) <br>
- [Modèles de définition de SLA (SLA Templates)](references/sla_templates.md) <br>
- [Page de la compétence sur ClawHub](https://clawhub.ai/bettermen/skills/data-warehouse-ops) <br>


## Sortie de la compétence : <br>
**Type(s) de sortie :** [texte, markdown, code, commandes shell, configuration, guidance] <br>
**Format de sortie :** [guidance Markdown avec SQL, YAML, Python, commandes shell et fichiers de rapport HTML générés] <br>
**Paramètres de sortie :** [1D] <br>
**Autres propriétés liées à la sortie :** [Peut générer des modèles DDL, dbt ou Airflow, des vérifications de qualité des données, des graphes de lignage, des rapports de coûts et des tableaux de bord SLA à réviser avant tout usage en production.] <br>

## Version(s) de la compétence : <br>
1.0.0 (source : preuve de version serveur) <br>

## Considérations éthiques : <br>
Les utilisateurs doivent évaluer si cette compétence convient à leur environnement, réviser tout fichier généré ou modifié avant de s'y fier, et appliquer les exigences de sûreté, de sécurité et de conformité de leur organisation avant le déploiement. <br>
