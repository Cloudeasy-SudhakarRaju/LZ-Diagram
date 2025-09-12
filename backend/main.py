from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # open for dev, restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CustomerInputs(BaseModel):
    regulatory: Optional[str] = None
    industry: Optional[str] = None
    org_structure: Optional[str] = None
    identity: Optional[str] = None
    governance: Optional[str] = None
    connectivity: Optional[str] = None
    network_model: Optional[str] = None
    security_zone: Optional[str] = None
    ip_strategy: Optional[str] = None
    security_posture: Optional[str] = None
    key_vault: Optional[str] = None
    threat_protection: Optional[str] = None
    workload: Optional[str] = None
    architecture_style: Optional[str] = None
    scalability: Optional[str] = None
    ops_model: Optional[str] = None
    monitoring: Optional[str] = None
    backup: Optional[str] = None
    topology_pattern: Optional[str] = None
    business_objective: Optional[str] = None


# ---------- Helper: Generate Draw.io XML ----------
def generate_drawio_xml(inputs: CustomerInputs) -> str:
    def esc(s): return html.escape(s) if s else ""

    return f"""
<mxfile host="app.diagrams.net">
  <diagram name="Azure Landing Zone">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <mxCell id="hub" value="Hub VNet ({esc(inputs.network_model) or 'Hub-Spoke'})" style="shape=mxgraph.azure.vnet;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="80" as="geometry" />
        </mxCell>

        <mxCell id="spoke1" value="Spoke VNet" style="shape=mxgraph.azure.vnet;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="120" height="80" as="geometry" />
        </mxCell>

        <mxCell id="workload" value="{esc(inputs.workload) or 'App Service'}" style="shape=mxgraph.azure.app_services;" vertex="1" parent="1">
          <mxGeometry x="500" y="100" width="120" height="80" as="geometry" />
        </mxCell>

        <mxCell id="edge1" edge="1" source="hub" target="spoke1" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge2" edge="1" source="spoke1" target="workload" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
""".strip()


# ---------- Mermaid Endpoint ----------
@app.post("/generate-diagram")
def generate_diagram(inputs: CustomerInputs):
    lines = ["graph TD", "  MG[📁 Management Group] --> SUB1[📦 Subscription 1]"]

    if inputs.network_model:
        lines.append(f"  SUB1 --> HUB[🌐 Hub VNet ({inputs.network_model})]")
        lines.append("  HUB --> SPOKE1[🏷 Spoke VNet 1]")

    if inputs.identity:
        lines.append(f"  SUB1 --> AAD[🔐 {inputs.identity}]")

    if inputs.workload:
        lines.append(f"  SUB1 --> WORKLOAD[{inputs.workload}]")

    if inputs.monitoring:
        lines.append(f"  SUB1 --> MON[📊 Monitoring: {inputs.monitoring}]")

    mermaid = "\n".join(lines)
    drawio_xml = generate_drawio_xml(inputs)

    return {
        "mermaid": mermaid,
        "drawio": drawio_xml,
        "tsd": f"TSD: Generated with objective {inputs.business_objective or 'N/A'}",
        "hld": f"HLD: Topology = {inputs.topology_pattern or inputs.network_model or 'Hub-Spoke'}",
        "lld": f"LLD: Workload = {inputs.workload or 'Generic'}, Identity = {inputs.identity or 'Azure AD'}"
    }


# ---------- Draw.io Endpoint ----------
@app.post("/generate-drawio", response_class=Response)
def generate_drawio(inputs: CustomerInputs):
    xml = generate_drawio_xml(inputs)
    return Response(content=xml, media_type="text/xml")
