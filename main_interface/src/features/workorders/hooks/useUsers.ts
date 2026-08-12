// src/features/workorders/hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../api/client';
import type { User } from '../../users/types';

const fetchUsers = async (params?: { role?: User['role'] }) => {
  const response = await apiClient.get<User[]>('/api/utilisateurs/', { params });
  return response.data;
};

// ✅ Hook pour tous les utilisateurs
export const useUsers = (params?: { role?: User['role'] }) => {
  return useQuery<User[], Error>({
    queryKey: ['users', params],
    queryFn: () => fetchUsers(params),
  });
};

// ✅ Hook spécialisé pour les techniciens
export const useTechniciens = () => {
  return useUsers({ role: 'technicien' });
};

// ✅ Hook spécialisé pour les experts
export const useExperts = () => {
  return useUsers({ role: 'expert' });
};
