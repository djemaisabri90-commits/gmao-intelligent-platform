// src/features/predictive/components/ValidationMetricsTable.tsx
//import type { TrainingLog } from "../types";
/*
type MetricValues = {
  precision?: number;
  recall?: number;
  ["f1-score"]?: number;
  support?: number;
}

export const ValidationMetricsTable = ({ log }: { log: TrainingLog }) => {
  if (!log.validation_metrics) return null;

  return (
    <div className="mt-6 space-y-4">
      {Object.entries(log.validation_metrics).map(([method, metrics]) => (
        <div key={method} className="border rounded p-4 shadow-sm bg-white">
          <h3 className="text-lg font-semibold mb-2">Méthode : {method}</h3>
          <table className="min-w-full text-sm border border-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-2 py-1 border">Classe</th>
                <th className="px-2 py-1 border">Precision</th>
                <th className="px-2 py-1 border">Recall</th>
                <th className="px-2 py-1 border">F1-score</th>
                <th className="px-2 py-1 border">Support</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(metrics as Record<string, MetricValues>).map(([cls, values]) =>
                ["accuracy", "macro avg", "weighted avg"].includes(cls) ? null : (
                  <tr key={cls}>
                    <td className="border px-2 py-1">{cls}</td>
                    <td className="border px-2 py-1">{values["precision"]?.toFixed(3)}</td>
                    <td className="border px-2 py-1">{values["recall"]?.toFixed(3)}</td>
                    <td className="border px-2 py-1">{values["f1-score"]?.toFixed(3)}</td>
                    <td className="border px-2 py-1">{values["support"]}</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
          
          <p className="mt-2 text-sm text-gray-600">
            Accuracy globale : {metrics["accuracy"]?.toFixed(3)}
          </p>
        </div>
      ))}
    </div>
  );
};
*/


// src/features/predictive/components/ValidationMetricsTable.tsx
import type { TrainingLog, ClassMetrics, ValidationResult } from "../types";

export const ValidationMetricsTable = ({ log }: { log: TrainingLog }) => {
  if (!log.validation_metrics) return null;

  return (
    <div className="mt-6 space-y-4">
      {Object.entries(log.validation_metrics).map(([method, metrics]) => {
        const result = metrics as ValidationResult;
        const report = result.report;

        return (
          <div key={method} className="border rounded p-4 shadow-sm bg-white">
            <h3 className="text-lg font-semibold mb-2">Méthode : {method}</h3>
            <table className="min-w-full text-sm border border-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-2 py-1 border">Classe / Moyenne</th>
                  <th className="px-2 py-1 border">Precision</th>
                  <th className="px-2 py-1 border">Recall</th>
                  <th className="px-2 py-1 border">F1-score</th>
                  <th className="px-2 py-1 border">Support</th>
                </tr>
              </thead>
              <tbody>
                {/* ✅ Classes */}
                {Object.entries(report.classes ?? {}).map(([cls, values]) => {
                  const v = values as ClassMetrics;
                  return (
                    <tr key={cls}>
                      <td className="border px-2 py-1">{cls}</td>
                      <td className="border px-2 py-1">{typeof v.precision === "number" ? v.precision.toFixed(3) : "-"}</td>
                      <td className="border px-2 py-1">{typeof v.recall === "number" ? v.recall.toFixed(3) : "-"}</td>
                      <td className="border px-2 py-1">{typeof v["f1-score"] === "number" ? v["f1-score"].toFixed(3) : "-"}</td>
                      <td className="border px-2 py-1">{v.support ?? "-"}</td>
                    </tr>
                  );
                })}

                {/* ✅ Accuracy globale */}
                <tr className="bg-gray-50 font-semibold">
                  <td className="border px-2 py-1">Accuracy globale</td>
                  <td className="border px-2 py-1" colSpan={4}>
                    {report.accuracy?.toFixed(3) ?? "-"}
                  </td>
                </tr>

                {/* ✅ Moyennes */}
                {["macro avg", "weighted avg"].map(avgKey => {
                  const avg = report[avgKey] as ClassMetrics | undefined;
                  if (!avg) return null;
                  return (
                    <tr key={avgKey} className="bg-gray-50">
                      <td className="border px-2 py-1">{avgKey}</td>
                      <td className="border px-2 py-1">{avg.precision?.toFixed(3) ?? "-"}</td>
                      <td className="border px-2 py-1">{avg.recall?.toFixed(3) ?? "-"}</td>
                      <td className="border px-2 py-1">{avg["f1-score"]?.toFixed(3) ?? "-"}</td>
                      <td className="border px-2 py-1">{avg.support ?? "-"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            <p className="mt-2 text-sm text-gray-600">
              CV mean : {result.cv_mean.toFixed(3)} | Scores : {result.cv_scores.map(s => s.toFixed(3)).join(", ")}
            </p>
          </div>
        );
      })}
    </div>
  );
};
