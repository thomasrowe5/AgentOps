import React, { useState } from "react";
import axios from "axios";

export default function TriggerOptimizationButton({ onRunComplete }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const runOptimization = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/optimize/run");

      if (res.data.success) {
        setResult(res.data.output);
        if (onRunComplete) onRunComplete();
      } else {
        setError(res.data.error || "Optimization failed on backend.");
      }
    } catch (err) {
      console.error(err);
      setError("❌ Optimization failed. Check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: "2rem" }}>
      <button
        onClick={runOptimization}
        disabled={loading}
        style={{
          padding: "12px 20px",
          background: loading ? "#9ca3af" : "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "🚀 Running Optimization..." : "⚙️ Run Optimization"}
      </button>

      {result && (
        <pre
          style={{
            background: "#f3f4f6",
            padding: "1rem",
            marginTop: "1rem",
            maxHeight: "300px",
            overflow: "auto",
            fontSize: "14px",
            borderRadius: "6px",
          }}
        >
          {result}
        </pre>
      )}

      {error && (
        <p style={{ color: "red", marginTop: "1rem", fontWeight: "bold" }}>
          {error}
        </p>
      )}
    </div>
  );
}

