//src/features/piecesUtilisees/components/InterventionPiecesList.tsx

import React from 'react';
import { useInterventionPieces, useDeletePieceUtilisee } from '../hooks/usePiecesUtilisees';
import type { PieceUtilisee } from '../types';

interface InterventionPiecesListProps {
  interventionId: number;
  onEdit?: (pieceUtilisee: PieceUtilisee) => void;
}

const InterventionPiecesList: React.FC<InterventionPiecesListProps> = ({ interventionId, onEdit }) => {
  const { data: piecesUtilisees, isLoading, isError } = useInterventionPieces(interventionId);
  const deleteMutation = useDeletePieceUtilisee();

  if (isLoading) return <p>Chargement des pièces utilisées...</p>;
  if (isError) return <p>Erreur lors du chargement des pièces utilisées.</p>;

  const handleDelete = (id: number) => {
    deleteMutation.mutate(id, {
      onSuccess: () => alert('Pièce utilisée supprimée avec succès !'),
      onError: () => alert('Erreur lors de la suppression.'),
    });
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Nom de la pièce</th>
          <th>Référence</th>
          <th>Quantité</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {piecesUtilisees?.map((pu) => (
          <tr key={pu.id}>
            <td>{pu.piece_nom}</td>
            <td>{pu.piece_reference}</td>
            <td>{pu.quantite}</td>
            <td>
              <button onClick={() => onEdit?.(pu)}>Modifier</button>
              <button onClick={() => handleDelete(pu.id)}>Supprimer</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default InterventionPiecesList;
