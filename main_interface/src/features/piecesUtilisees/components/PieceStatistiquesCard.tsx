// features/piecesUtilisees/components/PieceStatistiquesCard.tsx

import { usePieceStatistiques } from "../hooks/usePieceStatistiques";

export const PieceStatistiquesCard = () => {
  const { data, isLoading } = usePieceStatistiques();

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        Chargement...
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">

      <h3 className="text-lg font-bold text-gray-800 mb-4">
        Coût de maintenance
      </h3>

      <div className="space-y-4">

        <div>
          <p className="text-sm text-gray-500">
            Pièces consommées
          </p>

          <p className="text-3xl font-bold text-blue-600">
            {data?.pieces_consommees ?? 0}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Coût total des pièces
          </p>

          <p className="text-3xl font-bold text-green-600">
            {Number(data?.cout_total_pieces ?? 0).toFixed(3)} DT
          </p>
        </div>

      </div>
      <div className="border-t pt-4 mt-4 space-y-3">

  <div>
    <p className="text-xs text-gray-500">
      Coût moyen / intervention
    </p>

    <p className="font-semibold text-gray-800">
      {data?.cout_moyen_intervention?.toFixed(3)} DT
    </p>
  </div>

  <div>
    <p className="text-xs text-gray-500">
      Intervention la plus coûteuse
    </p>

    <p className="font-semibold text-red-600">
      #{data?.intervention_plus_couteuse?.intervention_id}
      {" - "}
      {data?.intervention_plus_couteuse?.cout_total.toFixed(3)} DT
    </p>
  </div>

  <div>
    <p className="text-xs text-gray-500">
      Intervention la moins coûteuse
    </p>

    <p className="font-semibold text-green-600">
      #{data?.intervention_moins_couteuse?.intervention_id}
      {" - "}
      {data?.intervention_moins_couteuse?.cout_total.toFixed(3)} DT
    </p>
  </div>

</div>

    </div>
  );
};