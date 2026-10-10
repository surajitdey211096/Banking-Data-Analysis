import React from "react";
import KPICard from "./KPICard.jsx";
import LineChart from "./LineChart.jsx";
import BarChart from "./BarChart.jsx";
import DonutChart from "./DonutChart.jsx";
import AIChat from "./AIChat.jsx";
import "./index.css";

const monthlyData = [
  { month: "2026-07", total_amount: 125000 },
  { month: "2026-08", total_amount: 158000 },
  { month: "2026-09", total_amount: 142000 },
  { month: "2026-10", total_amount: 190000 },
];

const categoryData = [
  { category: "Deposit", total_amount: 250000 },
  { category: "Withdrawal", total_amount: 175000 },
  { category: "Transfer", total_amount: 320000 },
  { category: "Payment", total_amount: 95000 },
];

const distributionData = [
  { name: "Deposit", value: 400 },
  { name: "Withdrawal", value: 250 },
  { name: "Transfer", value: 180 },
  { name: "Payment", value: 120 },
];

export default function App() {
  return (
    <main style={{ padding: 24, background: "#f8fafc" }}>
      <h1>Banking Analytics Dashboard</h1>
      <p>Transaction monitoring and AI-assisted analysis</p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 16,
          margin: "24px 0",
        }}
      >
        <KPICard
          title="Total Customers"
          value="12,450"
          change="+8.2%"
          icon="customers"
        />
        <KPICard
          title="Transaction Value"
          value="₹8.4M"
          icon="transactions"
        />
        <KPICard
          title="Active Loans"
          value="1,240"
          icon="loans"
        />
        <KPICard
          title="Fraud Alerts"
          value="18"
          icon="fraud"
          subtitle="Requires review"
        />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: 16,
        }}
      >
        <LineChart data={monthlyData} />
        <BarChart data={categoryData} />
        <DonutChart data={distributionData} />
      </div>

      <div style={{ marginTop: 24 }}>
        <AIChat />
      </div>
    </main>
  );
}
