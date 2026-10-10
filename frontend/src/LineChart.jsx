import React from "react";
import {
  ResponsiveContainer,
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export default function LineChart({
  data = [],
  title = "Transaction Trends",
  dataKey = "total_amount",
  xKey = "month",
  color = "#6366f1",
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
            <RechartsLineChart
              data={data}
              margin={{ top: 10, right: 15, left: 5, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#e5e7eb"
              />

              <XAxis dataKey={xKey} tick={{ fontSize: 12 }} />
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

              <Line
                type="monotone"
                dataKey={dataKey}
                name="Transaction Amount"
                stroke={color}
                strokeWidth={3}
                dot={{ r: 3 }}
                activeDot={{ r: 6 }}
              />
            </RechartsLineChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
