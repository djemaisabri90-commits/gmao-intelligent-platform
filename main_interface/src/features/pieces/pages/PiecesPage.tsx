import React, { useState } from 'react';
import PieceList from '../components/PieceList';
import PieceForm from '../components/PieceForm';
import type { Piece } from '../types';

const PiecesPage: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingPiece, setEditingPiece] = useState<Piece | null>(null);

  const handleAdd = () => {
    setEditingPiece(null);
    setShowForm(true);
  };

  const handleEdit = (piece: Piece) => {
    setEditingPiece(piece);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingPiece(null);
  };

  return (
  <div className="p-6 space-y-6">

    {/* HEADER */}
    <div className="flex items-center justify-between">

      <h1 className="text-2xl font-semibold text-gray-800">
        Gestion des pièces
      </h1>

      {!showForm && (
        <button
          onClick={handleAdd}
          className="flex items-center gap-2 px-4 py-2 rounded-lg
                     bg-blue-600 text-white text-sm font-medium
                     hover:bg-blue-700 active:scale-95 transition"
        >
          <span className="text-lg">＋</span>
          Ajouter une pièce
        </button>
      )}

    </div>

    {/* LIST */}
    {!showForm && (
      <PieceList onEdit={handleEdit} />
    )}

    {/* FORM */}
    {showForm && (
  <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">

    <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl p-6">

      <h2 className="text-lg font-semibold mb-4">
        {editingPiece ? "Modifier une pièce" : "Ajouter une pièce"}
      </h2>

      <PieceForm
        piece={editingPiece ?? undefined}
        onSuccess={handleCloseForm}
      />

      <div className="flex justify-end mt-4">
        <button
          onClick={handleCloseForm}
          className="text-gray-600 hover:text-black transition"
        >
          Annuler
        </button>
      </div>

    </div>

  </div>
)}

  </div>
);
};

export default PiecesPage;
