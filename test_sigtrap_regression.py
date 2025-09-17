#!/usr/bin/env python3
"""
Regression test for Graphviz SIGTRAP error fix

This test ensures that the node size issues that caused SIGTRAP errors
in the Azure Landing Zone diagram generation have been resolved.

Run this test after any changes to the diagram generation code to ensure
the fix remains effective.
"""

import subprocess
import sys
import os
import tempfile
import json

def test_diagram_generation_stability():
    """Test that diagram generation doesn't crash with SIGTRAP errors"""
    
    # Create a minimal test script
    test_script = '''
import sys
sys.path.append("/home/runner/work/LZ-Diagram/LZ-Diagram/backend")
from main import CustomerInputs, generate_azure_architecture_diagram

# Test with complex service configuration
inputs = CustomerInputs(
    org_structure="Test Enterprise Organization",
    primary_workload="complex_enterprise_workloads",
    landing_zone_template="enterprise_scale", 
    region="eastus",
    compute_services=["aks", "app_services", "virtual_machines", "functions"],
    network_services=["virtual_network", "application_gateway", "firewall"],
    storage_services=["storage_accounts", "blob_storage", "data_lake"],
    database_services=["sql_database", "cosmos_db", "redis_cache"],
    security_services=["key_vault", "defender"],
    monitoring_services=["monitor", "log_analytics"],
    integration_services=["api_management", "logic_apps"],
    analytics_services=["synapse", "databricks"]
)

try:
    # Generate PNG diagram
    result = generate_azure_architecture_diagram(inputs, format="png")
    print(f"SUCCESS: Generated {result}")
    exit(0)
except Exception as e:
    print(f"ERROR: {str(e)}")
    exit(1)
'''
    
    # Write test script to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        script_path = f.name
    
    try:
        print("🔍 Running regression test for SIGTRAP error fix...")
        
        # Run the test script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ REGRESSION TEST PASSED")
            print("   Diagram generation completed successfully without SIGTRAP errors")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ REGRESSION TEST FAILED")
            print(f"   Return code: {result.returncode}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ REGRESSION TEST FAILED")
        print("   Test timed out - possible hang or infinite loop")
        return False
    except Exception as e:
        print(f"❌ REGRESSION TEST FAILED")
        print(f"   Exception: {str(e)}")
        return False
    finally:
        # Clean up temporary file
        try:
            os.unlink(script_path)
        except OSError:
            pass

if __name__ == "__main__":
    print("🧪 Graphviz SIGTRAP Error Fix - Regression Test")
    print("=" * 55)
    
    success = test_diagram_generation_stability()
    
    print("\n" + "=" * 55)
    if success:
        print("🎉 All regression tests passed!")
        print("   The SIGTRAP error fix is working correctly.")
    else:
        print("💥 Regression test failed!")
        print("   The SIGTRAP error may have reoccurred.")
    
    sys.exit(0 if success else 1)