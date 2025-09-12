import * as React from "react";
import {
  ChakraProvider,
  Box,
  Heading,
  VStack,
  Button,
  Select,
  Textarea,
  Text,
  SimpleGrid,
} from "@chakra-ui/react";
import Mermaid from "./components/Mermaid"; // ✅ You'll add this component

function App() {
  const [formData, setFormData] = React.useState<any>({});
  const [results, setResults] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(false);

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8001/generate-diagram", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Box p="8" bg="gray.50" minH="100vh">
        <Heading size="lg" color="blue.600" mb="6">
          Azure Landing Zone Agent – Customer Inputs
        </Heading>

        <VStack spacing="6" align="stretch">
          {/* Section 1: Business */}
          <Heading size="md">1. Business & Compliance</Heading>
          <SimpleGrid columns={2} spacing={4}>
            <Select
              placeholder="Business Objective"
              onChange={(e) => handleChange("business_objective", e.target.value)}
            >
              <option value="cost">Cost</option>
              <option value="agility">Agility</option>
              <option value="innovation">Innovation</option>
              <option value="scalability">Scalability</option>
            </Select>
            <Select
              placeholder="Regulatory Requirement"
              onChange={(e) => handleChange("regulatory", e.target.value)}
            >
              <option value="HIPAA">HIPAA</option>
              <option value="PCI-DSS">PCI-DSS</option>
              <option value="GDPR">GDPR</option>
              <option value="RBI">RBI</option>
              <option value="ITAR">ITAR</option>
            </Select>
          </SimpleGrid>

          {/* Section 2: Org */}
          <Heading size="md">2. Organization</Heading>
          <Textarea
            placeholder="Org structure (tenants, subscriptions...)"
            onChange={(e) => handleChange("org_structure", e.target.value)}
          />

          {/* Section 3: Networking */}
          <Heading size="md">3. Networking & Connectivity</Heading>
          <Select
            placeholder="Networking Model"
            onChange={(e) => handleChange("network_model", e.target.value)}
          >
            <option value="hub-spoke">Hub-Spoke</option>
            <option value="mesh">Mesh</option>
            <option value="vwan">Virtual WAN</option>
          </Select>

          {/* Section 4: Security */}
          <Heading size="md">4. Security</Heading>
          <Select
            placeholder="Security Posture"
            onChange={(e) => handleChange("security_posture", e.target.value)}
          >
            <option value="zero-trust">Zero Trust</option>
            <option value="siem">SIEM/SOAR</option>
          </Select>

          {/* Section 5: Workloads */}
          <Heading size="md">5. Workloads</Heading>
          <Select
            placeholder="Workload Type"
            onChange={(e) => handleChange("workload", e.target.value)}
          >
            <option value="aks">AKS</option>
            <option value="appservices">App Services</option>
            <option value="vm">VMs</option>
            <option value="sap">SAP</option>
            <option value="ai">AI/ML</option>
            <option value="data">Data & Analytics</option>
          </Select>

          {/* Section 6: Ops */}
          <Heading size="md">6. Operations</Heading>
          <Select
            placeholder="Ops Model"
            onChange={(e) => handleChange("ops_model", e.target.value)}
          >
            <option value="centralized">Centralized</option>
            <option value="federated">Federated</option>
          </Select>

          {/* Section 7: Cost */}
          <Heading size="md">7. Cost</Heading>
          <Select
            placeholder="Optimization Priority"
            onChange={(e) => handleChange("cost_priority", e.target.value)}
          >
            <option value="cost">Cost-first</option>
            <option value="performance">Performance-first</option>
          </Select>

          {/* Section 8: Migration */}
          <Heading size="md">8. Migration</Heading>
          <Select
            placeholder="Migration Scope"
            onChange={(e) => handleChange("migration_scope", e.target.value)}
          >
            <option value="new">New workloads only</option>
            <option value="lift-shift">Lift & Shift</option>
          </Select>

          {/* Section 9: Preferences */}
          <Heading size="md">9. Customer Preferences</Heading>
          <Select
            placeholder="Preferred IaC"
            onChange={(e) => handleChange("iac", e.target.value)}
          >
            <option value="terraform">Terraform</option>
            <option value="bicep">Bicep</option>
            <option value="arm">ARM</option>
          </Select>

          <Button
            colorScheme="blue"
            isLoading={loading}
            loadingText="Generating..."
            onClick={handleSubmit}
          >
            Generate Architecture
          </Button>

          {/* Results */}
          {results && (
            <>
              <Heading size="md">Mermaid Diagram</Heading>
              <Mermaid chart={results.mermaid} />

              <Heading size="md">📘 TSD</Heading>
              <Text whiteSpace="pre-wrap">{results.tsd}</Text>

              <Heading size="md">📗 HLD</Heading>
              <Text whiteSpace="pre-wrap">{results.hld}</Text>

              <Heading size="md">📙 LLD</Heading>
              <Text whiteSpace="pre-wrap">{results.lld}</Text>
            </>
          )}
        </VStack>
      </Box>
    </ChakraProvider>
  );
}

export default App;

