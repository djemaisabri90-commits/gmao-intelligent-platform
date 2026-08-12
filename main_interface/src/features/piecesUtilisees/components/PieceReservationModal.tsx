import { useState } from "react";
import { PieceSelectionTable } from "./PieceSelectionTable";
import type { Piece } from "@/features/pieces/types";

interface Props {
  isOpen: boolean;
  onClose: () => void;

  pieces: Piece[];

  onConfirm: (
    reservations: {
      pieceId: number;
      quantite: number;
    }[]
  ) => void;
}

export const PieceReservationModal = ({
  isOpen,
  onClose,
  pieces,
  onConfirm,
}: Props) => {

  const [selection, setSelection] = useState<any[]>([]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">

      <div className="bg-white w-full max-w-3xl rounded-lg shadow-lg p-6">

        <h2 className="text-xl font-bold mb-4">
          Réservation des pièces
        </h2>

        <PieceSelectionTable
          pieces={pieces}
          onChange={setSelection}
        />

        <div className="flex justify-end gap-3 mt-6">

          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 rounded"
          >
            Annuler
          </button>

          <button
            onClick={() => onConfirm(selection)}
            className="px-4 py-2 bg-blue-600 text-white rounded"
          >
            Réserver et démarrer
          </button>

          <button
          onClick={() => onConfirm([])}
          className="px-4 py-2 bg-green-600 text-white rounded"
          >
            Démarrer sans pièce
          </button>

        </div>

      </div>

    </div>
  );
};