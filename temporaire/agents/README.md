# Agents du workspace

Export de 12 agents Multica.

| Agent | Fichier | Description |
|---|---|---|
| Alfred - Agent de notifications 🤖 | [alfred-agent-de-notifications.md](./alfred-agent-de-notifications.md) | Responsable des notifications de fin de tâches. |
| André - Spécialiste Terraform 🐧 | [andre-specialiste-terraform.md](./andre-specialiste-terraform.md) | Spécialiste Terraform du Homelab : écrit et modifie les fichiers Terraform .tf/.tfvars d'une stack (skill configuration-applications). N'exécute JAMAIS terraform init/apply/destroy — il prépare, l'humain exécute. Contrôle qualité par le Tech Lead. |
| Bob - Spécialiste Docker 🧠 | [bob-specialiste-docker.md](./bob-specialiste-docker.md) | Spécialiste Docker du Homelab : crée et modifie les fichiers docker-compose optimisés Docker Swarm (skill docker-composer). Il produit le livrable ; la vérification/correction revient au QA Docker. |
| Hector - Leader Analyses Financières 👾 | [hector-leader-analyses-financieres.md](./hector-leader-analyses-financieres.md) | Leader de l'équipe d'analyse financière : coordonne Leo (data), Nestor (technique) et Victor (fondamental), synthétise par Actions/FNB/Entreprise et produit des rapports pour investisseur intermédiaire. |
| Hugo - Expert Home Assistant 🌙 | [hugo-expert-home-assistant.md](./hugo-expert-home-assistant.md) | Expert en domotique Home Assistant, pilote l'installation via le serveur MCP officiel (interrogation et contrôle des entités, scènes, automatisations). |
| Kevin -QA Docker 🔥 | [kevin-qa-docker.md](./kevin-qa-docker.md) | QA Docker du Homelab : vérifie et corrige les docker-compose produits par le Spécialiste Docker — syntaxe YAML, compatibilité Swarm, hardening, cohérence Traefik (docker-composer, dockerfile-validator, traefik-manager-read). Intervient après la création. |
| Leo - Data Provider ⭐ | [leo-data-provider.md](./leo-data-provider.md) | Collecte les données de marché et fondamentales des titres canadiens de titres.md (sources gratuites), livrables data/<TICKER>.json + data/synthese.json. |
| Marilyne - Expert n8n 🐙 | [marilyne-expert-n8n.md](./marilyne-expert-n8n.md) | Expert n8n : crée, modifie, analyse et optimise les flux n8n, et diagnostique bugs et problèmes de performance via le serveur MCP de l'instance. |
| Mika 🦄 | [mika.md](./mika.md) | Your workspace Chief of Staff. Mika turns goals into issues, coordinates agents, and helps build reusable workflows. |
| Nestor - Analyse Technique 🐧 | [nestor-analyse-technique.md](./nestor-analyse-technique.md) | Expert en analyse technique : indicateurs (MM, RSI, MACD, Bollinger), tendances 1J/1S/1M, risques et avis pour les titres de titres.md. |
| Stuart - Teach Lead Homelab 🐸 | [stuart-teach-lead-homelab.md](./stuart-teach-lead-homelab.md) | Tech Lead Homelab, Leader de l'équipe DevOps : coordonne Spécialiste Docker, QA Docker, Spécialiste Terraform, Expert n8n et Expert Home Assistant ; supervise Ansible, Kestra, surveillance Homelab. Contrôle qualité central avant revue humaine. |
| Victor - Analyse Fondamentale ⚡ | [victor-analyse-fondamentale.md](./victor-analyse-fondamentale.md) | Expert en analyse fondamentale : news par titre, tendances marché et géopolitiques, santé de l'entreprise, risques et points positifs 1J/1S/1M. |
