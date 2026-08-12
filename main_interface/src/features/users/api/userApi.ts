// src/features/users/api/userApi.ts
import { apiClient } from '../../../api/client';
import type { User } from '../types';

export const getUsers = async (params?: Record<string, any>) => {
  const response = await apiClient.get<User[]>('/utilisateurs/', { params });
  return response.data;
};

export const getUser = async (id: number) => {
  const response = await apiClient.get<User>(`/utilisateurs/${id}/`);
  return response.data;
};

export const createUser = async (data: Partial<User>) => {
  const response = await apiClient.post<User>('/utilisateurs/', data);
  return response.data;
};

export const updateUser = async (id: number, data: Partial<User>) => {
  const response = await apiClient.patch<User>(`/utilisateurs/${id}/`, data);
  return response.data;
};


export const updateUserPut = async (id: number, data: Partial<User>) => {
  const response = await apiClient.post<User>(`/utilisateurs/${id}/`, data);
  return response.data;
};

export const deleteUser = async (id: number) => {
  await apiClient.delete(`/utilisateurs/${id}/`);
};

export const changeUserPassword = async (id: number, password: string) => {
  const response = await apiClient.post(`/utilisateurs/${id}/change_password/`, { password });
  return response.data;
};


// ✅ Nouveau endpoint pour mot de passe oublié (non connecté)
export const changePasswordByUsername = async (username: string, password: string) => {
  const response = await apiClient.post(`/utilisateurs/change_password_by_username/`, {
    username,
    password,
  });
  return response.data;
};