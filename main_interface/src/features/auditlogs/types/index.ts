// src/features/auditlogs/types/index.ts

export interface AuditLog {
  id: number;
  user?: number | null;
  user_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
  } | null;
  action: string;
  model: string;
  object_id: number;
  changements?: string | null;
  ip_address?: string | null;
  user_agent?: string | null;
  endpoint?: string | null;
  method?: string | null;
  timestamp: string; 
}

export interface AuditLogWithDetails extends AuditLog {
  user_detail?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
  };
}