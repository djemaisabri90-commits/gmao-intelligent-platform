// src/features/predictive/components/ValidationMetricsChart.tsx
import type { FC } from "react";
import { ScaleIcon } from "@heroicons/react/24/outline";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import type { TrainingLog } from "../types";

type Props = {
  log: TrainingLog;
};

export const ValidationMetricsChart: FC<Props> = ({ log }) => {
  if (!log.validation_metrics) return null;

  // Transformer les données pour le graphique
  const data = Object.entries(log.validation_metrics).map(([method, result]) => ({
    method,
    accuracy: result.report?.accuracy ?? 0,
    precision: result.report?.["weighted avg"]?.["precision"] ?? 0,
    recall: result.report?.["weighted avg"]?.["recall"] ?? 0,
    f1: result.report?.["weighted avg"]?.["f1-score"] ?? 0,
    macro_f1: result.report?.["macro avg"]?.["f1-score"] ?? 0,
  }));

  return (
    <div className="mt-6">
      <h3 className="flex items-center justify-center gap-2 
               text-lg font-semibold text-indigo-700 mb-4">
        <ScaleIcon className="w-5 h-5 text-indigo-600" />
        Comparaison des méthodes de rééquilibrage (SMOTE vs ROS)
      </h3>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <XAxis dataKey="method" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="accuracy" fill="#4CAF50" name="Accuracy" />
          <Bar dataKey="precision" fill="#2196F3" name="Precision" />
          <Bar dataKey="recall" fill="#FF9800" name="Recall" />
          <Bar dataKey="f1" fill="#9C27B0" name="F1-score (pondéré)" />
          <Bar dataKey="macro_f1" fill="#3F51B5" name="Macro F1" />
          <Bar dataKey="balanced_accuracy" fill="#00BCD4" name="Balanced Accuracy" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
