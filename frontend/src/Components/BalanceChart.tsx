import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import type { GasFlowRecord } from "../Types/gasFlowTypes";

interface BalanceChartProps {
  records: GasFlowRecord[];
  unit: string;
}

export default function BalanceChart({ records, unit }: BalanceChartProps) {
  const chartData = records.map((record) => ({
    gas_day: record.gas_day,
    demand: record.demand.total,
    supply: record.supply.total,
    balance: record.balance
  }));

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <h2>Supply, demand, and balance</h2>
          <p>Totals by gas day.</p>
        </div>
        <span>{unit}</span>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 16, right: 24, bottom: 8, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="gas_day" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="demand"
              name="Demand"
              stroke="#b45309"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="supply"
              name="Supply"
              stroke="#0f766e"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="balance"
              name="Balance"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
