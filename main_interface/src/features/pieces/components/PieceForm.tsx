import React, { useState, useEffect } from 'react';
import { useCreatePiece, useUpdatePiece } from '../hooks/usePieces';
import type { Piece, PieceCreate, PieceUpdate } from '../types';

interface PieceFormProps {
  piece?: Piece; // si présent → mode édition
  onSuccess?: () => void;
}

const PieceForm: React.FC<PieceFormProps> = ({ piece, onSuccess }) => {
  const [formData, setFormData] = useState<PieceCreate>({
    nom: '',
    reference: '',
    stock_disponible: 0,
    fournisseur: '',
    prix_unitaire: '',
  });

  const createMutation = useCreatePiece();
  const updateMutation = useUpdatePiece();

  // Pré-remplir le formulaire si mode édition
  useEffect(() => {
    if (piece) {
      setFormData({
        nom: piece.nom,
        reference: piece.reference,
        stock_disponible: piece.stock_disponible,
        fournisseur: piece.fournisseur,
        prix_unitaire: piece.prix_unitaire,

      });
    }
  }, [piece]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'stock_disponible' ? Number(value) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (piece) {
      // mode édition
      const updateData: PieceUpdate = { ...formData };
      updateMutation.mutate(
        { id: piece.id, data: updateData },
        { onSuccess: onSuccess }
      );
    } else {
      // mode création
      createMutation.mutate(formData, { onSuccess: onSuccess });
    }
  };

  return (
  <form
    onSubmit={handleSubmit}
    className="space-y-5"
  >

    {/* NOM */}
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Nom
      </label>
      <input
        type="text"
        name="nom"
        value={formData.nom}
        onChange={handleChange}
        required
        className="w-full px-4 py-2 border border-gray-200 rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Ex: Roulement"
      />
    </div>

    {/* RÉFÉRENCE */}
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Référence
      </label>
      <input
        type="text"
        name="reference"
        value={formData.reference}
        onChange={handleChange}
        required
        className="w-full px-4 py-2 border border-gray-200 rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Ex: BR-001"
      />
    </div>

    {/* STOCK */}
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Stock disponible
      </label>
      <input
        type="number"
        name="stock_disponible"
        value={formData.stock_disponible}
        onChange={handleChange}
        min={0}
        className="w-full px-4 py-2 border border-gray-200 rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    {/* PRIX UNITAIRE */}
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Prix unitaire (DT)
      </label>

      <input
        type="number"
        step="0.001"
        min="0"
        name="prix_unitaire"
        value={formData.prix_unitaire}
        onChange={handleChange}
        required
        className="w-full px-4 py-2 border border-gray-200 rounded-lg
               focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Ex: 45.000"
      />
    </div>

    {/* FOURNISSEUR */}
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Fournisseur
      </label>
      <input
        type="text"
        name="fournisseur"
        value={formData.fournisseur}
        onChange={handleChange}
        className="w-full px-4 py-2 border border-gray-200 rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Ex: SKF"
      />
    </div>

    {/* BUTTON */}
    <button
      type="submit"
      className="w-full bg-blue-600 text-white py-2.5 rounded-lg
                 hover:bg-blue-700 active:scale-95 transition
                 font-medium"
    >
      {piece ? "Mettre à jour" : "Créer la pièce"}
    </button>

  </form>
);
};

export default PieceForm;
