// src/features/interventions/api/interventionApi.ts

import { apiClient } from '../../../api/client';
import type { Intervention, InterventionStats, InterventionWithDetails } from '../types';

// --- CRUD de base ---
export const getInterventions = async (params?: Record<string, any>) => {
  const response = await apiClient.get<InterventionWithDetails[]>('/interventions/', { params });
  return response.data;
};

export const getIntervention = async (id: number) => {
  const response = await apiClient.get<InterventionWithDetails>(`/interventions/${id}/`);
  return response.data;
};

export const createIntervention = async (data: Partial<Intervention>) => {
  const response = await apiClient.post<InterventionWithDetails>('/interventions/', data);
  return response.data;
};

export const updateIntervention = async (id: number, data: Partial<Intervention>) => {
  const response = await apiClient.put<InterventionWithDetails>(`/interventions/${id}/`, data);
  return response.data;
};

export const deleteIntervention = async (id: number) => {
  await apiClient.delete(`/interventions/${id}/`);
};

// --- Actions métier ---
/*export const startIntervention = async (id: number) => {
  const response = await apiClient.post<InterventionWithDetails>(`/interventions/${id}/start/`);
  return response.data;
};*/

export const startIntervention = (
  id: number,
  pieces: {
    pieceId: number;
    quantite: number;
  }[]
) => {
  return apiClient.post(
    `/interventions/${id}/start/`,
    {
      pieces: pieces.map((p) => ({
        piece_id: p.pieceId,
        quantite: p.quantite,
      })),
    }
  );
};

export const finishIntervention = async (id: number, actions_realisees: string) => {
  const response = await apiClient.post<InterventionWithDetails>(
    `/interventions/${id}/finish/`,
    { actions_realisees }
  );
  return response.data;
};

export const validateIntervention = async (id: number) => {
  const response = await apiClient.post<InterventionWithDetails>(`/interventions/${id}/validate/`);
  return response.data;
};
/*
export const changeInterventionStatus = async (
  id: number,
  statut: 'en_attente' | 'en_cours' | 'termine'
) => {
  const response = await apiClient.post<InterventionWithDetails>(`/interventions/${id}/change-statut/`, { statut });
  return response.data;
};

// --- Statistiques ---
export const getInterventionStats = async () => {
  const response = await apiClient.get<Record<string, any>>('/interventions/statistiques/');
  return response.data;
};
*/
// --- Statistiques ---
export const getInterventionStats = async () => {
  const response = await apiClient.get<InterventionStats>("/interventions/statistiques/");
  return response.data;
};