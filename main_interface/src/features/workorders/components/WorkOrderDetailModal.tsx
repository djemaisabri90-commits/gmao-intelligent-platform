// src/features/workorders/components/WorkOrderDetailModal.tsx

//import { useState } from 'react';
import type { WorkOrderWithDetails } from '../types';
/*import { 
  useInterventionsByWorkorder, 
  useStartIntervention, 
  useFinishIntervention, 
  useValidateIntervention 
} from '../../interventions/hooks/useInterventions';
*/
import { 
  useInterventionsByWorkorder  
} from '../../interventions/hooks/useInterventions';


//import { usePieces } from '../../pieces/hooks/usePieces';
//import { toast } from 'react-hot-toast';

interface WorkOrderDetailModalProps {
  workorder: WorkOrderWithDetails | null;
  isOpen: boolean;
  onClose: () => void;
}

export const WorkOrderDetailModal = ({ workorder, isOpen, onClose }: WorkOrderDetailModalProps) => {
  //const [actionsRealisees, setActionsRealisees] = useState('');
  //const [selectedPieces, setSelectedPieces] = useState<number[]>([]);
  //const { data: interventions, refetch } = useInterventionsByWorkorder(workorder?.id ?? 0);
  const { data: interventions } = useInterventionsByWorkorder(workorder?.id ?? 0);

  /*const startIntervention = useStartIntervention();
  const finishIntervention = useFinishIntervention();
  const validateIntervention = useValidateIntervention();
  */
 //const { data: pieces } = usePieces();

  if (!isOpen || !workorder) return null;

  const intervention = interventions?.[0];
  /*
  const handleStart = async () => {
    if (!intervention) return toast.error("Aucune intervention associée");
    try {
      await startIntervention.mutateAsync(intervention.id);
      toast.success("Intervention démarrée");
      refetch();
      onClose();
    } catch {
      toast.error("Erreur lors du démarrage");
    }
  };
  
  const handleFinish = async () => {
    if (!intervention) return toast.error("Aucune intervention associée");
    try {
      await finishIntervention.mutateAsync({ id: intervention.id, actions_realisees: actionsRealisees });
      toast.success("Intervention terminée");
      refetch();
      onClose();
    } catch {
      toast.error("Erreur lors de la clôture");
    }
  };
  
  const handleValidate = async () => {
    if (!intervention) return toast.error("Aucune intervention associée");
    try {
      await validateIntervention.mutateAsync(intervention.id);
      toast.success("Intervention validée");
      refetch();
      onClose();
    } catch {
      toast.error("Erreur lors de la validation");
    }
  };
  */

  if (!interventions) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div className="bg-white p-4 rounded">Chargement de l'intervention...</div>
      </div>
    );
  }

  if (!intervention) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div className="bg-white p-4 rounded">Aucune intervention trouvée pour ce bon de travail.</div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" aria-hidden="true">
          <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={onClose}></div>
        </div>
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Détails du bon de travail #{workorder.id}
            </h3>
            <div className="mt-4 space-y-4">
              <p><strong>Machine :</strong> {workorder.machine_detail?.nom}</p>
              <p><strong>Description :</strong> {workorder.description}</p>
              <p><strong>Type :</strong> {workorder.type}</p>
              <p><strong>Priorité :</strong> {workorder.priorite}</p>
              <p><strong>État workorder :</strong> {workorder.etat}</p>
              <p><strong>Statut intervention :</strong> {intervention.etat}</p>
              <p>
                <strong>Techniciens assignés :</strong>{" "}
                {workorder.techniciens_detail?.length
                  ? workorder.techniciens_detail
                      .map(t => `${t.username}${t.categorie_detail ? ` (${t.categorie_detail.nom})` : ''}`)
                      .join(', ')
                  : '-'}
              </p>
              <p><strong>Expert :</strong> {workorder.expert_detail?.username ?? '-'}</p>

              {/* Actions réalisées */}
              {/*<div>
                <label className="block text-sm font-medium text-gray-700">Actions réalisées</label>
                <textarea
                  rows={3}
                  value={actionsRealisees}
                  onChange={(e) => setActionsRealisees(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Décrivez les actions effectuées..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Actions réalisées</label>
                <textarea
                rows={3}
                value={intervention.actions_realisees ?? "—"}
                disabled
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-gray-100 text-gray-600 sm:text-sm"
                />
              </div>
              */}


              {/* Pièces utilisées 
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Pièces utilisées</label>
                <div className="space-y-2 max-h-40 overflow-y-auto border rounded-md p-2">
                  {pieces?.map(piece => (
                    <label key={piece.id} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={selectedPieces.includes(piece.id)}
                        onChange={() => setSelectedPieces(prev =>
                          prev.includes(piece.id) ? prev.filter(id => id !== piece.id) : [...prev, piece.id]
                        )}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span>{piece.nom} (réf: {piece.reference}) - Stock: {piece.stock_disponible}</span>
                    </label>
                  ))}
                </div>
              </div>
              */}
              
              {/* Boutons d'action 
              <div className="flex flex-wrap gap-2 mt-4">
                {intervention.etat === 'en_attente' && (
                  <button onClick={handleStart} className="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded-md text-sm">
                    Démarrer l'intervention
                  </button>
                )}
                {intervention.etat === 'en_cours' && (
                  <button onClick={handleFinish} className="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm">
                    Terminer l'intervention
                  </button>
                )}
                {intervention.etat === 'termine' && (
                  <button onClick={handleValidate} className="bg-purple-600 hover:bg-purple-700 text-white py-1 px-3 rounded-md text-sm">
                    Valider l'intervention
                  </button>
                )}
              </div>
              */}
            </div>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              onClick={onClose}
              className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
            >
              Fermer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
