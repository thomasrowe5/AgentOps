import axios from "axios";

const API_BASE = "http://localhost:8000"; // FastAPI backend

export async function getMetricsHistory() {
  const res = await axios.get(`${API_BASE}/metrics/history`);
  return res.data;
}

export async function getStrategyStats() {
  const res = await axios.get(`${API_BASE}/strategy/memory`);
  return res.data;
}

export async function triggerOptimization() {
  const res = await axios.post(`${API_BASE}/optimize/run`);
  return res.data;
}

