// src/features/predictive/components/HistoryMetricsSummary.tsx
/*import type { FC } from "react";
import type { TrainingLog } from "../types";

type Props = {
  latestLog: TrainingLog;
};

const getCellColor = (value: number) => {
  if (value >= 0.8) return "bg-green-100 text-green-800 font-semibold";
  if (value >= 0.6) return "bg-yellow-100 text-yellow-800 font-semibold";
  return "bg-red-100 text-red-800 font-semibold";
};

export const HistoryMetricsSummary: FC<Props> = ({ latestLog }) => {
  if (!latestLog) return null;

  const smote = latestLog.validation_metrics?.SMOTE;
  const ros = latestLog.validation_metrics?.RandomOverSampler;

  return (
    <div className="mt-8">
      <h3 className="text-lg font-semibold mb-4">
        Tableau récapitulatif des dernières métriques
      </h3>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300 text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-4 py-2">Méthode</th>
              <th className="border px-4 py-2">Accuracy</th>
              <th className="border px-4 py-2">F1-score</th>
              <th className="border px-4 py-2">Balanced Accuracy</th>
              <th className="border px-4 py-2">Macro F1</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border px-4 py-2 font-medium">Global</td>
              <td className={`border px-4 py-2 ${getCellColor(latestLog.accuracy)}`}>
                {latestLog.accuracy}
              </td>
              <td className={`border px-4 py-2 ${getCellColor(latestLog.f1_score)}`}>
                {latestLog.f1_score}
              </td>
              <td className={`border px-4 py-2 ${getCellColor(latestLog.balanced_accuracy ?? 0)}`}>
                {latestLog.balanced_accuracy}
              </td>
              <td className={`border px-4 py-2 ${getCellColor(latestLog.macro_f1 ?? 0)}`}>
                {latestLog.macro_f1}
              </td>
            </tr>
            {smote && (
              <tr>
                <td className="border px-4 py-2 font-medium">SMOTE</td>
                <td className={`border px-4 py-2 ${getCellColor(smote.accuracy ?? 0)}`}>
                  {smote.accuracy}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(smote["weighted avg"]?.["f1-score"] ?? 0)}`}>
                  {smote["weighted avg"]?.["f1-score"]}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(smote["macro avg"]?.["recall"] ?? 0)}`}>
                  {smote["macro avg"]?.["recall"]}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(smote["macro avg"]?.["f1-score"] ?? 0)}`}>
                  {smote["macro avg"]?.["f1-score"]}
                </td>
              </tr>
            )}
            {ros && (
              <tr>
                <td className="border px-4 py-2 font-medium">ROS</td>
                <td className={`border px-4 py-2 ${getCellColor(ros.accuracy ?? 0)}`}>
                  {ros.accuracy}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(ros["weighted avg"]?.["f1-score"] ?? 0)}`}>
                  {ros["weighted avg"]?.["f1-score"]}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(ros["macro avg"]?.["recall"] ?? 0)}`}>
                  {ros["macro avg"]?.["recall"]}
                </td>
                <td className={`border px-4 py-2 ${getCellColor(ros["macro avg"]?.["f1-score"] ?? 0)}`}>
                  {ros["macro avg"]?.["f1-score"]}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
*/