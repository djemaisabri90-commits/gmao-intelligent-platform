// src/features/predictive/components/LogDetailsModal.tsx
import { Dialog } from "@headlessui/react";
import { ValidationMetricsChart } from "./ValidationMetricsChart";
import type { TrainingLog } from "../types";

type LogDetailsModalProps = {
  log: TrainingLog;
  onClose: () => void;
};

export const LogDetailsModal = ({ log, onClose }: LogDetailsModalProps) => {
  return (
    <Dialog open={true} onClose={onClose} className="fixed inset-0 z-50">
      <div className="flex items-center justify-center min-h-screen">
        <Dialog.Panel className="bg-white rounded-lg shadow-lg p-6 w-[600px]">
          <Dialog.Title className="text-lg font-bold">
            Détails du modèle v{log.model_version}
          </Dialog.Title>
          <div className="mt-4 space-y-2">
            <p>Date : {log.trained_at}</p>
            <p>Accuracy : {log.accuracy}</p>
            <p>F1 Score : {log.f1_score}</p>
            {/* ✅ nouveau champ minority_ratio */}
            <p>Minority Ratio : {log.minority_ratio ?? "-"}</p>
            <ValidationMetricsChart log={log} />
          </div>
          <button
            onClick={onClose}
            className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Fermer
          </button>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
};
