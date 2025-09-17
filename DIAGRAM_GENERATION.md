# Azure Landing Zone Agent - Enhanced Diagram Generation

## Overview

The Azure Landing Zone Agent now supports **enterprise-grade Azure architecture diagrams** following 50+ design principles with official Microsoft Azure icons and stencils. This addresses the previous limitation where diagrams used emoji icons instead of proper Azure architectural styling.

## Enhanced Diagram Generation (RECOMMENDED) 

**Endpoint:** `POST /generate-azure-diagram`

### 🎯 Enterprise Architecture Principles (50+ Implemented)

**Visual Hierarchy & Layout (1-10)**
- ✅ Clear containers/swimlanes with distinct logical layers
- ✅ Minimal crossing connections with polyline routing  
- ✅ Proper visual hierarchy: Internet Edge → Identity/Security → Network/Apps → Data
- ✅ Enhanced cluster styling with bordered boxes and gradient backgrounds
- ✅ Clear region separation between Active and Standby regions

**Workflow & Connectivity (11-20)**  
- ✅ Numbered workflow steps (1. Internet → 2. Front Door → 3. App Service → 4. Database)
- ✅ Clear connection labeling with descriptive labels for all connection types
- ✅ All specified components: Front Door, Queue Storage, Table Storage, Redis
- ✅ Line type distinctions: solid (primary), dashed (governance), dotted (monitoring)
- ✅ Directional clarity with single/bidirectional connections

**Security & Environment (21-30)**
- ✅ Security zone shading (Untrusted: Red, Semi-trusted: Green, Trusted: Blue)
- ✅ Environment labeling: DEV, UAT, PROD, DR with consistent color codes
- ✅ High Availability indicators (Active-Active, Active-Passive annotations)
- ✅ Monitoring/observability overlay with Log Analytics, Azure Monitor, Sentinel
- ✅ Disaster recovery separation with dotted borders and labels

**Legend & Standards (31-40)**
- ✅ Comprehensive legend covering line types, clusters, icons, security zones
- ✅ Standardized iconography using latest official Azure icons consistently
- ✅ Annotation minimization with callouts instead of cluttered text
- ✅ Cloud-native vs. legacy differentiation (PaaS vs. IaaS)
- ✅ Service tier notation (Basic/Standard/Premium) for databases

**Advanced Enterprise Features (41-50)**
- ✅ Scalability indicators with auto-scaling symbols
- ✅ Compliance/regulatory overlays (GDPR, HIPAA zones)
- ✅ Cost management integration with budget alerts and optimization
- ✅ Identity & access clarity with Azure AD, RBAC, Conditional Access
- ✅ Backup & recovery overlay with cross-region replication arrows
- ✅ Enhanced readability with improved spacing, sizing, and layout constraints

### 🔧 Technical Features

**Enhanced Rendering:**
- Uses the Python Diagrams library (https://diagrams.mingrammer.com)
- Official Azure node components for all service categories
- Professional clustering and visual hierarchy
- High-resolution output (300 DPI) for presentations
- Both PNG and SVG format support

**Enterprise Styling:**
- Proper enterprise architectural styling following Microsoft CAF/WAF standards
- Color-coded security zones with proper ranking and positioning
- Professional font rendering (Arial, sans-serif)
- Optimal spacing and layout constraints for readability

### 📋 Legacy Options (Still Available)

**Mermaid Diagrams:** `POST /generate-diagram` - Text-based diagrams with emoji icons
**Draw.io XML:** `POST /generate-drawio` - XML format for Draw.io editor

> **Note:** These legacy options are maintained for backward compatibility but do not include the enhanced 50+ enterprise architecture principles. Use the enhanced diagram generation for professional enterprise architectures.

## API Usage

### Generate Azure Architecture Diagram

```bash
curl -X POST "http://localhost:8000/generate-azure-diagram" \
  -H "Content-Type: application/json" \
  -d '{
    "business_objective": "Enterprise cloud transformation",
    "org_structure": "Enterprise",
    "network_model": "hub-spoke",
    "security_posture": "zero-trust",
    "compute_services": ["virtual_machines", "aks", "app_services"],
    "network_services": ["virtual_network", "firewall", "application_gateway"],
    "storage_services": ["storage_accounts", "blob_storage"],
    "database_services": ["sql_database", "cosmos_db"],
    "security_services": ["key_vault", "active_directory", "security_center"],
    "analytics_services": ["synapse", "data_factory"],
    "integration_services": ["logic_apps", "api_management"],
    "devops_services": ["devops"]
  }'
```

### Response Format

```json
{
  "success": true,
  "diagram_path": "/tmp/azure_landing_zone_20240912_120000.png",
  "diagram_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "tsd": "# Technical Specification Document...",
  "hld": "# High Level Design...",
  "lld": "# Low Level Design...",
  "architecture_template": {...},
  "metadata": {
    "generated_at": "2024-09-12T12:00:00.000000",
    "version": "1.0.0",
    "agent": "Azure Landing Zone Agent - Python Diagrams",
    "diagram_format": "PNG with Azure official icons"
  }
}
```

## Dependencies

The new functionality requires:

- `diagrams==0.23.4` - Python Diagrams library
- `graphviz==0.20.1` - Python Graphviz wrapper  
- System Graphviz installation (`apt-get install graphviz graphviz-dev`)

## Azure Service Support

The system supports official Azure icons for:

- **Compute:** Virtual Machines, AKS, App Services, Functions, Container Instances
- **Network:** Virtual Networks, Firewall, Application Gateway, Load Balancers, VPN Gateway
- **Storage:** Storage Accounts, Blob Storage, Data Lake Storage
- **Database:** SQL Database, Cosmos DB, MySQL, PostgreSQL
- **Security:** Key Vault, Active Directory, Security Center, Sentinel
- **Analytics:** Synapse Analytics, Data Factory, Databricks, Stream Analytics
- **Integration:** Logic Apps, Service Bus, Event Grid, API Management
- **DevOps:** Azure DevOps, Pipelines

## Visual Improvements

**Before (Old Approach):**
- Emoji icons: 🖥️ ☸️ 🌐 🛡️ 🔐
- Basic text-based diagrams
- Limited visual hierarchy

**After (New Approach):**
- Official Microsoft Azure icons
- Professional enterprise styling
- Proper color coding and visual hierarchy
- Industry-standard architectural diagrams
- High-quality PNG rendering

## File Output

Generated diagrams are saved as PNG files with:
- High resolution for professional presentations
- Proper Azure branding and styling
- File sizes typically 150-300KB
- Suitable for documentation and architecture reviews

## Troubleshooting

### Draw.io XML Issues

**Problem**: "Not a diagram file (error on line 1 at column 1: Start tag expected, '<' not found)" when uploading to app.diagrams.net

**Solution**: This issue was resolved in version 1.0.0. The problem was caused by emoji characters being used as shape names in the XML (e.g., `shape=mxgraph.azure.☸️`). The fix replaced emoji icons with valid Draw.io shape names (e.g., `shape=mxgraph.azure.kubernetes_service`).

**Testing**: To verify your generated .drawio file is valid:
```bash
# Test with AKS workload
curl -X POST http://localhost:8001/generate-drawio \
  -H "Content-Type: application/json" \
  -d '{"workload": "aks"}' \
  --output diagram.drawio

# Verify XML structure
python3 -c "import xml.etree.ElementTree as ET; ET.parse('diagram.drawio'); print('✅ Valid XML')"
```

The generated XML should contain proper shape references like:
- `shape=mxgraph.azure.kubernetes_service` ✅
- NOT `shape=mxgraph.azure.☸️` ❌