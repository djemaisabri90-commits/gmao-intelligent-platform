// src/features/users/hooks/useForcePasswordChange.ts
import { useMutation } from "@tanstack/react-query";
import { changeUserPassword } from "../api/userApi";
import type { User } from "../types";

interface ChangePasswordPayload {
  id: number;
  password: string;
}

export const useForcePasswordChange = () => {
  return useMutation<User, Error, ChangePasswordPayload>({
    mutationFn: ({ id, password }) => changeUserPassword(id, password),
    retry: false, // éviter les retries automatiques sur erreurs de validation
  });
};
