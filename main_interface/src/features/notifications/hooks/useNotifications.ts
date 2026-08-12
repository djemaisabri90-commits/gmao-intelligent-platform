// src/features/notifications/hooks/useNotifications.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/api/client";
import type { Notification } from "../types";

interface PaginatedResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Notification[];
}

const getNotifications = async (page: number = 1): Promise<PaginatedResponse> => {
  const { data } = await apiClient.get(`/notifications/?page=${page}`);
  return data;
};


const markAsRead = async (id: number): Promise<void> => {
  await apiClient.patch(`/notifications/${id}/`, { is_read: true });
};

export const useNotifications = (page: number = 1) => {
  return useQuery<PaginatedResponse>({
    queryKey: ["notifications", page],
    queryFn: () => getNotifications(page),
  });
};

/*
optionnel ...
préciser que la valeur retournée est toujours un tableau (même vide) :
export const useNotifications = () => {
  return useQuery<Notification[]>({
    queryKey: ["notifications"],
    queryFn: async () => {
      const { data } = await apiClient.get<Notification[]>("/notifications/");
      return data ?? []; // ✅ garantit un tableau
    },
  });
};

*/

export const useMarkNotificationRead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
    },
  });
};
