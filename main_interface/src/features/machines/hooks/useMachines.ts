// src/features/machines/hooks/useMachines.tsx

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getMachines,
  getMachine,
  createMachine,
  updateMachine,
  deleteMachine,
  getMachineStats,
} from "../api/machineApi";
import type { Machine, MachineStats } from "../types";
import toast from "react-hot-toast"; // ✅ ajout

// Récupérer toutes les machines

export const useMachines = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ["machines", params],
    queryFn: () => getMachines(params),
  });
};



// Récupérer une machine par id
export const useMachine = (id: number) => {
  return useQuery({
    queryKey: ["machine", id],
    queryFn: () => getMachine(id),
    enabled: !!id,
  });
};

// Créer une machine
export const useCreateMachine = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Omit<Machine, "id" | "etat">) => createMachine(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["machines"] });
      toast.success("Machine créée avec succès ✅");
    },
    onError: (error: any) => {
      toast.error(`Erreur lors de la création : ${error.message}`);
    },
  });
};

// Mettre à jour une machine
export const useUpdateMachine = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Machine> }) =>
      updateMachine(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["machines"] });
      queryClient.invalidateQueries({ queryKey: ["machine", variables.id] });
      toast.success("Machine mise à jour avec succès ✨"); // ✅ toast succès
    },
    onError: (error: any) => {
      toast.error(`Erreur lors de la mise à jour : ${error.message}`); // ✅ toast erreur
    },
  });
};

// Supprimer une machine
export const useDeleteMachine = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteMachine(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["machines"] });
      toast.success("Machine supprimée avec succès 🗑️");
    },
    onError: (error: any) => {
      toast.error(`Erreur lors de la suppression : ${error.message}`);
    },
  });
};

// --- Statistiques ---
export const useMachineStats = () => {
  return useQuery<MachineStats, Error>({
    queryKey: ['machine-stats'],
    queryFn: getMachineStats,
  });
};