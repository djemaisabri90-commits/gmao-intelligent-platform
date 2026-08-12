// src/features/predictive/components/ClassDistributionPie.tsx
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import type { TrainingLog } from "../types";

interface Props {
  log: TrainingLog;
}

const COLORS = ["#FF9800", "#9C27B0", "#03A9F4", "#4CAF50"];

export const ClassDistributionPie = ({ log }: Props) => {
  const data = Object.entries(log.class_distribution).map(([label, value]) => ({
    name: label,
    value,
  }));

  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" outerRadius={100}>
          {data.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
};
