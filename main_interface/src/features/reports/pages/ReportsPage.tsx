// src/features/reports/pages/ReportsPage.tsx
import { ChartBarIcon, ExclamationTriangleIcon, WrenchScrewdriverIcon, KeyIcon, PresentationChartLineIcon, SparklesIcon, BellAlertIcon } from "@heroicons/react/24/outline";

import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip
} from "recharts";

//import { StockAlertsTable } from "../components/StockAlertsTable";
import { PieceStatistiquesCard } from "@/features/piecesUtilisees/components/PieceStatistiquesCard";
import { RecentLogsTable } from "../components/RecentLogsTable";
import { KpiCard } from "../components/KpiCard";
import { useReports } from "../hooks/useReports";
import { usePredictive } from "@/features/predictive/hooks/usePredictive";
import { useTrainingLogs } from "../../predictive/hooks/useTrainingLogs";

// 🔮 Nouveaux imports pour predictive
//import { useLatestTrainingLog } from "../../predictive/hooks/useTrainingLogs";
//import { HistoryMetricsChart } from "../../predictive/components/HistoryMetricsChart";
//import { MinorityVsBalancedChart } from "../../predictive/components/MinorityVsBalancedChart";

import { RiskHeatmap } from "@/features/predictive/components/RiskHeatmap";
import { UpcomingFailuresTimeline } from "@/features/predictive/components/UpcomingFailuresTimeline";
import { AccuracyChart } from "@/features/predictive/components/AccuracyChart";
import { WorkOrderStatusChart } from "../components/WorkOrderStatusChart";



export const ReportsPage = () => {
  const { data: reports, isLoading: loadingReports, error: errorReports } = useReports();
  //const { data: latestLog, isLoading: loadingTraining } = useLatestTrainingLog();
  const { data: predictive, isLoading: loadingPredictive, error: errorPredictive } = usePredictive();

  const { data: logs, isLoading: loadingLog } = useTrainingLogs();

  //if (loadingReports || loadingTraining || loadingPredictive || loadingLog) return <p>Chargement...</p>;
  if (loadingReports || loadingPredictive || loadingLog) return <p>Chargement...</p>;
  
  if (errorReports || errorPredictive) return <p>Erreur lors du chargement des données</p>;
  if (!reports || !predictive) return <p>Données indisponibles</p>;
  if (!logs) return <div className="text-gray-500">Aucun log trouvé.</div>;

  const { interventions, workorders, machines } = reports;

  // KPI logic (inchangé)
  const totalInterventions = interventions.total;
  const validatedInterventions = interventions.valide ?? 0;
  const percentValidated =
    totalInterventions > 0
      ? Math.round((validatedInterventions / totalInterventions) * 100)
      : 0;

  const avgResolutionTime = interventions.avg_duration ?? "—";
  const avgCompletionTime = workorders.avg_completion_time ?? "—";
  const etat = workorders.by_etat?.en_attente ?? 0;
  const totalWo = workorders.total;
  const woEnPanne = workorders.by_etat?.en_attente ?? 0;
  const percentWoEnattente =
    totalWo > 0 ? Math.round((woEnPanne / totalWo) * 100) : 0;

  const totalMachines = machines.total;
  const machinesEnPanne = machines.by_status?.PANNE ?? 0;
  const percentMachinesEnPanne =
    totalMachines > 0 ? Math.round((machinesEnPanne / totalMachines) * 100) : 0;

  const kpiData = [
  { metric: "Validation", value: percentValidated },
  { metric: "WO en attente", value: percentWoEnattente },
  { metric: "Machines en panne", value: percentMachinesEnPanne },
  { metric: "Durée résol.", value: avgResolutionTime || 0 },
  { metric: "Durée WO", value: avgCompletionTime || 0 },
];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
  {/* 🧠 HEADER */}
  <header className="text-center mb-12">
    <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-600 
                  text-white rounded-xl shadow-lg p-6 inline-flex items-center gap-3">
    <PresentationChartLineIcon className="w-8 h-8 text-white" />
    <h1 className="text-3xl font-extrabold">Tableau de bord intelligent</h1>
  </div>
    <p className="text-sm text-gray-500 mt-2">
      Anticiper, analyser et optimiser la maintenance
    </p>
  </header>

  {/* 📦 Analyses Graphiques */}
  <section className="mb-12 bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
    <h2 className="flex items-center gap-2 text-xl font-semibold text-indigo-600">
      <ChartBarIcon className="w-6 h-6 text-indigo-500" />
      Analyses Graphiques
    </h2>
    <div className="flex flex-col md:flex-row justify-center items-center gap-6">
      <div className="bg-gray-50 dark:bg-gray-900/50 rounded-xl p-8 hover:shadow-lg transition-all duration-300">
        <RadarChart cx={250} cy={200} outerRadius={150} width={600} height={400} data={kpiData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="metric" />
          <PolarRadiusAxis />
          <Tooltip />
          <Radar name="KPIs" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
        </RadarChart>
      </div>
      <div className="bg-gray-50 dark:bg-gray-900/50 rounded-xl p-8 hover:shadow-lg transition-all duration-300">
        <WorkOrderStatusChart />
      </div>
    </div>
  </section>

  {/* 🔑 Indicateurs clés */}
  <section className="mb-12">
    <h2 className="flex items-center gap-2 text-xl font-semibold text-purple-600">
      <KeyIcon className="w-6 h-6 text-purple-500" />
      Indicateurs clés
    </h2>
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
      {/* Exemple KPI */}
      <KpiCard
        title="Taux de validation"
        value={`${percentValidated}%`}
        description={`${validatedInterventions}/${totalInterventions} interventions`}
        color="bg-purple-100 text-purple-800 hover:scale-105 transition-transform"
      />
      <KpiCard
            title="Temps moyen résolution"
            value={avgResolutionTime}
            description="Durée moyenne des interventions"
            color="bg-blue-100 text-blue-800"
          />
          <KpiCard
            title="WorkOrders en attente"
            value={`${etat} ~~ ${percentWoEnattente}%`}
            description={`${woEnPanne}/${totalWo} WO`}
            color="bg-red-100 text-red-800"
          />
          <KpiCard
            title="Durée moyenne WO"
            value={avgCompletionTime}
            description="Temps moyen de clôture"
            color="bg-green-100 text-green-800"
          />
          <KpiCard
            title="Machines en panne"
            value={`${percentMachinesEnPanne}%`}
            description={`${machinesEnPanne}/${totalMachines} machines`}
            color="bg-yellow-100 text-yellow-800"
          />
      {/* autres KPI... */}
    </div>
  </section>

  {/* 🔮 Maintenance prédictive */}
  <section className="mb-12 text-center bg-white rounded-xl shadow-md p-6">
    <h2 className="text-xl font-semibold text-blue-700 flex items-center justify-center gap-2">
      <SparklesIcon className="w-6 h-6 text-blue-500" />
      Maintenance prédictive
    </h2>
    <div className="flex justify-center mt-4">
      <AccuracyChart logs={logs} />
    </div>
    <a href="/predictive" className="mt-4 inline-block text-sm font-medium text-blue-600 hover:underline hover:text-blue-800 transition-all duration-300">
      Voir détails dans Predictive →
    </a>
  </section>

  {/* ⚠️ Prospection du risque */}
  <section className="mb-12 text-center bg-white rounded-xl shadow-md p-6">
    <h2 className="text-xl font-semibold text-red-600 flex items-center justify-center gap-2">
      <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />
      Prospection du risque en temps réel
    </h2>
    <div className="flex justify-center mt-4">
      <RiskHeatmap data={predictive.machineRisks} />
    </div>
  </section>

  {/* 🛠️ Pannes anticipées */}
  <section className="mb-12 text-center bg-white rounded-xl shadow-md p-6">
    <h2 className="text-xl font-semibold text-yellow-600 flex items-center justify-center gap-2">
      <WrenchScrewdriverIcon className="w-6 h-6 text-yellow-500" />
      Pannes anticipées
    </h2>
    <div className="flex justify-center mt-4">
      <UpcomingFailuresTimeline data={predictive.predictions} />
    </div>
  </section>

  {/* 🚨 Alertes & activité */}
  <section className="mb-12">
    <h2 className="text-xl font-semibold text-orange-600 flex items-center justify-center gap-2">
      <BellAlertIcon className="w-6 h-6 text-orange-500"/>
      Coût & activité
    </h2>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-6">
      <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500 hover:shadow-lg transition-all duration-300">
        {/*<h3 className="text-lg font-bold mb-4">Alertes de stock</h3>
        <StockAlertsTable />*/}
        <PieceStatistiquesCard />
      </div>
      <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500 hover:shadow-lg transition-all duration-300">
        <h3 className="text-lg font-bold mb-4">Journaux récents</h3>
        <RecentLogsTable />
      </div>
    </div>
  </section>
</div>

  );
};
