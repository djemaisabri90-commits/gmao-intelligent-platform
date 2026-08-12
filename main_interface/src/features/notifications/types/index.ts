// src/features/notifications/types/index.ts
export interface Notification {
  id: number;
  user: number;
  user_username?: string;
  message: string;
  workorder?: number | null;
  categorie?: number | null;
  url?: string | null;
  is_read: boolean;
  created_at: string;
}
