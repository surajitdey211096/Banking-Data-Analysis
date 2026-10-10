import React from "react";
import KPICard from "../components/KPICard";
import LineChart from "../components/LineChart";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const monthlyVolume = [
{ month: "Jan", total_amount: 12500 },
{ month: "Feb", total_amount: 13900 },
{ month: "Mar", total_amount: 14600 },
{ month: "Apr", total_amount: 15800 },
{ month: "May", total_amount: 17100 },
{ month: "Jun", total_amount: 18420 },
];

const paymentMethods = [
{ name: "UPI", value: 42 },
{ name: "Debit Card", value: 25 },
{ name: "Bank Transfer", value: 20 },
{ name: "Cash", value: 13 },
];

const transactionStatuses = [
{ category: "Successful", total_amount: 17240 },
{ category: "Pending", total_amount: 760 },
{ category: "Failed", total_amount: 420 },
];

export default function TransactionAnalytics() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Transaction Analytics</h1>
<p>Monitor payment activity, transaction value, and processing status</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Total Transactions"
      value="18,420"
      change="+12.6%"
      icon="transactions"
      subtitle="Transactions processed"
    />
    <KPICard
      title="Transaction Value"
      value="₹1.12 Cr"
      change="+9.3%"
      icon="growth"
      subtitle="Total transaction amount"
    />
    <KPICard
      title="Success Rate"
      value="93.6%"
      change="+2.1%"
      icon="transactions"
      subtitle="Successful transactions"
    />
    <KPICard
      title="Failed Transactions"
      value="420"
      change="-4.5%"
      icon="fraud"
      subtitle="Failed transaction records"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Monthly Transaction Volume</h2>
      <p>Number of transactions per month</p>
      <LineChart
        data={monthlyVolume}
        xKey="month"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card">
      <h2>Payment Method Distribution</h2>
      <p>Share of transactions by payment method</p>
      <DonutChart
        data={paymentMethods}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Transactions by Status</h2>
      <p>Count of successful, pending, and failed transactions</p>
      <BarChart
        data={transactionStatuses}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>
</main>
);
}