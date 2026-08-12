// src/features/reports/hooks/useKpiMetrics.ts

import { useMemo } from 'react';

/**
 * Types basiques (à adapter si tu as déjà des types dans /types)
 */
type Interventions = {
  total: number;
  by_status?: {
    valide?: number;
    [key: string]: number | undefined;
  };
  avg_duration?: string | number;
};

type WorkOrders = {
  pending_count: number;
  avg_completion_time?: string | number;
};

type Machines = {
  total: number;
  by_status?: {
    en_panne?: number;
    [key: string]: number | undefined;
  };
};

type ReportsData = {
  interventions: Interventions;
  workorders: WorkOrders;
  machines: Machines;
};

export const useKpiMetrics = (reports?: ReportsData) => {
  return useMemo(() => {
    if (!reports) {
      return {
        percentValidated: 0,
        validatedInterventions: 0,
        totalInterventions: 0,
        avgResolutionTime: '—',
        pendingWorkOrders: 0,
        avgCompletionTime: '—',
        percentMachinesEnPanne: 0,
        machinesEnPanne: 0,
        totalMachines: 0,
      };
    }

    const { interventions, workorders, machines } = reports;

    // 🔹 Interventions
    const totalInterventions = interventions?.total ?? 0;
    const validatedInterventions = interventions?.by_status?.valide ?? 0;

    const percentValidated =
      totalInterventions > 0
        ? Math.round((validatedInterventions / totalInterventions) * 100)
        : 0;

    const avgResolutionTime = interventions?.avg_duration ?? '—';

    // 🔹 WorkOrders
    const pendingWorkOrders = workorders?.pending_count ?? 0;
    const avgCompletionTime = workorders?.avg_completion_time ?? '—';

    // 🔹 Machines
    const totalMachines = machines?.total ?? 0;
    const machinesEnPanne = machines?.by_status?.en_panne ?? 0;

    const percentMachinesEnPanne =
      totalMachines > 0
        ? Math.round((machinesEnPanne / totalMachines) * 100)
        : 0;

    return {
      percentValidated,
      validatedInterventions,
      totalInterventions,
      avgResolutionTime,
      pendingWorkOrders,
      avgCompletionTime,
      percentMachinesEnPanne,
      machinesEnPanne,
      totalMachines,
    };
  }, [reports]);
};