// src/features/auth/api/authApi.ts
import { apiClient } from '../../../api/client';
import { clearTokens } from '../../../api/auth';
import type { User } from '@/features/users/types';

interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

/**
 * Authentification : récupère les tokens JWT puis le profil utilisateur.
 */

export const login = async (username: string, password: string) => {

  console.log("BASE URL =", apiClient.defaults.baseURL);
  console.log(
    "LOGIN URL =",
    `${apiClient.defaults.baseURL}/auth/login/`
  );

  const response = await apiClient.post<LoginResponse>('/auth/login/', {
    username,
    password,
  });

  return response.data;
};

/*export const login = async (username: string, password: string) => {
  // 1. Obtenir les tokens
  const response = await apiClient.post<LoginResponse>('/auth/login/', {
    username,
    password,
  });
  // Le backend renvoie directement { access, refresh, user }
  return response.data;
};*/
  // 2. Récupérer les informations de l'utilisateur connecté
  //const userResponse = await apiClient.get<User>('/utilisateurs/me/');
  //return { access, refresh, user: userResponse.data };


/**
 * Récupère l'utilisateur actuel (utile pour restaurer la session).
 */
export const fetchCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get<User>('/utilisateurs/me/');
  return response.data;
};

/**
 * Déconnexion : efface les tokens et redirige vers la page de login.
 */
export const logout = () => {
  clearTokens();
  // Optionnel : appel à un endpoint de déconnexion backend si nécessaire
  window.location.href = '/login';
};