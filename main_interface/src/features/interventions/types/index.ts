// src/features/interventions/types/index.ts
export type EtatIntervention = "en_attente" | "en_cours" | "termine" | "valide";

export interface Intervention {
  id: number;
  workorder: number;
  techniciens?: number[]; // ✅ tableau ManyToMany

  date_debut?: string | null;
  date_fin?: string | null;
  actions_realisees?: string;

  // 🔹 etat est calculé côté backend
  etat: EtatIntervention;

  priorite: 'basse' | 'moyenne' | 'haute';
  type_intervention: 'corrective' | 'preventive' | 'inspection';

  valide_par?: number | null;
  date_validation?: string | null;

  created_at: string;
  updated_at: string;
  is_locked: boolean;
}

import type { WorkOrderWithDetails } from '../../workorders/types';

export interface InterventionWithDetails extends Intervention {
  workorder_detail?: WorkOrderWithDetails;
  techniciens_detail?: { // ✅ tableau de techniciens détaillés
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    role?: string;
  }[];
  valide_par_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    role?: string;
  };
}

// ✅ Statistiques Interventions
export interface InterventionStats {
  total: number;
  en_attente?: number;
  termine?: number;
  valide?: number;
  en_cours?: number;
  by_status: Record<EtatIntervention, number>;
  by_priority?: Record<'high' | 'medium' | 'low', number>;
  by_type?: Record<'corrective' | 'preventive' | 'predictive', number>;
  avg_duration?: number | null; // durée moyenne des interventions
  pending_count?: number;       // nombre en attente
}