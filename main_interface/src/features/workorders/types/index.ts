// src/features/workorders/types/index.ts
export type EtatWorkOrder = "en_attente" | "en_cours" | "valide" | "clos";

export interface WorkOrder {
  id: number;
  signalement?: number | null;
  source?: 'manuel' | 'preventif' | 'iot' | null; // hérité du signalement
  machine: number;
  categorie?: number | null; // FK vers Categorie
  techniciens?: number[]; // ✅ tableau de techniciens (ManyToMany)
  expert?: number | null;
  cree_par?: number | null;

  type: 'corrective' | 'preventive' | 'predictive';
  priorite: 'high' | 'medium' | 'low';

  description: string;
  date_creation: string;
  date_cloture?: string | null;

  // ✅ propriétés calculées exposées par le serializer
  etat: EtatWorkOrder;
}

export interface WorkOrderWithDetails extends WorkOrder {
  machine_detail?: {
    id: number;
    nom: string;
  };
  categorie_detail?: {
    id: number;
    nom: string;
    description?: string;
  };
  techniciens_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    categorie_detail?: {
      id: number;
      nom: string;
    };
  }[]; // ✅ tableau de techniciens détaillés
  expert_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
  };
  cree_par_detail?: {
    id: number;
    username: string;
  };
  signalement_detail?: {
    id: number;
    description: string;
    created_at: string;
    source: string;
  };
}
// ✅ Statistiques WorkOrders
export interface WorkOrderStats {
  total: number;
  by_etat: Record<EtatWorkOrder, number>; // ex: { en_attente: 3, en_cours: 2, valide: 5, clos: 1 }
  by_priority?: Record<'high' | 'medium' | 'low', number>;
  by_type?: Record<'corrective' | 'preventive' | 'predictive', number>;
  by_source?: Record<'manuel' | 'preventif' | 'iot', number>;
  avg_completion_time?: number | null; // durée moyenne de clôture
  pending_count?: number; // nombre en attente
  workorders_with_interventions?: number; // nombre de machines liées à des bons de travail

}