// src/features/auditlogs/hooks/useAuditLogs.ts

import { useQuery } from '@tanstack/react-query';
import { getAuditLogs, getAuditLog, getAuditLogsByObject } from '../api/auditlogApi';

export const useAuditLogs = (params?: Record<string, any>) => {
  return useQuery({
    queryKey: ['auditLogs', params],
    queryFn: () => getAuditLogs(params),
    select: (data) => data.results,
  });
};

export const useAuditLog = (id: number) => {
  return useQuery({
    queryKey: ['auditLog', id],
    queryFn: () => getAuditLog(id),
    enabled: !!id,
  });
};

export const useAuditLogsByObject = (model: string, objectId: number) => {
  return useQuery({
    queryKey: ['auditLogs', model, objectId],
    queryFn: () => getAuditLogsByObject(model, objectId),
    enabled: !!model && !!objectId,
  });
};