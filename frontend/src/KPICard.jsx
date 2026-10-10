import React from "react";
import {
  Users,
  ArrowLeftRight,
  Landmark,
  ShieldAlert,
  TrendingUp,
} from "lucide-react";

const iconMap = {
  customers: Users,
  transactions: ArrowLeftRight,
  loans: Landmark,
  fraud: ShieldAlert,
  growth: TrendingUp,
};

export default function KPICard({
  title,
  value,
  change,
  icon = "growth",
  subtitle,
}) {
  const Icon = iconMap[icon] || TrendingUp;
  const isNegative = String(change ?? "").trim().startsWith("-");

  return (
    <article className="kpi-card">
      <div className="kpi-card__top">
        <span className="kpi-card__title">{title}</span>

        <span className="kpi-card__icon">
          <Icon size={21} />
        </span>
      </div>

      <div className="kpi-card__value">
        {value ?? "—"}
      </div>

      {change != null && (
        <div
          className={`kpi-card__change ${
            isNegative ? "negative" : "positive"
          }`}
        >
          {change}
        </div>
      )}

      {subtitle && (
        <p className="kpi-card__subtitle">{subtitle}</p>
      )}
    </article>
  );
}
