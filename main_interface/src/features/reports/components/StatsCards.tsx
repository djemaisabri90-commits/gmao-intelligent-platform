// src/features/reports/components/StatsCards.tsx

import { useWorkOrderStats } from "@/features/workorders/hooks/useWorkOrders";
import { useMachineStats } from "@/features/machines/hooks/useMachines";
import { useInterventionStats } from "@/features/interventions/hooks/useInterventions";

export const StatsCards = () => {
  const { data: woStats, isLoading: woLoading } = useWorkOrderStats();
  const { data: machineStats, isLoading: machineLoading } = useMachineStats();
  const { data: interStats, isLoading: interLoading } = useInterventionStats();

  if (woLoading || machineLoading || interLoading) {
    return <div className="text-gray-500">Chargement des statistiques...</div>;
  }

  const totalWO = woStats?.total ?? 0;
  const woPending = woStats?.by_etat.en_attente ?? woStats?.pending_count ?? 0;

  const totalMachines = machineStats?.total ?? 0;
  const machinesEnPanne = machineStats?.by_status?.PANNE ?? 0;

  const totalInterventions = interStats?.total ?? 0;
  const interventionsEnCours = interStats?.en_cours ?? 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-12 mb-12">
      {/* WorkOrders */}
      <div className="bg-white rounded-lg shadow p-6 min-w-[300px] hover:shadow-md transition-shadow">
        <h3 className="text-sm font-semibold text-gray-500">Bons de travail</h3>
        <p className="text-4xl font-bold text-blue-600 mt-2">{totalWO}</p>
        <p className="text-sm text-gray-600 mt-1">En attente : {woPending}</p>
      </div>

      {/* Machines */}
      <div className="bg-white rounded-lg shadow p-6 min-w-[300px] hover:shadow-md transition-shadow">
        <h3 className="text-sm font-semibold text-gray-500">Machines</h3>
        <p className="text-4xl font-bold text-orange-600 mt-2">{totalMachines}</p>
        <p className="text-sm text-gray-600 mt-1">En panne : {machinesEnPanne}</p>
      </div>

      {/* Interventions */}
      <div className="bg-white rounded-lg shadow p-6 min-w-[300px] hover:shadow-md transition-shadow">
        <h3 className="text-sm font-semibold text-gray-500">Interventions</h3>
        <p className="text-4xl font-bold text-green-600 mt-2">{totalInterventions}</p>
        <p className="text-sm text-gray-600 mt-1">En cours : {interventionsEnCours}</p>
      </div>

      {/* Stock Alerts 
      <div className="bg-white rounded-lg shadow p-6 min-w-[300px] hover:shadow-md transition-shadow">
        <h3 className="text-sm font-semibold text-gray-500">Alertes stock</h3>
        <p className="text-4xl font-bold text-red-600 mt-2">À venir</p>
      </div>
      */}
    </div>
  );
};
