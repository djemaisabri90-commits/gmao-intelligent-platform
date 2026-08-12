// src/features/predictive/components/MinorityVsBalancedChart.tsx
/* 
ici on va comparer les voisins
--avec le nuage de points
== SCATTER PLOT
*/

//Corrélation directe entre Minority Ratio et Balanced Accuracy (nuage de points).
/*
une coloration des points par statut (succès/échec)
dans ton scatter plot va rendre
la lecture beaucoup plus intuitive :
tu verras immédiatement quels runs ont abouti
et lesquels ont échoué,
tout en comparant Minority Ratio et Balanced Accuracy.
*/

// src/features/predictive/components/MinorityVsBalancedChart.tsx
import type { FC } from "react";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import type { TrainingLog } from "../types";

type Props = {
  logs: TrainingLog[];
};

export const MinorityVsBalancedChart: FC<Props> = ({ logs }) => {
  if (!logs || logs.length === 0) return null;

  // Séparer les runs réussis et échoués
  const successData = logs
    .filter((log) => log.success)
    .map((log) => ({
      minority_ratio: (log.minority_ratio ?? 0) * 100,
      balanced_accuracy: log.balanced_accuracy ?? 0,
      version: `v${log.model_version}`,
    }));

  const failedData = logs
    .filter((log) => !log.success)
    .map((log) => ({
      minority_ratio: (log.minority_ratio ?? 0) * 100,
      balanced_accuracy: log.balanced_accuracy ?? 0,
      version: `v${log.model_version}`,
    }));

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">
        Minority Ratio vs Balanced Accuracy
      </h3>
      <ResponsiveContainer width="100%" height={350}>
        <ScatterChart>
          <CartesianGrid />
          <XAxis
            type="number"
            dataKey="minority_ratio"
            name="Minority Ratio (%)"
            unit="%"
          />
          <YAxis
            type="number"
            dataKey="balanced_accuracy"
            name="Balanced Accuracy"
            domain={[0, 1]}
          />
          <Tooltip cursor={{ strokeDasharray: "3 3" }}
            formatter={(value, name) => {
              if (name === "minority_ratio") {
                return [`${value}%`, "Minority Ratio"];
              }
              if (name === "balanced_accuracy") {
                return [value, "Balanced Accuracy"];
              }
              return [value, name];
            }}
            labelFormatter={(label) => `Version: ${label}`}
          />
          {/* ✅ Points verts pour succès */}
          <Scatter
            name="Succès"
            data={successData}
            fill="#4CAF50"
            shape="circle"
          />
          {/* ✅ Points rouges pour échec */}
          <Scatter
            name="Échec"
            data={failedData}
            fill="#F44336"
            shape="triangle"
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};
