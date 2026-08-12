// src/features/predictive/hooks/usePredictive.ts
import { useQuery } from "@tanstack/react-query";
import { predictiveClient } from "@/api/client";
import type { MachineRisk, Prediction, TrainingLog } from "../types";

interface PredictiveData {
  machineRisks: MachineRisk[];
  predictions: Prediction[];
  metricsHistory: TrainingLog[];
}

export const usePredictive = () => {
  return useQuery<PredictiveData>({
    queryKey: ["predictive"],
    queryFn: async () => {
      // 🔮 Appels backend en parallèle
      const [machineRiskRes, trainHistoryRes] = await Promise.all([
        predictiveClient.get("/machine-risk/"),
        predictiveClient.get("/train-history/"),
      ]);

      // ✅ Typage strict
      const machineRisks: MachineRisk[] = machineRiskRes.data.map((m: any) => ({
        id: m.id,
        nom: m.nom,
        etat: m.etat,
        description: m.description,
        localisation: m.localisation,
        type: m.type,
        date_installation: m.date_installation,
        risk: m.risk,
        predicted_failure_date: m.predicted_failure_date,
        lastTraining: m.lastTraining ?? undefined,
      }));

      const predictions: Prediction[] = machineRisks.map((m) => ({
        machine: {
          id: m.id,
          nom: m.nom,
          etat: m.etat,
          description: m.description,
          localisation: m.localisation,
          type: m.type,
          date_installation: m.date_installation,
        },
        risk: m.risk,
        predicted_failure_date: m.predicted_failure_date!,
      }));

      const metricsHistory: TrainingLog[] = trainHistoryRes.data;

      return { machineRisks, predictions, metricsHistory };
    },
    refetchOnWindowFocus: false,
  });
};
