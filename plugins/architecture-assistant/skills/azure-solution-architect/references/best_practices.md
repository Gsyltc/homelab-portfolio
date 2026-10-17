# Azure Best Practices for Startups

Production-ready practices for serverless, cost optimization, security, and operational excellence, aligned with the Azure Well-Architected Framework.

---

## Table of Contents

- [Serverless Best Practices](#serverless-best-practices)
- [Cost Optimization](#cost-optimization)
- [Security Hardening](#security-hardening)
- [Scalability Patterns](#scalability-patterns)
- [DevOps and Reliability](#devops-and-reliability)
- [Common Pitfalls](#common-pitfalls)

---

## Serverless Best Practices

### Azure Functions Design

#### 1. Keep Functions Stateless

Store state externally in Cosmos DB, Blob Storage, or Azure Cache for Redis.

```python
# BAD: Function-level state
cache = {}

def main(event):
    if event['key'] in cache:
        return cache[event['key']]
    # ...

# GOOD: External state
from azure.cosmos import CosmosClient
container = CosmosClient.from_connection_string(conn).get_database_client("db").get_container_client("cache")

def main(event):
    items = list(container.read_item(item=event['key'], partition_key=event['key']))
    if items:
        return items['value']
    # ...
```

#### 2. Implement Idempotency

Handle retries gracefully with unique request IDs.

```python
import hashlib, time
from azure.cosmos import CosmosClient

container = CosmosClient.from_connection_string(conn).get_database_client("db").get_container_client("idempotency")

def main(event):
    idempotency_key = hashlib.sha256(
        f"{event['orderId']}-{event['action']}".encode()
    ).hexdigest()

    try:
        existing = container.read_item(item=idempotency_key, partition_key=idempotency_key)
        return existing['result']
    except Exception:
        pass

    result = process_order(event)

    container.upsert_item({
        'id': idempotency_key,
        'pk': idempotency_key,
        'result': result,
        'ttl': 86400  # 24h TTL
    })
    return result
```

#### 3. Optimize Cold Starts

```python
# Initialize outside the function entry point (reused across invocations)
from azure.cosmos import CosmosClient

client = CosmosClient.from_connection_string(conn)   # once per worker
container = client.get_database_client("db").get_container_client("my-container")

def main(event):
    return container.read_item(item=event['id'], partition_key=event['id'])
```

**Cold Start Reduction Techniques:**
- Use the Premium plan with pre-warmed instances for critical paths
- Minimize package size and dependency count
- Choose interpreted languages (Python, Node.js) over heavy startup runtimes
- Avoid unnecessary VNet integration (adds cold-start latency)

#### 4. Set Appropriate Timeouts

```json
// host.json
{
  "functionTimeout": "00:00:30",
  "extensions": { "http": { "routePrefix": "api" } }
}
```

**Timeout Guidelines:**
- API handlers: 10-30 seconds
- Event processors: 60-300 seconds
- Use Durable Functions for long/multi-step workflows

---

## Cost Optimization

### 1. Right-Sizing Strategy

```bash
# Check VM utilization via Azure Monitor metrics
az monitor metrics list \
  --resource <vm-resource-id> \
  --metric "Percentage CPU" \
  --start-time $(date -d '7 days ago' -u +"%Y-%m-%dT%H:%M:%SZ") \
  --end-time $(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --interval PT1H \
  --aggregation Average
```

**Right-Sizing Rules:**
- <10% CPU average: downsize SKU
- >80% CPU average: upgrade SKU or scale out
- Review Azure Advisor recommendations monthly for the first 6 months

### 2. Reservations and Savings Plans

| Commitment | Savings | Best For |
|------------|---------|----------|
| Savings Plan, 1-year | ~20-30% | Flexible compute, unknown future |
| Reserved Instance, 1-year | ~30-40% | Stable, specific SKUs |
| Reserved Instance, 3-year | ~50-60% | Stable long-term workloads |

```bash
# Review reservation recommendations
az consumption reservation recommendation list --output table
```

### 3. Blob Lifecycle Policies

```json
{
  "rules": [
    {
      "name": "transition-to-cheaper-storage",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["logs/"] },
        "actions": {
          "baseBlob": {
            "tierToCool": { "daysAfterModificationGreaterThan": 30 },
            "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
            "delete": { "daysAfterModificationGreaterThan": 365 }
          }
        }
      }
    }
  ]
}
```

### 4. Functions Plan Optimization

Match plan to workload. Consumption scales to zero (cheapest for spiky traffic); Premium removes cold starts and adds VNet at a fixed baseline cost.

```
Consumption: pay per execution + GB-s, scale to zero
Premium EP1: pre-warmed instances, VNet, higher baseline cost
Dedicated (App Service plan): fixed capacity, predictable billing
```

### 5. NAT Gateway / Egress Alternatives

```
NAT Gateway: hourly + per-GB processed

Alternatives:
1. Private Endpoints: private access to Azure PaaS without egress through NAT
2. Service Endpoints: free, VNet-to-PaaS over the Azure backbone
3. No NAT: keep workloads on PaaS with private endpoints
```

### 6. Log Retention

```bash
# Set Log Analytics workspace retention to avoid unbounded growth
az monitor log-analytics workspace update \
  --resource-group my-rg \
  --workspace-name my-logs \
  --retention-time 30
```

**Retention Guidelines:**
- Development: 7-30 days
- Production non-critical: 30 days
- Production critical: 90 days
- Compliance requirements: As specified

---

## Security Hardening

### 1. RBAC Least Privilege

```jsonc
// BAD: Overly permissive (Owner/Contributor at subscription scope)
{ "role": "Contributor", "scope": "/subscriptions/<sub>" }

// GOOD: Narrow built-in role at the smallest scope
{
  "role": "Cosmos DB Built-in Data Contributor",
  "scope": ".../databaseAccounts/users/dbs/app/colls/users",
  "principalType": "ServicePrincipal"
}
```

### 2. Encryption Configuration

```bicep
// Encryption is on by default; use customer-managed keys (CMK) for control
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${appName}sa'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    encryption: {
      services: { blob: { enabled: true }, file: { enabled: true } }
      keySource: 'Microsoft.Keyvault'
      keyvaultproperties: { keyname: cmkKeyName, keyvaulturi: keyVault.properties.vaultUri }
    }
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}
```

### 3. Network Isolation

```bicep
// Private subnets with private endpoints to PaaS
resource appSubnet 'Microsoft.Network/virtualNetworks/subnets@2023-09-01' = {
  name: 'app'
  properties: {
    addressPrefix: '10.0.11.0/24'
    privateEndpointNetworkPolicies: 'Enabled'
  }
}

// Cosmos DB reached only via private endpoint; public network access disabled
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: '${appName}-cosmos'
  location: location
  properties: {
    databaseAccountOfferType: 'Standard'
    publicNetworkAccess: 'Disabled'
    locations: [ { locationName: location, failoverPriority: 0 } ]
  }
}
```

### 4. Secrets Management

```python
# Never hardcode secrets — use Key Vault + Managed Identity
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url="https://my-vault.vault.azure.net", credential=DefaultAzureCredential())

def get_secret(name):
    return client.get_secret(name).value

db_password = get_secret("prod-database-password")
```

### 5. API Protection

```bicep
// Azure WAF on Application Gateway / Front Door
resource wafPolicy 'Microsoft.Network/ApplicationGatewayWebApplicationFirewallPolicies@2023-09-01' = {
  name: '${appName}-waf'
  location: location
  properties: {
    policySettings: { state: 'Enabled', mode: 'Prevention' }
    managedRules: {
      managedRuleSets: [ { ruleSetType: 'OWASP', ruleSetVersion: '3.2' } ]
    }
    customRules: [
      {
        name: 'RateLimit'
        priority: 1
        ruleType: 'RateLimitRule'
        action: 'Block'
        rateLimitThreshold: 2000
        matchConditions: [ /* IP-based */ ]
      }
    ]
  }
}
```

### 6. Audit Logging

```bash
# Route the subscription Activity Log and resource diagnostics to Log Analytics
az monitor diagnostic-settings subscription create \
  --name audit-to-logs \
  --location eastus \
  --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true}]' \
  --workspace <log-analytics-workspace-id>
```

---

## Scalability Patterns

### 1. Horizontal vs Vertical Scaling

```
Horizontal (preferred):
- Add more Functions instances (scale-out)
- Add more Container Apps replicas (KEDA)
- Increase Cosmos DB RU/s or enable autoscale

Vertical (when necessary):
- Larger Functions Premium SKU
- Upgrade PostgreSQL/SQL compute tier
- Larger VM size
```

### 2. Database Partitioning

```python
# Partition by tenant ID (Cosmos DB logical partition key)
def partition_key(tenant_id):
    return f"TENANT#{tenant_id}"

# Or shard across containers for very high throughput
def container_for_tenant(tenant_id, num_shards):
    return f"data-shard-{hash(tenant_id) % num_shards}"
```

### 3. Caching Layers

```
Edge (Front Door):        Global, static content, TTL: hours-days
Application (Redis):      Regional, session/query cache, TTL: minutes-hours
Database (integrated):    Cosmos DB integrated cache, TTL: minutes
```

```python
# Azure Cache for Redis caching pattern
import redis, json

cache = redis.Redis(host='my-cache.redis.cache.windows.net', port=6380, ssl=True, password=key)

def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.get_user(user_id)
    cache.setex(f"user:{user_id}", 300, json.dumps(user))  # 5 min
    return user
```

### 4. Auto-Scaling Configuration

```bicep
// Container Apps KEDA HTTP scaling
resource app 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  location: location
  properties: {
    template: {
      scale: {
        minReplicas: 2
        maxReplicas: 10
        rules: [
          { name: 'http-rule', http: { metadata: { concurrentRequests: '50' } } }
        ]
      }
    }
  }
}
```

---

## DevOps and Reliability

### 1. Infrastructure as Code

```bash
# Version control all infrastructure (Bicep)
git init
git add .
git commit -m "Initial infrastructure setup"

# Separate deployments per environment
az deployment group create -g app-dev-rg     --template-file main.bicep --parameters env=dev
az deployment group create -g app-staging-rg --template-file main.bicep --parameters env=staging
az deployment group create -g app-prod-rg    --template-file main.bicep --parameters env=production
```

### 2. Blue/Green & Canary Deployments

```bicep
// Container Apps traffic splitting across revisions (blue/green or canary)
resource app 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  properties: {
    configuration: {
      ingress: {
        traffic: [
          { revisionName: '${appName}--blue',  weight: 90 }
          { revisionName: '${appName}--green', weight: 10 }
        ]
      }
    }
  }
}
```

### 3. Health Checks

```python
# Application health endpoint
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/health')
def health():
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'external_api': check_external_api()
    }
    status = 'healthy' if all(checks.values()) else 'unhealthy'
    code = 200 if status == 'healthy' else 503
    return jsonify({'status': status, 'checks': checks}), code

def check_database():
    try:
        db.execute('SELECT 1')
        return True
    except Exception:
        return False
```

### 4. Monitoring Setup

```bicep
// Application Insights + metric alert
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${appName}-ai'
  location: location
  kind: 'web'
  properties: { Application_Type: 'web', WorkspaceResourceId: logAnalytics.id }
}

resource errorAlert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'high-error-rate'
  location: 'global'
  properties: {
    severity: 2
    scopes: [ functionApp.id ]
    evaluationFrequency: 'PT1M'
    windowSize: 'PT5M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [
        { name: 'errors', metricName: 'Http5xx', operator: 'GreaterThan', threshold: 10, timeAggregation: 'Total' }
      ]
    }
    actions: [ { actionGroupId: actionGroup.id } ]
  }
}
```

---

## Common Pitfalls

### Technical Debt

| Pitfall | Solution |
|---------|----------|
| Over-engineering early | Start simple, scale when needed |
| Under-monitoring | Set up Application Insights from day one |
| Ignoring costs | Enable Cost Management budgets and alerts |
| Single region only | Plan for multi-region / zones from start |

### Security Mistakes

| Mistake | Prevention |
|---------|------------|
| Public storage containers | Disable public blob access, use SAS / RBAC |
| Overly permissive RBAC | Never use Owner broadly; scope narrow roles |
| Hardcoded credentials | Use Key Vault + managed identities |
| Unencrypted data | Encryption on by default; add CMK where required |

### Performance Issues

| Issue | Solution |
|-------|----------|
| No caching | Add Front Door, Azure Cache for Redis early |
| Inefficient queries | Use proper partition keys, avoid cross-partition scans |
| Large function packages | Trim dependencies, use Premium pre-warm |
| N+1 queries | Batch operations, server-side joins where possible |

### Cost Surprises

| Surprise | Prevention |
|----------|------------|
| Undeleted resources | Tag everything, review with Azure Advisor weekly |
| Data transfer / egress costs | Keep traffic within region / availability zone |
| NAT Gateway charges | Use private/service endpoints for Azure PaaS |
| Log accumulation | Set Log Analytics retention policies |
