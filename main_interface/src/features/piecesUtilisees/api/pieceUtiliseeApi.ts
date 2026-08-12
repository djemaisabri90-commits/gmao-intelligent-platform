// src/features/piecesUtilisees/api/pieceUtiliseeApi.ts
import { apiClient } from '../../../api/client';
import type { PieceUtilisee, PieceUtiliseeCreate, PieceUtiliseeUpdate } from '../types';

// Liste globale
export const getPiecesUtilisees = async (): Promise<PieceUtilisee[]> => {
  const response = await apiClient.get<PieceUtilisee[]>('/pieces-utilisees/');
  return response.data;
};

// Liste par intervention
export const getInterventionPieces = async (interventionId: number): Promise<PieceUtilisee[]> => {
  const response = await apiClient.get<PieceUtilisee[]>(`/interventions/${interventionId}/pieces/`);
  return response.data;
};

// Détail
export const getPieceUtilisee = async (id: number): Promise<PieceUtilisee> => {
  const response = await apiClient.get<PieceUtilisee>(`/pieces-utilisees/${id}/`);
  return response.data;
};

// Création
export const createPieceUtilisee = async (data: PieceUtiliseeCreate): Promise<PieceUtilisee> => {
  const response = await apiClient.post<PieceUtilisee>('/pieces-utilisees/', data);
  return response.data;
};

// Mise à jour
export const updatePieceUtilisee = async (id: number, data: PieceUtiliseeUpdate): Promise<PieceUtilisee> => {
  const response = await apiClient.put<PieceUtilisee>(`/pieces-utilisees/${id}/`, data);
  return response.data;
};

// Suppression
export const deletePieceUtilisee = async (id: number): Promise<void> => {
  await apiClient.delete(`/pieces-utilisees/${id}/`);
};
