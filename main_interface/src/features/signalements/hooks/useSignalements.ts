// src/features/signalements/hooks/useSignalements.ts

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getSignalements,
  getSignalement,
  createSignalement,
  updateSignalement,
  deleteSignalement,
  changeSignalementStatut,
} from "../api/signalementApi";
import type { Signalement, SignalementStatus } from "../types";

export const useSignalements = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ["signalements", params],
    queryFn: () => getSignalements(params),
  });
};

export const useSignalement = (id: number) => {
  return useQuery({
    queryKey: ["signalement", id],
    queryFn: () => getSignalement(id),
    enabled: !!id,
  });
};

export const useCreateSignalement = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createSignalement,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["signalements"] });
    },
  });
};

export const useUpdateSignalement = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Signalement> }) =>
      updateSignalement(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["signalements"] });
      queryClient.invalidateQueries({ queryKey: ["signalement", variables.id] });
    },
  });
};

export const useDeleteSignalement = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteSignalement,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["signalements"] });
    },
  });
};

export const useChangeSignalementStatut = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, statut }: { id: number; statut: SignalementStatus }) =>
      changeSignalementStatut(id, statut),
    //onSuccess: (_, variables) => {
onSuccess: (data, variables) => {
      console.log(`Signalement #${variables.id} changé en statut: ${data.statut}`);
      
      queryClient.invalidateQueries({ queryKey: ["signalements"] });
      queryClient.invalidateQueries({ queryKey: ["signalement", variables.id] });
    },
  });
};
