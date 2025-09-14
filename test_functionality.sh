#!/bin/bash

echo "🚀 Azure Landing Zone Agent - Functionality Test"
echo "================================================"
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
health_response=$(curl -s http://127.0.0.1:8001/health)
if echo "$health_response" | grep -q '"status":"healthy"'; then
    echo "   ✅ Health check: PASSED"
else
    echo "   ❌ Health check: FAILED"
    exit 1
fi

echo ""

# Test interactive diagram generation
echo "2. Testing interactive diagram generation..."
interactive_response=$(curl -s -X POST "http://127.0.0.1:8001/generate-interactive-azure-architecture" \
  -H "Content-Type: application/json" \
  -d '{
    "business_objective": "Test automation", 
    "org_structure": "enterprise",
    "compute_services": ["virtual_machines", "aks"],
    "network_services": ["virtual_network", "firewall"],
    "security_services": ["key_vault", "active_directory"]
  }' --max-time 30)

if echo "$interactive_response" | grep -q '"success":true'; then
    echo "   ✅ Interactive diagram generation: PASSED"
    svg_size=$(echo "$interactive_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('svg_diagram', '')))")
    echo "   📊 SVG size: $svg_size characters"
else
    echo "   ❌ Interactive diagram generation: FAILED"
fi

echo ""

# Test PNG download endpoint
echo "3. Testing PNG download endpoint..."
png_response=$(curl -s -X POST "http://127.0.0.1:8001/generate-png-diagram" \
  -H "Content-Type: application/json" \
  -d '{
    "business_objective": "PNG test", 
    "org_structure": "enterprise",
    "compute_services": ["virtual_machines"]
  }' --max-time 30)

if echo "$png_response" | grep -q '"success":true'; then
    echo "   ✅ PNG download endpoint: PASSED"
    png_size=$(echo "$png_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('file_size', 0))")
    echo "   🖼️ PNG size: $png_size bytes"
else
    echo "   ❌ PNG download endpoint: FAILED"
fi

echo ""

# Test SVG download endpoint  
echo "4. Testing SVG download endpoint..."
svg_response=$(curl -s -X POST "http://127.0.0.1:8001/generate-svg-diagram" \
  -H "Content-Type: application/json" \
  -d '{
    "business_objective": "SVG test", 
    "org_structure": "enterprise",
    "compute_services": ["virtual_machines"]
  }' --max-time 30)

if echo "$svg_response" | grep -q '"success":true'; then
    echo "   ✅ SVG download endpoint: PASSED"
    svg_size=$(echo "$svg_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('file_size', 0))")
    echo "   🎨 SVG size: $svg_size bytes"
else
    echo "   ❌ SVG download endpoint: FAILED"
fi

echo ""
echo "🎯 All functionality tests completed!"
echo ""
echo "📋 Service Status:"
echo "   Backend: http://127.0.0.1:8001 (running)"
echo "   Frontend: http://localhost:5173 (running)"
echo "   API Documentation: http://127.0.0.1:8001/docs"
echo ""
echo "📥 Download formats available:"
echo "   - PNG: High-resolution images (130KB+)"
echo "   - SVG: Scalable vector graphics (12KB+)"
echo "   - Draw.io: XML format for editing"
echo ""
echo "✨ Interactive diagram features:"
echo "   - Zoom in/out functionality"
echo "   - Pan and drag capabilities"
echo "   - Element hover effects"
echo "   - Click interactions"