// src/features/predictive/api/predictiveApi.ts
import { predictiveClient } from "@/api/client";
import type { TrainingLog, ExportFormat, MachineFeatures } from "../types";


// 🔄 Entraînement du modèle
export const retrainModel = async (
  scratch = false,
  minority_ratio: number = 0.2
): Promise<TrainingLog> => {
  const { data } = await predictiveClient.post("/train/", {
    scratch,
    minority_ratio,
  });
  return data;
};

// 📜 Historique complet
export const fetchTrainingHistory = async (): Promise<TrainingLog[]> => {
  const { data } = await predictiveClient.get("/train-history/");
  return data;
};

// 📜 Dernier log
export const fetchLatestTrainingLog = async (): Promise<TrainingLog> => {
  const { data } = await predictiveClient.get("/train-history/latest/");
  return data;
};

// 📜 Log par version
export const fetchTrainingLogByVersion = async (version: number): Promise<TrainingLog> => {
  const { data } = await predictiveClient.get(`/train-history/${version}/`);
  return data;
};

// 📋 Liste des features
export const fetchFeatures = async (): Promise<string[]> => {
  const { data } = await predictiveClient.get("/features/");
  return data;
};

export const featureData = async (): Promise<MachineFeatures[]> => {
  const { data } = await predictiveClient.get("/features_data/");
  return data;
};

// 📤 Export log (JSON, CSV, XLSX)
export const exportLog = async (
  version: number,
  format: ExportFormat = "json"
): Promise<Blob | object> => {
  const url = `/export/${version}/${format}/`;
  const response = await predictiveClient.get(url, {
    responseType: format === "json" ? "json" : "blob",
  });
  return response.data;
};
