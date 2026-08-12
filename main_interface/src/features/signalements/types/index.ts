// src/features/signalements/types/index.ts

// Enum des statuts (aligné avec backend)
export const SignalementStatus = {
  nouveau: "nouveau",
  en_cours: "en_cours",
  traite: "traite",
  clos: "clos",
} as const;

export type SignalementStatus =
  typeof SignalementStatus[keyof typeof SignalementStatus];

// Enum des sources (aligné avec backend)
export type SignalementSource = "manuel" | "preventif" | "iot";

// Rôles utilisateurs
export type UserRole = "operateur" | "technicien" | "expert" | "admin";

// Interface principale
export interface Signalement {
  id: number;
  machine: number;
  description: string;
  source: SignalementSource;
  statut: SignalementStatus;
  cree_par: number;
  created_at: string;
  updated_at: string;
}

// Interface enrichie avec détails
export interface SignalementWithDetails extends Signalement {
  machine_detail?: {
    id: number;
    nom: string;
    etat?: string;
  };
  cree_par_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    role?: UserRole;
  };
}
