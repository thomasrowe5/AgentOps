import React, { useState } from "react";
import SmartScoreChart from "./components/SmartScoreChart";
import TriggerOptimizationButton from "./components/TriggerOptimizationButton";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  // This refreshes the chart after a new optimization run
  const handleOptimizationComplete = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div style={{ padding: "2rem", background: "#f9fafb", minHeight: "100vh" }}>
      <h1 style={{ fontSize: "2rem", marginBottom: "1.5rem" }}>🚀 AgentOps Dashboard</h1>

      <TriggerOptimizationButton onRunComplete={handleOptimizationComplete} />

      {/* Pass refreshKey so the chart re-fetches when it changes */}
      <SmartScoreChart key={refreshKey} />
    </div>
  );
}

export default App;

