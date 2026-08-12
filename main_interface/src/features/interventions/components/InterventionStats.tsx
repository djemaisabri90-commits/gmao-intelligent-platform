// src/features/interventions/components/InterventionStats.tsx

import { useInterventionStats } from '../hooks/useInterventions';

export const InterventionStats = () => {
  const { data: stats, isLoading, error } = useInterventionStats();

  if (isLoading) return <div className="p-4 text-gray-500">Chargement des statistiques...</div>;
  if (error) return <div className="p-4 text-red-500">Erreur lors du chargement</div>;

  const total =
    (stats?.en_attente ?? 0) +
    (stats?.en_cours ?? 0) +
    (stats?.termine ?? 0) +
    (stats?.valide ?? 0);

  const validated = stats?.valide ?? 0; //+ (stats?.clos ?? 0); ✅ inclure clos dans la progression globale
  const percentValidated = total > 0 ? Math.round((validated / total) * 100) : 0;

  return (
    <div className="mb-8">
      {/* Stats par état */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-yellow-100 p-4 rounded shadow text-center">
          <p className="text-lg font-bold text-yellow-800">{stats?.en_attente ?? 0}</p>
          <p className="text-sm text-yellow-700">En attente</p>
        </div>
        <div className="bg-blue-100 p-4 rounded shadow text-center">
          <p className="text-lg font-bold text-blue-800">{stats?.en_cours ?? 0}</p>
          <p className="text-sm text-blue-700">En cours</p>
        </div>
        <div className="bg-green-100 p-4 rounded shadow text-center">
          <p className="text-lg font-bold text-green-800">{stats?.termine ?? 0}</p>
          <p className="text-sm text-green-700">Terminées</p>
        </div>
        <div className="bg-purple-100 p-4 rounded shadow text-center">
          <p className="text-lg font-bold text-purple-800">{stats?.valide ?? 0}</p>
          <p className="text-sm text-purple-700">Validées</p>
        </div>
      </div>

      {/* Progress bar globale */}
      <div>
        <p className="text-sm font-medium text-gray-700 mb-2">
          Progression globale : {percentValidated}% validées/clôturées
        </p>
        <div className="w-full bg-gray-200 rounded h-4">
          <div
            className="bg-purple-600 h-4 rounded"
            style={{ width: `${percentValidated}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};
