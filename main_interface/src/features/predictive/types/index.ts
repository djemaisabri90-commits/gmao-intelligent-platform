// src/features/predictive/types/index.ts
// Métriques par classe (issues du classification_report scikit-learn)
import type { Machine } from "../../machines/types";

// 🔮 Types prédictifs basés sur Machine

// Machine enrichie avec un score de risque
export interface MachineRisk extends Machine {
  risk: number;          // % de risque calculé par le modèle
  lastTraining?: string;  // date du dernier entraînement (optionnel) (formaté côté backend)
  predicted_failure_date?: string; // 🔮 nouvelle donnée
}

// Prédiction d’une panne anticipée
export interface Prediction {
  machine: Machine;      // machine concernée
  risk: number;          // % de risque
  predicted_failure_date?: string;
}

export type ExportFormat = "json" | "csv" | "xlsx";

export interface ClassMetrics {
  precision?: number;
  recall?: number;
  ["f1-score"]?: number;
  support?: number;
}

// Rapport complet pour une méthode de validation (SMOTE, ROS, etc.)
export interface ValidationReport {
  accuracy?: number;
  ["macro avg"]?: ClassMetrics;
  ["weighted avg"]?: ClassMetrics;
  //[classLabel: string]: ClassMetrics | number | undefined;
  classes?: Record<string, ClassMetrics>;
}

export interface ValidationResult {
report: {
    ["accuracy"]?: number;
    ["macro avg"]?: ClassMetrics;
    ["weighted avg"]?: ClassMetrics;
    [classLabel: string]: ClassMetrics | number | undefined;
  };
  cv_scores: number[];
  cv_mean: number;
}



// Ensemble des rapports par méthode
export interface ValidationMetrics {
  //[method: string]: ValidationReport;
  [method: string]: ValidationResult;
}

/*
// Structure principale d’un log d’entraînement
export interface TrainingLog {
  model_version: number;
  trained_at: string; // formaté côté backend en "dd/mm/yyyy HH:MM"
  user: number | null;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  dataset_size: number;
  class_distribution: Record<string, number>;
  success: boolean;
  status: string,
  validation_metrics?: ValidationMetrics;
  // ✅ nouveaux champs
  balanced_accuracy?: number;
  macro_f1?: number;
  confusion_matrix?: number[][]; // JSON serializable
  minority_ratio?: number; // ✅ ajout pour suivre le ratio minoritaire
}
*/

// Structure principale d’un log d’entraînement
export interface TrainingLog {
  model_version: number;
  trained_at: string; // formaté côté backend en "dd/mm/yyyy HH:MM"
  user: {
    id: number | null;
    username: string | null;
  }; // ✅ correction : objet au lieu de number
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  dataset_size: number;
  class_distribution: Record<string, number>;
  success: boolean;
  status: string;
  validation_metrics?: ValidationMetrics;
  balanced_accuracy?: number;
  macro_f1?: number;
  confusion_matrix?: number[][]; // JSON serializable
  minority_ratio?: number;
  hyperparameters?: Record<string, string | number>; // ✅ ajout pour cohérence
}

// src/features/predictive/types/index.ts
export interface MachineFeatures {
  machine_id: number;
  total_interventions: number;
  validated_interventions: number;
  pending_interventions: number;
  recent_interventions: number;
  total_workorders: number;
  high_priority_workorders: number;
  workorders_en_cours: number;
  workorders_clos: number;
  total_pieces_used: number;
  stock_critique: number;
  recent_notifications: number;
  is_in_failure: number;
  target: number;
  latitude?: number;   // si dispo dans ton modèle Machine
  longitude?: number;
}

