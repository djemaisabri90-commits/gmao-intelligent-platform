import { useState } from 'react';
import toast from 'react-hot-toast';
import type { InterventionWithDetails } from '../types';
import {
  useStartIntervention,
  useFinishIntervention,
  useValidateIntervention,
} from '../hooks/useInterventions';
import { PieceReservationModal } from '@/features/piecesUtilisees/components/PieceReservationModal';

import { usePieces } from '@/features/pieces/hooks/usePieces';

interface Props {
  intervention: InterventionWithDetails;
}

export const InterventionModal = ({ intervention }: Props) => {
  const startMutation = useStartIntervention();
  const finishMutation = useFinishIntervention();
  const validateMutation = useValidateIntervention();

  const [showModal, setShowModal] = useState(false);
  const [actionsText, setActionsText] = useState('');
  const [errorMessage, setErrorMessage] = useState("");

  const [showReservationModal, setShowReservationModal] = useState(false);

  //const [selectedPieces, setSelectedPieces] = useState<any[]>([]);

  const { data: pieces } = usePieces();

  const handleFinish = () => {
    // action requise
    if (!actionsText.trim()) {
      setErrorMessage("Ce champ est obligatoire pour terminer l’intervention."); // ✅ validation
      return;
    }
    finishMutation.mutate(
      { id: intervention.id, actions_realisees: actionsText },
      {
        onSuccess: () => {
          toast.success('Intervention terminée avec succès ✅');
          setShowModal(false);
          setActionsText('');
          setErrorMessage('');
        },
        onError: () => {
          toast.error('Erreur lors de la terminaison ❌');
        },
      }
    );
  };

  // Badge dynamique selon etat
  const badgeClass =
    intervention.etat === 'en_cours'
      ? 'bg-blue-100 text-blue-800'
      : intervention.etat === 'termine'
      ? 'bg-green-100 text-green-800'
      : intervention.etat === 'valide'
      ? 'bg-purple-100 text-purple-800'
      : 'bg-yellow-100 text-yellow-800';

  return (
    <div className="p-4 bg-white shadow rounded">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold">Intervention #{intervention.id}</h3>
        <span className={`px-2 py-1 text-xs rounded-full ${badgeClass}`}>
          {intervention.etat}
        </span>
      </div>

      <p><strong>Technicien:</strong>{" "}
        {intervention.techniciens_detail && intervention.techniciens_detail.length > 0
          ? intervention.techniciens_detail
            .map(t => `${t.username}${t.role ? ` (${t.role})` : ''}`)
            .join(', ')
          : '-'}
      </p>
      <p><strong>Machine:</strong> {intervention.workorder_detail?.machine_detail?.nom}</p>
      <p><strong>Type:</strong> {intervention.type_intervention}</p>
      <p><strong>Priorité:</strong> {intervention.priorite}</p>

      {/* Boutons d’action */}
      <div className="mt-4 flex gap-2">
        {intervention.etat === 'en_attente' && (
          <button
            className="px-3 py-1 bg-blue-500 text-white rounded"
            onClick={() => setShowReservationModal(true)}
              /*startMutation.mutate(intervention.id, {
                onSuccess: () => toast.success('Intervention démarrée 🚀'),
                onError: () => toast.error('Erreur lors du démarrage ❌'),
              })*/           
          >
            Démarrer
          </button>        
        )}

        {intervention.etat === 'en_cours' && (
          <button
            className="px-3 py-1 bg-orange-500 text-white rounded"
            onClick={() => setShowModal(true)}
          >
            Terminer
          </button>
        )}

        {intervention.etat === 'termine' && !intervention.is_locked && (
          <button
            className="px-3 py-1 bg-green-600 text-white rounded"
            onClick={() =>
              validateMutation.mutate(intervention.id, {
                onSuccess: () => toast.success('Intervention validée 🎉'),
                onError: () => toast.error('Erreur lors de la validation ❌'),
              })
            }
          >
            Valider
          </button>
        )}
        
      </div>
      <PieceReservationModal
  isOpen={showReservationModal}
  onClose={() => setShowReservationModal(false)}
  pieces={pieces ?? []}
  onConfirm={(reservations) => {
    startMutation.mutate(
      {
        id: intervention.id,
        pieces: reservations,
      },
      {
        onSuccess: () => {
          toast.success(
            "Intervention démarrée et pièces réservées 🚀"
          );

          setShowReservationModal(false);
        },

        onError: (error: any) => {
          toast.error(
            error?.response?.data?.detail ||
            "Erreur lors du démarrage"
          );
        },
      }
    );
  }}
/>

      {/* Modale pour actions réalisées */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white p-6 rounded shadow-lg w-96">
            <h4 className="text-lg font-semibold mb-4">Actions réalisées</h4>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleFinish();
              }}
            >
            <textarea
              value={actionsText}
              onChange={(e) => setActionsText(e.target.value)}
              className="w-full border rounded p-2 mb-4"
              rows={4}
              placeholder="Décrivez les actions effectuées..."
              required
            />
            {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}
            <div className="flex justify-end gap-2">
              <button
                type="button"
                className="px-3 py-1 bg-gray-400 text-white rounded"
                onClick={() => setShowModal(false)}
              >
                Annuler
              </button>
              <button
                type="submit"
                className="px-3 py-1 bg-orange-600 text-white rounded"
              >
                Confirmer
              </button>
            </div>
            
      
      </form>
            </div>

          </div>
        
      )}
    </div>
  );
};
