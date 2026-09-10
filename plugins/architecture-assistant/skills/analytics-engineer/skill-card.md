## Description : <br>
Cette compétence guide le travail d'analytics engineering à travers la transformation dbt, la conception d'entrepôt, la business intelligence, l'orchestration de pipelines et les tests de qualité des données. <br>

Cette compétence est prête pour un usage commercial/non commercial. <br>

## Éditeur : <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### Licence/Conditions d'utilisation : <br>
MIT-0 <br>


## Cas d'usage : <br>
Les développeurs, les ingénieurs de données, les analytics engineers et les équipes BI utilisent cette compétence pour ébaucher des modèles de données, des structures de projet dbt, des tests de qualité, des procédures de gouvernance, des plans de surveillance et des runbooks opérationnels pour les stacks analytiques modernes. <br>

### Zone géographique de déploiement pour l'usage : <br>
Mondiale <br>

## Risques connus et mesures d'atténuation : <br>
Risque : les exemples analytiques générés peuvent être des modèles sensibles pour la production plutôt que du code prêt au déploiement. <br>
Atténuation : réviser et adapter le code généré avant usage, tester les changements en développement ou en staging, et exiger une approbation avant tout déploiement en production. <br>
Risque : les exemples d'entrepôt, de BI ou d'alerting générés peuvent impliquer des identifiants, des données sensibles ou des services privilégiés. <br>
Atténuation : placer les identifiants dans un gestionnaire de secrets, utiliser des comptes de service à moindre privilège, et éviter d'exposer des données d'entrepôt sensibles dans les sorties générées. <br>
Risque : les exemples d'automatisation peuvent rafraîchir des actifs BI, déployer des changements dbt, interroger des données sensibles ou envoyer des alertes par e-mail. <br>
Atténuation : exiger une approbation humaine explicite avant d'exécuter ces actions et vérifier l'environnement cible, les destinataires et le périmètre des données. <br>


## Référence(s) : <br>
- [Analytics Engineer — Exemples de code](references/examples.md) <br>


## Sortie de la compétence : <br>
**Type(s) de sortie :** [texte, markdown, code, commandes shell, configuration, guidance] <br>
**Format de sortie :** [Markdown avec blocs de code en ligne et exemples de configuration] <br>
**Paramètres de sortie :** [1D] <br>
**Autres propriétés liées à la sortie :** [Peut inclure des structures de projet dbt, des exemples SQL et Python, des schémas d'intégration BI, des configurations de surveillance et des runbooks.] <br>

## Version(s) de la compétence : <br>
1.0.0 (source : métadonnées de version serveur) <br>

## Considérations éthiques : <br>
Les utilisateurs doivent évaluer si cette compétence convient à leur environnement, réviser tout fichier généré ou modifié avant de s'y fier, et appliquer les exigences de sûreté, de sécurité et de conformité de leur organisation avant le déploiement. <br>
