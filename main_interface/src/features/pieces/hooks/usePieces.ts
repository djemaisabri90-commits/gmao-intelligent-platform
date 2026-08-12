// src/features/pieces/hooks/usePieces.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getPieces,
  getPiece,
  createPiece,
  updatePiece,
  deletePiece,
} from '../api/pieceApi';
import type { Piece, PieceCreate, PieceUpdate } from '../types';

// 🔹 Liste des pièces
export const usePieces = () => {
  return useQuery<Piece[]>({
    queryKey: ['pieces'],
    queryFn: () => getPieces(),
  });
};

// 🔹 Détail d'une pièce
export const usePiece = (id: number) => {
  return useQuery<Piece>({
    queryKey: ['pieces', id],
    queryFn: () => getPiece(id),
    enabled: !!id,
  });
};

// 🔹 Création d'une pièce
export const useCreatePiece = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PieceCreate) => createPiece(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pieces'] });
    },
  });
};

// 🔹 Mise à jour d'une pièce
export const useUpdatePiece = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: PieceUpdate }) =>
      updatePiece(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['pieces'] });
      queryClient.invalidateQueries({ queryKey: ['pieces', variables.id] });
    },
  });
};

// 🔹 Suppression d'une pièce
export const useDeletePiece = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deletePiece(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pieces'] });
    },
  });
};
