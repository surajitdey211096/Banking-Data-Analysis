import React from "react";
import {
  ResponsiveContainer,
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export default function BarChart({
  data = [],
  title = "Transaction Analysis",
  dataKey = "total_amount",
  xKey = "category",
  color = "#0d9488",
  height = 300,
}) {
  return (
    <section className="chart-card">
      <h3 className="chart-card__title">{title}</h3>

      {data.length === 0 ? (
        <p className="chart-empty">No chart data available.</p>
      ) : (
        <div style={{ width: "100%", height }}>
          <ResponsiveContainer>
            <RechartsBarChart
              data={data}
              margin={{ top: 10, right: 15, left: 5, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#e5e7eb"
              />

              <XAxis
                dataKey={xKey}
                tick={{ fontSize: 12 }}
                interval={0}
              />

              <YAxis
                tick={{ fontSize: 12 }}
                tickFormatter={(value) =>
                  Number(value).toLocaleString("en-IN")
                }
              />

              <Tooltip
                formatter={(value) =>
                  Number(value).toLocaleString("en-IN")
                }
              />

              <Bar
                dataKey={dataKey}
                name="Amount"
                fill={color}
                radius={[5, 5, 0, 0]}
                maxBarSize={55}
              />
            </RechartsBarChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
