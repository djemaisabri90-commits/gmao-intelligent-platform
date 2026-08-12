// src/features/predictive/pages/PredictiveDashboard.tsx
import { useTrainingLogs } from "../hooks/useTrainingLogs";
import { AccuracyChart } from "../components/AccuracyChart";
import { ClassDistributionPie } from "../components/ClassDistributionPie";
import { ValidationMetricsChart } from "../components/ValidationMetricsChart";
import { RetrainButton } from "../components/RetrainButton";
import { useRetrainModel } from "../hooks/useRetrainModel";
import { useExportLog } from "../hooks/useExportLog"; // ✅ nouveau hook
import { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ pour navigation
import { LogDetailsModal } from "../components/LogDetailsModal";
import type { TrainingLog } from "../types";
import { HistoryMetricsChart } from "../components/HistoryMetricsChart";
import { MinorityVsBalancedChart } from "../components/MinorityVsBalancedChart";
//import { HistoryMetricsSummary } from "../components/HistoryMetricsSummary";

import { ArrowPathIcon, ChartPieIcon } from "@heroicons/react/24/outline";
/*
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
*/
export const PredictiveDashboard = () => {
  const { data: logs, isLoading } = useTrainingLogs();
  const { mutate, isPending } = useRetrainModel();
  const { mutate: exportLog, isPending: isExporting } = useExportLog();
  const [selectedVersion, setSelectedVersion] = useState<number | null>(null);
  const [modalLog, setModalLog] = useState<TrainingLog | null>(null);
  const navigate = useNavigate();

  if (isLoading) return <div className="text-gray-500">Chargement...</div>;
  if (!logs) return <div className="text-gray-500">Aucun log trouvé.</div>;

  const latest = logs[0];

  // 🔄 Trier les logs du plus récent au plus ancien
  //const sortedLogs = [...logs].sort((a, b) => b.model_version - a.model_version);
  // ✅ Définir latestLog
  //const latestLog = sortedLogs[0];

  /*const validationData = sortedLogs.map((log) => ({
    version: `v${log.model_version}`,
    smote_accuracy: log.validation_metrics?.SMOTE?.accuracy ?? 0,
    smote_f1: log.validation_metrics?.SMOTE?.["weighted avg"]?.["f1-score"] ?? 0,
    ros_accuracy: log.validation_metrics?.RandomOverSampler?.accuracy ?? 0,
    ros_f1: log.validation_metrics?.RandomOverSampler?.["weighted avg"]?.["f1-score"] ?? 0,
  }));
  */
  return (
    <div className="space-y-8">
      <h1 className="flex items-center justify-center gap-3 
               px-6 py-3 bg-indigo-100 text-indigo-700 
               rounded-full shadow-lg text-3xl font-extrabold 
                 mx-auto w-fit tracking-wide">
        <img
              src="/src/assets/ia.png"
              alt="Logo GMAO Délice Groupe"
              className="h-10"
            /> Tableau de bord prédictif
      </h1>

      {/* Bouton global */}
      {/* Section actions */}
      <section className="bg-white rounded-xl shadow-md p-6 mx-auto w-full md:w-3/4 text-center space-y-6">
        <h2 className="flex items-center justify-center gap-2 
               text-lg font-semibold text-indigo-700 mb-4">
          <ArrowPathIcon className="w-5 h-5 text-indigo-600" />
            Actions de réentraînement
        </h2>
      <div className="flex justify-center">
        <RetrainButton />
      </div>

      {/* Combo box pour réentraîner une version spécifique */}
      <div className="flex flex-col md:flex-row items-center justify-center gap-4 mt-4">
        <select
          className="border rounded px-3 py-2 w-full md:w-auto"
          value={selectedVersion ?? ""}
          onChange={(e) => setSelectedVersion(Number(e.target.value))}
        >
          <option value="">-- Choisir une version --</option>
          {logs.map((log) => (
            <option key={log.model_version} value={log.model_version}>
              Version {log.model_version} ({log.trained_at})
            </option>
          ))}
        </select>
        <button
          onClick={() => {
            if (selectedVersion) {
              mutate({ scratch: false }); // ⚡ tu peux adapter pour cibler une version
            }
          }}
          disabled={isPending || !selectedVersion}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {isPending ? "Réentraînement en cours..." : "Réentraîner cette version"}
        </button>
      </div>
      </section>

{/* Section charts */}
  <section className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all mx-auto w-full md:w-3/4">
    
      <AccuracyChart logs={logs} />
    
  </section>

  <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all">
      <h2 className="flex items-center justify-center gap-2 
               text-lg font-semibold text-indigo-700 mb-4">
  <ChartPieIcon className="w-5 h-5 text-indigo-600" />
  Répartition des classes du dataset
</h2>
      <ClassDistributionPie log={latest} />
    </div>

    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all">
      <ValidationMetricsChart log={latest} />
    </div>
  </section>

      {modalLog && (
      <LogDetailsModal
      log={modalLog}
      onClose={() => setModalLog(null)} // ✅ callback pour fermer
      />
      )}

      {/* Tableau modernisé avec onRowClick */}
      <section className="bg-white rounded-xl shadow-md p-6 mt-8">
    <h2 className="text-lg font-semibold text-indigo-700 mb-4">
      📊 Historique des entraînements
    </h2>
    <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 bg-white">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Version</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Accuracy</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">F1 Score</th>
              {/* ✅ nouvelle colonne */}
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Minority Ratio</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {logs.map((log) => (
              <tr key={log.model_version} className="hover:bg-gray-50 transition"
              onClick={() => setModalLog(log)} // ✅ onRowClick ouvre le modal
              >
                <td className="px-6 py-4">{log.model_version}</td>
                <td className="px-6 py-4">{log.trained_at}</td>
                <td className="px-6 py-4 text-green-600 font-semibold">{log.accuracy}</td>
                <td className="px-6 py-4 text-blue-600 font-semibold">{log.f1_score}</td>
                {/* ✅ affichage du minority_ratio */}
                <td className="px-6 py-4">
        <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded">
          {(log.minority_ratio ?? 0) * 100}%
        </span>
      </td>
                <td className="px-6 py-4">
                  {log.success ? (
                    <span className="px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full">
                      ✅ {log.status} {/*Succès*/}
                    </span>
                  ) : (
                    <span className="px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full">
                      ❌ {log.status} {/*Échec*/}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 flex gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation(); // ✅ éviter de déclencher le modal
                      exportLog({ version: log.model_version, format: "csv" });
                    }}
                    disabled={isExporting}
                    className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
                  >
                    Exporter CSV
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      exportLog({ version: log.model_version, format: "json" });
                    }}
                    disabled={isExporting}
                    className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                  >
                    Exporter JSON
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      exportLog({ version: log.model_version, format: "xlsx" });
                    }}
                    disabled={isExporting}
                    className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Exporter Excel
                  </button>
                  
                  
                     
                        {/* Redirection vers page dédiée */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/predictive/train-history/${log.model_version}`);
                    }}
                    className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                  >
                    Détails
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
  </section>
  
        <HistoryMetricsChart logs={logs} />
        {/* 🔹 Graphique secondaire : Comparaison SMOTE vs ROS */}
        {/*
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
                </ResponsiveContainer>
              </div>
              */}
        {/* 🔹 Tableau récapitulatif */}
        {/*<HistoryMetricsSummary latestLog={latestLog} />*/}
        <MinorityVsBalancedChart logs={logs} />
      </div>
    
  );
};
