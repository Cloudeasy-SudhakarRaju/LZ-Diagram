from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import html
import json
import uuid
import os
import base64
from datetime import datetime

# Import diagrams for Azure architecture generation
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import VM, AKS, AppServices, FunctionApps, ContainerInstances, ServiceFabricClusters, BatchAccounts
from diagrams.azure.network import VirtualNetworks, ApplicationGateway, LoadBalancers, Firewall, ExpressrouteCircuits, VirtualNetworkGateways
from diagrams.azure.storage import StorageAccounts, BlobStorage, DataLakeStorage
from diagrams.azure.database import SQLDatabases, CosmosDb, DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.security import KeyVaults, SecurityCenter, Sentinel
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.analytics import SynapseAnalytics, DataFactories, Databricks, StreamAnalyticsJobs, EventHubs
from diagrams.azure.integration import LogicApps, ServiceBus, EventGridTopics, APIManagement
from diagrams.azure.devops import Devops, Pipelines
from diagrams.azure.general import Subscriptions, Resourcegroups
from diagrams.azure.web import AppServices as WebApps

app = FastAPI(
    title="Azure Landing Zone Agent",
    description="Professional Azure Landing Zone Architecture Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # open for dev, restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CustomerInputs(BaseModel):
    # Business Requirements
    business_objective: Optional[str] = Field(None, description="Primary business objective")
    regulatory: Optional[str] = Field(None, description="Regulatory requirements")
    industry: Optional[str] = Field(None, description="Industry vertical")
    
    # Organization Structure
    org_structure: Optional[str] = Field(None, description="Organization structure")
    governance: Optional[str] = Field(None, description="Governance model")
    
    # Identity & Access Management
    identity: Optional[str] = Field(None, description="Identity management approach")
    
    # Networking & Connectivity
    connectivity: Optional[str] = Field(None, description="Connectivity requirements")
    network_model: Optional[str] = Field(None, description="Network topology model")
    ip_strategy: Optional[str] = Field(None, description="IP address strategy")
    
    # Security
    security_zone: Optional[str] = Field(None, description="Security zone requirements")
    security_posture: Optional[str] = Field(None, description="Security posture")
    key_vault: Optional[str] = Field(None, description="Key management approach")
    threat_protection: Optional[str] = Field(None, description="Threat protection strategy")
    
    # Legacy fields for backward compatibility
    workload: Optional[str] = Field(None, description="Primary workload type")
    architecture_style: Optional[str] = Field(None, description="Architecture style")
    scalability: Optional[str] = Field(None, description="Scalability requirements")
    
    # Operations
    ops_model: Optional[str] = Field(None, description="Operations model")
    monitoring: Optional[str] = Field(None, description="Monitoring strategy")
    backup: Optional[str] = Field(None, description="Backup and recovery strategy")
    
    # Infrastructure
    topology_pattern: Optional[str] = Field(None, description="Topology pattern")
    
    # Migration & Cost
    migration_scope: Optional[str] = Field(None, description="Migration scope")
    cost_priority: Optional[str] = Field(None, description="Cost optimization priority")
    iac: Optional[str] = Field(None, description="Infrastructure as Code preference")
    
    # Specific Azure Service Selections
    # Compute Services
    compute_services: Optional[List[str]] = Field(default_factory=list, description="Selected compute services")
    
    # Networking Services
    network_services: Optional[List[str]] = Field(default_factory=list, description="Selected networking services")
    
    # Storage Services
    storage_services: Optional[List[str]] = Field(default_factory=list, description="Selected storage services")
    
    # Database Services
    database_services: Optional[List[str]] = Field(default_factory=list, description="Selected database services")
    
    # Security Services
    security_services: Optional[List[str]] = Field(default_factory=list, description="Selected security services")
    
    # Monitoring Services
    monitoring_services: Optional[List[str]] = Field(default_factory=list, description="Selected monitoring services")
    
    # AI/ML Services
    ai_services: Optional[List[str]] = Field(default_factory=list, description="Selected AI/ML services")
    
    # Analytics Services
    analytics_services: Optional[List[str]] = Field(default_factory=list, description="Selected analytics services")
    
    # Integration Services
    integration_services: Optional[List[str]] = Field(default_factory=list, description="Selected integration services")
    
    # DevOps Services
    devops_services: Optional[List[str]] = Field(default_factory=list, description="Selected DevOps services")
    
    # Backup Services
    backup_services: Optional[List[str]] = Field(default_factory=list, description="Selected backup services")


# Azure Architecture Templates and Patterns
AZURE_TEMPLATES = {
    "enterprise": {
        "name": "Enterprise Scale Landing Zone",
        "management_groups": ["Root", "Platform", "Landing Zones", "Sandbox", "Decommissioned"],
        "subscriptions": ["Connectivity", "Identity", "Management", "Production", "Development"],
        "core_services": ["Azure AD", "Azure Policy", "Azure Monitor", "Key Vault", "Security Center"]
    },
    "small_medium": {
        "name": "Small-Medium Enterprise Landing Zone", 
        "management_groups": ["Root", "Platform", "Workloads"],
        "subscriptions": ["Platform", "Production", "Development"],
        "core_services": ["Azure AD", "Azure Monitor", "Key Vault"]
    },
    "startup": {
        "name": "Startup Landing Zone",
        "management_groups": ["Root", "Workloads"],
        "subscriptions": ["Production", "Development"],
        "core_services": ["Azure AD", "Azure Monitor"]
    }
}

AZURE_SERVICES_MAPPING = {
    # Compute Services
    "virtual_machines": {"name": "Azure Virtual Machines", "icon": "🖥️", "diagram_class": VM, "category": "compute"},
    "aks": {"name": "Azure Kubernetes Service", "icon": "☸️", "diagram_class": AKS, "category": "compute"},
    "app_services": {"name": "Azure App Services", "icon": "🌐", "diagram_class": AppServices, "category": "compute"},
    "web_apps": {"name": "Azure Web Apps", "icon": "🌐", "diagram_class": WebApps, "category": "compute"},
    "functions": {"name": "Azure Functions", "icon": "⚡", "diagram_class": FunctionApps, "category": "compute"},
    "container_instances": {"name": "Container Instances", "icon": "📦", "diagram_class": ContainerInstances, "category": "compute"},
    "service_fabric": {"name": "Service Fabric", "icon": "🏗️", "diagram_class": ServiceFabricClusters, "category": "compute"},
    "batch": {"name": "Azure Batch", "icon": "⚙️", "diagram_class": BatchAccounts, "category": "compute"},
    
    # Networking Services
    "virtual_network": {"name": "Virtual Network", "icon": "🌐", "diagram_class": VirtualNetworks, "category": "network"},
    "vpn_gateway": {"name": "VPN Gateway", "icon": "🔒", "diagram_class": VirtualNetworkGateways, "category": "network"},
    "expressroute": {"name": "ExpressRoute", "icon": "⚡", "diagram_class": ExpressrouteCircuits, "category": "network"},
    "load_balancer": {"name": "Load Balancer", "icon": "⚖️", "diagram_class": LoadBalancers, "category": "network"},
    "application_gateway": {"name": "Application Gateway", "icon": "🚪", "diagram_class": ApplicationGateway, "category": "network"},
    "firewall": {"name": "Azure Firewall", "icon": "🛡️", "diagram_class": Firewall, "category": "network"},
    "waf": {"name": "Web Application Firewall", "icon": "🛡️", "diagram_class": ApplicationGateway, "category": "network"},
    "cdn": {"name": "Content Delivery Network", "icon": "🌍", "diagram_class": None, "category": "network"},  # No specific CDN class
    "traffic_manager": {"name": "Traffic Manager", "icon": "🚦", "diagram_class": None, "category": "network"},  # No specific class
    "virtual_wan": {"name": "Virtual WAN", "icon": "🌐", "diagram_class": VirtualNetworks, "category": "network"},
    
    # Storage Services
    "storage_accounts": {"name": "Storage Accounts", "icon": "💾", "diagram_class": StorageAccounts, "category": "storage"},
    "blob_storage": {"name": "Blob Storage", "icon": "📄", "diagram_class": BlobStorage, "category": "storage"},
    "file_storage": {"name": "Azure Files", "icon": "📁", "diagram_class": StorageAccounts, "category": "storage"},
    "disk_storage": {"name": "Managed Disks", "icon": "💿", "diagram_class": StorageAccounts, "category": "storage"},
    "data_lake": {"name": "Data Lake Storage", "icon": "🏞️", "diagram_class": DataLakeStorage, "category": "storage"},
    
    # Database Services
    "sql_database": {"name": "Azure SQL Database", "icon": "🗄️", "diagram_class": SQLDatabases, "category": "database"},
    "sql_managed_instance": {"name": "SQL Managed Instance", "icon": "🗄️", "diagram_class": SQLDatabases, "category": "database"},
    "cosmos_db": {"name": "Cosmos DB", "icon": "🌍", "diagram_class": CosmosDb, "category": "database"},
    "mysql": {"name": "Azure Database for MySQL", "icon": "🐬", "diagram_class": DatabaseForMysqlServers, "category": "database"},
    "postgresql": {"name": "Azure Database for PostgreSQL", "icon": "🐘", "diagram_class": DatabaseForPostgresqlServers, "category": "database"},
    "mariadb": {"name": "Azure Database for MariaDB", "icon": "🗄️", "diagram_class": DatabaseForMysqlServers, "category": "database"},
    "redis_cache": {"name": "Azure Cache for Redis", "icon": "⚡", "diagram_class": None, "category": "database"},  # No specific Redis class
    
    # Security Services
    "key_vault": {"name": "Azure Key Vault", "icon": "🔐", "diagram_class": KeyVaults, "category": "security"},
    "active_directory": {"name": "Azure Active Directory", "icon": "👤", "diagram_class": ActiveDirectory, "category": "security"},
    "security_center": {"name": "Azure Security Center", "icon": "🛡️", "diagram_class": SecurityCenter, "category": "security"},
    "sentinel": {"name": "Azure Sentinel", "icon": "👁️", "diagram_class": Sentinel, "category": "security"},
    "defender": {"name": "Microsoft Defender", "icon": "🛡️", "diagram_class": SecurityCenter, "category": "security"},
    "information_protection": {"name": "Azure Information Protection", "icon": "🔒", "diagram_class": None, "category": "security"},
    
    # Monitoring & Management
    "monitor": {"name": "Azure Monitor", "icon": "📊", "diagram_class": None, "category": "monitoring"},  # No specific Monitor class
    "log_analytics": {"name": "Log Analytics", "icon": "📋", "diagram_class": None, "category": "monitoring"},
    "application_insights": {"name": "Application Insights", "icon": "📈", "diagram_class": None, "category": "monitoring"},
    "service_health": {"name": "Service Health", "icon": "❤️", "diagram_class": None, "category": "monitoring"},
    "advisor": {"name": "Azure Advisor", "icon": "💡", "diagram_class": None, "category": "monitoring"},
    
    # AI/ML Services  
    "cognitive_services": {"name": "Cognitive Services", "icon": "🧠", "diagram_class": None, "category": "ai"},
    "machine_learning": {"name": "Azure Machine Learning", "icon": "🤖", "diagram_class": None, "category": "ai"},
    "bot_service": {"name": "Bot Service", "icon": "🤖", "diagram_class": None, "category": "ai"},
    "form_recognizer": {"name": "Form Recognizer", "icon": "📄", "diagram_class": None, "category": "ai"},
    
    # Data & Analytics
    "synapse": {"name": "Azure Synapse Analytics", "icon": "📊", "diagram_class": SynapseAnalytics, "category": "analytics"},
    "data_factory": {"name": "Azure Data Factory", "icon": "🏭", "diagram_class": DataFactories, "category": "analytics"},
    "databricks": {"name": "Azure Databricks", "icon": "📊", "diagram_class": Databricks, "category": "analytics"},
    "stream_analytics": {"name": "Stream Analytics", "icon": "🌊", "diagram_class": StreamAnalyticsJobs, "category": "analytics"},
    "power_bi": {"name": "Power BI", "icon": "📊", "diagram_class": None, "category": "analytics"},
    
    # Integration Services
    "logic_apps": {"name": "Logic Apps", "icon": "🔗", "diagram_class": LogicApps, "category": "integration"},
    "service_bus": {"name": "Service Bus", "icon": "🚌", "diagram_class": ServiceBus, "category": "integration"},
    "event_grid": {"name": "Event Grid", "icon": "⚡", "diagram_class": EventGridTopics, "category": "integration"},
    "event_hubs": {"name": "Event Hubs", "icon": "📡", "diagram_class": EventHubs, "category": "integration"},
    "api_management": {"name": "API Management", "icon": "🔌", "diagram_class": APIManagement, "category": "integration"},
    
    # DevOps & Management
    "devops": {"name": "Azure DevOps", "icon": "⚙️", "diagram_class": Devops, "category": "devops"},
    "automation": {"name": "Azure Automation", "icon": "🤖", "diagram_class": None, "category": "devops"},
    "policy": {"name": "Azure Policy", "icon": "📋", "diagram_class": None, "category": "governance"},
    "blueprints": {"name": "Azure Blueprints", "icon": "📐", "diagram_class": None, "category": "governance"},
    "resource_manager": {"name": "Azure Resource Manager", "icon": "🏗️", "diagram_class": Resourcegroups, "category": "governance"},
    
    # Backup & Recovery
    "backup": {"name": "Azure Backup", "icon": "💾", "diagram_class": None, "category": "backup"},
    "site_recovery": {"name": "Azure Site Recovery", "icon": "🔄", "diagram_class": None, "category": "backup"},
}

def generate_azure_architecture_diagram(inputs: CustomerInputs, output_dir: str = "/tmp") -> str:
    """Generate Azure architecture diagram using the Python Diagrams library with proper Azure icons"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"azure_landing_zone_{timestamp}"
    filepath = os.path.join(output_dir, filename)
    
    # Determine organization template
    template = generate_architecture_template(inputs)
    org_name = inputs.org_structure or "Enterprise"
    
    try:
        with Diagram(
            f"Azure Landing Zone - {template['template']['name']}", 
            filename=filepath, 
            show=False, 
            direction="TB",
            graph_attr={
                "fontsize": "16",
                "fontname": "Arial",
                "rankdir": "TB",
                "nodesep": "1.0",
                "ranksep": "1.5",
                "bgcolor": "#ffffff",
                "margin": "0.5"
            },
            node_attr={
                "fontsize": "12",
                "fontname": "Arial"
            },
            edge_attr={
                "fontsize": "10",
                "fontname": "Arial"
            }
        ):
            
            # Core Identity and Security Services
            with Cluster("Identity & Security", graph_attr={"bgcolor": "#e8f4f8", "style": "rounded"}):
                aad = ActiveDirectory("Azure Active Directory")
                key_vault = KeyVaults("Key Vault")
                if inputs.security_services and "security_center" in inputs.security_services:
                    sec_center = SecurityCenter("Security Center")
                if inputs.security_services and "sentinel" in inputs.security_services:
                    sentinel = Sentinel("Sentinel")
            
            # Management Groups and Subscriptions Structure
            with Cluster("Management & Governance", graph_attr={"bgcolor": "#f0f8ff", "style": "rounded"}):
                root_mg = Subscriptions("Root Management Group")
                if template['template']['name'] == "Enterprise Scale Landing Zone":
                    platform_mg = Subscriptions("Platform MG")
                    workloads_mg = Subscriptions("Landing Zones MG")
                    root_mg >> [platform_mg, workloads_mg]
                else:
                    platform_mg = Subscriptions("Platform MG")
                    workloads_mg = Subscriptions("Workloads MG")
                    root_mg >> [platform_mg, workloads_mg]
            
            # Networking Architecture
            with Cluster("Network Architecture", graph_attr={"bgcolor": "#f0fff0", "style": "rounded"}):
                # Hub VNet
                hub_vnet = VirtualNetworks("Hub VNet\n(Shared Services)")
                
                # Network services based on selections
                network_services = []
                if inputs.network_services:
                    for service in inputs.network_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            network_services.append(diagram_class(service_name))
                
                # Default network services if none specified
                if not network_services:
                    firewall = Firewall("Azure Firewall")
                    vpn_gw = VirtualNetworkGateways("VPN Gateway")
                    network_services = [firewall, vpn_gw]
                
                # Spoke VNets
                prod_vnet = VirtualNetworks("Production VNet")
                dev_vnet = VirtualNetworks("Development VNet")
                
                # Connect hub to spokes
                hub_vnet >> [prod_vnet, dev_vnet]
                
                # Connect platform subscription to hub
                platform_mg >> hub_vnet
                
                # Connect network services to hub
                for ns in network_services:
                    hub_vnet >> ns
            
            # Compute and Application Services
            if inputs.compute_services or inputs.workload:
                with Cluster("Compute & Applications", graph_attr={"bgcolor": "#fff8dc", "style": "rounded"}):
                    compute_services = []
                    
                    # Add selected compute services
                    if inputs.compute_services:
                        for service in inputs.compute_services:
                            if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                                diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                                service_name = AZURE_SERVICES_MAPPING[service]["name"]
                                compute_services.append(diagram_class(service_name))
                    
                    # Fallback to workload if no specific compute services
                    if not compute_services and inputs.workload:
                        if inputs.workload in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[inputs.workload]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[inputs.workload]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[inputs.workload]["name"]
                            compute_services.append(diagram_class(service_name))
                    
                    # Default to App Services if nothing specified
                    if not compute_services:
                        compute_services.append(AppServices("Azure App Services"))
                    
                    # Connect compute services to production VNet
                    for cs in compute_services:
                        prod_vnet >> cs
                        workloads_mg >> cs
            
            # Storage Services
            if inputs.storage_services:
                with Cluster("Storage & Data", graph_attr={"bgcolor": "#f5f5dc", "style": "rounded"}):
                    storage_services = []
                    for service in inputs.storage_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            storage_services.append(diagram_class(service_name))
                    
                    if not storage_services:
                        storage_services.append(StorageAccounts("Storage Accounts"))
                    
                    # Connect storage to production VNet and workloads
                    for ss in storage_services:
                        prod_vnet >> ss
                        workloads_mg >> ss
            
            # Database Services
            if inputs.database_services:
                with Cluster("Databases", graph_attr={"bgcolor": "#e6f3ff", "style": "rounded"}):
                    database_services = []
                    for service in inputs.database_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            database_services.append(diagram_class(service_name))
                    
                    # Connect databases to production VNet and workloads
                    for ds in database_services:
                        prod_vnet >> ds
                        workloads_mg >> ds
            
            # Analytics Services
            if inputs.analytics_services:
                with Cluster("Analytics & AI", graph_attr={"bgcolor": "#f0e6ff", "style": "rounded"}):
                    analytics_services = []
                    for service in inputs.analytics_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            analytics_services.append(diagram_class(service_name))
                    
                    # Connect analytics to production VNet and workloads
                    for as_service in analytics_services:
                        prod_vnet >> as_service
                        workloads_mg >> as_service
            
            # Integration Services
            if inputs.integration_services:
                with Cluster("Integration", graph_attr={"bgcolor": "#fff0e6", "style": "rounded"}):
                    integration_services = []
                    for service in inputs.integration_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            integration_services.append(diagram_class(service_name))
                    
                    # Connect integration services to production VNet and workloads
                    for is_service in integration_services:
                        prod_vnet >> is_service
                        workloads_mg >> is_service
            
            # DevOps Services
            if inputs.devops_services:
                with Cluster("DevOps & Automation", graph_attr={"bgcolor": "#f5f5f5", "style": "rounded"}):
                    devops_services = []
                    for service in inputs.devops_services:
                        if service in AZURE_SERVICES_MAPPING and AZURE_SERVICES_MAPPING[service]["diagram_class"]:
                            diagram_class = AZURE_SERVICES_MAPPING[service]["diagram_class"]
                            service_name = AZURE_SERVICES_MAPPING[service]["name"]
                            devops_services.append(diagram_class(service_name))
                    
                    # Connect DevOps services to management
                    for ds in devops_services:
                        platform_mg >> ds
            
            # Core security connections
            aad >> key_vault
            platform_mg >> [aad, key_vault]
            
    except Exception as e:
        raise Exception(f"Error generating Azure architecture diagram: {str(e)}")
    
    # Return the file path of the generated PNG
    png_path = f"{filepath}.png"
    if os.path.exists(png_path):
        return png_path
    else:
        raise Exception(f"Diagram generation failed - PNG file not found: {png_path}")


def generate_architecture_template(inputs: CustomerInputs) -> Dict[str, Any]:
    """Generate architecture template based on inputs"""
    
    # Determine organization size and template
    if inputs.org_structure and "enterprise" in inputs.org_structure.lower():
        template = AZURE_TEMPLATES["enterprise"]
    elif inputs.org_structure and any(x in inputs.org_structure.lower() for x in ["small", "medium", "sme"]):
        template = AZURE_TEMPLATES["small_medium"]
    else:
        template = AZURE_TEMPLATES["startup"]
    
    # Build architecture components
    components = {
        "template": template,
        "identity": inputs.identity or "Azure AD",
        "network_model": inputs.network_model or "hub-spoke",
        "workload": inputs.workload or "app-services",
        "security": inputs.security_posture or "zero-trust",
        "monitoring": inputs.monitoring or "azure-monitor",
        "governance": inputs.governance or "azure-policy"
    }
    
    return components

def generate_professional_mermaid(inputs: CustomerInputs) -> str:
    """Generate professional Mermaid diagram for Azure Landing Zone"""
    
    template = generate_architecture_template(inputs)
    network_model = inputs.network_model or "hub-spoke"
    
    lines = [
        "graph TB",
        "    subgraph \"Azure Tenant\"",
        "        subgraph \"Management Groups\"",
        "            ROOT[\"🏢 Root Management Group\"]"
    ]
    
    # Add management group hierarchy
    if template["template"]["name"] == "Enterprise Scale Landing Zone":
        lines.extend([
            "            PLATFORM[\"🏗️ Platform\"]",
            "            LANDINGZONES[\"🚀 Landing Zones\"]", 
            "            SANDBOX[\"🧪 Sandbox\"]",
            "            DECOM[\"🗑️ Decommissioned\"]",
            "            ROOT --> PLATFORM",
            "            ROOT --> LANDINGZONES",
            "            ROOT --> SANDBOX", 
            "            ROOT --> DECOM"
        ])
    else:
        lines.extend([
            "            PLATFORM[\"🏗️ Platform\"]",
            "            WORKLOADS[\"💼 Workloads\"]",
            "            ROOT --> PLATFORM",
            "            ROOT --> WORKLOADS"
        ])
    
    lines.append("        end")
    
    # Add subscription structure
    lines.extend([
        "        subgraph \"Subscriptions\"",
        "            CONN[\"🌐 Connectivity\"]",
        "            IDENTITY[\"🔐 Identity\"]",
        "            MGMT[\"📊 Management\"]",
        "            PROD[\"🏭 Production\"]",
        "            DEV[\"👩‍💻 Development\"]"
    ])
    
    if template["template"]["name"] == "Enterprise Scale Landing Zone":
        lines.extend([
            "            PLATFORM --> CONN",
            "            PLATFORM --> IDENTITY", 
            "            PLATFORM --> MGMT",
            "            LANDINGZONES --> PROD",
            "            LANDINGZONES --> DEV"
        ])
    else:
        lines.extend([
            "            PLATFORM --> CONN",
            "            PLATFORM --> IDENTITY",
            "            WORKLOADS --> PROD",
            "            WORKLOADS --> DEV"
        ])
    
    lines.append("        end")
    
    # Add networking services based on selections
    if inputs.network_services:
        lines.extend([
            "        subgraph \"Networking Services\""
        ])
        
        service_connections = []
        for service in inputs.network_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            CONN --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add compute services based on selections
    if inputs.compute_services:
        lines.extend([
            "        subgraph \"Compute Services\""
        ])
        
        service_connections = []
        for service in inputs.compute_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add storage services based on selections
    if inputs.storage_services:
        lines.extend([
            "        subgraph \"Storage Services\""
        ])
        
        service_connections = []
        for service in inputs.storage_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add database services based on selections
    if inputs.database_services:
        lines.extend([
            "        subgraph \"Database Services\""
        ])
        
        service_connections = []
        for service in inputs.database_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add security services based on selections
    if inputs.security_services:
        lines.extend([
            "        subgraph \"Security & Identity\""
        ])
        
        service_connections = []
        for service in inputs.security_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            IDENTITY --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add monitoring services based on selections
    if inputs.monitoring_services:
        lines.extend([
            "        subgraph \"Monitoring & Management\""
        ])
        
        service_connections = []
        for service in inputs.monitoring_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            MGMT --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add AI/ML services based on selections  
    if inputs.ai_services:
        lines.extend([
            "        subgraph \"AI & Machine Learning\""
        ])
        
        service_connections = []
        for service in inputs.ai_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add analytics services based on selections
    if inputs.analytics_services:
        lines.extend([
            "        subgraph \"Data & Analytics\""
        ])
        
        service_connections = []
        for service in inputs.analytics_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add integration services based on selections
    if inputs.integration_services:
        lines.extend([
            "        subgraph \"Integration Services\""
        ])
        
        service_connections = []
        for service in inputs.integration_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            PROD --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add DevOps services based on selections
    if inputs.devops_services:
        lines.extend([
            "        subgraph \"DevOps & Governance\""
        ])
        
        service_connections = []
        for service in inputs.devops_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            MGMT --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Add backup services based on selections
    if inputs.backup_services:
        lines.extend([
            "        subgraph \"Backup & Recovery\""
        ])
        
        service_connections = []
        for service in inputs.backup_services:
            if service in AZURE_SERVICES_MAPPING:
                service_info = AZURE_SERVICES_MAPPING[service]
                service_id = service.upper().replace("_", "")
                lines.append(f"            {service_id}[\"{service_info['icon']} {service_info['name']}\"]")
                service_connections.append(f"            MGMT --> {service_id}")
        
        lines.extend(service_connections)
        lines.append("        end")
    
    # Fallback for legacy workload field
    if not any([inputs.compute_services, inputs.network_services, inputs.storage_services, 
               inputs.database_services, inputs.security_services, inputs.monitoring_services,
               inputs.ai_services, inputs.analytics_services, inputs.integration_services,
               inputs.devops_services, inputs.backup_services]) and inputs.workload:
        workload_name = AZURE_SERVICES_MAPPING.get(inputs.workload, {"name": inputs.workload, "icon": "⚙️"})["name"]
        lines.extend([
            "        subgraph \"Workloads\"",
            f"            WORKLOAD[\"{workload_name}\"]",
            "            PROD --> WORKLOAD",
            "        end"
        ])
    
    lines.append("    end")
    
    # Add styling
    lines.extend([
        "",
        "    classDef mgmtGroup fill:#e1f5fe,stroke:#01579b,stroke-width:2px;",
        "    classDef subscription fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;", 
        "    classDef compute fill:#fff3e0,stroke:#e65100,stroke-width:2px;",
        "    classDef network fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px;",
        "    classDef storage fill:#fce4ec,stroke:#880e4f,stroke-width:2px;",
        "    classDef database fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px;",
        "    classDef security fill:#ffebee,stroke:#b71c1c,stroke-width:2px;",
        "    classDef monitoring fill:#f1f8e9,stroke:#33691e,stroke-width:2px;",
        "    classDef ai fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;",
        "    classDef analytics fill:#e8eaf6,stroke:#1a237e,stroke-width:2px;",
        "    classDef integration fill:#fff8e1,stroke:#f57f17,stroke-width:2px;",
        "    classDef devops fill:#fafafa,stroke:#424242,stroke-width:2px;",
        "    classDef backup fill:#e0f2f1,stroke:#00695c,stroke-width:2px;",
        "",
        "    class ROOT,PLATFORM,LANDINGZONES,SANDBOX,DECOM,WORKLOADS mgmtGroup;",
        "    class CONN,IDENTITY,MGMT,PROD,DEV subscription;"
    ])
    
    return "\n".join(lines)

def generate_enhanced_drawio_xml(inputs: CustomerInputs) -> str:
    """Generate enhanced Draw.io XML with better Azure stencils"""
    
    def esc(s): 
        return html.escape(s) if s else ""
    
    template = generate_architecture_template(inputs)
    
    return f"""<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="Azure Landing Zone Agent" version="1.0.0">
  <diagram name="Azure Landing Zone Architecture" id="azure-lz-{uuid.uuid4()}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Azure Tenant Container -->
        <mxCell id="tenant" value="Azure Tenant - {esc(inputs.org_structure or 'Enterprise')}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=16;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="1800" height="1100" as="geometry" />
        </mxCell>
        
        <!-- Management Groups -->
        <mxCell id="mgmt-groups" value="Management Groups" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="400" height="300" as="geometry" />
        </mxCell>
        
        <mxCell id="root-mg" value="Root MG" style="shape=mxgraph.azure.management;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="150" y="150" width="80" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="platform-mg" value="Platform" style="shape=mxgraph.azure.management;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="280" y="150" width="80" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="workloads-mg" value="Workloads" style="shape=mxgraph.azure.management;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="400" y="150" width="80" height="60" as="geometry" />
        </mxCell>
        
        <!-- Subscriptions -->
        <mxCell id="subscriptions" value="Subscriptions" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="600" y="100" width="500" height="300" as="geometry" />
        </mxCell>
        
        <mxCell id="connectivity-sub" value="Connectivity" style="shape=mxgraph.azure.subscription;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="650" y="150" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="identity-sub" value="Identity" style="shape=mxgraph.azure.subscription;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="800" y="150" width="100" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="prod-sub" value="Production" style="shape=mxgraph.azure.subscription;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="950" y="150" width="100" height="60" as="geometry" />
        </mxCell>
        
        <!-- Network Architecture -->
        <mxCell id="network" value="Network Architecture - {esc(inputs.network_model or 'Hub-Spoke')}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="100" y="500" width="600" height="400" as="geometry" />
        </mxCell>
        
        <mxCell id="hub-vnet" value="Hub VNet\\nShared Services" style="shape=mxgraph.azure.virtual_network;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="200" y="600" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="spoke1-vnet" value="Spoke VNet 1\\nProduction" style="shape=mxgraph.azure.virtual_network;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="400" y="550" width="120" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="spoke2-vnet" value="Spoke VNet 2\\nDevelopment" style="shape=mxgraph.azure.virtual_network;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="400" y="700" width="120" height="80" as="geometry" />
        </mxCell>
        
        <!-- Workloads -->
        <mxCell id="workloads" value="Workloads - {esc(inputs.workload or 'Application Services')}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="800" y="500" width="400" height="400" as="geometry" />
        </mxCell>
        
        <mxCell id="primary-workload" value="{esc(AZURE_SERVICES_MAPPING.get(inputs.workload or 'appservices', {'name': 'App Services'})['name'])}" style="shape=mxgraph.azure.{AZURE_SERVICES_MAPPING.get(inputs.workload or 'appservices', {'icon': 'app_services'})['icon']};fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="900" y="600" width="120" height="80" as="geometry" />
        </mxCell>
        
        <!-- Security & Governance -->
        <mxCell id="security" value="Security &amp; Governance" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcccc;strokeColor=#ff6666;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
          <mxGeometry x="1300" y="100" width="500" height="800" as="geometry" />
        </mxCell>
        
        <mxCell id="azure-ad" value="Azure AD" style="shape=mxgraph.azure.azure_active_directory;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="1400" y="200" width="80" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="azure-policy" value="Azure Policy" style="shape=mxgraph.azure.azure_governance;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="1400" y="350" width="80" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="key-vault" value="Key Vault" style="shape=mxgraph.azure.key_vault;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="1400" y="500" width="80" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="security-center" value="Security Center" style="shape=mxgraph.azure.security_center;fillColor=#0078d4;strokeColor=#005a9e;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="1400" y="650" width="80" height="80" as="geometry" />
        </mxCell>
        
        <!-- Connections -->
        <mxCell id="conn1" edge="1" source="root-mg" target="platform-mg" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn2" edge="1" source="root-mg" target="workloads-mg" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn3" edge="1" source="platform-mg" target="connectivity-sub" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn4" edge="1" source="platform-mg" target="identity-sub" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn5" edge="1" source="workloads-mg" target="prod-sub" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn6" edge="1" source="connectivity-sub" target="hub-vnet" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn7" edge="1" source="hub-vnet" target="spoke1-vnet" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn8" edge="1" source="hub-vnet" target="spoke2-vnet" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn9" edge="1" source="prod-sub" target="primary-workload" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="conn10" edge="1" source="identity-sub" target="azure-ad" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


def generate_professional_documentation(inputs: CustomerInputs) -> Dict[str, str]:
    """Generate professional TSD, HLD, and LLD documentation"""
    
    template = generate_architecture_template(inputs)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Technical Specification Document (TSD)
    tsd = f"""# Technical Specification Document (TSD)
## Azure Landing Zone Architecture

**Document Version:** 1.0
**Date:** {timestamp}
**Business Objective:** {inputs.business_objective or 'Not specified'}

### Executive Summary
This document outlines the technical specifications for implementing an Azure Landing Zone architecture based on the customer requirements.

### Business Requirements
- **Primary Objective:** {inputs.business_objective or 'Cost optimization and operational efficiency'}
- **Industry:** {inputs.industry or 'General'}
- **Regulatory Requirements:** {inputs.regulatory or 'Standard compliance'}
- **Organization Size:** {inputs.org_structure or 'Enterprise'}

### Architecture Template
**Selected Template:** {template['template']['name']}

### Key Components
- **Identity Management:** {inputs.identity or 'Azure Active Directory'}
- **Network Model:** {inputs.network_model or 'Hub-Spoke architecture'}
- **Security Posture:** {inputs.security_posture or 'Zero Trust approach'}
- **Primary Workload:** {inputs.workload or 'Application Services'}
- **Monitoring Strategy:** {inputs.monitoring or 'Azure Monitor suite'}

### Compliance & Governance
- **Governance Model:** {inputs.governance or 'Centralized with delegated permissions'}
- **Policy Framework:** Azure Policy for compliance enforcement
- **Security Framework:** {inputs.security_posture or 'Zero Trust'} security model
"""

    # High Level Design (HLD)
    hld = f"""# High Level Design (HLD)
## Azure Landing Zone Implementation

**Document Version:** 1.0
**Date:** {timestamp}

### Architecture Overview
The proposed Azure Landing Zone follows the {template['template']['name']} pattern.

### Management Group Structure
"""
    
    for mg in template['template']['management_groups']:
        hld += f"- **{mg}:** Management group for {mg.lower()} resources\n"
    
    hld += f"""
### Subscription Strategy
"""
    
    for sub in template['template']['subscriptions']:
        hld += f"- **{sub}:** Dedicated subscription for {sub.lower()} workloads\n"
    
    hld += f"""
### Network Architecture
**Topology:** {inputs.network_model or 'Hub-Spoke'}
- **Hub VNet:** Central connectivity and shared services
- **Spoke VNets:** Workload-specific virtual networks
- **Connectivity:** {inputs.connectivity or 'ExpressRoute and VPN Gateway'}

### Security Architecture
**Security Model:** {inputs.security_posture or 'Zero Trust'}
- **Identity:** {inputs.identity or 'Azure Active Directory'} with conditional access
- **Network Security:** Network Security Groups and Azure Firewall
- **Data Protection:** {inputs.key_vault or 'Azure Key Vault'} for secrets management
- **Threat Protection:** {inputs.threat_protection or 'Azure Security Center and Sentinel'}

### Workload Architecture
**Primary Workload:** {inputs.workload or 'Application Services'}
- **Compute:** {AZURE_SERVICES_MAPPING.get(inputs.workload or 'appservices', {'name': 'Azure App Services'})['name']}
- **Architecture Style:** {inputs.architecture_style or 'Microservices'}
- **Scalability:** {inputs.scalability or 'Auto-scaling enabled'}
"""

    # Low Level Design (LLD)
    lld = f"""# Low Level Design (LLD)
## Azure Landing Zone Technical Implementation

**Document Version:** 1.0
**Date:** {timestamp}

### Resource Configuration

#### Management Groups
"""
    
    for i, mg in enumerate(template['template']['management_groups']):
        lld += f"""
**{mg} Management Group:**
- Management Group ID: mg-{mg.lower().replace(' ', '-')}
- Parent: {template['template']['management_groups'][i-1] if i > 0 else 'Tenant Root'}
- Applied Policies: Azure Policy assignments for {mg.lower()}
"""

    lld += f"""
#### Subscriptions
"""
    
    for sub in template['template']['subscriptions']:
        lld += f"""
**{sub} Subscription:**
- Subscription Name: sub-{sub.lower().replace(' ', '-')}
- Resource Groups: Multiple RGs based on workload segregation
- RBAC: Custom roles and assignments
- Budget: Cost management and alerting configured
"""

    lld += f"""
#### Network Configuration

**Hub Virtual Network:**
- VNet Name: vnet-hub-{inputs.network_model or 'spoke'}-001
- Address Space: 10.0.0.0/16
- Subnets:
  - GatewaySubnet: 10.0.0.0/24 (VPN/ExpressRoute Gateway)
  - AzureFirewallSubnet: 10.0.1.0/24 (Azure Firewall)
  - SharedServicesSubnet: 10.0.2.0/24 (Domain Controllers, etc.)

**Spoke Virtual Networks:**
- Production Spoke: vnet-prod-{inputs.workload or 'app'}-001 (10.1.0.0/16)
- Development Spoke: vnet-dev-{inputs.workload or 'app'}-001 (10.2.0.0/16)

#### Security Configuration

**Azure Active Directory:**
- Tenant: {inputs.org_structure or 'enterprise'}.onmicrosoft.com
- Custom Domains: Configured as required
- Conditional Access: {inputs.security_posture or 'Zero Trust'} policies
- PIM: Privileged Identity Management for admin roles

**Network Security:**
- Azure Firewall: Central security appliance
- NSGs: Network Security Groups on all subnets
- UDRs: User Defined Routes for traffic steering

**Key Management:**
- Key Vault: {inputs.key_vault or 'Azure Key Vault'} for certificates and secrets
- Managed Identities: For secure service-to-service authentication

#### Workload Configuration

**Primary Workload: {inputs.workload or 'Application Services'}**
- Service: {AZURE_SERVICES_MAPPING.get(inputs.workload or 'appservices', {'name': 'Azure App Services'})['name']}
- SKU: Production-grade tier
- Scaling: {inputs.scalability or 'Auto-scaling based on CPU/memory'}
- Monitoring: {inputs.monitoring or 'Azure Monitor'} with custom dashboards

#### Operations Configuration

**Monitoring and Alerting:**
- Log Analytics Workspace: Central logging for all resources
- Azure Monitor: Metrics and alerting
- Application Insights: Application performance monitoring

**Backup and Recovery:**
- Azure Backup: {inputs.backup or 'Daily backups with 30-day retention'}
- Site Recovery: Disaster recovery as needed

**Cost Management:**
- Budget Alerts: Monthly budget monitoring
- Cost Optimization: {inputs.cost_priority or 'Regular cost reviews and optimization'}

#### Infrastructure as Code

**IaC Tool:** {inputs.iac or 'Bicep/ARM Templates'}
- Template Structure: Modular templates for each component
- Deployment: CI/CD pipeline using Azure DevOps
- Version Control: Git repository with proper branching strategy
"""

    return {
        "tsd": tsd,
        "hld": hld, 
        "lld": lld
    }


# ---------- API Endpoints ----------

@app.get("/")
def root():
    return {
        "message": "Azure Landing Zone Agent API",
        "version": "1.0.0",
        "endpoints": [
            "/docs - API Documentation",
            "/generate-diagram - Generate architecture diagram (Mermaid + Draw.io)",
            "/generate-azure-diagram - Generate Azure architecture diagram with official Azure icons (Python Diagrams)",
            "/generate-drawio - Generate Draw.io XML",
            "/health - Health check"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate-diagram")
def generate_diagram(inputs: CustomerInputs):
    """Generate comprehensive Azure Landing Zone diagrams and documentation"""
    try:
        # Generate professional diagrams
        mermaid_diagram = generate_professional_mermaid(inputs)
        drawio_xml = generate_enhanced_drawio_xml(inputs)
        
        # Generate professional documentation
        docs = generate_professional_documentation(inputs)
        
        return {
            "success": True,
            "mermaid": mermaid_diagram,
            "drawio": drawio_xml,
            "tsd": docs["tsd"],
            "hld": docs["hld"],
            "lld": docs["lld"],
            "architecture_template": generate_architecture_template(inputs),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "agent": "Azure Landing Zone Agent"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating diagram: {str(e)}")

@app.post("/generate-azure-diagram")
def generate_azure_diagram_endpoint(inputs: CustomerInputs):
    """Generate Azure architecture diagram using Python Diagrams library with proper Azure icons"""
    try:
        # Generate Azure architecture diagram with proper icons
        diagram_path = generate_azure_architecture_diagram(inputs)
        
        # Read the generated PNG file
        with open(diagram_path, "rb") as f:
            diagram_data = f.read()
        
        # Generate professional documentation
        docs = generate_professional_documentation(inputs)
        
        # Encode the diagram as base64 for JSON response
        import base64
        diagram_base64 = base64.b64encode(diagram_data).decode('utf-8')
        
        return {
            "success": True,
            "diagram_path": diagram_path,
            "diagram_base64": diagram_base64,
            "tsd": docs["tsd"],
            "hld": docs["hld"],
            "lld": docs["lld"],
            "architecture_template": generate_architecture_template(inputs),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "agent": "Azure Landing Zone Agent - Python Diagrams",
                "diagram_format": "PNG with Azure official icons"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Azure diagram: {str(e)}")

@app.get("/generate-azure-diagram/download/{filename}")
def download_azure_diagram(filename: str):
    """Download generated Azure architecture diagram PNG file"""
    try:
        file_path = f"/tmp/{filename}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Diagram file not found")
        
        with open(file_path, "rb") as f:
            diagram_data = f.read()
        
        return Response(
            content=diagram_data,
            media_type="image/png", 
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading diagram: {str(e)}")

@app.post("/generate-drawio", response_class=Response)
def generate_drawio_endpoint(inputs: CustomerInputs):
    """Generate Draw.io XML file for download"""
    try:
        xml = generate_enhanced_drawio_xml(inputs)
        return Response(
            content=xml, 
            media_type="application/xml",
            headers={"Content-Disposition": "attachment; filename=azure-landing-zone.drawio"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Draw.io XML: {str(e)}")

@app.get("/templates")
def get_templates():
    """Get available Azure Landing Zone templates"""
    return {
        "templates": AZURE_TEMPLATES,
        "azure_services": AZURE_SERVICES_MAPPING
    }

@app.get("/services")
def get_services():
    """Get available Azure services categorized for form selection"""
    services_by_category = {}
    
    for service_key, service_info in AZURE_SERVICES_MAPPING.items():
        category = service_info["category"]
        if category not in services_by_category:
            services_by_category[category] = []
        
        services_by_category[category].append({
            "key": service_key,
            "name": service_info["name"],
            "icon": service_info["icon"],
            "azure_icon": service_info.get("azure_icon", ""),
        })
    
    return {
        "categories": services_by_category,
        "category_mapping": {
            "compute": "Compute Services",
            "network": "Networking Services", 
            "storage": "Storage Services",
            "database": "Database Services",
            "security": "Security Services",
            "monitoring": "Monitoring Services",
            "ai": "AI & Machine Learning",
            "analytics": "Data & Analytics",
            "integration": "Integration Services",
            "devops": "DevOps & Governance",
            "backup": "Backup & Recovery"
        }
    }
