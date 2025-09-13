# Azure Landing Zone Agent - Deployment & Troubleshooting Guide

## Quick Health Check

To verify the system is working correctly, check the health endpoint:

```bash
curl http://your-server:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "dependencies": {
    "graphviz_available": true,
    "diagrams_available": true,
    "output_directory_accessible": true,
    "sufficient_disk_space": true
  }
}
```

## Dependencies

### System Requirements
- **Graphviz**: Required for diagram generation
  ```bash
  sudo apt-get update
  sudo apt-get install -y graphviz graphviz-dev
  ```

### Python Dependencies
Install from `backend/requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

## Common Issues & Solutions

### 1. "Graphviz not available" Error
**Symptoms**: Health check shows `graphviz_available: false`

**Solution**: Install Graphviz system package
```bash
sudo apt-get install -y graphviz graphviz-dev
# Verify installation
dot -V
```

### 2. "Output directory not accessible" Error
**Symptoms**: Health check shows `output_directory_accessible: false`

**Solution**: The system tries multiple directories in order:
1. `/tmp` (preferred)
2. System temporary directory
3. `~/tmp` (user home)
4. `./tmp` (current directory)

Ensure at least one is writable by the application user.

### 3. "Low disk space" Warning
**Symptoms**: Health check shows `sufficient_disk_space: false`

**Solution**: Free up space in the output directory. The system automatically cleans up files older than 24 hours.

### 4. Input Validation Errors (HTTP 400)
**Symptoms**: "Invalid input" errors

**Common causes**:
- Text fields longer than 1000 characters
- More than 50 services selected in any category

**Solution**: Reduce input size or contact administrator to adjust limits.

### 5. Performance Issues
**Symptoms**: Slow response times or timeouts

**Solutions**:
- Check disk space and I/O performance
- Monitor system memory usage during diagram generation
- Consider increasing timeout values for complex diagrams
- Review server logs for specific performance bottlenecks

## Monitoring & Logging

### Application Logs
The application uses structured logging with these levels:
- `INFO`: Normal operation steps
- `ERROR`: Errors that need attention
- `WARNING`: Issues that don't stop operation

Key log messages to monitor:
- "Starting comprehensive Azure architecture generation"
- "Diagram generated successfully"
- "Failed to generate Azure architecture diagram"

### Health Monitoring
Set up regular health checks:
```bash
#!/bin/bash
HEALTH_URL="http://localhost:8001/health"
RESPONSE=$(curl -s "$HEALTH_URL")
STATUS=$(echo "$RESPONSE" | jq -r '.status')

if [ "$STATUS" != "healthy" ]; then
    echo "ALERT: Service health check failed"
    echo "$RESPONSE"
    # Send alert notification
fi
```

## Performance Optimization

### Recommended Settings
- **Timeout**: Set client timeouts to at least 60 seconds for complex diagrams
- **Concurrency**: The system handles concurrent requests well, but limit to avoid resource exhaustion
- **Memory**: Allocate at least 1GB RAM for complex enterprise architectures
- **Disk**: Ensure 1GB+ free space in output directory

### Cleanup Maintenance
The system automatically cleans up old files, but you can also run manual cleanup:
```bash
find /tmp -name "azure_landing_zone_*.png" -mtime +1 -delete
```

## Troubleshooting Commands

### Test Basic Functionality
```bash
# Test health
curl http://localhost:8001/health

# Test simple generation
curl -X POST http://localhost:8001/generate-comprehensive-azure-architecture \
  -H "Content-Type: application/json" \
  -d '{"business_objective": "Test", "org_structure": "enterprise"}'
```

### Check Dependencies
```bash
# Verify Graphviz
dot -V

# Check Python imports
python -c "from diagrams import Diagram; print('Diagrams library OK')"

# Check output directory
python -c "
import sys
sys.path.append('backend')
from main import get_safe_output_directory
print(f'Output directory: {get_safe_output_directory()}')
"
```

### Debug Mode
For detailed debugging, run with reload and debug logging:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

## Contact & Support

If issues persist after following this guide:
1. Check the application logs for specific error messages
2. Verify all dependencies are properly installed
3. Test with the troubleshooting commands above
4. Review the health check endpoint output

The improvements made ensure better error reporting and logging, making it easier to diagnose and resolve issues.