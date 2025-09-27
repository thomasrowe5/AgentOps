import React, { useEffect, useState } from "react";
import axios from "axios";

export default function StrategyLeaderboard() {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/strategy/leaderboard");
        setStrategies(res.data || []);
      } catch (err) {
        console.error("Failed to fetch leaderboard:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <p>⏳ Loading strategy leaderboard...</p>;

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>🏆 Strategy Leaderboard</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f3f4f6" }}>
            <th style={th}>Strategy</th>
            <th style={th}>Times Used</th>
            <th style={th}>Avg Accuracy ↑</th>
            <th style={th}>Avg F1 ↑</th>
            <th style={th}>Win Rate</th>
          </tr>
        </thead>
        <tbody>
          {strategies.map((s, i) => (
            <tr key={i} style={{ background: i % 2 === 0 ? "#ffffff" : "#f9fafb" }}>
              <td style={td}>{s.name}</td>
              <td style={td}>{s.times_used}</td>
              <td style={td}>{(s.avg_accuracy * 100).toFixed(1)}%</td>
              <td style={td}>{(s.avg_f1 * 100).toFixed(1)}%</td>
              <td style={td}>{(s.win_rate * 100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const th = {
  padding: "12px",
  textAlign: "left",
  fontWeight: "600",
  borderBottom: "2px solid #e5e7eb",
};

const td = {
  padding: "10px",
  borderBottom: "1px solid #e5e7eb",
};

