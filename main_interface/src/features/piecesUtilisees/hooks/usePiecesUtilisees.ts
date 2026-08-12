// src/features/piecesUtilisees/hooks/usePiecesUtilisees.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getPiecesUtilisees,
  getInterventionPieces,
  getPieceUtilisee,
  createPieceUtilisee,
  updatePieceUtilisee,
  deletePieceUtilisee,
} from '../api/pieceUtiliseeApi';
import type { PieceUtilisee, PieceUtiliseeCreate, PieceUtiliseeUpdate } from '../types';

// Liste globale
export const usePiecesUtilisees = () =>
  useQuery<PieceUtilisee[]>({
    queryKey: ['pieces-utilisees'],
    queryFn: getPiecesUtilisees,
  });

// Liste par intervention
export const useInterventionPieces = (interventionId: number) =>
  useQuery<PieceUtilisee[]>({
    queryKey: ['interventions', interventionId, 'pieces'],
    queryFn: () => getInterventionPieces(interventionId),
    enabled: !!interventionId,
  });

// Détail
export const usePieceUtilisee = (id: number) =>
  useQuery<PieceUtilisee>({
    queryKey: ['pieces-utilisees', id],
    queryFn: () => getPieceUtilisee(id),
    enabled: !!id,
  });

// Création
export const useCreatePieceUtilisee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PieceUtiliseeCreate) => createPieceUtilisee(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pieces-utilisees'] });
    },
  });
};

// Mise à jour
export const useUpdatePieceUtilisee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: PieceUtiliseeUpdate }) =>
      updatePieceUtilisee(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['pieces-utilisees'] });
      queryClient.invalidateQueries({ queryKey: ['pieces-utilisees', variables.id] });
    },
  });
};

// Suppression
export const useDeletePieceUtilisee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deletePieceUtilisee(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pieces-utilisees'] });
    },
  });
};
