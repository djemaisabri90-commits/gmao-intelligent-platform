// src/features/machines/api/machineApi.ts

import { apiClient } from "../../../api/client";
import type { Machine, MachineEtat, MachineStats } from "../types";
import type { Signalement } from "@/features/signalements/types";
import type { WorkOrder } from "@/features/workorders/types";
// Récupérer toutes les machines
export const getMachines = async (params?: Record<string, any>) => {
  const response = await apiClient.get<Machine[]>("/machines/", { params });
  return response.data;
};

// Récupérer une machine par ID
export const getMachine = async (id: number) => {
  const response = await apiClient.get<Machine>(`/machines/${id}/`);
  return response.data;
};

// Créer une machine
export const createMachine = async (data: Omit<Machine, "id" | "etat">) => {
  const response = await apiClient.post<Machine>("/machines/", data);
  return response.data;
};

// Mettre à jour une machine (PATCH recommandé)
export const updateMachine = async (id: number, data: Partial<Machine>) => {
  const response = await apiClient.patch<Machine>(`/machines/${id}/`, data);
  return response.data;
};

// Supprimer une machine
export const deleteMachine = async (id: number) => {
  await apiClient.delete(`/machines/${id}/`);
};

// Récupérer les workorders liés à une machine
export const getMachineWorkOrders = async (id: number) => {
  const response = await apiClient.get<WorkOrder[]>(`/machines/${id}/workorders/`);
  return response.data;
};

// Récupérer les signalements liés à une machine
export const getMachineSignalements = async (id: number) => {
  const response = await apiClient.get<Signalement[]>(`/machines/${id}/signalements/`);
  return response.data;
};

// Changer l’état d’une machine (override manuel par admin)
export const changeMachineEtat = async (id: number, etat: MachineEtat) => {
  const response = await apiClient.patch<Machine>(`/machines/${id}/change-etat/`, { etat });
  return response.data;
};

// ✅ Statistiques Machines
export const getMachineStats = async () => {
  const response = await apiClient.get<MachineStats>("/machines/statistiques/");
  return response.data;
};