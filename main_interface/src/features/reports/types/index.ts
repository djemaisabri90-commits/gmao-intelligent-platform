// src/features/reports/types/index.ts
import type { MachineStats } from '@/features/machines/types';
import type { WorkOrderStats } from '@/features/workorders/types';
import type { InterventionStats } from '@/features/interventions/types';


export interface PieceStockAlert {
  id: number;
  nom: string;
  reference: string;
  quantite: number;
  seuil_alerte: number;
}

export interface RecentLog {
  id: number;
  date_action: string;
  user: number;
  user_detail?: { username: string };
  workorder: number;
  workorder_detail?: { description: string };
  action: string;
}

export interface ReportsData {
  workorders: WorkOrderStats;
  machines: MachineStats;
  interventions: InterventionStats;
  stockAlerts: PieceStockAlert[];
  recentLogs: RecentLog[];
}