import { useEffect, useState } from 'react';
import { getAccessToken } from '../../../api/auth';
import { fetchCurrentUser } from '../api/authApi';

export interface AuthUser {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
  role?: string;
}

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      setIsAuthenticated(true);
      // récupérer le profil utilisateur
      fetchCurrentUser()
        .then((profile) => setUser(profile))
        .catch(() => {
          setIsAuthenticated(false);
          setUser(null);
        });
    } else {
      setIsAuthenticated(false);
      setUser(null);
    }
  }, []);

  return { isAuthenticated, user };
};