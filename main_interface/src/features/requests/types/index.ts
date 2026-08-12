export interface PasswordResetRequest {
  id: number;
  username: string;
  status: "pending" | "resolved" | "rejected";
  created_at: string;
  processed_at?: string | null;
}