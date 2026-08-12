// src/features/auditlogs/api/auditlogApi.ts

import { apiClient } from '../../../api/client';
import type { AuditLogWithDetails } from '../types';
import type { PaginatedResponse } from '../../../types/index';

export const getAuditLogs = async (params?: Record<string, any>) => {
  const response = await apiClient.get<PaginatedResponse<AuditLogWithDetails>>('/auditlogs/', { params });
  return response.data;
};

export const getAuditLog = async (id: number) => {
  const response = await apiClient.get<AuditLogWithDetails>(`/auditlogs/${id}/`);
  return response.data;
};

export const getAuditLogsByObject = async (model: string, objectId: number) => {
  const response = await apiClient.get<PaginatedResponse<AuditLogWithDetails>>('/auditlogs/', {
    params: { model, object_id: objectId },
  });
  return response.data;
};