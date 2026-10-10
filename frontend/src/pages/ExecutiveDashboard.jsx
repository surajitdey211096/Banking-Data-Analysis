import React from "react";
import { Users, CreditCard, Landmark, ShieldAlert } from "lucide-react";
import KPICard from "../components/KPICard";
import LineChart from "../components/LineChart";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const monthlyTransactions = [
{ month: "Jan", total_amount: 1250000 },
{ month: "Feb", total_amount: 1480000 },
{ month: "Mar", total_amount: 1390000 },
{ month: "Apr", total_amount: 1720000 },
{ month: "May", total_amount: 1850000 },
{ month: "Jun", total_amount: 2100000 },
];

const transactionTypes = [
{ name: "UPI", value: 42 },
{ name: "Card", value: 25 },
{ name: "Transfer", value: 20 },
{ name: "Cash", value: 13 },
];

const transactionCategories = [
{ category: "UPI", total_amount: 4200000 },
{ category: "Card", total_amount: 2500000 },
{ category: "Transfer", total_amount: 3100000 },
{ category: "Cash", total_amount: 1300000 },
];

export default function ExecutiveDashboard() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Executive Dashboard</h1>
<p>Banking performance overview and business KPIs</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Total Customers"
      value="24,580"
      change="+8.4%"
      icon="customers"
      subtitle="Compared with previous period"
    />
    <KPICard
      title="Transactions"
      value="18,420"
      change="+12.6%"
      icon="transactions"
      subtitle="Total processed transactions"
    />
    <KPICard
      title="Loan Portfolio"
      value="₹8.4 Cr"
      change="+5.2%"
      icon="loans"
      subtitle="Total outstanding loan value"
    />
    <KPICard
      title="Fraud Alerts"
      value="38"
      change="-6.1%"
      icon="fraud"
      subtitle="Alerts requiring review"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Monthly Transaction Value</h2>
      <p>Transaction value trend across six months</p>
      <LineChart
        data={monthlyTransactions}
        xKey="month"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card">
      <h2>Transaction Type Distribution</h2>
      <p>Share by payment method</p>
      <DonutChart
        data={transactionTypes}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Transaction Value by Category</h2>
      <p>Compare payment channel performance</p>
      <BarChart
        data={transactionCategories}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>
</main>
);
}