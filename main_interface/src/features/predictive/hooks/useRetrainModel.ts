// src/features/predictive/hooks/useRetrainModel.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { retrainModel } from "../api/predictiveApi";
import type { TrainingLog } from "../types";
import { toast } from "react-toastify";

export const useRetrainModel = () => {
  const queryClient = useQueryClient();

  return useMutation<TrainingLog, Error, { scratch?: boolean; minority_ratio?: number }>({
    mutationFn: ({ scratch = false, minority_ratio = 0.2 }) =>
      retrainModel(scratch, minority_ratio), // ✅ transmettre minority_ratio
    onSuccess: (data) => {
      toast.success(
        `✅ Réentraînement réussi — Accuracy: ${data.accuracy}, F1: ${data.f1_score}, Balanced Acc: ${data.balanced_accuracy}`
      );
      // 🔄 Rafraîchir automatiquement la liste des logs
      queryClient.invalidateQueries({ queryKey: ["trainingLogs"] });
    },
    onError: (error) => {
      toast.error(`❌ Erreur lors du réentraînement: ${error.message}`);
    },
  });
};
