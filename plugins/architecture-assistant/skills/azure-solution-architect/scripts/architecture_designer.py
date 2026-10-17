"""
Azure architecture design and service recommendation module.
Generates architecture patterns based on application requirements.
"""

from typing import Dict, List, Any
from enum import Enum


class ApplicationType(Enum):
    """Types of applications supported."""
    WEB_APP = "web_application"
    MOBILE_BACKEND = "mobile_backend"
    DATA_PIPELINE = "data_pipeline"
    MICROSERVICES = "microservices"
    SAAS_PLATFORM = "saas_platform"
    IOT_PLATFORM = "iot_platform"


class ArchitectureDesigner:
    """Design Azure architectures based on requirements."""

    def __init__(self, requirements: Dict[str, Any]):
        """
        Initialize with application requirements.

        Args:
            requirements: Dictionary containing app type, traffic, budget, etc.
        """
        self.app_type = requirements.get('application_type', 'web_application')
        self.expected_users = requirements.get('expected_users', 1000)
        self.requests_per_second = requirements.get('requests_per_second', 10)
        self.budget_monthly = requirements.get('budget_monthly_usd', 500)
        self.team_size = requirements.get('team_size', 3)
        self.azure_experience = requirements.get('azure_experience', 'beginner')
        self.compliance_needs = requirements.get('compliance', [])
        self.data_size_gb = requirements.get('data_size_gb', 10)

    def recommend_architecture_pattern(self) -> Dict[str, Any]:
        """
        Recommend architecture pattern based on requirements.

        Returns:
            Dictionary with recommended pattern and services
        """
        if self.app_type in ['web_application', 'saas_platform']:
            if self.expected_users < 10000:
                return self._serverless_web_architecture()
            elif self.expected_users < 100000:
                return self._modern_three_tier_architecture()
            else:
                return self._multi_region_architecture()

        elif self.app_type == 'mobile_backend':
            return self._serverless_mobile_backend()

        elif self.app_type == 'data_pipeline':
            return self._event_driven_data_pipeline()

        elif self.app_type == 'microservices':
            return self._event_driven_microservices()

        elif self.app_type == 'iot_platform':
            return self._iot_architecture()

        else:
            return self._serverless_web_architecture()  # Default

    def _serverless_web_architecture(self) -> Dict[str, Any]:
        """Serverless web application pattern."""
        return {
            'pattern_name': 'Serverless Web Application',
            'description': 'Fully serverless architecture with zero server management',
            'use_case': 'SaaS platforms, low to medium traffic websites, MVPs',
            'services': {
                'frontend': {
                    'service': 'Blob Storage ($web) + Front Door',
                    'purpose': 'Static website hosting with global CDN',
                    'configuration': {
                        'storage_account': 'static website container ($web)',
                        'front_door': 'HTTPS with custom domain',
                        'caching': 'Cache-Control headers, edge caching'
                    }
                },
                'api': {
                    'service': 'API Management + Azure Functions',
                    'purpose': 'REST API backend with auto-scaling',
                    'configuration': {
                        'api_type': 'REST API',
                        'authorization': 'Entra External ID or subscription keys',
                        'throttling': f'{self.requests_per_second * 10} requests/second',
                        'functions_plan': 'Consumption (optimize based on testing)',
                        'functions_timeout': '30 seconds'
                    }
                },
                'database': {
                    'service': 'Cosmos DB',
                    'purpose': 'NoSQL database with serverless pricing',
                    'configuration': {
                        'capacity_mode': 'Serverless',
                        'backup': 'Continuous backup (point-in-time restore)',
                        'encryption': 'Encryption at rest (CMK optional)'
                    }
                },
                'authentication': {
                    'service': 'Entra External ID',
                    'purpose': 'Customer identity and access management (CIAM)',
                    'configuration': {
                        'user_flows': 'Email/password + social providers',
                        'mfa': 'Optional MFA with authenticator app or SMS',
                        'token_expiration': '1 hour access, 24h-90d refresh'
                    }
                },
                'cicd': {
                    'service': 'Azure DevOps or GitHub Actions',
                    'purpose': 'Automated deployment from Git',
                    'configuration': {
                        'source': 'GitHub or Azure Repos',
                        'build': 'Automatic on commit',
                        'environments': 'dev, staging, production'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': self._calculate_serverless_cost(),
                'breakdown': {
                    'Front Door': '10-30 USD',
                    'Azure Functions': '5-20 USD',
                    'API Management': '10-40 USD',
                    'Cosmos DB': '5-30 USD',
                    'Entra External ID': '0-10 USD (free MAU tier)',
                    'Blob Storage': '1-5 USD'
                }
            },
            'pros': [
                'No server management',
                'Auto-scaling built-in',
                'Pay only for what you use',
                'Fast to deploy and iterate',
                'High availability by default'
            ],
            'cons': [
                'Cold start latency (100-500ms)',
                'Vendor lock-in to Azure',
                'Debugging distributed systems complex',
                'Learning curve for serverless patterns'
            ],
            'scaling_characteristics': {
                'users_supported': '1k - 100k',
                'requests_per_second': '100 - 10,000',
                'scaling_method': 'Automatic (Functions consumption scale-out)'
            }
        }

    def _modern_three_tier_architecture(self) -> Dict[str, Any]:
        """Traditional three-tier with modern Azure services."""
        return {
            'pattern_name': 'Modern Three-Tier Application',
            'description': 'Classic architecture with containers and managed services',
            'use_case': 'Traditional web apps, e-commerce, content management',
            'services': {
                'load_balancer': {
                    'service': 'Application Gateway (with WAF)',
                    'purpose': 'Distribute traffic and protect with WAF',
                    'configuration': {
                        'scheme': 'internet-facing',
                        'target_type': 'Container Apps or VM Scale Sets',
                        'health_checks': '/health endpoint, 30s interval',
                        'ssl': 'Managed certificate for HTTPS'
                    }
                },
                'compute': {
                    'service': 'Container Apps or VM Scale Sets',
                    'purpose': 'Run containerized applications',
                    'configuration': {
                        'container_platform': 'Container Apps (serverless containers)',
                        'resources': '0.5 vCPU, 1 GiB (start small)',
                        'auto_scaling': f'2-{max(4, self.expected_users // 5000)} replicas',
                        'deployment': 'Revision-based, traffic splitting'
                    }
                },
                'database': {
                    'service': 'Azure Database for PostgreSQL Flexible Server',
                    'purpose': 'Managed relational database',
                    'configuration': {
                        'sku': 'GP_Standard_D2s_v3 or Burstable B-series',
                        'high_availability': 'Zone-redundant HA',
                        'read_replicas': '1-2 for read scaling',
                        'backup_retention': '7 days',
                        'encryption': 'Encryption at rest enabled'
                    }
                },
                'cache': {
                    'service': 'Azure Cache for Redis',
                    'purpose': 'Session storage, application caching',
                    'configuration': {
                        'tier': 'Basic/Standard C0-C1 (start small)',
                        'replication': 'Standard with replica for failover',
                        'eviction_policy': 'allkeys-lru'
                    }
                },
                'cdn': {
                    'service': 'Front Door',
                    'purpose': 'Cache static assets globally',
                    'configuration': {
                        'origins': 'Application Gateway (dynamic), Blob (static)',
                        'caching': 'Cache based on headers/cookies',
                        'compression': 'Compression enabled'
                    }
                },
                'storage': {
                    'service': 'Blob Storage',
                    'purpose': 'User uploads, backups, logs',
                    'configuration': {
                        'tier': 'Hot with lifecycle policies',
                        'versioning': 'Enabled for important containers',
                        'lifecycle': 'Transition to Cool after 30 days'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': self._calculate_three_tier_cost(),
                'breakdown': {
                    'Application Gateway': '20-30 USD',
                    'Container Apps': '50-200 USD',
                    'PostgreSQL Flexible Server': '100-300 USD',
                    'Azure Cache for Redis': '30-80 USD',
                    'Front Door': '10-50 USD',
                    'Blob Storage': '10-30 USD'
                }
            },
            'pros': [
                'Proven architecture pattern',
                'Easy to understand and debug',
                'Flexible scaling options',
                'Support for complex applications',
                'Managed services reduce operational burden'
            ],
            'cons': [
                'Higher baseline costs',
                'More complex than serverless',
                'Requires more operational knowledge',
                'Manual scaling configuration needed'
            ],
            'scaling_characteristics': {
                'users_supported': '10k - 500k',
                'requests_per_second': '1,000 - 50,000',
                'scaling_method': 'Auto-scale based on CPU/memory/requests (KEDA)'
            }
        }

    def _serverless_mobile_backend(self) -> Dict[str, Any]:
        """Serverless mobile backend with GraphQL."""
        return {
            'pattern_name': 'Serverless Mobile Backend',
            'description': 'Mobile-first backend with GraphQL and real-time features',
            'use_case': 'Mobile apps, single-page apps, offline-first applications',
            'services': {
                'api': {
                    'service': 'API Management (GraphQL) + Azure Functions',
                    'purpose': 'Flexible GraphQL API with real-time subscriptions',
                    'configuration': {
                        'api_type': 'GraphQL (synthetic or passthrough)',
                        'authorization': 'Entra External ID + subscription keys',
                        'resolvers': 'Azure Functions resolvers',
                        'subscriptions': 'WebSocket for real-time updates',
                        'caching': 'Policy-based caching (1 hour TTL)'
                    }
                },
                'database': {
                    'service': 'Cosmos DB',
                    'purpose': 'Fast NoSQL database with multi-region support',
                    'configuration': {
                        'capacity_mode': 'Serverless or autoscale',
                        'multi_region': 'Multi-region writes if needed',
                        'change_feed': 'Enabled for change data capture',
                        'ttl': 'Automatic expiration for temporary data'
                    }
                },
                'file_storage': {
                    'service': 'Blob Storage + Front Door',
                    'purpose': 'User uploads (images, videos, documents)',
                    'configuration': {
                        'access': 'SAS tokens or Entra credentials',
                        'lifecycle': 'Tiering for cost optimization',
                        'cdn': 'Front Door for fast global delivery'
                    }
                },
                'authentication': {
                    'service': 'Entra External ID',
                    'purpose': 'User management and federation',
                    'configuration': {
                        'identity_providers': 'Email, Google, Apple, Facebook',
                        'mfa': 'Authenticator app or SMS',
                        'groups': 'Admin, premium, free tiers',
                        'custom_attributes': 'User metadata storage'
                    }
                },
                'push_notifications': {
                    'service': 'Notification Hubs',
                    'purpose': 'Push notifications to mobile devices',
                    'configuration': {
                        'platforms': 'iOS (APNs), Android (FCM)',
                        'tags': 'Group notifications by tag',
                        'telemetry': 'Delivery telemetry for tracking'
                    }
                },
                'analytics': {
                    'service': 'Application Insights',
                    'purpose': 'User analytics and engagement',
                    'configuration': {
                        'events': 'Custom events tracking',
                        'funnels': 'User funnels and cohorts',
                        'segments': 'User segmentation'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': 50 + (self.expected_users * 0.005),
                'breakdown': {
                    'API Management': '5-40 USD',
                    'Cosmos DB': '10-50 USD',
                    'Entra External ID': '0-15 USD',
                    'Blob + Front Door': '10-40 USD',
                    'Notification Hubs': '1-10 USD',
                    'Application Insights': '10-30 USD'
                }
            },
            'pros': [
                'Single GraphQL endpoint',
                'Real-time subscriptions',
                'Offline-first capabilities',
                'Managed identity integration',
                'Flexible querying (no over/under fetching)'
            ],
            'cons': [
                'GraphQL learning curve',
                'Complex queries can be expensive',
                'Debugging subscriptions challenging',
                'Resolver orchestration complexity'
            ],
            'scaling_characteristics': {
                'users_supported': '1k - 1M',
                'requests_per_second': '100 - 100,000',
                'scaling_method': 'Automatic (API Management + Functions)'
            }
        }

    def _event_driven_microservices(self) -> Dict[str, Any]:
        """Event-driven microservices architecture."""
        return {
            'pattern_name': 'Event-Driven Microservices',
            'description': 'Loosely coupled services with event bus',
            'use_case': 'Complex business workflows, asynchronous processing',
            'services': {
                'event_bus': {
                    'service': 'Event Grid',
                    'purpose': 'Central event routing between services',
                    'configuration': {
                        'topic_type': 'Custom topic',
                        'subscriptions': 'Route events by type/subject',
                        'targets': 'Functions, Service Bus, Event Hubs',
                        'retry': 'Built-in retry with dead-lettering'
                    }
                },
                'compute': {
                    'service': 'Azure Functions + Container Apps (hybrid)',
                    'purpose': 'Service implementation',
                    'configuration': {
                        'functions': 'Lightweight services, event handlers',
                        'container_apps': 'Long-running services, heavy processing',
                        'auto_scaling': 'Functions (automatic), Container Apps (KEDA)'
                    }
                },
                'queues': {
                    'service': 'Service Bus',
                    'purpose': 'Decouple services, handle failures',
                    'configuration': {
                        'entity_type': 'Queue (point-to-point) or Topic (pub/sub)',
                        'dlq': 'Dead-letter after max delivery count',
                        'lock_duration': '30 seconds (adjust per service)',
                        'ttl': '4 days'
                    }
                },
                'orchestration': {
                    'service': 'Durable Functions',
                    'purpose': 'Complex workflows, saga patterns',
                    'configuration': {
                        'pattern': 'Fan-out/fan-in, chaining, saga',
                        'error_handling': 'Retry, compensation logic',
                        'timeouts': 'Per-activity timeouts',
                        'logging': 'Application Insights integration'
                    }
                },
                'database': {
                    'service': 'Cosmos DB (per service)',
                    'purpose': 'Each microservice owns its data',
                    'configuration': {
                        'pattern': 'Database per service',
                        'change_feed': 'Change feed for change events',
                        'backup': 'Continuous backup'
                    }
                },
                'api_gateway': {
                    'service': 'API Management',
                    'purpose': 'Unified API facade',
                    'configuration': {
                        'integration': 'Functions or HTTP backends',
                        'authentication': 'Entra ID or JWT validation policy',
                        'rate_limiting': 'Per-client throttling'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': 100 + (self.expected_users * 0.01),
                'breakdown': {
                    'Event Grid': '5-20 USD',
                    'Azure Functions': '20-100 USD',
                    'Service Bus': '1-10 USD',
                    'Durable Functions': '10-50 USD',
                    'Cosmos DB': '30-150 USD',
                    'API Management': '10-40 USD'
                }
            },
            'pros': [
                'Loose coupling between services',
                'Independent scaling and deployment',
                'Failure isolation',
                'Technology diversity possible',
                'Easy to test individual services'
            ],
            'cons': [
                'Operational complexity',
                'Distributed tracing required',
                'Eventual consistency challenges',
                'Network latency between services',
                'More moving parts to monitor'
            ],
            'scaling_characteristics': {
                'users_supported': '10k - 10M',
                'requests_per_second': '1,000 - 1,000,000',
                'scaling_method': 'Per-service auto-scaling'
            }
        }

    def _event_driven_data_pipeline(self) -> Dict[str, Any]:
        """Real-time data processing pipeline."""
        return {
            'pattern_name': 'Real-Time Data Pipeline',
            'description': 'Scalable data ingestion and processing',
            'use_case': 'Analytics, IoT data, log processing, ETL',
            'services': {
                'ingestion': {
                    'service': 'Event Hubs',
                    'purpose': 'Real-time data ingestion',
                    'configuration': {
                        'throughput_units': f'{max(1, self.data_size_gb // 10)} TU',
                        'retention': '1 day (extend to 7 days if needed)',
                        'encryption': 'Encryption at rest'
                    }
                },
                'processing': {
                    'service': 'Azure Functions or Stream Analytics',
                    'purpose': 'Transform and enrich data',
                    'configuration': {
                        'functions_scale': 'Match partition count',
                        'batch_size': '100-500 events per invocation',
                        'error_handling': 'Dead-letter for failed records'
                    }
                },
                'storage': {
                    'service': 'ADLS Gen2 (data lake)',
                    'purpose': 'Long-term storage and analytics',
                    'configuration': {
                        'format': 'Parquet (compressed, columnar)',
                        'partitioning': 'By date (year/month/day/hour)',
                        'lifecycle': 'Transition to Archive after 90 days',
                        'catalog': 'Purview / Unity-style catalog'
                    }
                },
                'analytics': {
                    'service': 'Synapse Serverless SQL',
                    'purpose': 'SQL queries on lake data',
                    'configuration': {
                        'query_results': 'Store in separate container',
                        'workspaces': 'Separate dev and prod',
                        'cost_controls': 'Query limits / budgets'
                    }
                },
                'visualization': {
                    'service': 'Power BI',
                    'purpose': 'Business intelligence dashboards',
                    'configuration': {
                        'source': 'Synapse or direct lake',
                        'refresh': 'Hourly or daily',
                        'sharing': 'Embedded dashboards or workspace access'
                    }
                },
                'alerting': {
                    'service': 'Azure Monitor + Action Groups',
                    'purpose': 'Monitor metrics and alerts',
                    'configuration': {
                        'metrics': 'Custom metrics from processing',
                        'alerts': 'Threshold-based alerts',
                        'notifications': 'Email, Teams, PagerDuty'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': self._calculate_data_pipeline_cost(),
                'breakdown': {
                    'Event Hubs': '15-100 USD (per TU)',
                    'Azure Functions': '10-50 USD',
                    'ADLS Gen2': '10-50 USD',
                    'Synapse Serverless SQL': '5-30 USD (per TB scanned)',
                    'Power BI': '10+ USD per user',
                    'Data Factory/Glue-equivalent': '5-20 USD'
                }
            },
            'pros': [
                'Real-time processing capability',
                'Scales to millions of events',
                'Cost-effective long-term storage',
                'SQL analytics on raw data',
                'Serverless architecture'
            ],
            'cons': [
                'Event Hubs throughput unit management',
                'Synapse costs based on data scanned',
                'Schema evolution complexity',
                'Cold data queries can be slow'
            ],
            'scaling_characteristics': {
                'events_per_second': '1,000 - 1,000,000',
                'data_volume': '1 GB - 1 PB per day',
                'scaling_method': 'Add Event Hubs TUs, partition the lake'
            }
        }

    def _iot_architecture(self) -> Dict[str, Any]:
        """IoT platform architecture."""
        return {
            'pattern_name': 'IoT Platform',
            'description': 'Scalable IoT device management and data processing',
            'use_case': 'Connected devices, sensors, smart devices',
            'services': {
                'device_management': {
                    'service': 'IoT Hub',
                    'purpose': 'Device connectivity and management',
                    'configuration': {
                        'protocol': 'MQTT/AMQP/HTTPS over TLS',
                        'device_registry': 'Device identity and metadata',
                        'device_twin': 'Desired and reported state',
                        'routing': 'Route messages to services'
                    }
                },
                'device_provisioning': {
                    'service': 'Device Provisioning Service (DPS)',
                    'purpose': 'Zero-touch fleet provisioning',
                    'configuration': {
                        'enrollment_groups': 'Group provisioning',
                        'attestation': 'TPM, X.509, symmetric key',
                        'allocation': 'Policy-based hub allocation'
                    }
                },
                'data_processing': {
                    'service': 'Stream Analytics',
                    'purpose': 'Process and analyze IoT data',
                    'configuration': {
                        'inputs': 'Ingest device telemetry',
                        'queries': 'Transform and enrich (SQL-like)',
                        'outputs': 'Lake, Cosmos DB, Power BI',
                        'windows': 'Tumbling/sliding window aggregates'
                    }
                },
                'time_series_db': {
                    'service': 'Azure Data Explorer',
                    'purpose': 'Store time-series metrics',
                    'configuration': {
                        'hot_cache': 'Recent data (fast queries)',
                        'cold_storage': 'Historical data (years)',
                        'retention': 'Policy-based tiering'
                    }
                },
                'real_time_alerts': {
                    'service': 'Azure Functions + Event Grid',
                    'purpose': 'Detect and respond to events',
                    'configuration': {
                        'rules': 'Define alert conditions',
                        'actions': 'Service Bus, Functions, webhooks',
                        'state_tracking': 'Per-device state in Cosmos DB'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': 50 + (self.expected_users * 0.1),  # expected_users = device count
                'breakdown': {
                    'IoT Hub': '10-100 USD (per tier/messages)',
                    'Stream Analytics': '5-50 USD',
                    'Azure Data Explorer': '10-80 USD',
                    'Event Grid': '1-20 USD',
                    'Data transfer': '10-50 USD'
                }
            },
            'pros': [
                'Built for IoT scale',
                'Secure device connectivity',
                'Managed device lifecycle',
                'Time-series optimized',
                'Real-time event detection'
            ],
            'cons': [
                'IoT-specific pricing model',
                'Protocol/SDK requirements',
                'Regional limitations',
                'Complexity for simple use cases'
            ],
            'scaling_characteristics': {
                'devices_supported': '100 - 10,000,000',
                'messages_per_second': '1,000 - 100,000',
                'scaling_method': 'Automatic (managed service, hub units)'
            }
        }

    def _multi_region_architecture(self) -> Dict[str, Any]:
        """Multi-region high availability architecture."""
        return {
            'pattern_name': 'Multi-Region High Availability',
            'description': 'Global deployment with disaster recovery',
            'use_case': 'Global applications, 99.99% uptime, compliance',
            'services': {
                'dns': {
                    'service': 'Azure Front Door / Traffic Manager',
                    'purpose': 'Global traffic routing',
                    'configuration': {
                        'routing_policy': 'Geolocation or latency-based',
                        'health_checks': 'Active health probes with failover',
                        'failover': 'Automatic to secondary region'
                    }
                },
                'cdn': {
                    'service': 'Front Door',
                    'purpose': 'Edge caching and acceleration',
                    'configuration': {
                        'origins': 'Multiple regions (primary + secondary)',
                        'origin_failover': 'Automatic failover',
                        'edge_locations': 'Global points of presence'
                    }
                },
                'compute': {
                    'service': 'Multi-region Functions or Container Apps',
                    'purpose': 'Active-active deployment',
                    'configuration': {
                        'regions': 'eastus (primary), westeurope (secondary)',
                        'deployment': 'Blue/Green in each region',
                        'traffic_split': '70/30 or 50/50'
                    }
                },
                'database': {
                    'service': 'Cosmos DB multi-region or Azure SQL geo-replication',
                    'purpose': 'Multi-region replication',
                    'configuration': {
                        'replication': 'Sub-second replication lag (Cosmos DB)',
                        'read_locality': 'Read from nearest region',
                        'write_mode': 'Multi-region writes (Cosmos DB)',
                        'conflict_resolution': 'Last writer wins / custom'
                    }
                },
                'storage': {
                    'service': 'Blob Storage (RA-GRS)',
                    'purpose': 'Replicate data across regions',
                    'configuration': {
                        'replication': 'Geo-redundant (async to secondary)',
                        'read_access': 'Read-access geo-redundant',
                        'rpo': 'Minutes (async replication)'
                    }
                }
            },
            'estimated_cost': {
                'monthly_usd': self._calculate_three_tier_cost() * 1.8,
                'breakdown': {
                    'Front Door / Traffic Manager': '10-30 USD',
                    'Front Door (CDN)': '20-100 USD',
                    'Compute (2 regions)': '100-500 USD',
                    'Database (multi-region)': '200-800 USD',
                    'Data transfer (cross-region)': '50-200 USD'
                }
            },
            'pros': [
                'Global low latency',
                'High availability (99.99%+)',
                'Disaster recovery built-in',
                'Data sovereignty compliance',
                'Automatic failover'
            ],
            'cons': [
                '1.5-2x costs vs single region',
                'Complex deployment pipeline',
                'Data consistency challenges',
                'More operational overhead',
                'Cross-region data transfer costs'
            ],
            'scaling_characteristics': {
                'users_supported': '100k - 100M',
                'requests_per_second': '10,000 - 10,000,000',
                'scaling_method': 'Per-region auto-scaling + global routing'
            }
        }

    def _calculate_serverless_cost(self) -> float:
        """Estimate serverless architecture cost."""
        requests_per_month = self.requests_per_second * 2_592_000  # 30 days
        functions_cost = (requests_per_month / 1_000_000) * 0.20  # ~$0.20 per 1M executions
        apim_cost = (requests_per_month / 1_000_000) * 3.50  # ~$3.50 per 1M calls (consumption)
        cosmos_cost = max(5, self.data_size_gb * 0.25)  # ~$0.25 per GB/month
        front_door_cost = max(10, self.expected_users * 0.01)

        total = functions_cost + apim_cost + cosmos_cost + front_door_cost
        return min(total, self.budget_monthly)  # Cap at budget

    def _calculate_three_tier_cost(self) -> float:
        """Estimate three-tier architecture cost."""
        replicas = max(2, self.expected_users // 5000)
        container_apps_cost = replicas * 30  # ~$30 per replica/month
        postgres_cost = 150  # GP_D2s_v3 baseline
        redis_cost = 40  # Standard C0/C1
        app_gateway_cost = 25

        total = container_apps_cost + postgres_cost + redis_cost + app_gateway_cost
        return min(total, self.budget_monthly)

    def _calculate_data_pipeline_cost(self) -> float:
        """Estimate data pipeline cost."""
        throughput_units = max(1, self.data_size_gb // 10)
        event_hubs_cost = throughput_units * 15  # ~$15 per TU/month
        lake_cost = self.data_size_gb * 0.023  # ~$0.023 per GB/month
        functions_cost = 20  # Processing
        synapse_cost = 15  # Serverless queries

        total = event_hubs_cost + lake_cost + functions_cost + synapse_cost
        return min(total, self.budget_monthly)

    def generate_service_checklist(self) -> List[Dict[str, Any]]:
        """Generate implementation checklist for recommended architecture."""
        architecture = self.recommend_architecture_pattern()

        checklist = [
            {
                'phase': 'Planning',
                'tasks': [
                    'Review architecture pattern and services',
                    'Estimate costs using the Azure Pricing Calculator',
                    'Define environment strategy (dev, staging, prod)',
                    'Set up management groups and subscriptions',
                    'Define tagging strategy for resources'
                ]
            },
            {
                'phase': 'Foundation',
                'tasks': [
                    'Create VNet with public/private subnets',
                    'Configure NAT Gateway or private endpoints',
                    'Set up managed identities and RBAC role assignments',
                    'Route Activity Log and diagnostics to Log Analytics',
                    'Configure Azure Policy for compliance'
                ]
            },
            {
                'phase': 'Core Services',
                'tasks': [
                    f"Deploy {service['service']}"
                    for service in architecture['services'].values()
                ]
            },
            {
                'phase': 'Security',
                'tasks': [
                    'Configure network security groups and private endpoints',
                    'Enable encryption (CMK) where required',
                    'Set up Azure WAF rules',
                    'Configure Key Vault for secrets',
                    'Enable Microsoft Defender for Cloud'
                ]
            },
            {
                'phase': 'Monitoring',
                'tasks': [
                    'Create Azure Monitor dashboards',
                    'Set up alerts for critical metrics',
                    'Configure Action Groups for notifications',
                    'Enable Application Insights for distributed tracing',
                    'Set up log aggregation and retention'
                ]
            },
            {
                'phase': 'CI/CD',
                'tasks': [
                    'Set up Azure DevOps or GitHub Actions',
                    'Configure automated testing',
                    'Implement blue/green deployment',
                    'Set up rollback procedures',
                    'Document deployment process'
                ]
            }
        ]

        return checklist
