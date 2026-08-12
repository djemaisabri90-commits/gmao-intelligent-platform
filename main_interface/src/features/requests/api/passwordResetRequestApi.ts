import { apiClient } from "../../../api/client";
import type { PasswordResetRequest } from "../types";

export const getPasswordResetRequests = async () => {
  const response = await apiClient.get<PasswordResetRequest[]>(
    "/password-reset-requests/"
  );

  return response.data;
};

// passwordResetRequestApi.ts

export const processPasswordResetRequest = async (
  id: number
) => {
  const response = await apiClient.post(
    `/password-reset-requests/${id}/process/`
  );

  return response.data;
};