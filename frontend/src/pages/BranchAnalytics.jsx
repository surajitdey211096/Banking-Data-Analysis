import React from "react";
import KPICard from "../components/KPICard";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const branchCustomers = [
{ category: "Kolkata", total_amount: 5200 },
{ category: "Bhubaneswar", total_amount: 3900 },
{ category: "Delhi", total_amount: 3500 },
{ category: "Mumbai", total_amount: 3100 },
{ category: "Bengaluru", total_amount: 2800 },
];

const branchTransactions = [
{ category: "Kolkata", total_amount: 3200000 },
{ category: "Bhubaneswar", total_amount: 2450000 },
{ category: "Delhi", total_amount: 2900000 },
{ category: "Mumbai", total_amount: 2750000 },
{ category: "Bengaluru", total_amount: 2200000 },
];

const branchShare = [
{ name: "Kolkata", value: 28 },
{ name: "Bhubaneswar", value: 21 },
{ name: "Delhi", value: 20 },
{ name: "Mumbai", value: 18 },
{ name: "Bengaluru", value: 13 },
];

export default function BranchAnalytics() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Branch Analytics</h1>
<p>Compare customer distribution and financial activity by branch</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Total Branches"
      value="42"
      change="+2"
      icon="customers"
      subtitle="Branches in the reporting dataset"
    />
    <KPICard
      title="Customers"
      value="24,580"
      change="+8.4%"
      icon="customers"
      subtitle="Across all selected branches"
    />
    <KPICard
      title="Transaction Value"
      value="₹1.32 Cr"
      change="+9.1%"
      icon="transactions"
      subtitle="Combined branch transaction value"
    />
    <KPICard
      title="Top Branch"
      value="Kolkata"
      change="+10.2%"
      icon="growth"
      subtitle="Illustrative performance leader"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Customers by Branch</h2>
      <p>Customer count across selected locations</p>
      <BarChart
        data={branchCustomers}
        xKey="category"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card">
      <h2>Branch Contribution</h2>
      <p>Illustrative share of total activity</p>
      <DonutChart
        data={branchShare}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Transaction Value by Branch</h2>
      <p>Compare transaction amounts across locations</p>
      <BarChart
        data={branchTransactions}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>
</main>
);
}