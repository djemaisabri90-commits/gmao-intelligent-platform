// src/features/predictive/components/UpcomingFailuresTimeline.tsx
import { useState } from "react";
import type { FC } from "react";
import type { Prediction } from "../types";

type Props = {
  data: Prediction[];
};

export const UpcomingFailuresTimeline: FC<Props> = ({ data }) => {
  const [showCriticalOnly, setShowCriticalOnly] = useState(false);
  const [showNext7DaysOnly, setShowNext7DaysOnly] = useState(false);

  if (!data || data.length === 0) {
    return <p className="text-gray-500">Aucune panne anticipée</p>;
  }

  // 🔄 Tri par date prévue (ascendant)
  const sortedData = [...data].sort((a, b) => {
    const dateA = a.predicted_failure_date
      ? new Date(a.predicted_failure_date).getTime()
      : Number.MAX_SAFE_INTEGER;
    const dateB = b.predicted_failure_date
      ? new Date(b.predicted_failure_date).getTime()
      : Number.MAX_SAFE_INTEGER;
    return dateA - dateB;
  });

  // 📌 Application des filtres
  const today = new Date();
  const in7Days = new Date();
  in7Days.setDate(today.getDate() + 7);

  let filteredData = sortedData;
  if (showCriticalOnly) {
    filteredData = filteredData.filter((p) => p.risk >= 80);
  }
  if (showNext7DaysOnly) {
    filteredData = filteredData.filter(
      (p) =>
        p.predicted_failure_date &&
        new Date(p.predicted_failure_date).getTime() <= in7Days.getTime()
    );
  }

  // 📊 Compteurs
  const totalCount = sortedData.length;
  const criticalCount = sortedData.filter((p) => p.risk >= 80).length;
  const next7DaysCount = sortedData.filter(
    (p) =>
      p.predicted_failure_date &&
      new Date(p.predicted_failure_date).getTime() <= in7Days.getTime()
  ).length;

  // 🔮 Sous‑titre dynamique
  let subtitle = `Total des pannes anticipées (${totalCount})`;
  if (showCriticalOnly && showNext7DaysOnly) {
    subtitle = `Pannes critiques dans les 7 jours (${filteredData.length})`;
  } else if (showCriticalOnly) {
    subtitle = `Pannes critiques (${criticalCount})`;
  } else if (showNext7DaysOnly) {
    subtitle = `Pannes prévues dans les 7 jours (${next7DaysCount})`;
  }

  return (
    <div className="space-y-6">
      <h3 className="text-center text-lg font-bold text-gray-700">{subtitle}</h3>

      {/* 🎛️ Boutons filtres */}
      <div className="flex flex-col items-center space-y-2">
        <div className="flex justify-center space-x-4">

        <button
          onClick={() => setShowCriticalOnly(!showCriticalOnly)}
          className="px-3 py-1 rounded bg-blue-500 text-white text-sm hover:bg-blue-600"
        >
          {showCriticalOnly ? "Toutes les pannes" : "Uniquement critiques"}
        </button>

        <button
          onClick={() => setShowNext7DaysOnly(!showNext7DaysOnly)}
          className="px-3 py-1 rounded bg-green-500 text-white text-sm hover:bg-green-600"
        >
          {showNext7DaysOnly ? "Toutes les dates" : "Dans les 7 jours"}
        </button>
        </div>

        {/* 📊 Indicateur optionnel 
        <span className="text-sm text-gray-500">
          {filteredData.length} résultats
        </span>
        */}
      </div>

      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredData.map((prediction, idx) => {
          let riskColor = "bg-green-100 text-green-800";
          let icon = "✅";
          if (prediction.risk >= 0.8) {
            riskColor = "bg-red-100 text-red-800";
            icon = "⚠️";
          } else if (prediction.risk >= 0.5) {
            riskColor = "bg-yellow-100 text-yellow-800";
            icon = "⏳";
          }

          return (
            <li
              key={idx}
              className="flex flex-col space-y-2 bg-gray-50 p-4 rounded-lg shadow"
            >
              <span
                className={`px-2 py-1 rounded-full text-sm font-bold ${riskColor}`}
              >
                {icon} {prediction.risk}%
              </span>
              <div>
                <p className="font-semibold">{prediction.machine.nom}</p>
                <p className="text-sm text-gray-500">
                  Date prévue:{" "}
                  {prediction.predicted_failure_date ?? "Non disponible"}
                </p>
                <p className="text-xs text-gray-400">
                  État actuel: {prediction.machine.etat}
                </p>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};
