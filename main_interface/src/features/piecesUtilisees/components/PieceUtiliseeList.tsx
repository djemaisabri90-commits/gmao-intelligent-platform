interface Props {
  piecesUtilisees: {
    id: number;
    piece_nom: string;
    quantite: number;
  }[];
}

export const PieceUtiliseeList = ({
  piecesUtilisees,
}: Props) => {

  if (!piecesUtilisees.length) {
    return (
      <p className="text-gray-500">
        Aucune pièce utilisée.
      </p>
    );
  }

  return (
    <div className="border rounded-md overflow-hidden">

      <table className="w-full">

        <thead className="bg-gray-100">

          <tr>
            <th className="p-2 text-left">
              Pièce
            </th>

            <th className="p-2 text-left">
              Quantité
            </th>
          </tr>

        </thead>

        <tbody>

          {piecesUtilisees.map((item) => (

            <tr
              key={item.id}
              className="border-t"
            >
              <td className="p-2">
                {item.piece_nom}
              </td>

              <td className="p-2">
                {item.quantite}
              </td>
            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
};