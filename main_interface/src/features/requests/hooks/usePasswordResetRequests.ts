import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query";

import { getPasswordResetRequests } from "../api/passwordResetRequestApi";
import { processPasswordResetRequest } from "../api/passwordResetRequestApi";

export const usePasswordResetRequests = () => {
  return useQuery({
    queryKey: ["password-reset-requests"],
    queryFn: getPasswordResetRequests,
    refetchInterval: 30000,
  });
};

export const useProcessPasswordResetRequest = () => {

  const queryClient = useQueryClient();

  return useMutation({

    mutationFn: processPasswordResetRequest,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["password-reset-requests"],
      });
    },
  });
};