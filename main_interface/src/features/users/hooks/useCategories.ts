// src/features/users/hooks/useCategories.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../api/client';

export interface Categorie {
  id: number;
  nom: string; // ✅ string générique pour éviter blocage si nouvelle catégorie
  description?: string;
}

// Fonction API
const getCategories = async (): Promise<Categorie[]> => {
  const { data } = await apiClient.get<Categorie[]>('/categories/');
  return data;
};

// Hook React Query
export const useCategories = () => {
  return useQuery<Categorie[], Error>({
    queryKey: ['categories'],
    queryFn: getCategories,
  });
};
