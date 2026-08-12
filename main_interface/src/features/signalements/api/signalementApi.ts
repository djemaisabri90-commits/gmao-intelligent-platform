// src/features/signalements/api/signalementApi.ts

import { apiClient } from "../../../api/client";
import type { Signalement, SignalementWithDetails, SignalementStatus } from "../types";

// Récupérer tous les signalements
export const getSignalements = async (params?: Record<string, any>) => {
  const response = await apiClient.get<SignalementWithDetails[]>("/signalements/", { params });
  return response.data;
};

// Récupérer un signalement par ID
export const getSignalement = async (id: number) => {
  const response = await apiClient.get<SignalementWithDetails>(`/signalements/${id}/`);
  return response.data;
};

// Créer un signalement
export const createSignalement = async (data: Partial<Signalement>) => {
  const response = await apiClient.post<Signalement>("/signalements/", data);
  return response.data;
};

// Mettre à jour un signalement
export const updateSignalement = async (id: number, data: Partial<Signalement>) => {
  const response = await apiClient.put<Signalement>(`/signalements/${id}/`, data);
  return response.data;
};

// Supprimer un signalement
export const deleteSignalement = async (id: number) => {
  await apiClient.delete(`/signalements/${id}/`);
};

// Changer le statut d’un signalement
export const changeSignalementStatut = async (id: number, statut: SignalementStatus) => {
  const response = await apiClient.post<Signalement>(`/signalements/${id}/close/`, { statut });
  return response.data;
};
