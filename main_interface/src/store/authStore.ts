// src/store/authStore.ts
/**
 * gestion de l’état d’authentification avec Zustand
 * --Initialisation : accessToken: getAccessToken() lit directement
 * depuis localStorage lors de la création du store.
 * --setAuth : stocke les tokens via setTokens (localStorage)
 * et met à jour l’état réactif.
 * --logout : efface les tokens (localStorage) et réinitialise l’état.
 * --Typage : utilise User importé depuis ../types.
 * --je vais vérifier les fonctions auxiliares dans =
 * ....-- auth.ts : recuperation + rafraichissement token 
 */

import { create } from 'zustand';
import { getAccessToken, setTokens, clearTokens } from '../api/auth';

import type { User } from '@/features/users/types'; 
//setUser()
//mise à jour du profil sans recréer tous les tokens.
//utile après une modification du compte.

interface AuthState {
  accessToken: string | null;
  user: User | null;
  setUser: (user: User) => void;
  setAuth: (access: string, refresh: string, user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: getAccessToken(),
  user: null,
  setUser: (user: User) => set({ user }),
  setAuth: (access, refresh, user) => {
    setTokens(access, refresh);
    set({ accessToken: access, user });
  },
  logout: () => {
    clearTokens();
    set({ accessToken: null, user: null });
  },
}));