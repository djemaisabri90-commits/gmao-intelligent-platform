// src/features/predictive/hooks/useTrainingLogs.ts
import { useQuery } from "@tanstack/react-query";
import { fetchLatestTrainingLog, fetchTrainingHistory, fetchTrainingLogByVersion } from "../api/predictiveApi";
import type { TrainingLog } from "../types";

export const useTrainingLogs = () => {
  return useQuery<TrainingLog[]>({
    queryKey: ["trainingLogs"],
    queryFn: fetchTrainingHistory,
        refetchOnWindowFocus: false, // optionnel pour éviter les refetchs trop fréquents
  });
};


// 📜 Dernier log
export const useLatestTrainingLog = () => {
  return useQuery<TrainingLog, Error>({
    queryKey: ["latestTrainingLog"],
    queryFn: fetchLatestTrainingLog,
    refetchOnWindowFocus: false,
  });
};

// 📜 Log par version
export const useTrainingLogByVersion = (version: number) => {
  return useQuery<TrainingLog, Error>({
    queryKey: ["trainingLog", version],
    queryFn: () => fetchTrainingLogByVersion(version),
    enabled: !!version, // évite le fetch si version est undefined
    refetchOnWindowFocus: false,
  });
};