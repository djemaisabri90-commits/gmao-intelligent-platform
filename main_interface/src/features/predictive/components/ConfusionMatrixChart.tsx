// src/features/predictive/components/ConfusionMatrixChart.tsx
import type { FC } from "react";

type Props = {
  matrix: number[][];   // matrice carrée [[TN, FP], [FN, TP]]
  labels: string[];     // noms des classes (ex: ["0", "1"])
};

export const ConfusionMatrixChart: FC<Props> = ({ matrix, labels }) => {
  return (
    <div className="overflow-x-auto mt-6">
      <h3 className="text-lg font-semibold mb-2">Matrice de confusion</h3>
      <table className="min-w-full border border-gray-300 text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="border px-2 py-1">Classe réelle ↓ / prédite →</th>
            {labels.map((label) => (
              <th key={label} className="border px-2 py-1">{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i}>
              <td className="border px-2 py-1 font-semibold">{labels[i]}</td>
              {row.map((val, j) => (
                <td key={j} className="border px-2 py-1 text-center">{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
