// src/features/workorders/api/workorderApi.ts
import { apiClient } from '../../../api/client';
import type { WorkOrder, WorkOrderStats, WorkOrderWithDetails } from '../types';
import { normalizeWorkOrderPayload } from "./utils";

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// --- CRUD de base ---
export const getWorkOrders = async (params?: Record<string, any>) => {
  const response = await apiClient.get<PaginatedResponse<WorkOrderWithDetails>>('/workorders/', { params });
  return response.data;
};

export const getWorkOrder = async (id: number) => {
  const response = await apiClient.get<WorkOrderWithDetails>(`/workorders/${id}/`);
  return response.data;
};

export const createWorkOrder = async (data: Partial<WorkOrder>) => {
  try {
    const payload = normalizeWorkOrderPayload(data);
    const response = await apiClient.post<WorkOrderWithDetails>(`/workorders/`, payload);
    return response.data;
  } catch (error: any) {
    console.error("Erreur création WorkOrder:", error.response?.data || error.message);
    throw error;
  }
};



export const updateWorkOrder = async (id: number, data: Partial<WorkOrder>) => {
  try {
    const payload = normalizeWorkOrderPayload(data);
    const response = await apiClient.patch<WorkOrderWithDetails>(`/workorders/${id}/`, payload);
    return response.data;
  } catch (error: any) {
    console.error("Erreur update WorkOrder:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteWorkOrder = async (id: number) => {
  await apiClient.delete(`/workorders/${id}/`);
};

// --- Statistiques ---
export const getWorkOrderStats = async () => {
  const response = await apiClient.get<WorkOrderStats>('/workorders/statistiques/');
  return response.data;
};

/*
// --- Actions métier ---
export const changeWorkOrderStatus = async (
  id: number,
  statut: 'en_attente' | 'valide' | 'en_cours' | 'termine'
) => {
  const response = await apiClient.post<WorkOrderWithDetails>(`/api/workorders/${id}/change-statut/`, { statut });
  return response.data;
};
*/