---
slug: human-granular-validation
phase: validation
execution: ALWAYS
condition: "Always executes — validation humaine granulaire (issue reste in_review)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [validation_humaine_explicite]
consumes: [{artifact: issue_in_review, required: true}]
requires_stage: [review-and-notification]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Configuration complète (Docker + Terraform), fichiers téléchargeables"
outputs: "Validation humaine explicite (ou demande de modifications → retour en Production)"
---

# Validation humaine granulaire

## Objectif

Obtenir la validation explicite, choix par choix, avant toute action à impact.

> **Validation humaine granulaire.** L'escalade sécurité critique/majeure
> est levée par la **délégation sécurité** ([`../production/security-delegation.md`](../production/security-delegation.md)).
> Sur un constat critique/majeur, le Tech Lead présente l'élément à l'humain, qui tranche choix par choix :
>
> - **Modify** → le Tech Lead mentionne les spécialistes concernés ;
> - **Redo / refus** → téléchargement du fichier pour validation granulaire élément par élément.

## Steps

### Step 1 — Soumettre la configuration complète

Le Tech Lead soumet à l'humain la **configuration complète** (Docker + Terraform), fichiers téléchargeables à l'appui, et demande une **validation explicite** en **un seul message** ([`output-format`](../../protocols/output-format.md)). Ce message porte **quatre groupes de décisions**, chacune validée séparément (Keep / Modify / Redo) :

1. **Livrables** : une décision par fichier (compose, `.tfvars`), avec leurs points d'information.
2. **Dépôt** : les chemins de destination proposés ([`file-deposit`](file-deposit.md) Step 1). **Proposition par défaut : les chemins conventionnels.**
3. **Écriture des clés Vault** ([`file-deposit`](file-deposit.md) Step 3 bis), **indépendante du déploiement Kestra** : l'humain peut la demander même s'il répond « non » à Kestra.
   - **Proposition par défaut : non** (les clés restent une action humaine).
   - Le message montre la liste des clés avec leur **catégorie** (nom + `generable` / `variable` / `humain`).
   - Sur « oui » : le Tech Lead écrit uniquement les clés `generable` et `variable` ; les clés `humain` restent à créer par l'humain.
   - **Absence de réponse = non.**
   - **Une liste modifiée après le « oui » annule l'accord.**
   - Aucune valeur n'est affichée ni transmise.
4. **Déploiement Kestra** ([`kestra-deployment`](kestra-deployment.md)) : lancer le flux `configure_service` après le dépôt.
   - Réponses possibles : **oui** ou **non** (déploiement manuel).
   - **Proposition par défaut : non**, confirmée par l'humain : une action à impact ne se déclenche jamais par défaut.
   - **« Oui » exige que les clés Vault de la stack existent** : déjà créées par l'humain, ou écrites par le Tech Lead sur « oui » à la décision 3.
   - Le message liste les clés (noms seuls) et rappelle les autres prérequis humains (secrets Swarm, dossiers NFS).
   - Clés absentes : répondre « non » ; le déploiement se fera plus tard, hors de ce workflow ou par une nouvelle demande.
   - Le message demande aussi l'environnement (production ou développement).

Un « oui » aux livrables ou au dépôt ne vaut **jamais** « oui » à l'écriture des clés Vault ni au déploiement : les décisions 3 et 4 sont répondues à part. Il n'y a plus de question Kestra posée après le dépôt. **L'issue reste en `in_review`** pendant toute cette phase ; rien n'avance sur un élément non validé (boucle Keep / Modify / Redo, chaque choix séparément).

### Step 2 — Modifications demandées → retour en Production

Si l'humain **demande des modifications** (rejet total ou partiel), le Tech Lead :

1. repasse l'issue en `in_progress` ;
2. intègre les modifications (nouvelle itération des stages de Production concernés + re-contrôle central) ;
3. repasse l'issue en `in_review` une fois la nouvelle version prête.

### Step 3 — Validation → dépôt

Si l'humain **valide** → poursuivre en [`file-deposit.md`](file-deposit.md), puis, si la décision 4 est un « oui », en [`kestra-deployment.md`](kestra-deployment.md), sans nouvelle sollicitation de l'humain.

## Sensors

Outputs: validation humaine explicite consignée. C'est le gate décisionnel **explicite** d'Operation — l'unique gate contraignant (invariant).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ce stage **porte le gate explicite** — le Tech Lead **n'y remonte aucun** candidat-règle : ceux capturés en Production sont consignés et remontés **en fin de workflow**, dans un message séparé ([`closure`](closure.md)), sans mélange avec la validation des livrables ; persistance des apprentissages **confirmés** dans `homelab/rules/` (jamais dans le run courant).
