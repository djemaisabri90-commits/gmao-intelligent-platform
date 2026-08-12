// src/features/predictive/components/HistoryMetricsChart.tsx
import type { FC } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

//import { HistoryMetricsSummary } from "./HistoryMetricsSummary";

import type { TrainingLog } from "../types";

type Props = {
  logs: TrainingLog[];
};

export const HistoryMetricsChart: FC<Props> = ({ logs }) => {
  if (!logs || logs.length === 0) return null;

  // 🔄 Trier les logs du plus récent au plus ancien
  const sortedLogs = [...logs].sort((a, b) => b.model_version - a.model_version);
  // ✅ Définir latestLog
  //const latestLog = sortedLogs[0];

  // Données principales
  const mainData = sortedLogs.map((log) => ({
    version: `v${log.model_version}`,
    accuracy: log.accuracy,
    f1: log.f1_score,
    balanced_accuracy: log.balanced_accuracy ?? 0,
    macro_f1: log.macro_f1 ?? 0,
    minority_ratio: (log.minority_ratio ?? 0) * 100,
  }));

  // Données comparatives SMOTE vs ROS
  /*
  const validationData = sortedLogs.map((log) => ({
    version: `v${log.model_version}`,
    smote_accuracy: log.validation_metrics?.SMOTE?.accuracy ?? 0,
    smote_f1: log.validation_metrics?.SMOTE?.["weighted avg"]?.["f1-score"] ?? 0,
    ros_accuracy: log.validation_metrics?.RandomOverSampler?.accuracy ?? 0,
    ros_f1: log.validation_metrics?.RandomOverSampler?.["weighted avg"]?.["f1-score"] ?? 0,
  }));
  */
  return (
    <div className="mt-6 space-y-10">
      {/* 🔹 Graphique principal */}
      <div>
        <h3 className="text-lg font-semibold mb-2">
          Évolution des métriques globales et Minority Ratio
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={mainData}>
            <XAxis dataKey="version" />
            <YAxis yAxisId="left" domain={[0, 1]} />
            <YAxis
              yAxisId="right"
              orientation="right"
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="accuracy" stroke="#4CAF50" name="Accuracy" />
            <Line yAxisId="left" type="monotone" dataKey="f1" stroke="#2196F3" name="F1-score (pondéré)" />
            <Line yAxisId="left" type="monotone" dataKey="balanced_accuracy" stroke="#FF9800" name="Balanced Accuracy" />
            <Line yAxisId="left" type="monotone" dataKey="macro_f1" stroke="#9C27B0" name="Macro F1" />
            <Line yAxisId="right" type="monotone" dataKey="minority_ratio" stroke="#3F51B5" name="Minority Ratio (%)" strokeDasharray="5 5" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* 🔹 Graphique secondaire : Comparaison SMOTE vs ROS 
      <div>
        <h3 className="text-lg font-semibold mb-2">
          Comparaison des méthodes de rééquilibrage (SMOTE vs ROS) (Versions récentes → anciennes)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={validationData}>
            <XAxis dataKey="version" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="smote_accuracy" stroke="#00BCD4" name="SMOTE Accuracy" />
            <Line type="monotone" dataKey="smote_f1" stroke="#009688" name="SMOTE F1-score" />
            <Line type="monotone" dataKey="ros_accuracy" stroke="#E91E63" name="ROS Accuracy" />
            <Line type="monotone" dataKey="ros_f1" stroke="#795548" name="ROS F1-score" />
          </LineChart>
        </ResponsiveContainer>*/}
        {/* 🔹 Tableau récapitulatif 
        <HistoryMetricsSummary latestLog={latestLog} /> */}
      </div>
    
  );
};
