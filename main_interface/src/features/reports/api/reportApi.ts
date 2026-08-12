// src/features/reports/api/reportApi.ts

import { apiClient } from '../../../api/client';
import type {
  PieceStockAlert,
  RecentLog,
} from '../types';

import type { MachineStats } from '@/features/machines/types';
import type { WorkOrderStats } from '@/features/workorders/types';
import type { InterventionStats } from '@/features/interventions/types';


export const getWorkOrderStats = async () => {
  const response = await apiClient.get<WorkOrderStats>('/workorders/statistiques/');
  return response.data;
};

export const getMachineStats = async () => {
  const response = await apiClient.get<MachineStats>('/machines/statistiques/');
  return response.data;
};

export const getInterventionStats = async () => {
  const response = await apiClient.get<InterventionStats>('/interventions/statistiques/');
  return response.data;
};

export const getStockAlerts = async () => {
  const response = await apiClient.get<PieceStockAlert[]>('/pieces/?stock_alert=true');
  return response.data;
};

export const getRecentLogs = async (limit: number = 10) => {
  const response = await apiClient.get<RecentLog[]>('/logs/', { params: { limit, order_by: '-date_action' } });
  return response.data;
};