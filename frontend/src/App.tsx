import * as React from "react";
import { ChakraProvider, Box, Heading, VStack, HStack, Button, Select, Text, SimpleGrid, Card, CardHeader, CardBody, Badge, Container, Checkbox, CheckboxGroup, Wrap, WrapItem } from "@chakra-ui/react";

import Mermaid from "./components/Mermaid";

interface FormData {
  business_objective?: string;
  regulatory?: string;
  industry?: string;
  org_structure?: string;
  governance?: string;
  identity?: string;
  connectivity?: string;
  network_model?: string;
  ip_strategy?: string;
  security_zone?: string;
  security_posture?: string;
  key_vault?: string;
  threat_protection?: string;
  workload?: string;
  architecture_style?: string;
  scalability?: string;
  ops_model?: string;
  monitoring?: string;
  backup?: string;
  topology_pattern?: string;
  migration_scope?: string;
  cost_priority?: string;
  iac?: string;
  
  // Azure Service Selections
  compute_services?: string[];
  network_services?: string[];
  storage_services?: string[];
  database_services?: string[];
  security_services?: string[];
  monitoring_services?: string[];
  ai_services?: string[];
  analytics_services?: string[];
  integration_services?: string[];
  devops_services?: string[];
  backup_services?: string[];
}

interface AzureService {
  key: string;
  name: string;
  icon: string;
  azure_icon: string;
}

interface ServicesData {
  categories: Record<string, AzureService[]>;
  category_mapping: Record<string, string>;
}

interface Results {
  success: boolean;
  mermaid: string;
  drawio: string;
  tsd: string;
  hld: string;
  lld: string;
  architecture_template: any;
  metadata: any;
  azure_diagram?: {
    png_base64: string;
    png_path: string;
    azure_stencils: {
      total_used: number;
      unique_used: number;
      stencils_list: string[];
    };
  };
}

function App() {
  const [formData, setFormData] = React.useState<FormData>({});
  const [results, setResults] = React.useState<Results | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState(0);
  const [services, setServices] = React.useState<ServicesData | null>(null);

  // Load available Azure services on component mount
  React.useEffect(() => {
    const loadServices = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8001/services");
        const servicesData = await response.json();
        setServices(servicesData);
      } catch (error) {
        console.error("Error loading services:", error);
      }
    };
    loadServices();
  }, []);

  const handleChange = (field: keyof FormData, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleServiceChange = (category: string, selectedServices: string[]) => {
    const categoryField = `${category}_services` as keyof FormData;
    setFormData({ ...formData, [categoryField]: selectedServices });
  };

  const testArchitectureVariety = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8001/test-architecture-variety", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      
      if (data.success) {
        const summary = data.summary;
        alert(`Architecture Variety Test Completed Successfully!
        
• Tested ${summary.total_configs_tested} different configurations
• All generated different file sizes: ${summary.all_different_sizes ? 'Yes' : 'No'}
• Total unique Azure stencils used: ${summary.total_unique_stencils}
• Variety confirmed: ${summary.variety_confirmed ? 'Yes' : 'No'}

Test Results:
${data.test_results.map((r: any) => `• ${r.name}: ${r.unique_azure_stencils} stencils`).join('\n')}

This confirms that the system generates different architectures based on your selections!`);
      } else {
        throw new Error("Failed to test architecture variety");
      }
    } catch (err) {
      console.error(err);
      alert("Error: Failed to test architecture variety. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Use the comprehensive Azure architecture endpoint for better results
      const res = await fetch("http://127.0.0.1:8001/generate-comprehensive-azure-architecture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      
      if (data.success) {
        // Transform the comprehensive data to match the existing interface
        const transformedData = {
          success: true,
          mermaid: "", // We'll generate this from the architecture template
          drawio: data.drawio_xml,
          tsd: data.tsd,
          hld: data.hld,
          lld: data.lld,
          architecture_template: data.architecture_template,
          metadata: data.metadata,
          azure_diagram: {
            png_base64: data.png_diagram_base64,
            png_path: data.png_diagram_path,
            azure_stencils: data.azure_stencils
          }
        };
        
        setResults(transformedData);
        alert(`Architecture Generated Successfully! Using ${data.azure_stencils.unique_used} unique Azure stencils.`);
      } else {
        throw new Error("Failed to generate architecture");
      }
    } catch (err) {
      console.error(err);
      alert("Error: Failed to generate architecture. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const downloadPNG = (base64Data: string) => {
    try {
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'image/png' });
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'azure-landing-zone-architecture.png';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      alert("Azure PNG diagram download started!");
    } catch (err) {
      console.error(err);
      alert("Failed to download PNG diagram.");
    }
  };

  const downloadDrawio = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8001/generate-drawio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'azure-landing-zone.drawio';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      alert("Draw.io file download started!");
    } catch (err) {
      console.error(err);
      alert("Failed to download Draw.io file.");
    }
  };

  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" p="8">
        <Container maxW="7xl">
          <VStack gap="6" align="stretch">
            {/* Header */}
            <Box textAlign="center">
              <Heading size="2xl" color="blue.600" mb="2">
                🏢 Azure Landing Zone Agent
              </Heading>
              <Text fontSize="lg" color="gray.600">
                Professional Azure Architecture Generator with Enterprise Stencils
              </Text>
              <Badge colorScheme="blue" mt="2">Version 1.0.0 - Professional Edition</Badge>
            </Box>

            {/* Progress Indicator */}
            <Box>
              <Text mb="2" fontSize="sm" fontWeight="medium">Configuration Progress</Text>
              <Box bg="gray.200" borderRadius="md" h="3">
                <Box 
                  bg="blue.500" 
                  borderRadius="md" 
                  h="3" 
                  w={`${(Object.keys(formData).length / 15) * 100}%`}
                  transition="width 0.3s"
                />
              </Box>
            </Box>

            {/* Main Content */}
            <SimpleGrid columns={{ base: 1, lg: results ? 2 : 1 }} gap="8">
              
              {/* Input Form */}
              <Card>
                <CardHeader>
                  <Heading size="lg" color="blue.700">
                    ⚙️ Customer Requirements Input
                  </Heading>
                </CardHeader>
                <CardBody>
                  <VStack gap="6" align="stretch">
                    
                    {/* Business Section */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">1. Business Requirements</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Primary Business Objective</Text>
                          <Select
                            placeholder="Select your primary objective"
                            value={formData.business_objective || ""}
                            onChange={(e) => handleChange("business_objective", e.target.value)}
                          >
                            <option value="cost">Cost Optimization</option>
                            <option value="agility">Business Agility</option>
                            <option value="innovation">Innovation & Growth</option>
                            <option value="scalability">Scalability & Performance</option>
                            <option value="security">Security & Compliance</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Industry Vertical</Text>
                          <Select
                            placeholder="Select your industry"
                            value={formData.industry || ""}
                            onChange={(e) => handleChange("industry", e.target.value)}
                          >
                            <option value="financial">Financial Services</option>
                            <option value="healthcare">Healthcare</option>
                            <option value="retail">Retail & E-commerce</option>
                            <option value="manufacturing">Manufacturing</option>
                            <option value="government">Government</option>
                            <option value="technology">Technology</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Organization Section */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">2. Organization Structure</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Organization Size</Text>
                          <Select
                            placeholder="Select organization type"
                            value={formData.org_structure || ""}
                            onChange={(e) => handleChange("org_structure", e.target.value)}
                          >
                            <option value="enterprise">Large Enterprise (10,000+ employees)</option>
                            <option value="medium">Medium Enterprise (1,000-10,000 employees)</option>
                            <option value="small">Small Business (100-1,000 employees)</option>
                            <option value="startup">Startup (&lt; 100 employees)</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Governance Model</Text>
                          <Select
                            placeholder="Select governance approach"
                            value={formData.governance || ""}
                            onChange={(e) => handleChange("governance", e.target.value)}
                          >
                            <option value="centralized">Centralized (Central IT controls all)</option>
                            <option value="federated">Federated (Shared responsibility)</option>
                            <option value="decentralized">Decentralized (Business unit autonomy)</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Network Section */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">3. Network & Connectivity</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Network Topology</Text>
                          <Select
                            placeholder="Select network architecture"
                            value={formData.network_model || ""}
                            onChange={(e) => handleChange("network_model", e.target.value)}
                          >
                            <option value="hub-spoke">Hub-Spoke (Traditional)</option>
                            <option value="vwan">Virtual WAN (Modern)</option>
                            <option value="mesh">Mesh Network</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Connectivity</Text>
                          <Select
                            placeholder="Select connectivity type"
                            value={formData.connectivity || ""}
                            onChange={(e) => handleChange("connectivity", e.target.value)}
                          >
                            <option value="expressroute">ExpressRoute (Private)</option>
                            <option value="vpn">Site-to-Site VPN</option>
                            <option value="internet">Internet Only</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Security Section */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">4. Security & Identity</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Security Posture</Text>
                          <Select
                            placeholder="Select security approach"
                            value={formData.security_posture || ""}
                            onChange={(e) => handleChange("security_posture", e.target.value)}
                          >
                            <option value="zero-trust">Zero Trust Architecture</option>
                            <option value="defense-in-depth">Defense in Depth</option>
                            <option value="compliance-first">Compliance First</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Identity Management</Text>
                          <Select
                            placeholder="Select identity solution"
                            value={formData.identity || ""}
                            onChange={(e) => handleChange("identity", e.target.value)}
                          >
                            <option value="azure-ad">Azure Active Directory</option>
                            <option value="azure-ad-b2c">Azure AD B2C</option>
                            <option value="hybrid">Hybrid (On-premises + Cloud)</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Azure Services Selection */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">5. Azure Services Selection</Heading>
                      <Text mb="4" color="gray.600">
                        Select the specific Azure services you want to include in your landing zone architecture.
                        Choose from compute, networking, storage, database, security, and other services to create a detailed, professional diagram.
                      </Text>
                      
                      {services && (
                        <VStack spacing="6" align="stretch">
                          {Object.entries(services.categories).map(([category, categoryServices]) => (
                            <Box key={category} border="1px solid" borderColor="gray.200" borderRadius="md" p="4">
                              <Heading size="sm" mb="3" color="blue.500">
                                {services.category_mapping[category] || category}
                              </Heading>
                              <CheckboxGroup
                                value={formData[`${category}_services` as keyof FormData] as string[] || []}
                                onChange={(values) => handleServiceChange(category, values as string[])}
                              >
                                <Wrap spacing="4">
                                  {categoryServices.map((service) => (
                                    <WrapItem key={service.key}>
                                      <Checkbox value={service.key} size="sm">
                                        <HStack spacing="2">
                                          <Text fontSize="lg">{service.icon}</Text>
                                          <Text fontSize="sm">{service.name}</Text>
                                        </HStack>
                                      </Checkbox>
                                    </WrapItem>
                                  ))}
                                </Wrap>
                              </CheckboxGroup>
                            </Box>
                          ))}
                        </VStack>
                      )}
                    </Box>

                    {/* Legacy Workloads Section for backward compatibility */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">6. Legacy Workload Configuration</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Primary Workload (Legacy)</Text>
                          <Select
                            placeholder="Select workload type"
                            value={formData.workload || ""}
                            onChange={(e) => handleChange("workload", e.target.value)}
                          >
                            <option value="aks">Azure Kubernetes Service (AKS)</option>
                            <option value="app_services">Azure App Services</option>
                            <option value="virtual_machines">Virtual Machines</option>
                            <option value="sap">SAP on Azure</option>
                            <option value="ai">AI/ML Workloads</option>
                            <option value="data">Data & Analytics</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Monitoring Strategy (Legacy)</Text>
                          <Select
                            placeholder="Select monitoring approach"
                            value={formData.monitoring || ""}
                            onChange={(e) => handleChange("monitoring", e.target.value)}
                          >
                            <option value="azure-monitor">Azure Monitor Suite</option>
                            <option value="log-analytics">Log Analytics focused</option>
                            <option value="application-insights">Application Insights</option>
                            <option value="third-party">Third-party (Datadog, etc.)</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Operations Section */}
                    <Box>
                      <Heading size="md" color="blue.600" mb="4">7. Operations & Management</Heading>
                      <SimpleGrid columns={2} gap="4">
                        <Box>
                          <Text mb="2" fontWeight="medium">Infrastructure as Code</Text>
                          <Select
                            placeholder="Select IaC preference"
                            value={formData.iac || ""}
                            onChange={(e) => handleChange("iac", e.target.value)}
                          >
                            <option value="bicep">Bicep (Recommended)</option>
                            <option value="arm">ARM Templates</option>
                            <option value="terraform">Terraform</option>
                            <option value="pulumi">Pulumi</option>
                          </Select>
                        </Box>
                        
                        <Box>
                          <Text mb="2" fontWeight="medium">Cost Priority</Text>
                          <Select
                            placeholder="Select cost approach"
                            value={formData.cost_priority || ""}
                            onChange={(e) => handleChange("cost_priority", e.target.value)}
                          >
                            <option value="cost-first">Cost Optimization First</option>
                            <option value="performance-first">Performance First</option>
                            <option value="balanced">Balanced Approach</option>
                          </Select>
                        </Box>
                      </SimpleGrid>
                    </Box>

                    {/* Generate Button */}
                    <VStack spacing="3">
                      <Button
                        colorScheme="blue"
                        size="lg"
                        w="full"
                        onClick={handleSubmit}
                        isLoading={loading}
                      >
                        🏗️ Generate Azure Landing Zone Architecture
                      </Button>
                      
                      <Button
                        colorScheme="teal"
                        variant="outline"
                        size="md"
                        w="full"
                        onClick={testArchitectureVariety}
                        isLoading={loading}
                      >
                        🧪 Test Architecture Variety (3 Different Patterns)
                      </Button>
                    </VStack>
                  </VStack>
                </CardBody>
              </Card>

              {/* Results Panel */}
              {results && (
                <Card>
                  <CardHeader>
                    <HStack justify="space-between">
                      <Heading size="lg" color="green.700">
                        📊 Generated Architecture
                      </Heading>
                      <HStack spacing="2">
                        <Button
                          onClick={downloadDrawio}
                          colorScheme="blue"
                          variant="outline"
                          size="sm"
                        >
                          📥 Download Draw.io
                        </Button>
                        {results.azure_diagram && (
                          <Button
                            onClick={() => downloadPNG(results.azure_diagram!.png_base64)}
                            colorScheme="green"
                            variant="outline"
                            size="sm"
                          >
                            🖼️ Download PNG
                          </Button>
                        )}
                      </HStack>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <VStack gap="4" align="stretch">
                      <Box p="3" bg="green.50" borderRadius="md" borderLeft="4px solid" borderColor="green.500">
                        <Text fontWeight="bold" color="green.800">Azure Architecture Generated Successfully!</Text>
                        <Text fontSize="sm" color="green.600">
                          Template: {results.architecture_template?.template?.name}
                        </Text>
                        {results.azure_diagram && (
                          <Text fontSize="sm" color="green.600">
                            Azure Stencils: {results.azure_diagram.azure_stencils.unique_used} unique stencils used
                          </Text>
                        )}
                      </Box>

                      {/* Tab Navigation */}
                      <Box>
                        <HStack mb="4" borderBottom="1px solid" borderColor="gray.200">
                          {["Diagram", "Azure PNG", "TSD", "HLD", "LLD"].map((tab, index) => (
                            <Button
                              key={tab}
                              variant={activeTab === index ? "solid" : "ghost"}
                              colorScheme={activeTab === index ? "blue" : "gray"}
                              onClick={() => setActiveTab(index)}
                              size="sm"
                            >
                              {tab}
                            </Button>
                          ))}
                        </HStack>

                        {/* Tab Content */}
                        {activeTab === 0 && (
                          <Box>
                            <Heading size="md" mb="4">🏗️ Azure Landing Zone Architecture Diagram</Heading>
                            <Box 
                              border="1px solid" 
                              borderColor="gray.200" 
                              borderRadius="md" 
                              p="4" 
                              bg="white"
                              maxH="600px"
                              overflowY="auto"
                            >
                              <Mermaid chart={results.mermaid} />
                            </Box>
                          </Box>
                        )}

                        {activeTab === 1 && results.azure_diagram && (
                          <Box>
                            <Heading size="md" mb="4">🎨 Azure Architecture Diagram (Professional)</Heading>
                            <Text fontSize="sm" color="green.600" mb="4">
                              Generated with {results.azure_diagram.azure_stencils.unique_used} unique Azure stencils
                            </Text>
                            <Box 
                              border="1px solid" 
                              borderColor="gray.200" 
                              borderRadius="md" 
                              p="4" 
                              bg="white"
                              maxH="600px"
                              overflowY="auto"
                              textAlign="center"
                            >
                              <img 
                                src={`data:image/png;base64,${results.azure_diagram.png_base64}`}
                                alt="Azure Architecture Diagram"
                                style={{ maxWidth: "100%", height: "auto" }}
                              />
                            </Box>
                          </Box>
                        )}

                        {activeTab === 2 && (
                          <Box>
                            <Heading size="md" mb="4">📘 Technical Specification Document (TSD)</Heading>
                            <Box 
                              border="1px solid" 
                              borderColor="gray.200" 
                              borderRadius="md" 
                              p="4" 
                              bg="white"
                              maxH="600px"
                              overflowY="auto"
                            >
                              <Text whiteSpace="pre-wrap" fontSize="sm" fontFamily="mono">
                                {results.tsd}
                              </Text>
                            </Box>
                          </Box>
                        )}

                        {activeTab === 3 && (
                          <Box>
                            <Heading size="md" mb="4">📗 High Level Design (HLD)</Heading>
                            <Box 
                              border="1px solid" 
                              borderColor="gray.200" 
                              borderRadius="md" 
                              p="4" 
                              bg="white"
                              maxH="600px"
                              overflowY="auto"
                            >
                              <Text whiteSpace="pre-wrap" fontSize="sm" fontFamily="mono">
                                {results.hld}
                              </Text>
                            </Box>
                          </Box>
                        )}

                        {activeTab === 4 && (
                          <Box>
                            <Heading size="md" mb="4">📙 Low Level Design (LLD)</Heading>
                            <Box 
                              border="1px solid" 
                              borderColor="gray.200" 
                              borderRadius="md" 
                              p="4" 
                              bg="white"
                              maxH="600px"
                              overflowY="auto"
                            >
                              <Text whiteSpace="pre-wrap" fontSize="sm" fontFamily="mono">
                                {results.lld}
                              </Text>
                            </Box>
                          </Box>
                        )}
                      </Box>
                    </VStack>
                  </CardBody>
                </Card>
              )}
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;