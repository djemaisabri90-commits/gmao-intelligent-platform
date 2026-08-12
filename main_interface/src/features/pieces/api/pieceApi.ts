// src/features/pieces/api/pieceApi.ts
import { apiClient } from '../../../api/client';
import type { Piece } from '../types';

// 🔹 Liste des pièces
export const getPieces = async (params?: Record<string, any>): Promise<Piece[]> => {
  const response = await apiClient.get<Piece[]>('/pieces/', { params });
  return response.data;
};

// 🔹 Détail d'une pièce
export const getPiece = async (id: number): Promise<Piece> => {
  const response = await apiClient.get<Piece>(`/pieces/${id}/`);
  return response.data;
};

// 🔹 Création d'une pièce
export const createPiece = async (data: Omit<Piece, 'id'>): Promise<Piece> => {
  const response = await apiClient.post<Piece>('/pieces/', data);
  return response.data;
};

// 🔹 Mise à jour d'une pièce
export const updatePiece = async (id: number, data: Partial<Piece>): Promise<Piece> => {
  const response = await apiClient.put<Piece>(`/pieces/${id}/`, data);
  return response.data;
};

// 🔹 Suppression d'une pièce
export const deletePiece = async (id: number): Promise<void> => {
  await apiClient.delete(`/pieces/${id}/`);
};
