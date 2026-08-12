// src/features/users/hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
  changeUserPassword,
} from '../api/userApi';
import type { User } from '../types';

// Liste des utilisateurs (avec params éventuels)
export const useUsers = (params?: Record<string, any>) => {
  return useQuery<User[]>({
    queryKey: ['users', params],
    queryFn: () => getUsers(params),
  });
};

// Détail d'un utilisateur
export const useUser = (id: number) => {
  return useQuery<User>({
    queryKey: ['user', id],
    queryFn: () => getUser(id),
    enabled: !!id,
  });
};

// Création d'un utilisateur
export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<User>) => createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Mise à jour d'un utilisateur
export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<User> }) =>
      updateUser(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
    },
  });
};

// Suppression d'un utilisateur
export const useDeleteUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Changement de mot de passe
export const useChangeUserPassword = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, password }: { id: number; password: string }) =>
      changeUserPassword(id, password),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
    },
  });
};
