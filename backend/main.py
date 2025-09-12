from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import html
import json
import uuid
from datetime import datetime

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
    
    # Workloads & Applications
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
    "aks": {"name": "Azure Kubernetes Service", "icon": "azure.kubernetes_services", "category": "compute"},
    "appservices": {"name": "Azure App Services", "icon": "azure.app_services", "category": "compute"},
    "vm": {"name": "Virtual Machines", "icon": "azure.virtual_machine", "category": "compute"},
    "sap": {"name": "SAP on Azure", "icon": "azure.sap_hana_on_azure", "category": "compute"},
    "functions": {"name": "Azure Functions", "icon": "azure.azure_functions", "category": "compute"},
    "batch": {"name": "Azure Batch", "icon": "azure.batch", "category": "compute"},
    "service_fabric": {"name": "Service Fabric", "icon": "azure.service_fabric", "category": "compute"},
    
    # Storage Services
    "storage": {"name": "Azure Storage", "icon": "azure.azure_storage", "category": "storage"},
    "blob_storage": {"name": "Blob Storage", "icon": "azure.blob_storage", "category": "storage"},
    "file_storage": {"name": "File Storage", "icon": "azure.file_storage", "category": "storage"},
    "disk_storage": {"name": "Disk Storage", "icon": "azure.disk_storage", "category": "storage"},
    
    # Database Services
    "sql_database": {"name": "SQL Database", "icon": "azure.sql_database", "category": "database"},
    "cosmos_db": {"name": "Cosmos DB", "icon": "azure.cosmos_db", "category": "database"},
    "mysql": {"name": "MySQL Database", "icon": "azure.mysql_database", "category": "database"},
    "postgresql": {"name": "PostgreSQL Database", "icon": "azure.postgresql_database", "category": "database"},
    
    # AI/ML Services
    "ai": {"name": "Azure AI/ML", "icon": "azure.machine_learning", "category": "ai"},
    "cognitive_services": {"name": "Cognitive Services", "icon": "azure.cognitive_services", "category": "ai"},
    "bot_service": {"name": "Bot Service", "icon": "azure.bot_service", "category": "ai"},
    
    # Data & Analytics
    "data": {"name": "Azure Data Services", "icon": "azure.data_factory", "category": "data"},
    "synapse": {"name": "Azure Synapse", "icon": "azure.synapse_analytics", "category": "data"},
    "databricks": {"name": "Azure Databricks", "icon": "azure.databricks", "category": "data"},
    "stream_analytics": {"name": "Stream Analytics", "icon": "azure.stream_analytics", "category": "data"},
    
    # Network Services
    "hub-spoke": {"name": "Hub-Spoke Network", "icon": "azure.virtual_network", "category": "network"},
    "mesh": {"name": "Mesh Network", "icon": "azure.virtual_network", "category": "network"},
    "vwan": {"name": "Virtual WAN", "icon": "azure.virtual_wan", "category": "network"},
    "load_balancer": {"name": "Load Balancer", "icon": "azure.load_balancer", "category": "network"},
    "application_gateway": {"name": "Application Gateway", "icon": "azure.application_gateway", "category": "network"},
    "firewall": {"name": "Azure Firewall", "icon": "azure.firewall", "category": "network"},
    "vpn_gateway": {"name": "VPN Gateway", "icon": "azure.vpn_gateway", "category": "network"},
    
    # Security Services
    "zero-trust": {"name": "Zero Trust Security", "icon": "azure.security_center", "category": "security"},
    "siem": {"name": "Azure Sentinel", "icon": "azure.sentinel", "category": "security"},
    "key_vault": {"name": "Key Vault", "icon": "azure.key_vault", "category": "security"},
    "azure_ad": {"name": "Azure Active Directory", "icon": "azure.azure_active_directory", "category": "security"},
    
    # Monitoring & Management
    "monitor": {"name": "Azure Monitor", "icon": "azure.monitor", "category": "management"},
    "log_analytics": {"name": "Log Analytics", "icon": "azure.log_analytics", "category": "management"},
    "application_insights": {"name": "Application Insights", "icon": "azure.application_insights", "category": "management"},
    
    # Integration Services
    "logic_apps": {"name": "Logic Apps", "icon": "azure.logic_apps", "category": "integration"},
    "service_bus": {"name": "Service Bus", "icon": "azure.service_bus", "category": "integration"},
    "event_grid": {"name": "Event Grid", "icon": "azure.event_grid", "category": "integration"},
}

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
    workload = inputs.workload or "appservices"
    
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
    
    # Add network topology
    if network_model == "hub-spoke":
        lines.extend([
            "        subgraph \"Hub-Spoke Network\"",
            "            HUB[\"🌐 Hub VNet<br/>Shared Services\"]",
            "            SPOKE1[\"🏷️ Spoke VNet 1<br/>Production\"]",
            "            SPOKE2[\"🏷️ Spoke VNet 2<br/>Development\"]",
            "            CONN --> HUB",
            "            HUB --> SPOKE1",
            "            HUB --> SPOKE2",
            "        end"
        ])
    elif network_model == "vwan":
        lines.extend([
            "        subgraph \"Virtual WAN\"",
            "            VWAN[\"🌐 Virtual WAN Hub\"]",
            "            VPNGW[\"🔐 VPN Gateway\"]",
            "            ERGW[\"⚡ ExpressRoute Gateway\"]", 
            "            CONN --> VWAN",
            "            VWAN --> VPNGW",
            "            VWAN --> ERGW",
            "        end"
        ])
    
    # Add workload specific components
    workload_name = AZURE_SERVICES_MAPPING.get(workload, {"name": workload})["name"]
    lines.extend([
        "        subgraph \"Workloads\"",
        f"            WORKLOAD[\"{workload_name}\"]",
        "            PROD --> WORKLOAD",
        "        end"
    ])
    
    # Add security and governance
    lines.extend([
        "        subgraph \"Security & Governance\"",
        "            AAD[\"🔐 Azure Active Directory\"]",
        "            POLICY[\"📋 Azure Policy\"]",
        "            MONITOR[\"📊 Azure Monitor\"]",
        "            KEYVAULT[\"🔑 Key Vault\"]",
        "            SECURITY[\"🛡️ Security Center\"]",
        "            IDENTITY --> AAD",
        "            MGMT --> POLICY",
        "            MGMT --> MONITOR",
        "            MGMT --> SECURITY",
        "        end"
    ])
    
    lines.append("    end")
    
    # Add styling
    lines.extend([
        "",
        "    classDef mgmtGroup fill:#e1f5fe,stroke:#01579b,stroke-width:2px;",
        "    classDef subscription fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;", 
        "    classDef network fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px;",
        "    classDef workload fill:#fff3e0,stroke:#e65100,stroke-width:2px;",
        "    classDef security fill:#ffebee,stroke:#b71c1c,stroke-width:2px;",
        "",
        "    class ROOT,PLATFORM,LANDINGZONES,SANDBOX,DECOM,WORKLOADS mgmtGroup;",
        "    class CONN,IDENTITY,MGMT,PROD,DEV subscription;",
        "    class HUB,SPOKE1,SPOKE2,VWAN,VPNGW,ERGW network;",
        "    class WORKLOAD workload;",
        "    class AAD,POLICY,MONITOR,KEYVAULT,SECURITY security;"
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
        <mxCell id="security" value="Security & Governance" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcccc;strokeColor=#ff6666;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;" vertex="1" parent="1">
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
            "/generate-diagram - Generate architecture diagram",
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
