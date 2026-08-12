// src/features/interventions/pages/InterventionsPage.tsx

import { useAuth } from '../../auth/hooks/useAuth';
//import { useInterventions, useInterventionNotifications } from '../hooks/useInterventions';
import { useInterventions} from '../hooks/useInterventions';

import { InterventionModal } from '../components/InterventionModal';
import { InterventionStats } from '../components/InterventionStats';

export const InterventionsPage = () => {
  const { user } = useAuth();
  const role = user?.role as 'technicien' | 'admin' | 'expert';
  const currentUsername = user?.username;
  /*
  const notifications = useInterventionNotifications();
  */
  const { data: interventions, isLoading, error } = useInterventions();
  
  // Filtrage par rôle
  const filteredInterventions = interventions?.filter((interv) => {
    if (role === "technicien") {
      // techniciens_detail est un tableau → vérifier si le technicien courant est dedans
      return (
        interv.techniciens_detail?.some(t => t.id === user?.id) ||
        interv.workorder_detail?.techniciens_detail?.some(t => t.id === user?.id)
    );
    }

    if (role === "expert" || role === "admin") {
      return true; // expert et admin voient tout
    }

    return false; // par défaut, rien
  });

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      {/* En-tête */}
      <header className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">
          Tableau des interventions
        </h1>
        <div className="text-right">
          <p className="text-lg font-semibold text-gray-700">
            {currentUsername}
          </p>
          <p className="text-sm text-gray-500">Rôle : {role}</p>
        </div>
      </header>

      {/* Statistiques globales */}
      <InterventionStats />

      {/* Notifications en temps réel 
      {notifications.map((notif, idx) => (
        <div key={idx} className="bg-yellow-100 p-2 rounded mb-2">
          {notif.message} (Machine: {notif.machine})
        </div>
      ))}
      */}

      {/* Liste des interventions */}
      {isLoading && <p>Chargement...</p>}
      {error && <p>Erreur: {(error as Error).message}</p>}
      {!isLoading && !error && filteredInterventions?.length === 0 && (
        <p>Aucune intervention disponible</p>
      )}

      <div className="grid gap-4">
        {filteredInterventions?.map((interv) => (
          <InterventionModal key={interv.id} intervention={interv} />
        ))}
      </div>
    </div>
  );
};
