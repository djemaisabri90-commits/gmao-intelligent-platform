import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip
} from "recharts";

import { useReports } from "../hooks/useReports";


const { data: reports } = useReports();

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

export const KpiRadarChart = () => (
  <div className="bg-white rounded-lg shadow p-6">
    <h3 className="text-lg font-bold mb-4">Indicateurs clés</h3>
    <RadarChart
      cx={200}
      cy={200}
      outerRadius={150}
      width={400}
      height={400}
      data={kpiData}
    >
      <PolarGrid />
      <PolarAngleAxis dataKey="metric" />
      <PolarRadiusAxis />
      <Tooltip />
      <Radar
        name="KPIs"
        dataKey="value"
        stroke="#8884d8"
        fill="#8884d8"
        fillOpacity={0.6}
      />
    </RadarChart>
  </div>
);
