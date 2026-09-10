# Modèles de définition de SLA (SLA Templates)

## Système de niveaux de SLA

### Définition des niveaux (Tier)

| Niveau | Nom | Fraîcheur | Taux de disponibilité | Taux d'échec maximal | Temps de réponse | Mode de notification |
|------|------|--------|--------|-----------|----------|----------|
| T1 | Cœur | ≤ 4h | ≥ 99,9% | < 1% | 15 min | PagerDuty + téléphone |
| T2 | Important | ≤ 8h | ≥ 99,5% | < 3% | 1h | Slack + e-mail |
| T3 | Courant | ≤ 24h | ≥ 99,0% | < 5% | 4h | E-mail |

### Critères de qualification d'un pipeline cœur T1
- Impacte directement des fonctionnalités produit orientées client
- Source de données des rapports quotidiens de niveau CEO/VP
- Source de données des rapports financiers
- Données de contrôle des risques/anti-fraude en temps réel

### Critères de qualification d'un pipeline important T2
- Source de données des rapports BI internes
- Support des décisions opérationnelles quotidiennes
- Impacte plusieurs data marts en aval
- Reporting réglementaire (non temps réel)

### Critères de qualification d'un pipeline courant T3
- Analyse exploratoire de données
- Rapports ad hoc internes
- Synchronisation de données non urgente
- Tâches d'archivage/sauvegarde

## Format du fichier de configuration SLA

```yaml
# sla_config.yaml
sla_tiers:
  tier_1_critical:
    name: "Tier 1 — Pipeline cœur"
    freshness_hours: 4
    uptime_pct: 99.9
    max_failure_rate_pct: 1.0
    response_time_minutes: 15
    notification_channels: ["pagerduty", "slack_alert", "phone"]
    escalation_policy: "escalation_t1"

  tier_2_important:
    name: "Tier 2 — Pipeline important"
    freshness_hours: 8
    uptime_pct: 99.5
    max_failure_rate_pct: 3.0
    response_time_minutes: 60
    notification_channels: ["slack_channel", "email"]
    escalation_policy: "escalation_t2"

  tier_3_normal:
    name: "Tier 3 — Pipeline courant"
    freshness_hours: 24
    uptime_pct: 99.0
    max_failure_rate_pct: 5.0
    response_time_minutes: 240
    notification_channels: ["email"]
    escalation_policy: "escalation_t3"

pipelines:
  - name: "orders_etl"
    tier: "tier_1_critical"
    schedule: "every 15 minutes"
    expected_duration_minutes: 10
    owners:
      - name: "Alice Martin"
        email: "zhangsan@company.com"
      - name: "Bruno Petit"
        email: "lisi@company.com"
    sla_window:
      start: "00:00"
      end: "23:59"
    dependencies:
      - "raw_orders_sync"
      - "customer_dim_refresh"
    quality_checks:
      - "row_count > 0"
      - "amount_sum within 5% of yesterday"

  - name: "daily_report_etl"
    tier: "tier_2_important"
    schedule: "daily at 02:00"
    expected_duration_minutes: 45
    owners:
      - name: "Chloé Durand"
        email: "wangwu@company.com"
    sla_window:
      start: "02:00"
      end: "06:00"
    dependencies:
      - "orders_etl"
      - "inventory_etl"

alert_rules:
  freshness_violation:
    description: "La fraîcheur des données dépasse le seuil SLA"
    check: "MAX(updated_at) < NOW() - INTERVAL 'SLA_HOURS hours'"
    action: "notify_owner + create_jira_ticket"

  failure_rate_spike:
    description: "Le taux d'échec augmente de > 200% par rapport à la moyenne des 7 derniers jours"
    check: "failure_rate_24h > avg_failure_rate_7d * 3"
    action: "notify_owner + page_oncall"

  volume_anomaly:
    description: "La variation du volume de données dépasse 50%"
    check: "ABS(row_count - avg_7d) / avg_7d > 0.5"
    action: "notify_owner"

  consecutive_failures:
    description: "Plus de 3 échecs consécutifs"
    check: "consecutive_failed_runs >= 3"
    action: "notify_owner + page_oncall"

notification_channels:
  pagerduty:
    service_key: "${PAGERDUTY_KEY}"
  slack_alert:
    webhook_url: "${SLACK_ALERT_WEBHOOK}"
    channel: "#data-alerts"
  slack_channel:
    webhook_url: "${SLACK_CHANNEL_WEBHOOK}"
    channel: "#data-engineering"
  email:
    smtp_host: "smtp.company.com"
    from: "data-platform@company.com"

escalation_policies:
  escalation_t1:
    steps:
      - delay_minutes: 0
        notify: ["pagerduty"]
      - delay_minutes: 30
        notify: ["phone_primary"]
      - delay_minutes: 60
        notify: ["phone_manager"]
  escalation_t2:
    steps:
      - delay_minutes: 0
        notify: ["slack_channel"]
      - delay_minutes: 60
        notify: ["email", "slack_alert"]
  escalation_t3:
    steps:
      - delay_minutes: 0
        notify: ["email"]
      - delay_minutes: 240
        notify: ["slack_channel"]
```

## Indicateurs du tableau de bord SLA

### KPI obligatoires
1. **Taux global de conformité SLA** — proportion de pipelines respectant le SLA
2. **Fraîcheur des données** — dernier horodatage des données de chaque pipeline
3. **Taux de réussite des pipelines** — nombre d'exécutions réussies / nombre total d'exécutions
4. **Durée d'exécution moyenne** — tendance du temps d'exécution des pipelines
5. **Répartition des échecs** — répartition par pipeline/temps/type d'échec

### Règles d'alerte
```yaml
alerts:
  - name: "Retard du pipeline cœur"
    condition: "latest_run > SLA_hours AND tier == 'tier_1_critical'"
    severity: "critical"

  - name: "Échecs consécutifs du pipeline"
    condition: "consecutive_failures >= 3"
    severity: "critical"

  - name: "Anomalie de volume de données"
    condition: "volume_change_pct > 50 AND tier in ['tier_1_critical', 'tier_2_important']"
    severity: "warning"

  - name: "Dégradation de la durée d'exécution"
    condition: "recent_avg_duration > historical_avg * 2"
    severity: "warning"
```

## Format CSV des journaux d'exécution de pipeline

```csv
pipeline_name,status,start_time,end_time,duration_sec,rows_processed,error_message
orders_etl,success,2025-06-01 02:00:00,2025-06-01 02:08:30,510,152340,
orders_etl,success,2025-06-01 02:15:00,2025-06-01 02:23:45,525,153201,
orders_etl,failed,2025-06-01 02:30:00,2025-06-01 02:32:10,130,0,Connection timeout
daily_report_etl,success,2025-06-01 02:45:00,2025-06-01 03:20:15,2115,8923401,
```

## Modèle de rapport hebdomadaire SLA

```markdown
## Rapport hebdomadaire SLA des pipelines de données (YYYY-MM-DD ~ YYYY-MM-DD)

### Vue d'ensemble
- Nombre total de pipelines : XX
- Taux de conformité SLA : XX.X% (↑/↓ X.X%)
- Nombre total d'exécutions : X,XXX
- Nombre d'échecs : XX

### Événements anormaux
| Heure | Pipeline | Type | Impact | Statut de traitement |
|------|------|------|------|----------|
| ... | ... | ... | ... | ... |

### Analyse des tendances
- Tendance du taux d'échec de la semaine
- Évolution de la durée d'exécution
- Tendance de croissance du volume de données

### Actions d'amélioration
1. ...
2. ...
```

## Liste de contrôle

- [ ] Tous les pipelines se voient-ils attribuer un niveau de SLA (T1/T2/T3) ?
- [ ] Les règles d'alerte et canaux de notification correspondants sont-ils configurés ?
- [ ] Existe-t-il une stratégie d'escalade (remontée automatique en l'absence de réponse) ?
- [ ] Le tableau de bord SLA couvre-t-il les KPI cœur ?
- [ ] La conformité SLA est-elle revue régulièrement (chaque semaine) ?
- [ ] Les journaux de pipeline sont-ils correctement consignés (statut/temps/nombre de lignes/message d'erreur) ?
- [ ] Un processus de RCA (analyse des causes racines) en cas de manquement au SLA est-il défini ?
