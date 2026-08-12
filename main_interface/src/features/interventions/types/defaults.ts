// src/features/interventions/types/defaults.ts
import type { InterventionStats } from "./index";

export const DEFAULT_INTERVENTION_STATS: InterventionStats = {
  total: 0,
  by_status: {
    en_attente: 0,
    en_cours: 0,
    valide: 0,
    termine: 0,
  },
  by_priority: { high: 0, medium: 0, low: 0 },
  by_type: { corrective: 0, preventive: 0, predictive: 0 },
  avg_duration: null,
  pending_count: 0,
};
