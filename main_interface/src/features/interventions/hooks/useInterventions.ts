// src/features/interventions/hooks/useInterventions.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getInterventions,
  getIntervention,
  createIntervention,
  updateIntervention,
  deleteIntervention,
  startIntervention,
  finishIntervention,
  validateIntervention,
  getInterventionStats,
} from '../api/interventionApi';
import type { Intervention, InterventionWithDetails, InterventionStats } from '../types';

//import { useEffect, useState } from 'react';
/*
export const useInterventionNotifications = () => {
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/interventions/');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications((prev) => [...prev, data]);
    };

    return () => socket.close();
  }, []);

  return notifications;
};
*/
export const useInterventionsByWorkorder = (workorderId: number) => {
  return useQuery({
    queryKey: ['interventions', { workorder: workorderId }],
    queryFn: () => getInterventions({ workorder: workorderId }),
    enabled: !!workorderId,
  });
};


// --- Hook pour liste des interventions ---
export const useInterventions = (params?: Record<string, any>) => {
  return useQuery<InterventionWithDetails[], Error>({
    queryKey: ['interventions', params],
    queryFn: () => getInterventions(params),
  });
};

// --- Hook pour une intervention spécifique ---
export const useIntervention = (id: number) => {
  return useQuery<InterventionWithDetails, Error>({
    queryKey: ['intervention', id],
    queryFn: () => getIntervention(id),
    enabled: !!id,
  });
};

// --- Hook pour statistiques ---
export const useInterventionStats = () => {
  return useQuery<InterventionStats, Error>({
    queryKey: ['intervention-stats'],
    //auto refresh
    queryFn: getInterventionStats, refetchInterval: 5000,
  });
};

// --- Mutations ---
export const useCreateIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Intervention>) => createIntervention(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
    },
  });
};

export const useUpdateIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Intervention> }) =>
      updateIntervention(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
      queryClient.invalidateQueries({ queryKey: ['intervention', id] });
    },
  });
};

export const useDeleteIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteIntervention(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
    },
  });
};

// --- Actions métier ---
/*export const useStartIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => startIntervention(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
      queryClient.invalidateQueries({ queryKey: ['intervention', id] });
    },
  });
};*/

export const useStartIntervention = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      pieces,
    }: {
      id: number;
      pieces: {
        pieceId: number;
        quantite: number;
      }[];
    }) => startIntervention(id, pieces),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["interventions"],
      });

      queryClient.invalidateQueries({
        queryKey: ["intervention", variables.id],
      });

      // rafraîchir le stock des pièces
      queryClient.invalidateQueries({
        queryKey: ["pieces"],
      });
    },
  });
};

export const useFinishIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, actions_realisees }: { id: number; actions_realisees: string }) =>
      finishIntervention(id, actions_realisees),
    onSuccess: (_, vars) => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
      queryClient.invalidateQueries({ queryKey: ['intervention', vars.id] });
    },
  });
}

export const useValidateIntervention = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => validateIntervention(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['interventions'] });
      queryClient.invalidateQueries({ queryKey: ['intervention', id] });
    },
  });
};

