# Azure Architecture Patterns for Startups

Reference guide for selecting the right Azure architecture pattern based on application requirements.

---

## Table of Contents

- [Pattern Selection Matrix](#pattern-selection-matrix)
- [Pattern 1: Serverless Web Application](#pattern-1-serverless-web-application)
- [Pattern 2: Event-Driven Microservices](#pattern-2-event-driven-microservices)
- [Pattern 3: Modern Three-Tier Application](#pattern-3-modern-three-tier-application)
- [Pattern 4: Real-Time Data Processing](#pattern-4-real-time-data-processing)
- [Pattern 5: GraphQL API Backend](#pattern-5-graphql-api-backend)
- [Pattern 6: Multi-Region High Availability](#pattern-6-multi-region-high-availability)

---

## Pattern Selection Matrix

| Pattern | Best For | Users | Monthly Cost | Complexity |
|---------|----------|-------|--------------|------------|
| Serverless Web | MVP, SaaS, mobile backend | <50K | $50-500 | Low |
| Event-Driven Microservices | Complex workflows, async processing | Any | $100-1000 | Medium |
| Three-Tier | Traditional web, e-commerce | 10K-500K | $300-2000 | Medium |
| Real-Time Data | Analytics, IoT, streaming | Any | $200-1500 | High |
| GraphQL Backend | Mobile apps, SPAs | <100K | $50-400 | Medium |
| Multi-Region HA | Global apps, DR requirements | >100K | 1.5-2x single | High |

---

## Pattern 1: Serverless Web Application

### Use Case
SaaS platforms, mobile backends, low-traffic websites, MVPs

### Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  Front Door │────▶│Blob Storage │     │ Entra External ID│
│    (CDN)    │     │  (Static)   │     │     (Auth)       │
└─────────────┘     └─────────────┘     └────────┬─────────┘
                                                 │
┌─────────────┐     ┌─────────────┐     ┌────────▼─────────┐
│  Azure DNS  │────▶│API Management│───▶│  Azure Functions │
│    (DNS)    │     │   (REST)     │    │   (Functions)    │
└─────────────┘     └─────────────┘     └────────┬─────────┘
                                                 │
                                          ┌──────▼──────┐
                                          │  Cosmos DB  │
                                          │ (Database)  │
                                          └─────────────┘
```

### Service Stack

| Layer | Service | Configuration |
|-------|---------|---------------|
| Frontend | Blob Storage ($web) + Front Door | Static hosting with HTTPS |
| API | API Management + Azure Functions | REST endpoints with throttling |
| Database | Cosmos DB | Serverless (consumption) billing |
| Auth | Entra External ID (CIAM) | User flows with MFA support |
| CI/CD | Azure DevOps or GitHub Actions | Automated deployments |

### Bicep Template

```bicep
param location string = resourceGroup().location
param appName string = 'my-app'

resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: '${appName}-fn'
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      functionAppScaleLimit: 200
      minimumElasticInstanceCount: 0
    }
  }
}

resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${appName}-plan'
  location: location
  sku: { name: 'Y1', tier: 'Dynamic' }
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: '${appName}-cosmos'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: [ { name: 'EnableServerless' } ]
    locations: [ { locationName: location, failoverPriority: 0 } ]
  }
}
```

### Cost Breakdown (10K users)

| Service | Monthly Cost |
|---------|-------------|
| Azure Functions | $5-20 |
| API Management (Consumption) | $10-30 |
| Cosmos DB (serverless) | $10-50 |
| Front Door | $5-15 |
| Blob Storage | $1-5 |
| Entra External ID | $0-50 |
| **Total** | **$31-170** |

### Pros and Cons

**Pros:**
- Zero server management
- Pay only for what you use
- Auto-scaling built-in
- Low operational overhead

**Cons:**
- Cold start latency (100-500ms)
- Consumption plan execution limits
- Vendor lock-in

---

## Pattern 2: Event-Driven Microservices

### Use Case
Complex business workflows, asynchronous processing, decoupled systems

### Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Service   │────▶│ Event Grid  │────▶│   Service   │
│      A      │     │ (Event Bus) │     │      B      │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │ Service Bus │
                    │   (Queue)   │
                    └──────┬──────┘
                           │
┌─────────────┐     ┌──────▼──────┐     ┌─────────────┐
│  Durable    │◀────│   Azure     │────▶│  Cosmos DB  │
│  Functions  │     │  Functions  │     │  (Storage)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Service Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| Events | Event Grid | Central event routing |
| Processing | Azure Functions or Container Apps | Event handlers |
| Queue | Service Bus | Dead letter queue for failures |
| Orchestration | Durable Functions | Complex workflow state |
| Storage | Cosmos DB, Blob Storage | Persistent data |

### Event Schema Example

```json
{
  "topic": "orders-topic",
  "eventType": "OrderCreated",
  "subject": "orders/ord-12345",
  "data": {
    "orderId": "ord-12345",
    "customerId": "cust-67890",
    "items": [],
    "total": 99.99
  },
  "eventTime": "2024-01-15T10:30:00Z"
}
```

### Cost Breakdown

| Service | Monthly Cost |
|---------|-------------|
| Event Grid | $1-10 |
| Azure Functions | $20-100 |
| Service Bus | $5-20 |
| Durable Functions | $25-100 |
| Cosmos DB | $20-100 |
| **Total** | **$71-330** |

### Pros and Cons

**Pros:**
- Loose coupling between services
- Independent scaling per service
- Failure isolation
- Easy to test individually

**Cons:**
- Distributed system complexity
- Eventual consistency
- Harder to debug

---

## Pattern 3: Modern Three-Tier Application

### Use Case
Traditional web apps, e-commerce, CMS, applications with complex queries

### Architecture Diagram

```
┌─────────────┐     ┌──────────────────┐
│  Front Door │────▶│ Application      │
│    (CDN)    │     │ Gateway (LB/WAF) │
└─────────────┘     └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Container Apps  │
                    │  (Auto-scale)    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
 ┌──────▼──────┐    ┌────────▼────────┐    ┌──────▼──────┐
 │ PostgreSQL  │    │ Azure Cache for │    │Blob Storage │
 │ Flexible Srv│    │     Redis       │    │ (Storage)   │
 └─────────────┘    └─────────────────┘    └─────────────┘
```

### Service Stack

| Layer | Service | Configuration |
|-------|---------|---------------|
| CDN | Front Door | Edge caching, HTTPS |
| Load Balancer / WAF | Application Gateway | Path-based routing, health checks |
| Compute | Container Apps | Container auto-scaling (KEDA) |
| Database | Azure Database for PostgreSQL Flexible Server | Zone-redundant HA, auto-scaling storage |
| Cache | Azure Cache for Redis | Session, query caching |
| Storage | Blob Storage | Static assets, uploads |

### Terraform Example

```hcl
resource "azurerm_container_app" "app" {
  name                         = "app"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    min_replicas = 2
    max_replicas = 10

    container {
      name   = "app"
      image  = "myregistry.azurecr.io/app:latest"
      cpu    = 0.5
      memory = "1Gi"
    }

    http_scale_rule {
      name                = "http-scaler"
      concurrent_requests = 50
    }
  }
}
```

### Cost Breakdown (50K users)

| Service | Monthly Cost |
|---------|-------------|
| Container Apps (2 replicas) | $100-200 |
| Application Gateway | $25-50 |
| PostgreSQL Flexible Server | $100-300 |
| Azure Cache for Redis | $50-100 |
| Front Door | $20-50 |
| **Total** | **$295-700** |

---

## Pattern 4: Real-Time Data Processing

### Use Case
Analytics, IoT data ingestion, log processing, streaming data

### Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  IoT Hub    │────▶│ Event Hubs  │────▶│   Azure     │
│  (Devices)  │     │  (Stream)   │     │  Functions  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────▼──────┐
│  Power BI   │◀────│   Synapse   │◀────│ ADLS Gen2   │
│   (Viz)     │     │Serverless SQL│     │ (Data Lake) │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                        ┌──────▼──────┐
                                        │Azure Monitor│
                                        │  (Alerts)   │
                                        └─────────────┘
```

### Service Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| Ingestion | Event Hubs | Real-time data capture |
| Processing | Azure Functions or Stream Analytics | Transform and analyze |
| Storage | ADLS Gen2 (data lake) | Long-term storage |
| Query | Synapse Serverless SQL | SQL queries on the lake |
| Visualization | Power BI | Dashboards and reports |
| Alerting | Azure Monitor + Action Groups | Threshold-based alerts |

### Event Hubs Producer Example

```python
from azure.eventhub import EventHubProducerClient, EventData
import json

producer = EventHubProducerClient.from_connection_string(
    conn_str="<connection-string>", eventhub_name="sensor-stream"
)

def send_event(data):
    batch = producer.create_batch()
    batch.add(EventData(json.dumps(data)))
    producer.send_batch(batch)

send_event({'sensor_id': 'temp-01', 'value': 23.5, 'unit': 'celsius'})
```

### Cost Breakdown

| Service | Monthly Cost |
|---------|-------------|
| Event Hubs (1 throughput unit) | $15-30 |
| Azure Functions | $10-50 |
| ADLS Gen2 | $5-50 |
| Synapse Serverless SQL | $5-25 |
| Power BI | $10+ per user |
| **Total** | **$45-175** |

---

## Pattern 5: GraphQL API Backend

### Use Case
Mobile apps, single-page applications, flexible data queries

### Architecture Diagram

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Mobile App │────▶│  API Management  │────▶│   Azure     │
│   or SPA    │     │    (GraphQL)     │     │  Functions  │
└─────────────┘     └────────┬─────────┘     └─────────────┘
                             │
                    ┌────────▼─────────┐
                    │    Cosmos DB     │
                    │    (Direct)      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │Entra External ID │
                    │     (Auth)       │
                    └──────────────────┘
```

### GraphQL Schema Example

```graphql
type Query {
  getUser(id: ID!): User
  listPosts(limit: Int, nextToken: String): PostConnection
}

type Mutation {
  createPost(input: CreatePostInput!): Post
  updatePost(input: UpdatePostInput!): Post
}

type User {
  id: ID!
  email: String!
  posts: [Post]
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: String!
}
```

> Azure exposes GraphQL through **API Management** (synthetic or passthrough GraphQL APIs) backed by **Azure Functions** resolvers, or through **Microsoft Fabric / Data API builder** for data-centric GraphQL. Real-time updates use GraphQL subscriptions over WebSocket on API Management or Azure Web PubSub.

### Cost Breakdown

| Service | Monthly Cost |
|---------|-------------|
| API Management | $4-50 |
| Azure Functions | $5-30 |
| Cosmos DB | $10-50 |
| Entra External ID | $0-50 |
| **Total** | **$19-180** |

---

## Pattern 6: Multi-Region High Availability

### Use Case
Global applications, disaster recovery, data sovereignty compliance

### Architecture Diagram

```
                    ┌─────────────┐
                    │Traffic Mgr /│
                    │ Front Door  │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                                 │
   ┌──────▼──────┐                   ┌──────▼──────┐
   │  eastus     │                   │ westeurope  │
   │ Front Door  │                   │ Front Door  │
   └──────┬──────┘                   └──────┬──────┘
          │                                 │
   ┌──────▼──────┐                   ┌──────▼──────┐
   │Functions/   │                   │Functions/   │
   │Container Apps│                  │Container Apps│
   └──────┬──────┘                   └──────┬──────┘
          │                                 │
   ┌──────▼──────┐◀── Replication ──▶┌──────▼──────┐
   │  Cosmos DB  │                   │  Cosmos DB  │
   │Multi-region │                   │Multi-region │
   └─────────────┘                   └─────────────┘
```

### Service Stack

| Component | Service | Configuration |
|-----------|---------|---------------|
| Global routing | Azure Front Door / Traffic Manager | Geolocation or latency routing |
| CDN | Front Door | Multiple origins per region |
| Compute | Azure Functions or Container Apps | Deployed in each region |
| Database | Cosmos DB multi-region writes | Automatic replication |
| Storage | Blob Storage (GRS/RA-GRS) | Geo-redundant replication |

### Front Door Failover (Bicep excerpt)

```bicep
resource afdOrigin 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  name: 'primary-origin'
  properties: {
    hostName: 'api-eastus.example.com'
    priority: 1
    weight: 1000
    enabledState: 'Enabled'
  }
}
```

### Cost Considerations

| Factor | Impact |
|--------|--------|
| Compute | 2x (each region) |
| Database | Premium for multi-region writes |
| Data Transfer | Cross-region replication costs |
| Front Door | Routing rules + health probes |
| **Total** | **1.5-2x single region** |

---

## Pattern Comparison Summary

### Latency

| Pattern | Typical Latency |
|---------|-----------------|
| Serverless | 50-200ms (cold: 500ms+) |
| Three-Tier | 20-100ms |
| GraphQL | 30-150ms |
| Multi-Region | <50ms (regional) |

### Scaling Characteristics

| Pattern | Scale Limit | Scale Speed |
|---------|-------------|-------------|
| Serverless | Consumption scale-out limits | Instant |
| Three-Tier | Replica / SKU limits | Minutes |
| Event-Driven | Virtually unlimited | Instant |
| Multi-Region | Regional limits | Instant |

### Operational Complexity

| Pattern | Setup | Maintenance | Debugging |
|---------|-------|-------------|-----------|
| Serverless | Low | Low | Medium |
| Three-Tier | Medium | Medium | Low |
| Event-Driven | High | Medium | High |
| Multi-Region | High | High | High |
