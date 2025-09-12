import React, { useEffect, useRef } from "react";
import mermaid from "mermaid";

type MermaidProps = {
  chart: string;
};

const Mermaid: React.FC<MermaidProps> = ({ chart }) => {
  const ref = useRef<HTMLDivElement>(null);

  // Unique ID for this diagram instance
  const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;

  // Initialize Mermaid ONCE
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: "default" });
  }, []);

  useEffect(() => {
    if (!chart || !ref.current) return;

    try {
      mermaid.render(id, chart, (svgCode) => {
        if (ref.current) {
          ref.current.innerHTML = svgCode;
        }
      });
    } catch (err) {
      console.error("Mermaid render error:", err);
      if (ref.current) {
        ref.current.innerHTML =
          "<p style='color:red'>❌ Failed to render diagram</p>";
      }
    }
  }, [chart, id]);

  return (
    <div ref={ref}>
      {!chart && <p style={{ color: "gray" }}>No diagram available</p>}
    </div>
  );
};

export default Mermaid;

