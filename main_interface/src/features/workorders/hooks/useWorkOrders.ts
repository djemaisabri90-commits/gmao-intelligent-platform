// src/features/workorders/hooks/useWorkOrders.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getWorkOrders,
  getWorkOrder,
  createWorkOrder,
  updateWorkOrder,
  deleteWorkOrder,
  getWorkOrderStats,
} from '../api/workorderApi';
import type { WorkOrder, WorkOrderStats, WorkOrderWithDetails } from '../types';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// --- Liste paginée des workorders ---
export const useWorkOrders = (params?: Record<string, any>) => {
  return useQuery<PaginatedResponse<WorkOrderWithDetails>, Error>({
    queryKey: ['workorders', params],
    queryFn: () => getWorkOrders(params), refetchInterval: 5000,
  });
};

// --- Détail d’un workorder ---
export const useWorkOrder = (id: number) => {
  return useQuery<WorkOrderWithDetails, Error>({
    queryKey: ['workorder', id],
    queryFn: () => getWorkOrder(id),
    enabled: !!id,
  });
};

// --- Statistiques ---
export const useWorkOrderStats = () => {
  return useQuery<WorkOrderStats, Error>({
    queryKey: ['workorder-stats'],
    queryFn: getWorkOrderStats,
  });
};

// --- Création ---
export const useCreateWorkOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<WorkOrderWithDetails, Error, Partial<WorkOrder>>({
    mutationFn: createWorkOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workorders'] });
    },
  });
};

// --- Mise à jour ---
export const useUpdateWorkOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<WorkOrderWithDetails, Error, { id: number; data: Partial<WorkOrder> }>({
    mutationFn: ({ id, data }) => updateWorkOrder(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['workorders'] });
      queryClient.invalidateQueries({ queryKey: ['workorder', id] });
    },
  });
};

// --- Suppression ---
export const useDeleteWorkOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, number>({
    mutationFn: deleteWorkOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workorders'] });
    },
  });
};
