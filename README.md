# Azure Landing Zone Agent

Professional Azure Landing Zone Architecture Generator that creates comprehensive diagrams and documentation.

## Features

- **Enterprise-Grade Diagrams**: Generate Azure architecture diagrams with official Microsoft Azure icons
- **Multiple Output Formats**: PNG diagrams with Python Diagrams library and Draw.io XML
- **Professional Documentation**: Technical Specification Document (TSD), High-Level Design (HLD), and Low-Level Design (LLD)
- **Architecture Variety**: Support for multiple Azure architecture patterns and templates
- **API-Driven**: RESTful API with comprehensive endpoints

## System Requirements

### Backend Dependencies

#### System Packages (Required)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y graphviz graphviz-dev

# RedHat/CentOS/Fedora
sudo yum install graphviz graphviz-devel
# or with dnf
sudo dnf install graphviz graphviz-devel

# macOS
brew install graphviz
```

#### Python Dependencies
```bash
cd backend
pip3 install -r requirements.txt
```

The required Python packages include:
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `diagrams==0.23.4` - Azure diagram generation
- `graphviz==0.20.1` - Python Graphviz wrapper

### Frontend Dependencies
```bash
cd frontend
npm install
```

## Quick Start

### Backend Server
```bash
cd backend
python3 -m uvicorn main:app --reload --port 8001
```

### Frontend Development Server
```bash
cd frontend
npm run dev
```

The application will be available at:
- Backend API: http://127.0.0.1:8001
- Frontend UI: http://localhost:5173
- API Documentation: http://127.0.0.1:8001/docs

## API Endpoints

### Health Check
```bash
GET /health
```
Comprehensive health check that verifies system dependencies including Graphviz availability.

### Generate Architecture
```bash
POST /generate-comprehensive-azure-architecture
```
Generate comprehensive Azure architecture with both Draw.io XML and PNG diagrams.

### Test Architecture Variety
```bash
POST /test-architecture-variety
```
Generate multiple different architecture patterns to test variety and ensure different diagrams are created.

## Troubleshooting

### Common Issues

#### 500 Internal Server Error
**Most Common Cause**: Missing Graphviz system dependencies

**Solution**:
```bash
# Install Graphviz system packages
sudo apt-get install -y graphviz graphviz-dev

# Verify installation
dot -V
```

#### Diagram Generation Fails
**Possible Causes**:
- Graphviz not installed
- `/tmp` directory not writable
- Python diagrams library not installed

**Verification**:
```bash
# Check health endpoint
curl http://127.0.0.1:8001/health

# Expected healthy response:
{
  "status": "healthy",
  "timestamp": "2025-09-12T16:27:31.201515",
  "issues": [],
  "dependencies": {
    "graphviz_available": true,
    "diagrams_available": true,
    "tmp_writable": true
  }
}
```

#### Draw.io XML Issues
**Problem**: "Not a diagram file" error when uploading to app.diagrams.net

**Solution**: Ensure you're using the latest version. Previous versions had emoji characters in XML shape names that have been fixed in v1.0.0.

## Architecture Support

The system supports comprehensive Azure services including:

- **Compute**: Virtual Machines, AKS, App Services, Functions, Container Instances
- **Network**: Virtual Networks, Firewall, Application Gateway, Load Balancers, VPN Gateway
- **Storage**: Storage Accounts, Blob Storage, Data Lake Storage
- **Database**: SQL Database, Cosmos DB, MySQL, PostgreSQL
- **Security**: Key Vault, Active Directory, Security Center, Sentinel
- **Analytics**: Synapse Analytics, Data Factory, Databricks, Stream Analytics
- **Integration**: Logic Apps, Service Bus, Event Grid, API Management
- **DevOps**: Azure DevOps, Pipelines

## File Output

Generated files are saved in the `/tmp` directory:
- PNG diagrams: High-quality architecture diagrams with official Azure icons
- Draw.io XML: Compatible with app.diagrams.net for editing
- Documentation: TSD, HLD, and LLD in structured format

For more details about diagram generation, see [DIAGRAM_GENERATION.md](DIAGRAM_GENERATION.md).