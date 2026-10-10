import React from "react";
import KPICard from "../components/KPICard";
import BarChart from "../components/BarChart";
import DonutChart from "../components/DonutChart";

const loanStatuses = [
{ name: "Active", value: 62 },
{ name: "Closed", value: 21 },
{ name: "Overdue", value: 11 },
{ name: "Default", value: 6 },
];

const loansByType = [
{ category: "Personal", total_amount: 3200000 },
{ category: "Home", total_amount: 6800000 },
{ category: "Vehicle", total_amount: 2400000 },
{ category: "Business", total_amount: 4100000 },
{ category: "Education", total_amount: 1200000 },
];

const riskCategories = [
{ category: "Low Risk", total_amount: 680 },
{ category: "Medium Risk", total_amount: 240 },
{ category: "High Risk", total_amount: 95 },
];

export default function LoanRisk() {
return (
<main className="dashboard-page">
<header className="page-header">
<div>
<h1>Loan & Risk Analytics</h1>
<p>Loan portfolio performance, repayment status, and credit risk</p>
</div>
<span className="dashboard-badge">Sample Data</span>
</header>
<section className="kpi-grid">
    <KPICard
      title="Total Loans"
      value="4,820"
      change="+7.5%"
      icon="loans"
      subtitle="Loans recorded in the portfolio"
    />
    <KPICard
      title="Outstanding Balance"
      value="₹8.4 Cr"
      change="+5.2%"
      icon="growth"
      subtitle="Outstanding loan principal"
    />
    <KPICard
      title="Overdue Loans"
      value="531"
      change="+3.4%"
      icon="fraud"
      subtitle="Accounts requiring review"
    />
    <KPICard
      title="High-Risk Loans"
      value="95"
      change="-1.8%"
      icon="fraud"
      subtitle="Flagged for risk assessment"
    />
  </section>

  <section className="dashboard-grid">
    <div className="chart-card">
      <h2>Loan Portfolio Status</h2>
      <p>Distribution of loans by current status</p>
      <DonutChart
        data={loanStatuses}
        nameKey="name"
        valueKey="value"
      />
    </div>

    <div className="chart-card">
      <h2>Loans by Type</h2>
      <p>Loan amount by product category</p>
      <BarChart
        data={loansByType}
        xKey="category"
        dataKey="total_amount"
      />
    </div>

    <div className="chart-card full-width">
      <h2>Credit Risk Distribution</h2>
      <p>Number of loan accounts in each risk category</p>
      <BarChart
        data={riskCategories}
        xKey="category"
        dataKey="total_amount"
      />
    </div>
  </section>

  <section className="chart-card">
    <h2>Risk Management Notes</h2>
    <ul>
      <li>Review overdue accounts and repayment history.</li>
      <li>Investigate high-risk loans before making credit decisions.</li>
      <li>Validate risk categories against your actual lending policy.</li>
    </ul>
    <p>
      These notes are general examples, not automated credit decisions.
    </p>
  </section>
</main>
);
}