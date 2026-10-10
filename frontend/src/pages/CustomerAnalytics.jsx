import React from "react";
import { Users, UserCheck, UserPlus, UserRoundX } from "lucide-react";
import KPICard from "../components/KPICard";
import LineChart from "../components/LineChart";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const customerGrowth = [
{ month: "Jan", total_amount: 18200 },
{ month: "Feb", total_amount: 19400 },
{ month: "Mar", total_amount: 20700 },
{ month: "Apr", total_amount: 21800 },
{ month: "May", total_amount: 23100 },
{ month: "Jun", total_amount: 24580 },
];

const customerSegments = [
{ name: "Retail", value: 58 },
{ name: "Salary", value: 22 },
{ name: "Business", value: 14 },
{ name: "Premium", value: 6 },
];

const customersByCity = [
{ category: "Kolkata", total_amount: 5200 },
{ category: "Bhubaneswar", total_amount: 3900 },
{ category: "Delhi", total_amount: 3500 },
{ category: "Mumbai", total_amount: 3100 },
{ category: "Bengaluru", total_amount: 2800 },
];

export default function CustomerAnalytics() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Customer Analytics</h1>
<p>Customer acquisition, growth, segments, and location insights</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Total Customers"
      value="24,580"
      change="+8.4%"
      icon="customers"
      subtitle="Total registered customers"
    />
    <KPICard
      title="New Customers"
      value="1,480"
      change="+11.2%"
      icon="growth"
      subtitle="Added during this period"
    />
    <KPICard
      title="Active Customers"
      value="21,360"
      change="+4.7%"
      icon="customers"
      subtitle="Customers active in the period"
    />
    <KPICard
      title="Inactive Customers"
      value="3,220"
      change="-2.3%"
      icon="fraud"
      subtitle="May need re-engagement"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Customer Growth</h2>
      <p>Total customer count by month</p>
      <LineChart
        data={customerGrowth}
        xKey="month"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card">
      <h2>Customer Segments</h2>
      <p>Distribution by customer type</p>
      <DonutChart
        data={customerSegments}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Customers by City</h2>
      <p>Customer distribution across selected cities</p>
      <BarChart
        data={customersByCity}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>
</main>
);
}