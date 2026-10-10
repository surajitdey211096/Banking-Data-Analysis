import React from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

const DEFAULT_COLORS = [
  "#6366f1",
  "#14b8a6",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
];

export default function DonutChart({
  data = [],
  title = "Transaction Distribution",
  nameKey = "name",
  valueKey = "value",
  colors = DEFAULT_COLORS,
  height = 320,
}) {
  const validData = data.filter(
    (item) =>
      Number.isFinite(Number(item[valueKey])) &&
      Number(item[valueKey]) >= 0
  );

  return (
    <section className="chart-card">
      <h3 className="chart-card__title">{title}</h3>

      {validData.length === 0 ? (
        <p className="chart-empty">No chart data available.</p>
      ) : (
        <div style={{ width: "100%", height }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={validData}
                dataKey={valueKey}
                nameKey={nameKey}
                cx="50%"
                cy="45%"
                innerRadius="55%"
                outerRadius="78%"
                paddingAngle={3}
              >
                {validData.map((entry, index) => (
                  <Cell
                    key={`${entry[nameKey]}-${index}`}
                    fill={colors[index % colors.length]}
                  />
                ))}
              </Pie>

              <Tooltip
                formatter={(value) =>
                  Number(value).toLocaleString("en-IN")
                }
              />

              <Legend verticalAlign="bottom" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
