// src/features/predictive/components/RiskHeatmap.tsx
import type { FC } from "react";
import type { Machine } from "../../machines/types";

type MachineRisk = Machine & {
  risk: number; // % de risque calculé par le modèle
  lastTraining?: string; // date du dernier entraînement
};

type Props = {
  data: MachineRisk[];
};

export const RiskHeatmap: FC<Props> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="text-gray-500">Aucune donnée disponible</p>;
  }

  return (
    <div className="flex justify-center sm:grid-cols-3 lg:grid-cols-4 gap-4">
      {data.map((machine) => {
        const riskColor =
          machine.risk >= 0.8
            ? "bg-red-500"
            : machine.risk >= 0.5
            ? "bg-yellow-500"
            : "bg-green-500";

        return (
          <div
            key={machine.id}
            className={`rounded-lg shadow p-4 text-center text-white ${riskColor}`}
          >
            <h4 className="font-bold">{machine.nom}</h4>
            <p>Etat actuel: {machine.etat}</p>
            <p>Risque: {machine.risk}%</p>
            {/*<p className="text-xs">Dernier entraînement: {machine.lastTraining}</p> */}
          </div>
        );
      })}
    </div>
  );
};
