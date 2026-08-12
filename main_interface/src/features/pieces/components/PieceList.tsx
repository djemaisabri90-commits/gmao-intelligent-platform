// src/features/pieces/components/PieceList.tsx
import React from 'react';
import { usePieces, useDeletePiece } from '../hooks/usePieces';
import type { Piece } from '../types';

interface PieceListProps {
  onEdit?: (piece: Piece) => void;
}

const PieceList: React.FC<PieceListProps> = ({ onEdit }) => {
  const { data: pieces, isLoading, isError } = usePieces();
  const deleteMutation = useDeletePiece();

  if (isLoading) return <p>Chargement des pièces...</p>;
  if (isError) return <p>Erreur lors du chargement des pièces.</p>;

  const handleDelete = (id: number) => {
    deleteMutation.mutate(id, {
      onSuccess: () => alert('Pièce supprimée avec succès !'),
      onError: () => alert('Erreur lors de la suppression.'),
    });
  };

  return (
  <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">

    {/* TABLE WRAPPER */}
    <div className="overflow-x-auto">

      <table className="w-full text-sm">

        {/* HEADER */}
        <thead className="bg-gray-50 text-gray-600 text-xs uppercase">
          <tr>
            <th className="px-6 py-4 text-left">Nom</th>
            <th className="px-6 py-4 text-left">Référence</th>
            <th className="px-6 py-4 text-left">Stock</th>
            <th className="px-6 py-4 text-left">Fournisseur</th>
            <th className="px-6 py-4 text-right">Actions</th>
          </tr>
        </thead>

        {/* BODY */}
        <tbody>
          {pieces?.map((piece) => (
            <tr
              key={piece.id}
              className="border-t hover:bg-gray-50 transition"
            >

              <td className="px-6 py-4 font-medium text-gray-800">
                {piece.nom}
              </td>

              <td className="px-6 py-4 text-gray-600">
                {piece.reference}
              </td>

              <td className="px-6 py-4">
                {piece.stock_disponible > 0 ? (
                  <span className="px-2 py-1 text-xs rounded-md bg-green-100 text-green-700">
                    {piece.stock_disponible}
                  </span>
                ) : (
                  <span className="px-2 py-1 text-xs rounded-md bg-red-100 text-red-600">
                    Rupture
                  </span>
                )}
              </td>

              <td className="px-6 py-4 text-gray-600">
                {piece.fournisseur}
              </td>

              {/* ACTIONS */}
              <td className="px-6 py-4 text-right space-x-2">

                <button
                  onClick={() => onEdit?.(piece)}
                  className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                >
                  Modifier
                </button>

                <button
                  onClick={() => handleDelete(piece.id)}
                  className="text-red-500 hover:text-red-700 font-medium text-sm"
                >
                  Supprimer
                </button>

              </td>

            </tr>
          ))}
        </tbody>

      </table>
    </div>
  </div>
);
};

export default PieceList;
