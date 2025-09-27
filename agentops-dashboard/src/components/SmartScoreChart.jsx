import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { getMetricsHistory } from "../api/agentOpsAPI";

export default function SmartScoreChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    getMetricsHistory()
      .then(metrics => {
        // Reformat data for the chart
        const formatted = metrics.map(row => ({
          timestamp: row.timestamp?.slice(0, 10) || "Unknown",
          smart_score: parseFloat(row.smart_score || 0),
          f1: parseFloat(row.f1 || 0),
          runtime: parseFloat(row.runtime || 0),
        }));
        setData(formatted);
      })
      .catch(err => console.error("Error fetching metrics:", err));
  }, []);

  return (
    <div style={{ background: "white", padding: 20, borderRadius: 12, boxShadow: "0 4px 12px rgba(0,0,0,0.1)", marginTop: 30 }}>
      <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>📊 SmartScore Performance Over Time</h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="smart_score" stroke="#2563eb" strokeWidth={2} name="SmartScore" />
          <Line type="monotone" dataKey="f1" stroke="#10b981" strokeWidth={2} name="F1 Score" />
          <Line type="monotone" dataKey="runtime" stroke="#f97316" strokeWidth={2} name="Runtime (s)" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

