import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { predictiveClient } from "@/api/client";

import { AccuracyChart } from "../components/AccuracyChart";
import { ValidationMetricsChart } from "../components/ValidationMetricsChart";
import { ClassDistributionPie } from "../components/ClassDistributionPie";
import { ValidationMetricsTable } from "../components/ValidationMetricsTable";
import { ConfusionMatrixChart } from "../components/ConfusionMatrixChart";

import type { TrainingLog } from "../types";

export const LogDetailsPage = () => {
  const navigate = useNavigate();
  const { version } = useParams<{ version: string }>();

  const { data: log, isLoading } = useQuery<TrainingLog>({
    queryKey: ["logDetails", version],
    queryFn: async () => {
      const { data } = await predictiveClient.get(`/train-history/${version}/`);
      return data;
    },
  });

  if (isLoading) return <p>Chargement...</p>;
  if (!log) return <p className="text-red-500">Log introuvable {version}</p>;

  return (
    <div className="p-6 space-y-4">
      <button
        onClick={() => navigate("/predictive")}
        className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
      >
        ← Retour au dashboard
      </button>

      <h1 className="text-2xl font-bold">Détails du modèle v{log.model_version}</h1>
      <p>Date : {log.trained_at}</p>

      {/* ✅ Affichage des métriques globales enrichies */}
      
      <div className="space-y-1">
        <p>Accuracy : {log.accuracy}</p>
        <p>Precision (pondérée) : {log.precision}</p>
        <p>Recall (pondérée) : {log.recall}</p>
        <p>F1 Score (pondéré) : {log.f1_score}</p>
        <p>Balanced Accuracy : {log.balanced_accuracy ?? "-"}</p>
        <p>Macro F1 : {log.macro_f1 ?? "-"}</p>
        <p>
          Minority Ratio :{" "}
          <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded">
            {(log.minority_ratio ?? 0) * 100}%
          </span>
        </p>
      </div>


      {/* ✅ Graphiques et tableaux */}
      <AccuracyChart logs={[log]} />
      <ClassDistributionPie log={log} />
      <ValidationMetricsChart log={log} />
      <ValidationMetricsTable log={log} />

      {/* ✅ Matrice de confusion */}
      {log.confusion_matrix && (
        <ConfusionMatrixChart
          matrix={log.confusion_matrix}
          labels={Object.keys(log.class_distribution)}
        />
      )}
    </div>
  );
};
