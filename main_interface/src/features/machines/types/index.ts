// src/features/machines/types/index.ts

// Définition des états possibles alignés avec STATUS_CHOICES du backend
export type MachineEtat = "SERVICE" | "PANNE" | "MAINTENANCE" | "INCONNU";

export interface Machine {
  id: number;
  nom: string;
  description?: string;
  localisation?: string;
  type?: string;
  date_installation?: string; // format ISO date (YYYY-MM-DD)
  etat: MachineEtat; // ✅ aligné avec le backend
}
// ✅ Statistiques Machines
export interface MachineStats {
  total: number; // nombre total de machines
  by_status: Record<MachineEtat, number>; // distribution par état
  machines_with_workorders?: number; // nombre de machines liées à des bons de travail
}