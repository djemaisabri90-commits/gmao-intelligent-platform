import { useState } from "react";
import type { Piece } from "@/features/pieces/types";

interface Props {
  pieces: Piece[];
  onChange: (selection: {
    pieceId: number;
    quantite: number;
  }[]) => void;
}

export const PieceSelectionTable = ({
  pieces,
  onChange,
}: Props) => {

  const [selected, setSelected] = useState<Record<number, number>>({});

  const handleQuantityChange = (
    pieceId: number,
    quantite: number
  ) => {

    const updated = {
      ...selected,
      [pieceId]: quantite,
    };

    setSelected(updated);

    const payload = Object.entries(updated)
      .filter(([_, q]) => q > 0)
      .map(([id, q]) => ({
        pieceId: Number(id),
        quantite: q,
      }));

    onChange(payload);
  };

  return (
    <table className="w-full border rounded-md">

      <thead className="bg-gray-100">
        <tr>
          <th className="p-2 text-left">Référence</th>
          <th className="p-2 text-left">Nom</th>
          <th className="p-2 text-left">Stock</th>
          <th className="p-2 text-left">Quantité</th>
        </tr>
      </thead>

      <tbody>

        {pieces.map((piece) => (

          <tr
            key={piece.id}
            className="border-t"
          >

            <td className="p-2">
              {piece.reference}
            </td>

            <td className="p-2">
              {piece.nom}
            </td>

            <td className="p-2">
              {piece.stock_disponible}
            </td>

            <td className="p-2">
              <input
                type="number"
                min={0}
                max={piece.stock_disponible}
                value={selected[piece.id] || ""}
                onChange={(e) =>
                  handleQuantityChange(
                    piece.id,
                    Number(e.target.value)
                  )
                }
                className="w-24 border rounded px-2 py-1"
              />
            </td>

          </tr>

        ))}

      </tbody>

    </table>
  );
};