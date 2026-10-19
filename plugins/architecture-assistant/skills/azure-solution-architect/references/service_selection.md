# Azure Service Selection Guide

Quick reference for choosing the right Azure service based on requirements.

---

## Table of Contents

- [Compute Services](#compute-services)
- [Database Services](#database-services)
- [Storage Services](#storage-services)
- [Messaging and Events](#messaging-and-events)
- [API and Integration](#api-and-integration)
- [Networking](#networking)
- [Security and Identity](#security-and-identity)

---

## Compute Services

### Decision Matrix

| Requirement | Recommended Service |
|-------------|---------------------|
| Event-driven, short tasks | Azure Functions |
| Containerized apps, microservices | Container Apps |
| Custom configs, GPU/specialized hardware | Virtual Machines / VM Scale Sets |
| Simple container from source | Container Apps / App Service |
| Kubernetes workloads | Azure Kubernetes Service (AKS) |
| Batch processing | Azure Batch |

### Azure Functions

**Best for:** Event-driven functions, API backends, scheduled tasks

```
Limits (Consumption plan):
- Execution: 5 min default, up to 10 min
- Memory: up to 1.5 GB per instance
- Scale-out: up to 200 instances
- Premium/Dedicated plans lift time and VNet limits

Pricing: Per execution + GB-seconds (consumption), free grant included
```

**Use when:**
- Variable/unpredictable traffic
- Pay-per-use is important
- No server management desired
- Short-duration operations

**Avoid when:**
- Long-running processes (use Durable Functions or Container Apps)
- Consistent low-latency (<50ms) needs (consider Premium plan)
- Heavy sustained compute (consider Container Apps)

### Container Apps

**Best for:** Containerized applications, microservices

```
Limits:
- vCPU: 0.25 - 4 per replica
- Memory: 0.5 GB - 8 GB per replica
- Scaling: KEDA-based (HTTP, queue, custom metrics), scale to zero

Pricing: Per vCPU-second + GiB-second (with free monthly grant)
```

**Use when:**
- Containerized applications
- Event- or HTTP-driven scaling (including scale to zero)
- Long-running processes
- Need more control than Functions

### Virtual Machines

**Best for:** Custom configurations, specialized hardware, lift-and-shift

```
VM Families:
- General: B, Dsv5
- Compute: Fsv2
- Memory: Esv5
- GPU: NC, ND
- Storage: Lsv3
```

**Use when:**
- Need GPU/specialized hardware
- Windows Server workloads (managed by Infrastructure Windows)
- Specific OS/instance configurations
- Reserved capacity makes sense

---

## Database Services

### Decision Matrix

| Data Type | Query Pattern | Scale | Recommended |
|-----------|--------------|-------|-------------|
| Key-value / document | Simple lookups | Any | Cosmos DB |
| Document | Flexible queries | <1TB | Cosmos DB (MongoDB API) |
| Relational | Complex joins | Variable | Azure Database for PostgreSQL Flexible Server |
| Relational | High volume, T-SQL | Fixed | Azure SQL Database |
| Time-series | Time-based | Any | Azure Data Explorer |
| Graph | Relationships | Any | Cosmos DB (Gremlin API) |

### Cosmos DB

**Best for:** Key-value and document data, serverless and globally distributed apps

```
Limits:
- Item size: 2 MB max
- Partition key throughput: 10,000 RU/s logical partition
- Multiple APIs: NoSQL, MongoDB, Cassandra, Gremlin, Table

Pricing:
- Serverless: per RU consumed
- Provisioned / autoscale: per RU/s per hour
```

**Data Modeling Example:**

```
# Single-container design for e-commerce (partition key = /pk)
pk                  id                  Attributes
USER#123            PROFILE             {name, email, ...}
USER#123            ORDER#456           {total, status, ...}
USER#123            ORDER#456#ITEM#1    {product, qty, ...}
PRODUCT#789         METADATA            {name, price, ...}
```

### Azure Database for PostgreSQL / Azure SQL

**Best for:** Relational data with complex queries

| Option | Use Case | Scaling |
|--------|----------|---------|
| PostgreSQL Flexible Server | Open-source relational | Burstable → General Purpose → Memory Optimized |
| Azure SQL Database (serverless) | Variable T-SQL workloads | Auto-pause, auto-scale vCores |
| Azure SQL Database (provisioned) | Predictable workloads | vCore-based |

```
Limits (PostgreSQL Flexible Server):
- Storage: up to 32 TB
- Read replicas: up to 5
- HA: zone-redundant with automatic failover

Pricing:
- Serverless (Azure SQL): per vCore-second
- Flexible Server: compute (vCore) + storage + backup
```

### Comparison: Cosmos DB vs Azure SQL

| Factor | Cosmos DB | Azure SQL |
|--------|-----------|-----------|
| Query flexibility | NoSQL / multi-model | Full T-SQL |
| Scaling | Instant, horizontal | vCore-based |
| Consistency | 5 tunable levels | ACID |
| Cost model | Per-RU | Per-vCore / DTU |
| Operational | Fully managed | Fully managed |

---

## Storage Services

### Blob Storage Access Tiers

| Tier | Access Pattern | Retrieval | Relative Cost |
|------|---------------|-----------|---------------|
| Hot | Frequent | Instant | Highest storage, lowest access |
| Cool (30+ days) | Infrequent | Instant | Lower storage, higher access |
| Cold (90+ days) | Rare | Instant | Lower still |
| Archive | Long-term archive | Hours (rehydrate) | Lowest storage |

### Lifecycle Policy Example

```json
{
  "rules": [
    {
      "name": "archive-old-data",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": { "blobTypes": ["blockBlob"] },
        "actions": {
          "baseBlob": {
            "tierToCool": { "daysAfterModificationGreaterThan": 30 },
            "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
            "delete": { "daysAfterModificationGreaterThan": 2555 }
          }
        }
      }
    }
  ]
}
```

### Disk and File Storage

| Service | Use Case | Access |
|---------|----------|--------|
| Managed Disks | VM block storage | Single VM |
| Azure Files | Shared file system (SMB/NFS) | Multiple clients |
| Azure NetApp Files | HPC / high throughput | High performance |
| Azure Files (Premium, SMB) | Windows apps / profiles | SMB protocol |

---

## Messaging and Events

### Decision Matrix

| Pattern | Service | Use Case |
|---------|---------|----------|
| Event routing | Event Grid | Microservices, reactive integration |
| Pub/sub | Service Bus Topics | Fan-out notifications |
| Queue | Service Bus Queues / Storage Queues | Decoupling, buffering |
| Streaming | Event Hubs | Real-time analytics |
| Message broker | Service Bus (AMQP) | Enterprise messaging, legacy migrations |

### Event Grid

**Best for:** Event-driven architectures, reactive integration

```json
{
  "topic": "orders-topic",
  "subjectBeginsWith": "orders/",
  "eventTypes": ["OrderCreated"],
  "advancedFilters": [
    { "operatorType": "NumberGreaterThanOrEquals", "key": "data.total", "value": 100 }
  ]
}
```

### Service Bus

**Best for:** Decoupling services, handling load spikes, ordered delivery

| Feature | Queue | Topic/Subscription |
|---------|-------|--------------------|
| Pattern | Point-to-point | Publish/subscribe |
| Ordering | Sessions (FIFO) | Sessions (FIFO) |
| Delivery | At least / exactly once (dedup) | Per-subscription |
| Dead-letter | Built-in | Built-in |

```python
from azure.servicebus import ServiceBusClient

def process_with_dlq(conn_str, queue_name):
    client = ServiceBusClient.from_connection_string(conn_str)
    with client.get_queue_receiver(queue_name, max_wait_time=20) as receiver:
        for msg in receiver:
            try:
                process(msg)
                receiver.complete_message(msg)
            except Exception:
                # After max delivery count, message auto-moves to the DLQ
                receiver.abandon_message(msg)
```

### Event Hubs

**Best for:** Real-time streaming data, analytics

| Capability | Use Case |
|------------|----------|
| Event Hubs | High-throughput ingestion / custom processing |
| Capture | Direct to Blob / ADLS |
| Stream Analytics | SQL on streams |
| Kafka endpoint | Kafka-compatible ingestion |

---

## API and Integration

### API Management (REST) vs API Management (GraphQL)

| Factor | REST API | GraphQL API |
|--------|----------|-------------|
| Protocol | REST, WebSocket | GraphQL |
| Real-time | WebSocket setup | Subscriptions over WebSocket |
| Caching | Response caching | Policy-based caching |
| Backend | Functions, HTTP, Azure services | Functions, HTTP resolvers |
| Pricing | Per-request / tier | Per-request / tier |

### API Management Configuration

```xml
<!-- Throttling and caching policy -->
<policies>
  <inbound>
    <rate-limit calls="1000" renewal-period="60" />
    <cache-lookup vary-by-developer="false" downstream-caching-type="public" />
  </inbound>
  <outbound>
    <cache-store duration="300" />
  </outbound>
</policies>
```

### Durable Functions / Logic Apps

**Best for:** Workflow orchestration, long-running processes

```json
{
  "startAt": "ProcessOrder",
  "states": {
    "ProcessOrder": { "type": "Activity", "resource": "processOrder", "next": "CheckInventory" },
    "CheckInventory": {
      "type": "Choice",
      "choices": [ { "variable": "$.inStock", "booleanEquals": true, "next": "ShipOrder" } ],
      "default": "BackOrder"
    },
    "ShipOrder": { "type": "Activity", "resource": "shipOrder", "end": true },
    "BackOrder": { "type": "Activity", "resource": "backOrder", "end": true }
  }
}
```

> Durable Functions is code-first orchestration (fan-out/fan-in, sagas). Logic Apps is a low-code connector-based alternative for integration workflows.

---

## Networking

### Virtual Network Components

| Component | Purpose |
|-----------|---------|
| Virtual Network (VNet) | Isolated network |
| Subnet | Network segment (public/private) |
| Public IP / Internet | Public internet access |
| NAT Gateway | Private subnet outbound |
| Private Endpoint | Private access to Azure PaaS services |
| VNet Peering | VNet interconnection |

### VNet Design Pattern

```
VNet: 10.0.0.0/16

App Gateway Subnet:
  10.0.0.0/24 - Application Gateway / WAF

Application Subnets (zones 1, 2, 3):
  10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24
  - Container Apps, Functions (VNet integration)

Data Subnets (zones 1, 2, 3):
  10.0.21.0/24, 10.0.22.0/24, 10.0.23.0/24
  - PostgreSQL, Azure Cache for Redis (private endpoints)
```

### Private Endpoints (secure PaaS access)

```bicep
resource keyVaultPe 'Microsoft.Network/privateEndpoints@2023-09-01' = {
  name: 'kv-pe'
  location: location
  properties: {
    subnet: { id: dataSubnet.id }
    privateLinkServiceConnections: [
      {
        name: 'kv-connection'
        properties: {
          privateLinkServiceId: keyVault.id
          groupIds: [ 'vault' ]
        }
      }
    ]
  }
}
```

---

## Security and Identity

### RBAC / Managed Identity Best Practices

```json
// Least privilege role assignment (concept) — prefer managed identity over secrets
{
  "roleDefinition": "Cosmos DB Built-in Data Contributor",
  "scope": "/subscriptions/<sub>/resourceGroups/app-rg/providers/Microsoft.DocumentDB/databaseAccounts/app-cosmos",
  "principalId": "<managed-identity-object-id>",
  "principalType": "ServicePrincipal"
}
```

Prefer **managed identities** (system- or user-assigned) over connection strings and keys; assign the narrowest built-in role at the smallest scope.

### Key Vault vs App Configuration

| Factor | Key Vault | App Configuration |
|--------|-----------|-------------------|
| Auto-rotation | Supported (with event-driven rotation) | N/A |
| Cross-resource | Via RBAC + private endpoint | Yes |
| Pricing | Per operation + per secret version | Per request / tier |
| Use case | Secrets, keys, certificates | Feature flags, non-secret config |

### Entra External ID Configuration (CIAM)

```jsonc
// User flow concept for a customer-facing app
{
  "userFlowType": "signUpOrSignIn",
  "identityProviders": ["EmailPassword", "Google", "Apple", "Facebook"],
  "mfa": { "state": "enabled", "methods": ["authenticatorApp", "sms"] },
  "passwordPolicy": {
    "minimumLength": 12,
    "requireLowercase": true,
    "requireUppercase": true,
    "requireNumbers": true,
    "requireSymbols": true
  },
  "accountRecovery": { "mechanisms": ["verifiedEmail"] }
}
```
