// src/features/predictive/components/AccuracyChart.tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import type { TrainingLog } from "../types";
import { PresentationChartLineIcon } from "@heroicons/react/24/outline";

interface Props {
  logs: TrainingLog[];
}

export const AccuracyChart = ({ logs }: Props) => {
  const data = [...logs]
  .sort((a, b) => a.model_version - b.model_version) // ✅ tri croissant
  .map(log => ({
    version: `v${log.model_version}`,
    accuracy: log.accuracy,
    f1: log.f1_score,
  }));

  return (
    <div className="mt-6">
      <h3 className="flex items-center justify-center gap-2 
               text-lg font-semibold text-purple-600 mb-6">
  <PresentationChartLineIcon className="w-5 h-5 text-purple-500" />        
  Vue globale : Historique des métriques (versions anciennes → récentes)
</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="version" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Line type="monotone" dataKey="accuracy" stroke="#4CAF50" name="Accuracy" />
          <Line type="monotone" dataKey="f1" stroke="#2196F3" name="F1 Score" />
        </LineChart>
      </ResponsiveContainer>
    </div>

  );
};
