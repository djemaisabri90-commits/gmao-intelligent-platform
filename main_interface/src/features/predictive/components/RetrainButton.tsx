// src/features/predictive/components/RetrainButton.tsx
import { useState } from "react"
import { useRetrainModel } from "../hooks/useRetrainModel";

export const RetrainButton = () => {
  const { mutate, isPending } = useRetrainModel();
    const [minorityRatio, setMinorityRatio] = useState(0.2);

  return (
    <div className="flex items-center gap-4">
      <input
        type="number"
        step="0.05"
        min="0.05"
        max="0.5"
        value={minorityRatio}
        onChange={(e) => setMinorityRatio(Number(e.target.value))}
        className="border rounded px-3 py-2 w-24"
      />



    <button
      onClick={() => mutate({ scratch: true, minority_ratio: minorityRatio })}
      disabled={isPending}
      style={{
        padding: "8px 16px",
        background: "#4CAF50",
        color: "white",
        border: "none",
        borderRadius: "4px",
        cursor: isPending ? "not-allowed" : "pointer",
      }}
    >
        {isPending && (
        <span
          style={{
            width: "16px",
            height: "16px",
            border: "2px solid white",
            borderTop: "2px solid transparent",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
          }}
        />
        )}
      {isPending ? "Réentraînement en cours..." : "Réentraîner depuis zéro"}
    </button>

    </div>
  
  );
};
