// src/features/auth/components/RoleRoute.tsx

import { Navigate } from "react-router-dom";
import { useAuthStore } from "../../../store/authStore";
import type { JSX } from "react";

interface RoleRouteProps {
  children: JSX.Element;
  allowedRoles: string[];
}

export const RoleRoute = ({
  children,
  allowedRoles,
}: RoleRouteProps) => {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/signalements" replace />;
  }

  return children;
};