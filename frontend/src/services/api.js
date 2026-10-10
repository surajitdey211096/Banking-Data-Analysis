import React from "react";
import {
BrowserRouter,
NavLink,
Navigate,
Route,
Routes,
} from "react-router-dom";
import {
LayoutDashboard,
Users,
ArrowLeftRight,
ShieldAlert,
Building2,
Headset,
} from "lucide-react";

import ExecutiveDashboard from "./pages/ExecutiveDashboard";
import CustomerAnalytics from "./pages/CustomerAnalytics";
import TransactionAnalytics from "./pages/TransactionAnalytics";
import LoanRisk from "./pages/LoanRisk";
import BranchAnalytics from "./pages/BranchAnalytics";
import ServiceAnalytics from "./pages/ServiceAnalytics";

const navigation = [
{
path: "/executive",
label: "Executive Dashboard",
icon: LayoutDashboard,
},
{
path: "/customers",
label: "Customer Analytics",
icon: Users,
},
{
path: "/transactions",
label: "Transaction Analytics",
icon: ArrowLeftRight,
},
{
path: "/loan-risk",
label: "Loan & Risk",
icon: ShieldAlert,
},
{
path: "/branches",
label: "Branch Analytics",
icon: Building2,
},
{
path: "/services",
label: "Service Analytics",
icon: Headset,
},
];

function DashboardLayout() {
return (
<div className="app-layout">
<aside className="sidebar">
<div className="brand">
<Building2 size={28} />
<div>
<strong>BankInsight</strong>
<small>Analytics Platform</small>
</div>
</div>
<nav className="sidebar-nav">
      {navigation.map(({ path, label, icon: Icon }) => (
        <NavLink
          key={path}
          to={path}
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          <Icon size={19} />
          <span>{label}</span>
        </NavLink>
      ))}
    </nav>

    <div className="sidebar-footer">
      Banking Data Analysis
      <small>React + FastAPI</small>
    </div>
  </aside>

  <div className="main-content">
    <header className="topbar">
      <span>Banking Intelligence</span>
      <span className="user-label">Analytics Workspace</span>
    </header>

    <Routes>
      <Route
        path="/"
        element={<Navigate to="/executive" replace />}
      />
      <Route path="/executive" element={<ExecutiveDashboard />} />
      <Route path="/customers" element={<CustomerAnalytics />} />
      <Route
        path="/transactions"
        element={<TransactionAnalytics />}
      />
      <Route path="/loan-risk" element={<LoanRisk />} />
      <Route path="/branches" element={<BranchAnalytics />} />
      <Route path="/services" element={<ServiceAnalytics />} />
      <Route
        path="*"
        element={<Navigate to="/executive" replace />}
      />
    </Routes>
  </div>
</div>
);
}

export default function App() {
return (
<BrowserRouter>
<DashboardLayout />
</BrowserRouter>
);
}