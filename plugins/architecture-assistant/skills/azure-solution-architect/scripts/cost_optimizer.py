"""
Azure cost optimization analyzer.
Provides cost-saving recommendations for startup budgets.
"""

from typing import Dict, List, Any


class CostOptimizer:
    """Analyze Azure costs and provide optimization recommendations."""

    def __init__(self, current_resources: Dict[str, Any], monthly_spend: float):
        """
        Initialize with current Azure resources and spending.

        Args:
            current_resources: Dictionary of current Azure resources
            monthly_spend: Current monthly Azure spend in USD
        """
        self.resources = current_resources
        self.monthly_spend = monthly_spend
        self.recommendations = []

    def analyze_and_optimize(self) -> Dict[str, Any]:
        """
        Analyze current setup and generate cost optimization recommendations.

        Returns:
            Dictionary with recommendations and potential savings
        """
        self.recommendations = []
        potential_savings = 0.0

        potential_savings += self._analyze_compute()
        potential_savings += self._analyze_storage()
        potential_savings += self._analyze_database()
        potential_savings += self._analyze_networking()
        potential_savings += self._analyze_general_optimizations()

        return {
            'current_monthly_spend': self.monthly_spend,
            'potential_monthly_savings': round(potential_savings, 2),
            'optimized_monthly_spend': round(self.monthly_spend - potential_savings, 2),
            'savings_percentage': round((potential_savings / self.monthly_spend) * 100, 2) if self.monthly_spend > 0 else 0,
            'recommendations': self.recommendations,
            'priority_actions': self._prioritize_recommendations()
        }

    def _analyze_compute(self) -> float:
        """Analyze compute resources (VMs, Functions, Container Apps)."""
        savings = 0.0

        vms = self.resources.get('virtual_machines', [])
        if vms:
            # Check for idle VMs
            idle_count = sum(1 for vm in vms if vm.get('cpu_utilization', 100) < 10)
            if idle_count > 0:
                idle_cost = idle_count * 50  # Assume $50/month per idle VM
                savings += idle_cost
                self.recommendations.append({
                    'service': 'Virtual Machines',
                    'type': 'Idle Resources',
                    'issue': f'{idle_count} VMs with <10% CPU utilization',
                    'recommendation': 'Deallocate or delete idle VMs, or resize to a smaller SKU / Burstable (B-series)',
                    'potential_savings': idle_cost,
                    'priority': 'high'
                })

            # Check for Reservations / Savings Plans
            payg_count = sum(1 for vm in vms if vm.get('pricing', 'payg') == 'payg')
            if payg_count >= 2:
                reservation_savings = payg_count * 50 * 0.30  # ~30% savings with reservations
                savings += reservation_savings
                self.recommendations.append({
                    'service': 'Virtual Machines',
                    'type': 'Pricing Optimization',
                    'issue': f'{payg_count} VMs on pay-as-you-go pricing',
                    'recommendation': 'Purchase an Azure Savings Plan for compute or Reserved VM Instances for predictable workloads (1-year commitment)',
                    'potential_savings': reservation_savings,
                    'priority': 'medium'
                })

        # Functions optimization
        function_apps = self.resources.get('function_apps', [])
        if function_apps:
            overprovisioned = sum(
                1 for fn in function_apps
                if fn.get('plan', 'consumption') != 'consumption' and fn.get('avg_utilization', 0) < 20
            )
            if overprovisioned > 0:
                functions_savings = overprovisioned * 50  # Premium/Dedicated baseline savings
                savings += functions_savings
                self.recommendations.append({
                    'service': 'Azure Functions',
                    'type': 'Plan Right-sizing',
                    'issue': f'{overprovisioned} Function Apps on Premium/Dedicated with low utilization',
                    'recommendation': 'Move low-traffic Function Apps to the Consumption plan (scale to zero)',
                    'potential_savings': functions_savings,
                    'priority': 'low'
                })

        return savings

    def _analyze_storage(self) -> float:
        """Analyze Blob Storage and other storage resources."""
        savings = 0.0

        storage_accounts = self.resources.get('storage_accounts', [])
        for account in storage_accounts:
            size_gb = account.get('size_gb', 0)
            access_tier = account.get('access_tier', 'Hot')

            # Check for lifecycle policies
            if not account.get('has_lifecycle_policy', False) and size_gb > 100:
                lifecycle_savings = size_gb * 0.015  # savings from Cool/Archive transition
                savings += lifecycle_savings
                self.recommendations.append({
                    'service': 'Blob Storage',
                    'type': 'Lifecycle Policy',
                    'issue': f'Account {account.get("name", "unknown")} ({size_gb} GB) has no lifecycle policy',
                    'recommendation': 'Add a lifecycle rule: tier to Cool after 30 days, Archive after 90 days',
                    'potential_savings': lifecycle_savings,
                    'priority': 'medium'
                })

            # Check for over-provisioned Hot tier
            if access_tier == 'Hot' and size_gb > 500 and account.get('access_frequency', 'high') == 'low':
                tier_savings = size_gb * 0.005
                savings += tier_savings
                self.recommendations.append({
                    'service': 'Blob Storage',
                    'type': 'Access Tier',
                    'issue': f'Large account ({size_gb} GB) on Hot tier with low access frequency',
                    'recommendation': 'Move infrequently accessed data to the Cool or Cold access tier',
                    'potential_savings': tier_savings,
                    'priority': 'high'
                })

        return savings

    def _analyze_database(self) -> float:
        """Analyze PostgreSQL/SQL, Cosmos DB, and other database costs."""
        savings = 0.0

        sql_servers = self.resources.get('sql_databases', [])
        for db in sql_servers:
            # Check for idle databases
            if db.get('connections_per_day', 1000) < 10:
                db_cost = db.get('monthly_cost', 100)
                savings += db_cost * 0.8  # Can save ~80% by pausing/removing
                self.recommendations.append({
                    'service': 'Azure SQL / PostgreSQL',
                    'type': 'Idle Resource',
                    'issue': f'Database {db.get("name", "unknown")} has <10 connections/day',
                    'recommendation': 'Stop the server if not needed, or export and delete after a final backup',
                    'potential_savings': db_cost * 0.8,
                    'priority': 'high'
                })

            # Check for serverless opportunity (Azure SQL)
            if db.get('engine', '') == 'azure-sql' and db.get('utilization', 100) < 30:
                serverless_savings = db.get('monthly_cost', 200) * 0.40
                savings += serverless_savings
                self.recommendations.append({
                    'service': 'Azure SQL',
                    'type': 'Serverless Migration',
                    'issue': f'SQL database {db.get("name", "unknown")} has low utilization (<30%)',
                    'recommendation': 'Switch to the Azure SQL serverless compute tier (auto-pause, per-second billing)',
                    'potential_savings': serverless_savings,
                    'priority': 'medium'
                })

        # Cosmos DB optimization
        cosmos_accounts = self.resources.get('cosmos_accounts', [])
        for account in cosmos_accounts:
            if account.get('capacity_mode', 'provisioned') == 'provisioned':
                provisioned_rus = account.get('provisioned_rus', 0)
                utilization = account.get('utilization_percentage', 100)

                if utilization < 20:
                    # Switching variable workloads to serverless / autoscale saves on idle RU/s
                    serverless_savings = provisioned_rus * 0.00008 * 730 * 0.3
                    savings += serverless_savings
                    self.recommendations.append({
                        'service': 'Cosmos DB',
                        'type': 'Capacity Mode',
                        'issue': f'Account {account.get("name", "unknown")} has low utilization with provisioned throughput',
                        'recommendation': 'Switch to serverless or autoscale throughput for variable workloads',
                        'potential_savings': serverless_savings,
                        'priority': 'medium'
                    })

        return savings

    def _analyze_networking(self) -> float:
        """Analyze networking costs (data transfer, NAT Gateway, etc.)."""
        savings = 0.0

        nat_gateways = self.resources.get('nat_gateways', [])
        if len(nat_gateways) > 1:
            multi_zone = self.resources.get('multi_zone_required', False)
            if not multi_zone:
                nat_savings = (len(nat_gateways) - 1) * 45  # ~$45/month per NAT Gateway
                savings += nat_savings
                self.recommendations.append({
                    'service': 'NAT Gateway',
                    'type': 'Resource Consolidation',
                    'issue': f'{len(nat_gateways)} NAT Gateways deployed (multi-zone not required)',
                    'recommendation': 'Use a single NAT Gateway in dev/staging, or use private/service endpoints for Azure PaaS',
                    'potential_savings': nat_savings,
                    'priority': 'high'
                })

        # Check for private/service endpoint opportunity
        if not self.resources.get('private_endpoints', []):
            paas_data_transfer = self.resources.get('paas_data_transfer_gb', 0)
            if paas_data_transfer > 100:
                endpoint_savings = paas_data_transfer * 0.09 * 0.5  # avoid NAT egress on PaaS traffic
                savings += endpoint_savings
                self.recommendations.append({
                    'service': 'Virtual Network',
                    'type': 'Private / Service Endpoints',
                    'issue': 'High PaaS data transfer without private/service endpoints',
                    'recommendation': 'Create private or service endpoints for Blob Storage and Cosmos DB to avoid NAT egress costs',
                    'potential_savings': endpoint_savings,
                    'priority': 'medium'
                })

        return savings

    def _analyze_general_optimizations(self) -> float:
        """General Azure cost optimizations."""
        savings = 0.0

        # Log Analytics retention
        workspaces = self.resources.get('log_analytics_workspaces', [])
        for ws in workspaces:
            if ws.get('retention_days', 30) > 90:
                ws_size_gb = ws.get('size_gb', 1)
                retention_savings = ws_size_gb * 0.50 * 0.7  # trim excessive retention
                savings += retention_savings
                self.recommendations.append({
                    'service': 'Log Analytics',
                    'type': 'Retention Policy',
                    'issue': f'Workspace {ws.get("name", "unknown")} retains logs longer than needed',
                    'recommendation': 'Set retention to 30 days for non-compliance logs; archive to cheaper storage if longer retention is required',
                    'potential_savings': retention_savings,
                    'priority': 'low'
                })

        # Unattached public IPs
        public_ips = self.resources.get('public_ips', [])
        unattached = sum(1 for ip in public_ips if not ip.get('attached', True))
        if unattached > 0:
            ip_savings = unattached * 3.65  # ~$0.005/hour = ~$3.65/month (Standard SKU)
            savings += ip_savings
            self.recommendations.append({
                'service': 'Public IP',
                'type': 'Unused Resources',
                'issue': f'{unattached} unattached public IP addresses',
                'recommendation': 'Delete unused public IPs to avoid hourly charges',
                'potential_savings': ip_savings,
                'priority': 'high'
            })

        # Unattached managed disks
        disks = self.resources.get('managed_disks', [])
        orphaned = sum(1 for d in disks if not d.get('attached', True))
        if orphaned > 0:
            disk_savings = orphaned * 5  # rough per-disk monthly estimate
            savings += disk_savings
            self.recommendations.append({
                'service': 'Managed Disks',
                'type': 'Unused Resources',
                'issue': f'{orphaned} unattached managed disks',
                'recommendation': 'Snapshot if needed, then delete orphaned disks',
                'potential_savings': disk_savings,
                'priority': 'high'
            })

        # Budgets
        if not self.resources.get('has_budget_alerts', False):
            self.recommendations.append({
                'service': 'Cost Management (Budgets)',
                'type': 'Cost Monitoring',
                'issue': 'No budget alerts configured',
                'recommendation': 'Create a Cost Management budget with alerts at 50%, 80%, 100% of the monthly budget',
                'potential_savings': 0,
                'priority': 'high'
            })

        # Azure Advisor
        if not self.resources.get('reviews_advisor', False):
            self.recommendations.append({
                'service': 'Azure Advisor',
                'type': 'Visibility',
                'issue': 'Azure Advisor cost recommendations not reviewed',
                'recommendation': 'Review Azure Advisor and Cost Analysis regularly to track spend and spot anomalies',
                'potential_savings': 0,
                'priority': 'medium'
            })

        return savings

    def _prioritize_recommendations(self) -> List[Dict[str, Any]]:
        """Get top priority recommendations."""
        high_priority = [r for r in self.recommendations if r['priority'] == 'high']
        high_priority.sort(key=lambda x: x.get('potential_savings', 0), reverse=True)
        return high_priority[:5]  # Top 5 high-priority recommendations

    def generate_optimization_checklist(self) -> List[Dict[str, Any]]:
        """Generate actionable checklist for cost optimization."""
        return [
            {
                'category': 'Immediate Actions (Today)',
                'items': [
                    'Delete unattached public IPs',
                    'Deallocate idle VMs',
                    'Delete unattached managed disks',
                    'Set up Cost Management budget alerts'
                ]
            },
            {
                'category': 'This Week',
                'items': [
                    'Add Blob Storage lifecycle policies',
                    'Consolidate NAT Gateways in non-prod',
                    'Set Log Analytics retention to 30 days',
                    'Review and right-size VM / database SKUs'
                ]
            },
            {
                'category': 'This Month',
                'items': [
                    'Evaluate Azure Savings Plans or Reserved Instances',
                    'Move low-utilization Azure SQL to the serverless tier',
                    'Add private/service endpoints for Blob and Cosmos DB',
                    'Switch Cosmos DB to serverless/autoscale if load is variable'
                ]
            },
            {
                'category': 'Ongoing',
                'items': [
                    'Review Cost Analysis weekly',
                    'Tag all resources for cost allocation',
                    'Act on Azure Advisor recommendations',
                    'Conduct monthly cost review meetings'
                ]
            }
        ]
