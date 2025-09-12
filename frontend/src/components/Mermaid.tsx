import React, { useEffect, useRef } from "react";
import mermaid from "mermaid";

type MermaidProps = {
  chart: string;
};

const Mermaid: React.FC<MermaidProps> = ({ chart }) => {
  const ref = useRef<HTMLDivElement>(null);

  // Initialize Mermaid ONCE
  useEffect(() => {
    mermaid.initialize({ 
      startOnLoad: false, 
      theme: "default",
      securityLevel: "loose"
    });
  }, []);

  useEffect(() => {
    if (!chart || !ref.current) return;

    // Clear previous content
    ref.current.innerHTML = "";

    const id = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    try {
      // Create a temporary element for mermaid to render into
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = chart;
      
      mermaid.render(id, chart)
        .then((result) => {
          if (ref.current) {
            ref.current.innerHTML = result.svg;
          }
        })
        .catch((err) => {
          console.error("Mermaid render error:", err);
          if (ref.current) {
            ref.current.innerHTML = 
              "<p style='color:red; padding: 20px; border: 1px solid red; border-radius: 4px; background: #ffebee;'>❌ Failed to render diagram. Please check the diagram syntax.</p>";
          }
        });
    } catch (err) {
      console.error("Mermaid render error:", err);
      if (ref.current) {
        ref.current.innerHTML =
          "<p style='color:red; padding: 20px; border: 1px solid red; border-radius: 4px; background: #ffebee;'>❌ Failed to render diagram. Please check the diagram syntax.</p>";
      }
    }
  }, [chart]);

  return (
    <div ref={ref} style={{ width: '100%', minHeight: '400px' }}>
      {!chart && <p style={{ color: "gray" }}>No diagram available</p>}
    </div>
  );
};

export default Mermaid;

