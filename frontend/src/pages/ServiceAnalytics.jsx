import React from "react";
import KPICard from "../components/KPICard";
import LineChart from "../components/LineChart";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const monthlyRequests = [
{ month: "Jan", total_amount: 820 },
{ month: "Feb", total_amount: 910 },
{ month: "Mar", total_amount: 875 },
{ month: "Apr", total_amount: 1020 },
{ month: "May", total_amount: 1140 },
{ month: "Jun", total_amount: 1080 },
];

const requestStatuses = [
{ name: "Resolved", value: 72 },
{ name: "In Progress", value: 18 },
{ name: "Open", value: 7 },
{ name: "Escalated", value: 3 },
];

const serviceCategories = [
{ category: "Account", total_amount: 420 },
{ category: "Cards", total_amount: 310 },
{ category: "Loans", total_amount: 180 },
{ category: "Payments", total_amount: 520 },
{ category: "Digital Banking", total_amount: 260 },
];

export default function ServiceAnalytics() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Service Analytics</h1>
<p>Customer requests, complaints, and service resolution performance</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Service Requests"
      value="1,080"
      change="+5.4%"
      icon="transactions"
      subtitle="Requests recorded this month"
    />
    <KPICard
      title="Resolution Rate"
      value="92.4%"
      change="+3.2%"
      icon="growth"
      subtitle="Illustrative resolved-request rate"
    />
    <KPICard
      title="Open Requests"
      value="76"
      change="-8.1%"
      icon="customers"
      subtitle="Requests awaiting resolution"
    />
    <KPICard
      title="Escalated Cases"
      value="32"
      change="-4.2%"
      icon="fraud"
      subtitle="Cases requiring additional attention"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Monthly Service Requests</h2>
      <p>Request volume trend over six months</p>
      <LineChart
        data={monthlyRequests}
        xKey="month"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card">
      <h2>Request Status</h2>
      <p>Distribution by resolution status</p>
      <DonutChart
        data={requestStatuses}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Requests by Service Category</h2>
      <p>Identify which services generate the most requests</p>
      <BarChart
        data={serviceCategories}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>
</main>
);
}