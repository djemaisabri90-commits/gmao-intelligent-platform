//src/features/interventions/pages/InterventionDetail.tsx
import React, { useState } from 'react';
import InterventionPiecesList from '../../piecesUtilisees/components/InterventionPiecesList';
import InterventionPieceForm from '../../piecesUtilisees/components/InterventionPieceForm';
import type { PieceUtilisee } from '../../piecesUtilisees/types';

interface InterventionDetailProps {
  interventionId: number;
}

const InterventionDetail: React.FC<InterventionDetailProps> = ({ interventionId }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingPieceUtilisee, setEditingPieceUtilisee] = useState<PieceUtilisee | null>(null);

  const handleAdd = () => {
    setEditingPieceUtilisee(null);
    setShowForm(true);
  };

  const handleEdit = (pieceUtilisee: PieceUtilisee) => {
    setEditingPieceUtilisee(pieceUtilisee);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingPieceUtilisee(null);
  };

  return (
    <div>
      <h2>Détails de l’intervention #{interventionId}</h2>

      {!showForm && (
        <>
          <button onClick={handleAdd}>➕ Ajouter une pièce utilisée</button>
          <InterventionPiecesList
            interventionId={interventionId}
            onEdit={handleEdit}
          />
        </>
      )}

      {showForm && (
        <div style={{ marginTop: '20px' }}>
          <InterventionPieceForm
            interventionId={interventionId}
            pieceUtilisee={editingPieceUtilisee ?? undefined}
            onSuccess={handleCloseForm}
          />
          <button onClick={handleCloseForm} style={{ marginTop: '10px' }}>
            Annuler
          </button>
        </div>
      )}
    </div>
  );
};

export default InterventionDetail;
