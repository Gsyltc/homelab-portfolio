"""
Serverless stack generator for Azure.
Creates Bicep / ARM / Terraform templates for serverless applications.
"""

from typing import Dict, Any


class ServerlessStackGenerator:
    """Generate serverless application stacks for Azure."""

    def __init__(self, app_name: str, requirements: Dict[str, Any]):
        """
        Initialize with application requirements.

        Args:
            app_name: Application name (used for resource naming)
            requirements: Dictionary with API, database, auth requirements
        """
        self.app_name = app_name.lower().replace(' ', '-')
        self.requirements = requirements
        self.location = requirements.get('location', 'eastus')

    def _safe_name(self) -> str:
        """Alphanumeric-only token for resources that disallow hyphens (e.g. storage)."""
        return self.app_name.replace('-', '')

    def generate_bicep_template(self) -> str:
        """
        Generate Bicep template for the serverless stack.

        Returns:
            Bicep template as string
        """
        safe = self._safe_name()
        template = f"""// Serverless stack for {self.app_name}

@description('Deployment environment')
@allowed([ 'dev', 'staging', 'production' ])
param environment string = 'dev'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('CORS allowed origins for API Management / Functions')
param corsAllowedOrigins array = [ '*' ]

var appName = '{self.app_name}'
var prefix = '${{environment}}-${{appName}}'

// Storage account (required by the Functions runtime)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {{
  name: '{safe}${{environment}}sa'
  location: location
  sku: {{ name: 'Standard_LRS' }}
  kind: 'StorageV2'
  properties: {{
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
  }}
  tags: {{ Environment: environment, Application: appName }}
}}

// Cosmos DB (serverless)
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {{
  name: '${{prefix}}-cosmos'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {{
    databaseAccountOfferType: 'Standard'
    capabilities: [ {{ name: 'EnableServerless' }} ]
    locations: [ {{ locationName: location, failoverPriority: 0 }} ]
    backupPolicy: {{ type: 'Continuous' }}
  }}
  tags: {{ Environment: environment, Application: appName }}
}}

// Log Analytics workspace + Application Insights
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {{
  name: '${{prefix}}-logs'
  location: location
  properties: {{ retentionInDays: 30, sku: {{ name: 'PerGB2018' }} }}
}}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {{
  name: '${{prefix}}-ai'
  location: location
  kind: 'web'
  properties: {{ Application_Type: 'web', WorkspaceResourceId: logAnalytics.id }}
}}

// Consumption plan + Function App (system-assigned managed identity)
resource functionPlan 'Microsoft.Web/serverfarms@2023-01-01' = {{
  name: '${{prefix}}-plan'
  location: location
  sku: {{ name: 'Y1', tier: 'Dynamic' }}
}}

resource functionApp 'Microsoft.Web/sites@2023-01-01' = {{
  name: '${{prefix}}-fn'
  location: location
  kind: 'functionapp'
  identity: {{ type: 'SystemAssigned' }}
  properties: {{
    serverFarmId: functionPlan.id
    httpsOnly: true
    siteConfig: {{
      minTlsVersion: '1.2'
      functionAppScaleLimit: 200
      minimumElasticInstanceCount: 0
      cors: {{ allowedOrigins: corsAllowedOrigins }}
      appSettings: [
        {{ name: 'FUNCTIONS_EXTENSION_VERSION', value: '~4' }}
        {{ name: 'AzureWebJobsStorage', value: 'DefaultEndpointsProtocol=https;AccountName=${{storageAccount.name}};EndpointSuffix=${{az.environment().suffixes.storage}}' }}
        {{ name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.properties.ConnectionString }}
        {{ name: 'COSMOS_ENDPOINT', value: cosmosAccount.properties.documentEndpoint }}
        {{ name: 'ENVIRONMENT', value: environment }}
      ]
    }}
  }}
  tags: {{ Environment: environment, Application: appName }}
}}

// Grant the Function App's managed identity data access to Cosmos DB (least privilege)
resource cosmosDataContributor 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-05-15' = {{
  parent: cosmosAccount
  name: guid(cosmosAccount.id, functionApp.id, 'data-contributor')
  properties: {{
    roleDefinitionId: '${{cosmosAccount.id}}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002' // Built-in Data Contributor
    principalId: functionApp.identity.principalId
    scope: cosmosAccount.id
  }}
}}

// API Management (Consumption tier) fronting the Function App
resource apim 'Microsoft.ApiManagement/service@2023-05-01-preview' = {{
  name: '${{prefix}}-apim'
  location: location
  sku: {{ name: 'Consumption', capacity: 0 }}
  properties: {{
    publisherEmail: 'devops@example.com'
    publisherName: appName
  }}
  tags: {{ Environment: environment, Application: appName }}
}}

output functionAppName string = functionApp.name
output apimGatewayUrl string = apim.properties.gatewayUrl
output cosmosEndpoint string = cosmosAccount.properties.documentEndpoint
output appInsightsConnectionString string = appInsights.properties.ConnectionString
"""
        return template

    def generate_arm_template(self) -> str:
        """
        Generate a minimal ARM (JSON) template for the serverless stack.

        Returns:
            ARM template as a JSON string
        """
        safe = self._safe_name()
        arm = f"""{{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {{
    "environment": {{
      "type": "string",
      "defaultValue": "dev",
      "allowedValues": [ "dev", "staging", "production" ]
    }},
    "location": {{
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }}
  }},
  "variables": {{
    "appName": "{self.app_name}",
    "prefix": "[concat(parameters('environment'), '-', variables('appName'))]",
    "storageName": "[concat('{safe}', parameters('environment'), 'sa')]"
  }},
  "resources": [
    {{
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "[variables('storageName')]",
      "location": "[parameters('location')]",
      "sku": {{ "name": "Standard_LRS" }},
      "kind": "StorageV2",
      "properties": {{
        "minimumTlsVersion": "TLS1_2",
        "supportsHttpsTrafficOnly": true,
        "allowBlobPublicAccess": false
      }}
    }},
    {{
      "type": "Microsoft.DocumentDB/databaseAccounts",
      "apiVersion": "2024-05-15",
      "name": "[concat(variables('prefix'), '-cosmos')]",
      "location": "[parameters('location')]",
      "kind": "GlobalDocumentDB",
      "properties": {{
        "databaseAccountOfferType": "Standard",
        "capabilities": [ {{ "name": "EnableServerless" }} ],
        "locations": [ {{ "locationName": "[parameters('location')]", "failoverPriority": 0 }} ],
        "backupPolicy": {{ "type": "Continuous" }}
      }}
    }},
    {{
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2023-01-01",
      "name": "[concat(variables('prefix'), '-plan')]",
      "location": "[parameters('location')]",
      "sku": {{ "name": "Y1", "tier": "Dynamic" }}
    }},
    {{
      "type": "Microsoft.Web/sites",
      "apiVersion": "2023-01-01",
      "name": "[concat(variables('prefix'), '-fn')]",
      "location": "[parameters('location')]",
      "kind": "functionapp",
      "identity": {{ "type": "SystemAssigned" }},
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', concat(variables('prefix'), '-plan'))]",
        "[resourceId('Microsoft.Storage/storageAccounts', variables('storageName'))]"
      ],
      "properties": {{
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', concat(variables('prefix'), '-plan'))]",
        "httpsOnly": true,
        "siteConfig": {{ "minTlsVersion": "1.2", "functionAppScaleLimit": 200 }}
      }}
    }}
  ],
  "outputs": {{
    "functionAppName": {{
      "type": "string",
      "value": "[concat(variables('prefix'), '-fn')]"
    }}
  }}
}}
"""
        return arm

    def generate_terraform_configuration(self) -> str:
        """
        Generate Terraform (azurerm) configuration for the serverless stack.

        Returns:
            Terraform HCL configuration as string
        """
        safe = self._safe_name()
        terraform = f"""terraform {{
  required_version = ">= 1.0"
  required_providers {{
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }}
  }}
}}

provider "azurerm" {{
  features {{}}
}}

variable "location" {{
  description = "Azure region"
  type        = string
  default     = "{self.location}"
}}

variable "environment" {{
  description = "Environment name"
  type        = string
  default     = "dev"
}}

variable "app_name" {{
  description = "Application name"
  type        = string
  default     = "{self.app_name}"
}}

locals {{
  prefix = "${{var.environment}}-${{var.app_name}}"
}}

resource "azurerm_resource_group" "main" {{
  name     = "${{local.prefix}}-rg"
  location = var.location
  tags = {{
    Environment = var.environment
    Application = var.app_name
  }}
}}

resource "azurerm_storage_account" "main" {{
  name                            = "{safe}${{var.environment}}sa"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
}}

resource "azurerm_cosmosdb_account" "main" {{
  name                = "${{local.prefix}}-cosmos"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  capabilities {{
    name = "EnableServerless"
  }}

  consistency_policy {{
    consistency_level = "Session"
  }}

  geo_location {{
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }}
}}

resource "azurerm_log_analytics_workspace" "main" {{
  name                = "${{local.prefix}}-logs"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}}

resource "azurerm_application_insights" "main" {{
  name                = "${{local.prefix}}-ai"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
}}

resource "azurerm_service_plan" "main" {{
  name                = "${{local.prefix}}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption
}}

resource "azurerm_linux_function_app" "main" {{
  name                       = "${{local.prefix}}-fn"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  service_plan_id            = azurerm_service_plan.main.id
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  https_only                 = true

  identity {{
    type = "SystemAssigned"
  }}

  site_config {{
    minimum_tls_version = "1.2"
    application_insights_connection_string = azurerm_application_insights.main.connection_string
  }}

  app_settings = {{
    COSMOS_ENDPOINT = azurerm_cosmosdb_account.main.endpoint
    ENVIRONMENT     = var.environment
  }}

  tags = {{
    Environment = var.environment
    Application = var.app_name
  }}
}}

# Grant the Function App managed identity data access to Cosmos DB (least privilege)
resource "azurerm_cosmosdb_sql_role_assignment" "fn_data" {{
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = "${{azurerm_cosmosdb_account.main.id}}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"
  principal_id        = azurerm_linux_function_app.main.identity[0].principal_id
  scope               = azurerm_cosmosdb_account.main.id
}}

output "function_app_name" {{
  description = "Function App name"
  value       = azurerm_linux_function_app.main.name
}}

output "cosmos_endpoint" {{
  description = "Cosmos DB endpoint"
  value       = azurerm_cosmosdb_account.main.endpoint
}}

output "app_insights_connection_string" {{
  description = "Application Insights connection string"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}}
"""
        return terraform
