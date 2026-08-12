// src/features/piecesUtilisees/components/InterventionPieceForm.tsx
import React, { useState, useEffect } from 'react';
import { useCreatePieceUtilisee, useUpdatePieceUtilisee } from '../hooks/usePiecesUtilisees';
import type { PieceUtilisee, PieceUtiliseeCreate, PieceUtiliseeUpdate } from '../types';

interface InterventionPieceFormProps {
  interventionId: number;
  pieceUtilisee?: PieceUtilisee; // si présent → mode édition
  onSuccess?: () => void;
}

const InterventionPieceForm: React.FC<InterventionPieceFormProps> = ({ interventionId, pieceUtilisee, onSuccess }) => {
  const [formData, setFormData] = useState<PieceUtiliseeCreate>({
    intervention: interventionId,
    piece: 0,
    quantite: 1,
  });

  const createMutation = useCreatePieceUtilisee();
  const updateMutation = useUpdatePieceUtilisee();

  // Pré-remplir si mode édition
  useEffect(() => {
    if (pieceUtilisee) {
      setFormData({
        intervention: interventionId,
        piece: pieceUtilisee.piece,
        quantite: pieceUtilisee.quantite,
      });
    }
  }, [pieceUtilisee, interventionId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'quantite' ? Number(value) : Number(value),
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (pieceUtilisee) {
      const updateData: PieceUtiliseeUpdate = { quantite: formData.quantite };
      updateMutation.mutate(
        { id: pieceUtilisee.id, data: updateData },
        { onSuccess: onSuccess }
      );
    } else {
      createMutation.mutate(formData, { onSuccess: onSuccess });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>ID de la pièce</label>
        <input
          type="number"
          name="piece"
          value={formData.piece}
          onChange={handleChange}
          required
          disabled={!!pieceUtilisee} // non modifiable en édition
        />
      </div>
      <div>
        <label>Quantité</label>
        <input
          type="number"
          name="quantite"
          value={formData.quantite}
          onChange={handleChange}
          min={1}
          required
        />
      </div>
      <button type="submit">
        {pieceUtilisee ? 'Mettre à jour' : 'Ajouter'}
      </button>
    </form>
  );
};

export default InterventionPieceForm;
