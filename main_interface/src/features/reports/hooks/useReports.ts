// src/features/reports/hooks/useReports.ts

import { useQuery } from '@tanstack/react-query';
import { getStockAlerts, getRecentLogs } from '../api/reportApi';
import { getWorkOrderStats } from '@/features/workorders/api/workorderApi';
import { getInterventionStats } from '@/features/interventions/api/interventionApi';
import { getMachineStats } from '@/features/machines/api/machineApi';

import type { ReportsData, PieceStockAlert, RecentLog } from '../types';

import type { MachineStats } from '@/features/machines/types';
import type { WorkOrderStats } from '@/features/workorders/types';
import type { EtatIntervention, InterventionStats } from '@/features/interventions/types';





// Hooks spécialisés
export const useWorkOrderStats = () => {
  return useQuery<WorkOrderStats>({
    queryKey: ['reports', 'workorder-stats'],
    queryFn: getWorkOrderStats,
  });
};

export const useMachineStats = () => {
  return useQuery<MachineStats>({
    queryKey: ['reports', 'machine-stats'],
    queryFn: getMachineStats,
  });
};

export const useInterventionStats = () => {
  return useQuery<InterventionStats>({
    queryKey: ['reports', 'intervention-stats'],
    queryFn: getInterventionStats,
  });
};

export const useStockAlerts = () => {
  return useQuery<PieceStockAlert[]>({
    queryKey: ['reports', 'stock-alerts'],
    queryFn: getStockAlerts,
  });
};

export const useRecentLogs = (limit: number = 10) => {
  return useQuery<RecentLog[]>({
    queryKey: ['reports', 'recent-logs', limit],
    queryFn: () => getRecentLogs(limit),
  });
};

// ✅ Hook agrégateur
export const useReports = () => {
  const workorders = useWorkOrderStats();
  const machines = useMachineStats();
  const interventions = useInterventionStats();
  const stockAlerts = useStockAlerts();
  const recentLogs = useRecentLogs(10);

  const isLoading =
    workorders.isLoading ||
    machines.isLoading ||
    interventions.isLoading ||
    stockAlerts.isLoading ||
    recentLogs.isLoading;

  const error =
    workorders.error ||
    machines.error ||
    interventions.error ||
    stockAlerts.error ||
    recentLogs.error;

  // ✅ Fournir des valeurs par défaut cohérentes
const data: ReportsData = {
  workorders: workorders.data ?? {
    total: 0,
    by_etat: {} as Record<"en_attente" | "en_cours" | "valide" | "clos", number>,
    by_priority: {} as Record<"high" | "medium" | "low", number>,
    by_type: {} as Record<"corrective" | "preventive" | "predictive", number>,
    by_source: {} as Record<"manuel" | "preventif" | "iot", number>,
    avg_completion_time: null,
    pending_count: 0,
  },
  machines: machines.data ?? {
    total: 0,
    by_status: {} as Record<"SERVICE" | "PANNE" | "MAINTENANCE" | "INCONNU", number>,
    machines_with_workorders: 0,
  },
  interventions: interventions.data ?? {
    total: 0,
    by_status: {} as Record<EtatIntervention, number>,
    by_priority: {} as Record<"high" | "medium" | "low", number>,
    by_type: {} as Record<"corrective" | "preventive" | "predictive", number>,
    avg_duration: null,
    pending_count: 0,
  },
  stockAlerts: stockAlerts.data ?? [],
  recentLogs: recentLogs.data ?? [],
};


  return { isLoading, error, data };
};
